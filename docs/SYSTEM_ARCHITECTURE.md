# Omni-Harvester: System Architecture

The Omni-Harvester is a multi-modal energy harvesting and power management architecture engineered to enable autonomous, battery-less (or battery-assisted) operation of low-power Internet of Things (IoT) nodes across heterogeneous deployment environments.

## Architectural Overview

Single-source energy harvesting mechanisms suffer from fundamental environmental dependencies:
- **Photovoltaic (PV)**: Inactive during nighttime or in dark indoor installations.
- **Piezoelectric**: Requires periodic mechanical excitation (machinery, vehicular transit, acoustic vibration).
- **Thermoelectric (TEG)**: Relies on sustained temperature gradients ($\Delta T$).
- **Radio Frequency (RF)**: Ambient field densities are characteristically sparse and non-deterministic.

Omni-Harvester circumvents single-point power starvation by combining four orthogonal ambient domains through a low-loss, self-starting diode-OR combining network into a central high-density supercapacitor buffer.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Solar PV      │       │  PZT Piezo      │       │  Seebeck TEG    │
│  (6V, 1W Monoc) │       │ (8x 35mm Array) │       │ (TEC1-12706)    │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │ DC                      │ AC                      │ DC Low-V
         ▼                         ▼                         ▼
  ┌──────────────┐         ┌──────────────┐          ┌──────────────┐
  │ Pass-Through │         │ Full-Bridge  │          │ Direct Boost │
  │ Circuit      │         │ Rect (DF02M) │          │ Ready        │
  └──────┬───────┘         └──────┬───────┘          └──────┬───────┘
         │                        │                         │
      D1 ▼ (1N5819)            D2 ▼ (1N5819)             D3 ▼ (1N5819)
         └───────────────┬────────┴─────────────────────────┘
                         │
┌─────────────────┐      │
│   Ambient RF    │      │
│ (Villard Mult)  │      │
└────────┬────────┘      │
         ▼               │
      D4 ▼ (1N5819)      │
         └───────────────┼──────────────────────────────────┐
                         │                                  │
                         ▼                                  ▼
               ┌──────────────────┐               ┌──────────────────┐
               │ Smoothing Filter │               │ Supercapacitor   │
               │ (1000uF / 16V)   │               │ (1.0F / 5.5V)    │
               └────────┬─────────┘               └────────┬─────────┘
                        │                                  │
                        └─────────────────┬────────────────┘
                                          │
                                          ▼ DC Bus (1.0V - 5.5V)
                              ┌───────────────────────┐
                              │ Synchronous Boost     │
                              │ Regulator (TPS610981) │
                              └───────────┬───────────┘
                                          │
                                          ▼ Regulated 3.3V Bus (85% η)
                              ┌───────────────────────┐
                              │ Ultra-Low Power MCU   │
                              │ (ESP32 / MSP430)      │
                              │ Duty-Cycled IoT Load  │
                              └───────────────────────┘
```

## Power Management Architecture

### 1. Combining Topology
The system implements a parallel diode-OR combining architecture. Low-threshold Schottky rectifiers ($V_F \approx 0.28\text{V}$) isolate each generator. 
- Prevents cross-conduction and reverse discharge into inactive transducers (e.g., prevents the solar panel from back-biasing the TEG at night).
- Facilitates concurrent power pooling: whenever any transducer terminal voltage exceeds $V_{bus} + V_F$, charge current is directly delivered to the storage reservoir.

### 2. Central Storage Matrix
The primary storage element comprises a $1.0\text{ F} \text{ / } 5.5\text{V}$ Electric Double Layer Capacitor (EDLC) in parallel with an electrolytic smoothing capacitor ($1000\ \mu\text{F}$). This dual-tier capacitive configuration provides:
- High transient current handling for burst transmissions without excessive voltage droop.
- Over $500,000$ complete charge-discharge cycles with zero capacity fading.

### 3. Step-Up Power Regulation
A high-efficiency synchronous boost regulator (TI TPS610981 / LTC3105) transforms variable bus voltages ($0.7\text{V} \le V_{bus} \le 5.0\text{V}$) into a constant, low-noise $3.3\text{V}$ rail. The converter demonstrates:
- Cold-start capability at $V_{in} \approx 0.70\text{V}$.
- Quiescent current draw of $< 350\text{ nA}$ in standby.
- Peak power conversion efficiency of $\approx 85\%$.
