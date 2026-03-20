"""
Oxford North Scenario Example Script for ViSAGE 1.1

This script:
- Loads origins and destinations
- Adds Oxford North as a new origin
- Recomputes the distance matrix
- Runs the scenario gravity model (baseline or quality)
- Computes site-level impacts
- Builds OD flows from Oxford North
- Produces the triptych visualisation
"""

from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd

# ------------------------------
# IMPORT MODULES
# ------------------------------

from src.data.load_origins import load_origins
from src.data.load_destinations import load_destinations

from src.behaviour.distance_decay import (
    LAMBDA_PANS,
    run_gravity_with_pans_lambda,
)

from src.model.quality_attractor import run_quality_sensitive_gravity

from src.scenarios.add_origin import (
    add_new_origin,
    compute_extended_distance_matrix,
)

from src.scenarios.run_scenario import (
    compute_scenario_visits,
    compute_impact,
)

from src.visualisation.scenario_triptych import plot_triptych


# ------------------------------
# 1. PATHS
# ------------------------------

DATA_DIR = Path("data") / "raw"

ORIGINS_PATH = DATA_DIR / "synthetic_pop(in).csv"
DESTINATIONS_PATH = DATA_DIR / "site_catalogue_with_quality.csv"


# ------------------------------
# 2. LOAD DATA
# ------------------------------

origins_gdf = load_origins(str(ORIGINS_PATH))
destinations_gdf = load_destinations(str(DESTINATIONS_PATH))


# ------------------------------
# 3. ADD OXFORD NORTH
# ------------------------------

OXFORD_NORTH_ID = "OXFORD_NORTH"
OXFORD_NORTH_E = 451900
OXFORD_NORTH_N = 208000
OXFORD_NORTH_POP = 4000

origins_extended = add_new_origin(
    origins_gdf,
    origin_id=OXFORD_NORTH_ID,
    easting=OXFORD_NORTH_E,
    northing=OXFORD_NORTH_N,
    population=OXFORD_NORTH_POP,
)


# ------------------------------
# 4. RECOMPUTE DISTANCE MATRIX
# ------------------------------

dist_matrix_extended = compute_extended_distance_matrix(
    origins_extended,
    destinations_gdf,
)


# ------------------------------
# 5. RUN BASELINE (NO OXFORD NORTH)
# ------------------------------

baseline_df = run_gravity_with_pans_lambda(
    origins_gdf.drop(columns="geometry"),
    destinations_gdf.drop(columns="geometry"),
    pd.DataFrame(
        np.sqrt(
            ((np.vstack([origins_gdf.geometry.x, origins_gdf.geometry.y]).T[:, None, :]
              - np.vstack([destinations_gdf.geometry.x, destinations_gdf.geometry.y]).T[None, :, :]) ** 2
            ).sum(axis=2)
        ),
        index=origins_gdf["origin_id"],
        columns=destinations_gdf["site_id"],
    )
)

baseline_visits = (
    baseline_df.groupby("site_id")["visits"]
    .sum()
    .reset_index()
    .rename(columns={"visits": "visits_baseline"})
)


# ------------------------------
# 6. RUN SCENARIO (WITH OXFORD NORTH)
# ------------------------------

scenario_df, scenario_visits = compute_scenario_visits(
    origins_df=origins_extended.drop(columns="geometry"),
    destinations_df=destinations_gdf.drop(columns="geometry"),
    dist_matrix=dist_matrix_extended,
    gravity_function=run_gravity_with_pans_lambda,
    lambda_value=LAMBDA_PANS,
)


# ------------------------------
# 7. COMPUTE IMPACT
# ------------------------------

impact_df = compute_impact(baseline_visits, scenario_visits)

print("\n=== TOP 20 IMPACTED SITES ===\n")
print(
    impact_df[
        ["site_id", "visits_baseline", "visits_scenario",
         "delta_visits", "pct_change"]
    ].head(20)
)


# ------------------------------
# 8. BUILD OD FLOWS FROM OXFORD NORTH
# ------------------------------

on_flows = scenario_df[scenario_df["origin_id"] == OXFORD_NORTH_ID].copy()
on_flows = on_flows.merge(
    destinations_gdf[["site_id", "geometry"]],
    on="site_id",
    how="left"
)

# Keep top 10 flows
on_flows = on_flows.nlargest(10, "visits")
flows_gdf = gpd.GeoDataFrame(on_flows, geometry="geometry", crs=destinations_gdf.crs)


# ------------------------------
# 9. PREPARE TRIPTYCH INPUT
# ------------------------------

trip = destinations_gdf.copy()

trip = trip.merge(baseline_visits, on="site_id", how="left")
trip = trip.merge(scenario_visits, on="site_id", how="left")

# Simple class bins (you can refine later)
trip["class_baseline"] = pd.qcut(trip["visits_baseline"], q=6, labels=False)
trip["class_scenario"] = pd.qcut(trip["visits_scenario"], q=6, labels=False)


# ------------------------------
# 10. PLOT TRIPTYCH
# ------------------------------

colour_map = {
    0: "#fee5d9",
    1: "#fcae91",
    2: "#fb6a4a",
    3: "#de2d26",
    4: "#a50f15",
    5: "#67000d",
}

plot_triptych(
    trip_df=trip,
    flows_gdf=flows_gdf,
    on_x=OXFORD_NORTH_E,
    on_y=OXFORD_NORTH_N,
    colour_map=colour_map,
)
