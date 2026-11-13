/**
 * @file power_manager.h
 * @brief Energy-Aware Adaptive Duty-Cycling and Power Management Unit
 * @author S. Affrin Wills, M. Abishek, G. S. Ajay Adithya
 */

#ifndef POWER_MANAGER_H
#define POWER_MANAGER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    POWER_STATE_CRITICAL = 0, // V_cap < 2.0V : Deep sleep, zero peripherals
    POWER_STATE_CHARGING = 1, // 2.0V <= V_cap < 3.0V : Minimal sleep wake, no RF
    POWER_STATE_SENSING  = 2, // 3.0V <= V_cap < 3.8V : Sensor acquisition only
    POWER_STATE_BURST_TX = 3  // V_cap >= 3.8V : Full telemetry burst transmission
} PowerOperatingState_t;

typedef struct {
    float v_supercap;        // Current supercapacitor buffer voltage in Volts
    float v_bus_input;       // Harvested input DC bus voltage in Volts
    float est_stored_joules; // Energy in storage: E = 0.5 * C * V^2
    uint32_t active_cycles;  // Total active cycles executed
    PowerOperatingState_t state;
} HarvesterTelemetry_t;

/**
 * @brief Initialize the ADC channels, storage thresholds, and RTC timer.
 * @param capacitance_farads Nominal capacitance of central buffer (e.g. 1.0F).
 */
void PowerManager_Init(float capacitance_farads);

/**
 * @brief Read analog bus voltages and evaluate current operating state.
 * @return Updated telemetry struct with state of charge.
 */
HarvesterTelemetry_t PowerManager_UpdateTelemetry(void);

/**
 * @brief Calculate optimal sleep duration based on energy inflow rate.
 * @param tele Current telemetry data.
 * @return Recommended sleep duration in microseconds (for deep-sleep timer).
 */
uint64_t PowerManager_CalculateSleepDurationUs(const HarvesterTelemetry_t* tele);

/**
 * @brief Enter ultra-low-power deep sleep mode.
 * @param sleep_us Sleep duration in microseconds.
 */
void PowerManager_EnterDeepSleep(uint64_t sleep_us);

#ifdef __cplusplus
}
#endif

#endif // POWER_MANAGER_H
