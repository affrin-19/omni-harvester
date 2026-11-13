/**
 * @file power_manager.cpp
 * @brief Energy-Aware Adaptive Duty-Cycling Implementation
 */

#include "power_manager.h"
#include <Arduino.h>

#if defined(ESP32)
  #include "esp_sleep.h"
#endif

// Pin configuration
#define PIN_ADC_SUPERCAP    34  // Analog pin monitoring supercapacitor voltage
#define PIN_ADC_BUS_INPUT   35  // Analog pin monitoring raw harvested DC bus
#define VOLTAGE_DIVIDER_RATIO 2.0f // R1=100k, R2=100k divider
#define ADC_REF_VOLTAGE     3.3f
#define ADC_MAX_COUNT       4095.0f

static float s_capacitance = 1.0f;
static uint32_t s_boot_counter = 0;

void PowerManager_Init(float capacitance_farads) {
    s_capacitance = (capacitance_farads > 0.01f) ? capacitance_farads : 1.0f;
    analogReadResolution(12);
    s_boot_counter++;
}

HarvesterTelemetry_t PowerManager_UpdateTelemetry(void) {
    HarvesterTelemetry_t tele;

    // Read ADC and convert to actual physical voltages
    int raw_cap = analogRead(PIN_ADC_SUPERCAP);
    int raw_bus = analogRead(PIN_ADC_BUS_INPUT);

    tele.v_supercap = ((float)raw_cap / ADC_MAX_COUNT) * ADC_REF_VOLTAGE * VOLTAGE_DIVIDER_RATIO;
    tele.v_bus_input = ((float)raw_bus / ADC_MAX_COUNT) * ADC_REF_VOLTAGE * VOLTAGE_DIVIDER_RATIO;

    // E = 0.5 * C * V^2
    tele.est_stored_joules = 0.5f * s_capacitance * (tele.v_supercap * tele.v_supercap);
    tele.active_cycles = s_boot_counter;

    // Adaptive state evaluation based on voltage hysteresis
    if (tele.v_supercap < 2.0f) {
        tele.state = POWER_STATE_CRITICAL;
    } else if (tele.v_supercap < 3.0f) {
        tele.state = POWER_STATE_CHARGING;
    } else if (tele.v_supercap < 3.8f) {
        tele.state = POWER_STATE_SENSING;
    } else {
        tele.state = POWER_STATE_BURST_TX;
    }

    return tele;
}

uint64_t PowerManager_CalculateSleepDurationUs(const HarvesterTelemetry_t* tele) {
    switch (tele->state) {
        case POWER_STATE_CRITICAL:
            // Storage near empty: sleep for 60 seconds to accumulate ambient charge
            return 60ULL * 1000000ULL;
        case POWER_STATE_CHARGING:
            // Moderate reserve: sleep for 20 seconds
            return 20ULL * 1000000ULL;
        case POWER_STATE_SENSING:
            // Safe operation: duty-cycle 5 seconds
            return 5ULL * 1000000ULL;
        case POWER_STATE_BURST_TX:
        default:
            // Surplus ambient power available: responsive 2-second duty cycle
            return 2ULL * 1000000ULL;
    }
}

void PowerManager_EnterDeepSleep(uint64_t sleep_us) {
#if defined(ESP32)
    esp_sleep_enable_timer_wakeup(sleep_us);
    Serial.printf("[PMU] Entering deep sleep for %llu ms...\n", sleep_us / 1000ULL);
    Serial.flush();
    esp_deep_sleep_start();
#else
    // Fallback for simulation / non-ESP32 targets
    delay((unsigned long)(sleep_us / 1000ULL));
#endif
}
