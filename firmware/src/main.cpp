/**
 * @file main.cpp
 * @brief Omni-Harvester Embedded IoT Node Firmware
 *
 * Implements autonomous operation powered exclusively by hybrid ambient energy.
 * Handles sensor telemetry acquisition, power budget calculation, and
 * energy-proportional transmission bursts.
 *
 * Authors: S. Affrin Wills, M. Abishek, G. S. Ajay Adithya
 */

#include <Arduino.h>
#include "power_manager.h"

// Diagnostic indicator pin
#define PIN_STATUS_LED 2

void setup() {
    Serial.begin(115200);
    pinMode(PIN_STATUS_LED, OUTPUT);
    digitalWrite(PIN_STATUS_LED, HIGH);

    Serial.println("\n=======================================================");
    Serial.println("  Omni-Harvester: Autonomous Energy-Harvesting Node");
    Serial.println("=======================================================");

    // Initialize PMU with 1.0 Farad storage
    PowerManager_Init(1.0f);

    // Read current energy telemetry
    HarvesterTelemetry_t tele = PowerManager_UpdateTelemetry();

    Serial.printf("[Tele] V_supercap   : %.2f V\n", tele.v_supercap);
    Serial.printf("[Tele] V_bus_input  : %.2f V\n", tele.v_bus_input);
    Serial.printf("[Tele] Stored Energy: %.3f Joules\n", tele.est_stored_joules);
    Serial.printf("[Tele] Power State  : %d\n", (int)tele.state);

    // Execute state-dependent task
    if (tele.state >= POWER_STATE_SENSING) {
        Serial.println("[Task] Acquiring onboard environmental sensor data...");
        // Simulated sensor reading (e.g., I2C temperature/vibration probe)
        delay(20); // 20ms minimal active time
    }

    if (tele.state == POWER_STATE_BURST_TX) {
        Serial.println("[Task] Energy budget sufficient -> Transmitting RF telemetry burst...");
        // Simulated BLE advertisement or LoRaWAN uplink
        delay(80); // 80ms active radio time
    }

    digitalWrite(PIN_STATUS_LED, LOW);

    // Calculate energy-aware deep sleep interval
    uint64_t sleep_us = PowerManager_CalculateSleepDurationUs(&tele);
    PowerManager_EnterDeepSleep(sleep_us);
}

void loop() {
    // Execution never reaches loop due to deep sleep reset cycle
}
