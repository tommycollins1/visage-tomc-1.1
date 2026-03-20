from pathlib import Path

from src.data.load_origins import load_origins
from src.data.load_destinations import load_destinations
from src.model.spatial_interaction import model_2
from src.visualisation.baseline_maps import plot_greenspace_visits_osm


DATA_DIR = Path("data") / "raw"

ORIGINS_PATH = DATA_DIR / "synthetic_pop(in).csv"
DESTINATIONS_PATH = DATA_DIR / "site_catalogue(in).csv"

VISITS_PER_PERSON = 50    # placeholder
LAMBDA_M = 1500           # placeholder (1.5 km decay)


def main():
    origins_gdf = load_origins(str(ORIGINS_PATH))
    destinations_gdf = load_destinations(str(DESTINATIONS_PATH))

    m2 = model_2(
        origins_df=origins_gdf.drop(columns="geometry"),
        destinations_df=destinations_gdf.drop(columns="geometry"),
        visits_per_person=VISITS_PER_PERSON,
        lambda_m=LAMBDA_M,
    )

    plot_greenspace_visits_osm(
        model_df=m2,
        destinations_gdf=destinations_gdf,
        title="Oxford Greenspace Visit Volume (Baseline, distance-only)",
    )


if __name__ == "__main__":
    main()
