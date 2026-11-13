# Bill of Materials (BOM) — Omni-Harvester

The Omni-Harvester architecture is designed using commercially available, cost-effective components optimized for low-power energy conversion, minimal forward drop, and maximum harvesting endurance.

## Component Breakdown

| Item | Reference | Component Name | Description | Key Specifications | Typical Part | Qty |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | **PV1** | Solar Panel | Monocrystalline micro-solar panel | $V_{oc} = 6.0\text{V}$, $I_{sc} = 167\text{mA}$, $P_{peak} = 1\text{W}$ | Generic 6V-1W | 1 |
| 2 | **PZ1–PZ8** | Piezoelectric Array | PZT Brass Disc Transducers | Resonant Freq: $2.9\text{ kHz}$, Capacitance: $30\text{ nF}$ | Murata 7BB-35-3C0 | 8 |
| 3 | **TEG1** | Thermoelectric Generator | Peltier/Seebeck Bismuth Telluride Module | $\Delta T = 20\text{–}60^\circ\text{C}$, Output: $0.3\text{–}1.8\text{V}$, $R_{int} \approx 2.5\ \Omega$ | TEC1-12706 / SP1848 | 1 |
| 4 | **ANT1** | RF Receiving Antenna | Multiband GSM / ISM / Wi-Fi Patch Antenna | $850\text{ MHz} \text{ / } 2.4\text{ GHz}$, Gain: $+3\text{ dBi}$, $Z_0 = 50\ \Omega$ | Molex 1461530100 | 1 |
| 5 | **BR1** | Full-Wave Bridge | AC-to-DC Bridge Rectifier (Piezo Stage) | $V_{RRM} = 100\text{V}$, Low leakage, Fast recovery | DF02M / DB107S | 1 |
| 6 | **D1–D4** | Isolation Diodes | Schottky Barrier Rectifiers (Bus Diode-OR) | $V_F \approx 0.28\text{V} @ 10\text{mA}$, $V_R = 40\text{V}$, $I_{rev} < 10\ \mu\text{A}$ | 1N5819 / BAT54S | 4 |
| 7 | **D_RF1–D_RF4** | RF Rectifiers | Germanium / Zero-Bias Schottky Diodes | Ultra-low turn-on ($V_F \approx 0.15\text{V}$), $C_j < 1\text{ pF}$ | 1N34A / SMS7630 | 4 |
| 8 | **C1** | Smoothing Capacitor | Low-ESR Electrolytic Bus Filter | $1000\ \mu\text{F}$, $16\text{V}$, ESR $< 50\text{ m}\Omega$ | Nichicon UVR1C102MPD | 1 |
| 9 | **C_SUPER** | Storage Supercapacitor | EDLC (Electric Double-Layer Capacitor) | $1.0\text{ F}$, $5.5\text{V}$, Low self-discharge | Eaton PB-5R5V105-R | 1 |
| 10 | **U1** | PMU Boost Converter | Ultra-Low Quiescent Synchronous Boost | $V_{in,min} = 0.65\text{V}$, $V_{out} = 3.3\text{V}$, $I_Q = 300\text{ nA}$, $\eta \approx 85\%$ | TI TPS610981 / LTC3105 | 1 |
| 11 | **U2** | MCU IoT Node | Ultra-Low Power Microcontroller | Deep sleep $< 5\ \mu\text{A}$, Active RF burst $20\text{ mA}$ | ESP32-PICO / MSP430 | 1 |
| 12 | **R1** | Current Limiter | Metal Film Resistor | $330\ \Omega$, $1/4\text{W}$, $1\%$ tolerance | Yageo MFR-25 | 1 |
| 13 | **D5** | Status Indicator | Ultra-Low Current LED (Diagnostic) | Red, $V_F = 1.7\text{V}$, $I_F = 2\text{mA}$ | Broadcom HLMP-1700 | 1 |

## Component Selection Rationale

### 1. Diode-OR Topology vs. Active Switches
Schottky barrier diodes (1N5819) provide an ultra-simple, robust, zero-control isolation mechanism. Unlike active MOSFET switches, diodes require zero gate-drive overhead, avoiding cold-start failure when all storage buffers are fully depleted ($0\text{V}$ start condition).

### 2. High-Frequency RF Diodes
RF voltage rectification requires diodes with sub-picofarad junction capacitance ($C_j < 1\text{ pF}$) and negligible forward threshold voltage. The 1N34A germanium point-contact diode (or SMS7630 zero-bias Schottky) provides rectification at microwatt input RF power levels.

### 3. Supercapacitor Selection
A $1.0\text{ F} \text{ / } 5.5\text{V}$ EDLC supercapacitor was selected over lithium-ion chemistry to eliminate degradation from repeated shallow charge/discharge cycles ($> 500,000$ cycle lifespan), wide thermal operating range ($-40^\circ\text{C}$ to $+85^\circ\text{C}$), and zero chemical fire hazard in unattended IoT installations.
