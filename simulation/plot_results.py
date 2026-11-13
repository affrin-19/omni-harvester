"""
Omni-Harvester: Plotting and Benchmark Reproduction
Generates high-resolution publication figures matching the research paper:
1. Cumulative Energy Harvested vs Time (Fig. 4)
2. Current Flow to Load vs Time (Fig. 5)
3. Boost Converter Vout & Efficiency vs Input Voltage (Slide 5)
4. Multi-Source Electrical Metrics Bar Chart (Slide 4)
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from energy_model import OmniHarvesterModel


def generate_all_plots(output_dir: str = "../docs/images"):
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    model = OmniHarvesterModel(c_supercap=1.0, v_target=3.3)

    # Simulation matching paper parameters:
    # Solar: 80%, Vibration: 40%, Delta T: 31 C, RF: 81%
    sim_data = model.simulate_transient(
        t_span=10.0,
        dt=0.1,
        solar_pct=80.0,
        vib_pct=40.0,
        delta_t=31.0,
        rf_pct=81.0,
    )

    t = sim_data["time"]

    # -------------------------------------------------------------
    # Figure 1: Cumulative Energy Harvested from All Sensors (Fig. 4)
    # -------------------------------------------------------------
    plt.figure(figsize=(7, 5), dpi=300)
    plt.plot(t, sim_data["e_cum_solar"], label="Solar", color="#2b7bba", linewidth=2.0)
    plt.plot(t, sim_data["e_cum_piezo"], label="Piezo", color="#e87d1e", linewidth=2.0)
    plt.plot(t, sim_data["e_cum_total"], label="Total", color="#2ca02c", linewidth=2.2, linestyle="--")

    plt.title("Cumulative Energy Harvested from All Sensors", fontsize=12, fontweight="bold")
    plt.xlabel("Time (s)", fontsize=11)
    plt.ylabel("Energy (Joules)", fontsize=11)
    plt.ylim(bottom=-0.05, top=0.95)
    plt.legend(frameon=True, loc="upper left")
    plt.tight_layout()
    fig4_path = os.path.join(output_dir, "fig4_cumulative_energy.png")
    plt.savefig(fig4_path)
    plt.close()
    print(f"[+] Saved: {fig4_path}")

    # -------------------------------------------------------------
    # Figure 2: Current Flow to Load vs Time (Fig. 5)
    # -------------------------------------------------------------
    plt.figure(figsize=(7, 5), dpi=300)
    plt.plot(t, sim_data["i_load"], color="#1f77b4", linewidth=2.2)
    plt.fill_between(t, sim_data["i_load"], color="#1f77b4", alpha=0.6)

    plt.title("Current Flow to Load vs Time", fontsize=12, fontweight="bold")
    plt.xlabel("Time (s)", fontsize=11)
    plt.ylabel("Load Current (A)", fontsize=11)
    plt.ylim(0.0160, 0.0205)
    plt.tight_layout()
    fig5_path = os.path.join(output_dir, "fig5_load_current.png")
    plt.savefig(fig5_path)
    plt.close()
    print(f"[+] Saved: {fig5_path}")

    # -------------------------------------------------------------
    # Figure 3: Boost Output Voltage and Efficiency vs Input (Slide 5)
    # -------------------------------------------------------------
    vin_sweep = np.linspace(0.0, 5.4, 100)
    vout_sweep = []
    eff_sweep = []

    for v in vin_sweep:
        if v >= 0.70:
            vout_sweep.append(3.30)
            eff_sweep.append(85.0 * (1.0 - np.exp(-1.8 * v)))
        elif v > 0.40:
            vout_sweep.append(v * 2.0)
            eff_sweep.append(40.0 * (v / 0.70))
        else:
            vout_sweep.append(0.0)
            eff_sweep.append(0.0)

    fig, ax1 = plt.subplots(figsize=(7.5, 5), dpi=300)

    ax1.set_xlabel("Supercapacitor / Bus Voltage (V)", fontsize=11)
    ax1.set_ylabel("Regulated Vout (V)", color="#46a346", fontsize=11)
    line1 = ax1.plot(vin_sweep, vout_sweep, color="#46a346", linewidth=2.5, label="Vout (3.3V Target)")
    ax1.tick_params(axis="y", labelcolor="#46a346")
    ax1.set_ylim(-0.2, 4.2)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Efficiency (%)", color="#73b82e", fontsize=11)
    line2 = ax2.plot(vin_sweep, eff_sweep, color="#73b82e", linewidth=2.0, linestyle="--", marker="o", markersize=3, label="Efficiency (%)")
    ax2.tick_params(axis="y", labelcolor="#73b82e")
    ax2.set_ylim(0, 105)

    plt.title("Boost Converter Output & Efficiency vs Input Voltage", fontsize=12, fontweight="bold")
    plt.tight_layout()
    eff_path = os.path.join(output_dir, "boost_efficiency_curve.png")
    plt.savefig(eff_path)
    plt.close()
    print(f"[+] Saved: {eff_path}")

    # -------------------------------------------------------------
    # Figure 4: Source Voltages & Current Breakdown (Slide 4)
    # -------------------------------------------------------------
    sources = ["Solar", "Piezo", "TEG", "RF"]
    out = sim_data["outputs"]
    voltages = [out["v_solar"], out["v_piezo"], out["v_teg"], out["v_rf"]]
    currents_ma = [out["i_solar"] * 1000, out["i_piezo"] * 1000, out["i_teg"] * 1000, out["i_rf"] * 1000]

    x = np.arange(len(sources))
    width = 0.35

    fig, ax_v = plt.subplots(figsize=(7.5, 5), dpi=300)
    rects1 = ax_v.bar(x - width/2, voltages, width, label="Voltage (V)", color="#c7781b")
    ax_v.set_ylabel("Voltage (V)", color="#c7781b", fontsize=11)
    ax_v.set_ylim(0, 7.0)

    ax_i = ax_v.twinx()
    rects2 = ax_i.bar(x + width/2, currents_ma, width, label="Current (mA)", color="#f5bc8c")
    ax_i.set_ylabel("Current (mA)", color="#b86b2e", fontsize=11)
    ax_i.set_ylim(0, 300)

    ax_v.set_xticks(x)
    ax_v.set_xticklabels(sources, fontsize=11, fontweight="bold")
    plt.title("Multi-Source Electrical Metrics Breakdown", fontsize=12, fontweight="bold")
    plt.tight_layout()
    bar_path = os.path.join(output_dir, "source_metrics_breakdown.png")
    plt.savefig(bar_path)
    plt.close()
    print(f"[+] Saved: {bar_path}")

    print("\n[✔] All research paper & presentation benchmark plots successfully generated!")


if __name__ == "__main__":
    generate_all_plots()
