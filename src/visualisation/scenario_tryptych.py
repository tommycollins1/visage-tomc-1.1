"""
Scenario Triptych Visualisation for ViSAGE 1.1

Panels:
1. Baseline visits
2. Scenario visits (with Oxford North)
3. OD flows from Oxford North to top destinations
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import contextily as ctx
import numpy as np


def plot_triptych(
    trip_df,
    flows_gdf,
    on_x,
    on_y,
    colour_map,
    sensitive_sites=None,
    ON_COLOR="#fca636"
):
    fig, axes = plt.subplots(1, 3, figsize=(36, 12))

    # ---------------------------------------------------------
    # PANEL 1 — BASELINE
    # ---------------------------------------------------------
    ax = axes[0]
    ax.scatter(
        trip_df.geometry.x,
        trip_df.geometry.y,
        s=np.sqrt(trip_df["visits_baseline"]) * 3,
        c=trip_df["class_baseline"].map(colour_map),
        edgecolor="white",
        linewidth=0.4,
        alpha=0.9,
        zorder=3,
    )

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13, zorder=0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_title("Baseline Greenspace Visits", fontsize=20)
    ax.set_axis_off()

    # ---------------------------------------------------------
    # PANEL 2 — SCENARIO
    # ---------------------------------------------------------
    ax = axes[1]
    ax.scatter(
        trip_df.geometry.x,
        trip_df.geometry.y,
        s=np.sqrt(trip_df["visits_scenario"]) * 3,
        c=trip_df["class_scenario"].map(colour_map),
        edgecolor="white",
        linewidth=0.4,
        alpha=0.9,
        zorder=3,
    )

    # Oxford North marker
    ax.scatter(on_x, on_y, s=350, color=ON_COLOR, edgecolor="black", linewidth=1.2)
    ax.text(
        on_x + 50,
        on_y + 50,
        "OxN",
        fontsize=14,
        color=ON_COLOR,
        path_effects=[pe.withStroke(linewidth=2, foreground="black")],
    )

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13, zorder=0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_title("Scenario: Oxford North Added", fontsize=20)
    ax.set_axis_off()

    # ---------------------------------------------------------
    # PANEL 3 — OD FLOWS
    # ---------------------------------------------------------
    ax = axes[2]

    flows_gdf.plot(
        ax=ax,
        linewidth=flows_gdf["visits"] / flows_gdf["visits"].max() * 8,
        alpha=0.7,
        color="orange",
        zorder=3,
    )

    ax.scatter(
        flows_gdf.geometry.x,
        flows_gdf.geometry.y,
        s=np.sqrt(flows_gdf["visits"]) * 4,
        color="#fca636",
        edgecolor="white",
        linewidth=0.4,
        alpha=0.9,
        zorder=4,
    )

    ax.scatter(on_x, on_y, s=400, color=ON_COLOR, edgecolor="black", linewidth=1.2)
    ax.text(
        on_x + 50,
        on_y + 50,
        "Oxford North",
        fontsize=14,
        color=ON_COLOR,
        path_effects=[pe.withStroke(linewidth=2, foreground="black")],
    )

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13, zorder=0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_title("OD Flows from Oxford North", fontsize=20)
    ax.set_axis_off()

    plt.tight_layout()
    plt.show()
