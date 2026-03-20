"""
Scenario Engine: Adding new origins (e.g., Oxford North) to ViSAGE.

This module:
- Adds a new origin with coordinates + population
- Appends it to the existing origins GeoDataFrame
- Recomputes the origin × destination distance matrix
"""

import numpy as np
import pandas as pd
import geopandas as gpd


def add_new_origin(origins_gdf, origin_id, easting, northing, population):
    """
    Add a new origin (e.g., Oxford North) to the origins GeoDataFrame.
    """

    new_origin = pd.DataFrame({
        "origin_id": [origin_id],
        "easting": [easting],
        "northing": [northing],
        "population": [population],
    })

    new_origin_gdf = gpd.GeoDataFrame(
        new_origin,
        geometry=gpd.points_from_xy(new_origin.easting, new_origin.northing),
        crs=origins_gdf.crs,
    )

    return pd.concat([origins_gdf, new_origin_gdf], ignore_index=True)


def compute_extended_distance_matrix(origins_gdf, destinations_gdf):
    """
    Compute full origin × destination Euclidean distance matrix.
    """

    orig_xy = np.vstack([origins_gdf.geometry.x, origins_gdf.geometry.y]).T
    dest_xy = np.vstack([destinations_gdf.geometry.x, destinations_gdf.geometry.y]).T

    dist_matrix = pd.DataFrame(
        np.sqrt(((orig_xy[:, None, :] - dest_xy[None, :, :]) ** 2).sum(axis=2)),
        index=origins_gdf["origin_id"],
        columns=destinations_gdf["site_id"],
    )

    return dist_matrix
