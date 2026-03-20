from pathlib import Path

import pandas as pd
import geopandas as gpd
import numpy as np

from src.data.load_origins import load_origins
from src.data.load_destinations import load_destinations
from src.behaviour.distance_decay import LAMBDA_PANS
from src.model.quality_attractor import run_quality_sensitive_gravity
from src.visualisation.ranking_comparisons import (
    build_ranking_comparison,
    plot_top_n_rank_change,
)


# ---------------------------------------------------------
# 1. PATHS
# ---------------------------------------------------------

DATA_DIR = Path("data") / "raw"

ORIGINS_PATH = DATA_DIR / "synthetic_pop(in).csv"
DESTINATIONS_PATH = DATA_DIR / "site_catalogue_with_quality.csv"


# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------

origins_gdf = load_origins(str(ORIGINS_PATH))
destinations_gdf = load_destinations(str(DESTINATIONS_PATH))

# Ensure QualityScore exists
if "QualityScore" not in destinations_gdf.columns:
    raise ValueError("Expected 'QualityScore' column in site_catalogue_with_quality.csv")


# ---------------------------------------------------------
# 3. BUILD DISTANCE MATRIX
# ---------------------------------------------------------

orig_xy = np.vstack([origins_gdf.geometry.x, origins_gdf.geometry.y]).T
dest_xy = np.vstack([destinations_gdf.geometry.x, destinations_gdf.geometry.y]).T

dist_matrix = pd.DataFrame(
    np.sqrt(((orig_xy[:, None, :] - dest_xy[None, :, :]) ** 2).sum(axis=2)),
    index=origins_gdf["origin_id"],
    columns=destinations_gdf["site_id"],
)


# ---------------------------------------------------------
# 4. RUN BASELINE (distance-only)
# ---------------------------------------------------------

from src.behaviour.distance_decay import run_gravity_with_pans_lambda

baseline_df = run_gravity_with_pans_lambda(
    origins_gdf.drop(columns="geometry"),
    destinations_gdf.drop(columns="geometry"),
    dist_matrix
)


# ---------------------------------------------------------
# 5. RUN QUALITY-SENSITIVE MODEL
# ---------------------------------------------------------

quality_df = run_quality_sensitive_gravity(
    origins_df=origins_gdf.drop(columns="geometry"),
    destinations_df=destinations_gdf.drop(columns="geometry"),
    dist_matrix=dist_matrix,
    lambda_value=LAMBDA_PANS,
    beta=1.0,  # quality sensitivity
)


# ---------------------------------------------------------
# 6. BUILD RANKING COMPARISON TABLE
# ---------------------------------------------------------

ranking = build_ranking_comparison(baseline_df, quality_df)

print("\n=== TOP 20 RANKING COMPARISON ===\n")
print(
    ranking[
        ["site_id", "visits_baseline", "visits_quality",
         "rank_baseline", "rank_quality", "rank_change"]
    ].head(20)
)


# ---------------------------------------------------------
# 7. PLOT RANK CHANGE FOR TOP 10 QUALITY SITES
# ---------------------------------------------------------

plot_top_n_rank_change(ranking, top_n=10)
