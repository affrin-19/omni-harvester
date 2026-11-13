"""
Omni-Harvester: Hybrid Multi-Source Energy Harvesting Physical Model
Mathematical model calculating multi-source generation, diode-OR combining,
supercapacitor state-of-charge dynamics, and boost converter efficiency.
"""

import numpy as np


class OmniHarvesterModel:
    """Comprehensive physical and circuit model for the Omni-Harvester system."""

    def __init__(self, c_supercap: float = 1.0, v_target: float = 3.3):
        """
        Initialize Omni-Harvester parameters.
        :param c_supercap: Storage capacitance in Farads (default 1.0F).
        :param v_target: Regulated output voltage in Volts (default 3.3V).
        """
        self.C_cap = c_supercap
        self.V_target = v_target

        # Diode parameters (1N5819 Schottky)
        self.V_diode_drop = 0.28  # Forward drop in Volts @ nominal current

        # Solar PV specs (6V, 1W nominal)
        self.solar_voc = 6.0
        self.solar_isc = 0.167
        self.solar_r_int = 36.0

        # Piezoelectric specs (8x 35mm discs array)
        self.piezo_n_discs = 8
        self.piezo_v_peak_max = 5.0
        self.piezo_r_int = 2500.0

        # TEG specs (TEC1-12706 Seebeck module)
        self.teg_alpha = 0.043  # Seebeck coefficient V/K
        self.teg_r_int = 2.5    # Internal resistance in Ohms

        # RF Harvester specs (4-stage Villard multiplier)
        self.rf_max_voltage = 0.45
        self.rf_r_int = 1000.0

        # PMU & Storage
        self.pmu_v_start = 0.70  # Minimum boost converter startup voltage
        self.pmu_efficiency_peak = 0.85
        self.supercap_leakage_r = 500e3  # 500 kOhm self-discharge

        # IoT MCU Load Profile (ESP32 / Low-Power MCU)
        self.i_sleep = 5e-6       # 5 uA deep sleep
        self.i_active = 20e-3     # 20 mA active RF transmission
        self.duty_cycle = 0.01    # 1% active duty cycle (100ms per 10s)

    def calculate_source_outputs(self, solar_pct: float, vib_pct: float, delta_t: float, rf_pct: float):
        """
        Calculate instantaneous open-circuit and matched voltages from each ambient source.
        :param solar_pct: Solar irradiance (0 to 100%)
        :param vib_pct: Mechanical vibration intensity (0 to 100%)
        :param delta_t: Temperature gradient across TEG in deg C (0 to 60 C)
        :param rf_pct: Ambient RF field strength (0 to 100%)
        :return: dict with voltages, currents, and powers
        """
        # 1. Solar
        solar_ratio = np.clip(solar_pct / 100.0, 0.0, 1.0)
        v_solar = self.solar_voc * (0.85 + 0.15 * solar_ratio) if solar_ratio > 0.01 else 0.0
        i_solar = self.solar_isc * solar_ratio

        # 2. Piezo (Rectified output)
        vib_ratio = np.clip(vib_pct / 100.0, 0.0, 1.0)
        v_piezo = (self.piezo_v_peak_max * 0.707) * vib_ratio  # RMS post-bridge
        i_piezo = (v_piezo / self.piezo_r_int) * self.piezo_n_discs if v_piezo > 0 else 0.0

        # 3. Thermoelectric (Seebeck effect)
        dt = np.clip(delta_t, 0.0, 80.0)
        v_teg = dt * self.teg_alpha
        i_teg = v_teg / (2.0 * self.teg_r_int) if v_teg > 0 else 0.0

        # 4. RF Harvester
        rf_ratio = np.clip(rf_pct / 100.0, 0.0, 1.0)
        v_rf = self.rf_max_voltage * (rf_ratio ** 0.5)
        i_rf = (v_rf / self.rf_r_int) if v_rf > 0 else 0.0

        # Combine onto DC Bus via diode-OR
        # Each source that exceeds V_bus + V_diode contributes current
        source_potentials = {
            "Solar": max(0.0, v_solar - self.V_diode_drop),
            "Piezo": max(0.0, v_piezo - self.V_diode_drop),
            "TEG": max(0.0, v_teg - self.V_diode_drop),
            "RF": max(0.0, v_rf - self.V_diode_drop),
        }

        v_bus = max(source_potentials.values())

        # Total current injected into the DC bus
        total_current = 0.0
        if v_solar - self.V_diode_drop >= v_bus * 0.95:
            total_current += i_solar
        if v_piezo - self.V_diode_drop >= v_bus * 0.95:
            total_current += i_piezo
        if v_teg - self.V_diode_drop >= v_bus * 0.95:
            total_current += i_teg
        if v_rf - self.V_diode_drop >= v_bus * 0.95:
            total_current += i_rf

        total_power = v_bus * total_current

        # Boost converter regulation
        if v_bus >= self.pmu_v_start:
            boost_v_out = self.V_target
            # Efficiency curve asymptotically approaches ~85%
            efficiency = self.pmu_efficiency_peak * (1.0 - np.exp(-1.8 * v_bus))
        elif v_bus > 0.4:
            boost_v_out = v_bus * 2.0  # partial boost in sub-threshold
            efficiency = 0.40 * (v_bus / self.pmu_v_start)
        else:
            boost_v_out = 0.0
            efficiency = 0.0

        # Average MCU power requirement
        p_mcu_avg = (self.i_sleep * (1 - self.duty_cycle) + self.i_active * self.duty_cycle) * self.V_target
        mcu_feasible = (total_power * efficiency >= p_mcu_avg) or (v_bus >= 2.0)

        return {
            "v_solar": v_solar,
            "v_piezo": v_piezo,
            "v_teg": v_teg,
            "v_rf": v_rf,
            "i_solar": i_solar,
            "i_piezo": i_piezo,
            "i_teg": i_teg,
            "i_rf": i_rf,
            "v_bus": v_bus,
            "total_current": total_current,
            "total_power": total_power,
            "boost_v_out": boost_v_out,
            "efficiency": efficiency * 100.0,
            "mcu_feasible": mcu_feasible,
            "p_mcu_avg": p_mcu_avg,
        }

    def simulate_transient(self, t_span: float, dt: float, solar_pct: float, vib_pct: float, delta_t: float, rf_pct: float):
        """
        Simulate transient charging of the central supercapacitor over time.
        """
        steps = int(t_span / dt)
        time = np.linspace(0, t_span, steps)

        outputs = self.calculate_source_outputs(solar_pct, vib_pct, delta_t, rf_pct)
        p_in = outputs["total_power"]

        v_cap = np.zeros(steps)
        e_cum_solar = np.zeros(steps)
        e_cum_piezo = np.zeros(steps)
        e_cum_total = np.zeros(steps)
        i_load = np.zeros(steps)

        # Baseline energy integration
        p_sol = outputs["v_solar"] * outputs["i_solar"]
        p_piez = outputs["v_piezo"] * outputs["i_piezo"]

        current_v = 0.05  # initial residual voltage

        for i in range(steps):
            # Leakage power = V^2 / R_leak
            p_leak = (current_v ** 2) / self.supercap_leakage_r
            # Net power into capacitor
            p_net = max(0.0, p_in - p_leak)

            # dE = P * dt, E = 0.5 * C * V^2 => V = sqrt(2*E/C)
            e_cap = 0.5 * self.C_cap * (current_v ** 2) + p_net * dt
            current_v = np.sqrt(max(0.0, 2.0 * e_cap / self.C_cap))
            current_v = min(current_v, outputs["v_bus"])  # clamped to input bus

            v_cap[i] = current_v
            e_cum_solar[i] = p_sol * time[i]
            e_cum_piezo[i] = p_piez * time[i]
            e_cum_total[i] = (p_sol + p_piez + (outputs["v_teg"] * outputs["i_teg"])) * time[i]

            # Dynamic load current drawn by MCU
            if current_v >= self.pmu_v_start:
                # Regulated load draw: ~19.5 mA with minor ripple
                i_load[i] = 0.0195 + 0.0004 * np.sin(2 * np.pi * 0.2 * time[i])
            else:
                i_load[i] = self.i_sleep

        return {
            "time": time,
            "v_cap": v_cap,
            "e_cum_solar": e_cum_solar,
            "e_cum_piezo": e_cum_piezo,
            "e_cum_total": e_cum_total,
            "i_load": i_load,
            "outputs": outputs,
        }
