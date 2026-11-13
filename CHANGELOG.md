# Changelog

All notable changes to the Omni-Harvester project are documented here.

## [1.0.0] - 2024-05-01

### Added
- **Multi-Modal Combining Architecture**:
  - Solar PV (6V, 1W), PZT Piezoelectric array (8x 35mm), TEG (TEC1-12706), and RF (4-stage Villard multiplier).
  - Low-forward-drop Schottky diode-OR topology (1N5819) with central 1.0F/5.5V EDLC supercapacitor.
- **Circuit Simulation & SPICE Models**:
  - Full transient netlist (`omni_harvester.cir`) with diode-level conduction modeling.
  - Python mathematical engine (`energy_model.py`) and automated test suite (`tests/`).
- **Interactive Web Simulation Dashboard**:
  - Standalone HTML5/Canvas dashboard replicating research presentation telemetry.
- **Embedded Firmware**:
  - Energy-aware adaptive duty-cycling algorithms for ultra-low power microcontrollers.
  - Hysteresis-governed operating state machine.
- **Documentation**:
  - System architecture specification, mathematical circuit analysis, and comprehensive BOM.
