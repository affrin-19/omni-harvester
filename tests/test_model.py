"""
Unit tests for Omni-Harvester physical and circuit simulation engine.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../simulation")))

import pytest
from energy_model import OmniHarvesterModel


def test_model_initialization():
    model = OmniHarvesterModel(c_supercap=1.0, v_target=3.3)
    assert model.C_cap == 1.0
    assert model.V_target == 3.3
    assert model.V_diode_drop == 0.28


def test_solar_harvesting_calculation():
    model = OmniHarvesterModel()
    out_zero = model.calculate_source_outputs(solar_pct=0, vib_pct=0, delta_t=0, rf_pct=0)
    assert out_zero["v_solar"] == 0.0
    assert out_zero["i_solar"] == 0.0

    out_high = model.calculate_source_outputs(solar_pct=100, vib_pct=0, delta_t=0, rf_pct=0)
    assert out_high["v_solar"] > 5.5
    assert out_high["i_solar"] > 0.15
    assert bool(out_high["mcu_feasible"]) is True


def test_piezo_harvesting_calculation():
    model = OmniHarvesterModel()
    out = model.calculate_source_outputs(solar_pct=0, vib_pct=80, delta_t=0, rf_pct=0)
    assert out["v_piezo"] > 2.0
    assert out["i_piezo"] > 0.0


def test_teg_seebeck_calculation():
    model = OmniHarvesterModel()
    out = model.calculate_source_outputs(solar_pct=0, vib_pct=0, delta_t=30.0, rf_pct=0)
    assert out["v_teg"] > 1.0
    assert out["i_teg"] > 0.1


def test_diode_or_bus_selection():
    model = OmniHarvesterModel()
    # Solar should dominate bus voltage when high
    out = model.calculate_source_outputs(solar_pct=90, vib_pct=20, delta_t=10, rf_pct=10)
    assert out["v_bus"] > 4.0
    assert out["boost_v_out"] == 3.3


def test_transient_supercap_charging():
    model = OmniHarvesterModel()
    sim = model.simulate_transient(t_span=5.0, dt=0.5, solar_pct=80, vib_pct=40, delta_t=25, rf_pct=50)
    assert len(sim["time"]) == 10
    # Voltage should increase monotonically from initial residual state
    assert sim["v_cap"][-1] >= sim["v_cap"][0]
    assert sim["e_cum_total"][-1] > 0.0
