# Omni-Harvester: Schematic & Hardware Implementation Guide

This document provides circuit connection details, netlist nodes, and PCB design recommendations for fabricating the Omni-Harvester power management board.

## Proteus / SPICE Schematic Representation

```
                    D1 (1N5819)
    Solar (+)  ───────|>|───────┐
    (6V, 1W)                   │
                                │
                    D2 (1N5819) │
    TEG (+)    ───────|>|───────┼──────────┬──────────────┐
    (0.5V)                      │          │              │
                                │        + │              │
                    D3 (1N5819) │       ┌─────┐       ┌────────┐
    RF Harvester ─────|>|───────┤       │ C1  │       │ C_SUP  │
    (0.3V)                      │       │1000u│       │ 1.0F   │
                                │       │ 16V │       │  5.5V  │
    Piezo Array                 │       └─────┘       └────────┘
    (VSINE)                     │          │ -            │
        │                       │          │              │
     [Bridge]       D4 (1N5819) │          │              │
     (DF02M) ─────────|>|───────┘          │              │
        │                                  │              │
        └──────────────────────────────────┼──────────────┘
                                           │
                                           ▼ DC Bus (1.0V - 5.5V)
                                    ┌──────────────┐
                                    │ Boost Conv.  │
                                    │ (TPS610981)  │
                                    └──────┬───────┘
                                           │
                                           ▼ Regulated 3.3V
                                    ┌──────────────┐
                                    │ IoT MCU Load │
                                    └──────────────┘
```

## Trace Routing & Layout Guidelines
1. **RF Input Isolation**: Keep the RF rectenna feed trace separated by ground guard rings to prevent parasitic capacitive coupling into the switching boost converter.
2. **Low-ESR Supercapacitor Connections**: Minimize copper trace resistance between the supercapacitor terminals and the boost converter input pins ($< 20\text{ m}\Omega$) to prevent $I \cdot R$ drops during MCU radio transmit bursts.
3. **Diode Heat Dissipation**: Although currents are low, ensure solid copper pours around the solar Schottky diode cathode for thermal stability in high-ambient solar environments.
