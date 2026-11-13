# Energy Budget & Sizing Analysis — Omni-Harvester

## IoT Node Energy Consumption Profile

The system load is an ultra-low power wireless sensor node (e.g., ESP32-PICO or MSP430FR5969) operating in periodic sleep-wake cycles.

### Operating Modes & Power Draws

| Operational State | Duration ($T_i$) | Current ($I_i$ @ 3.3V) | Power ($P_i$) | Energy per Cycle ($E_i$) |
| :--- | :--- | :--- | :--- | :--- |
| **Deep Sleep (RTC on)** | $9.90\text{ s}$ | $5.0\ \mu\text{A}$ | $16.5\ \mu\text{W}$ | $163.35\ \mu\text{J}$ |
| **Sensor Wake & ADC Read** | $0.02\text{ s}$ ($20\text{ ms}$) | $3.5\text{ mA}$ | $11.55\text{ mW}$ | $231.00\ \mu\text{J}$ |
| **BLE/LoRa RF Burst Tx** | $0.08\text{ s}$ ($80\text{ ms}$) | $20.0\text{ mA}$ | $66.00\text{ mW}$ | $5280.00\ \mu\text{J}$ |
| **Total per 10s Cycle** | $\mathbf{10.00\text{ s}}$ | **Avg: $171.4\ \mu\text{A}$** | **Avg: $567.4\ \mu\text{W}$** | $\mathbf{5.674\text{ mJ}}$ |

---

## Supercapacitor Buffer Sizing

To guarantee uninterrupted operation through maximum expected blackout periods (e.g., zero sunlight, zero vibration, zero RF field for $T_{autonomy} = 12\text{ hours}$):

$$E_{required} = P_{sleep} \times T_{autonomy} = 16.5\ \mu\text{W} \times 43200\text{ s} \approx 0.713\text{ Joules}$$

The usable energy extracted from an electric double-layer capacitor between $V_{max} = 5.0\text{V}$ and the boost converter minimum cutoff voltage $V_{cutoff} = 0.70\text{V}$:

$$\Delta E_{usable} = \frac{1}{2} C \left( V_{max}^2 - V_{cutoff}^2 \right) \cdot \eta_{boost}$$

For $C = 1.0\text{ Farad}$ and $\eta_{boost} \approx 85\%$:

$$\Delta E_{usable} = \frac{1}{2} (1.0) \left( 5.0^2 - 0.70^2 \right) \times 0.85 = \frac{1}{2} (24.51) \times 0.85 \approx \mathbf{10.41\text{ Joules}}$$

$$\text{Autonomy Margin} = \frac{10.41\text{ J}}{0.713\text{ J}} \approx \mathbf{14.6\times \text{ safety factor}}$$

The $1.0\text{ F}$ supercapacitor provides more than **7.3 days** of sustained deep-sleep survival in total energy darkness, or over **1,830 complete sensing and transmission bursts** without any external harvesting contribution.
