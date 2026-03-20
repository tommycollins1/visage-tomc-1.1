"""
Scenario Engine: Running scenario gravity models (e.g., Oxford North).

This module:
- Runs baseline or quality-sensitive gravity model
- Computes site-level impacts (delta visits, % change)
"""

import pandas as pd


def compute_scenario_visits(
    origins_df,
    destinations_df,
    dist_matrix,
    gravity_function,
    lambda_value,
    **kwargs
):
    """
    Run a scenario gravity model using the provided gravity function.

    gravity_function must be one of:
    - run_gravity_with_pans_lambda (baseline)
    - run_quality_sensitive_gravity (quality model)
    """

    model_df = gravity_function(
        origins_df,
        destinations_df,
        dist_matrix,
        lambda_value=lambda_value,
        **kwargs
    )

    site_visits = (
        model_df.groupby("site_id")["visits"]
        .sum()
        .reset_index()
        .rename(columns={"visits": "visits_scenario"})
    )

    return model_df, site_visits


def compute_impact(baseline_visits, scenario_visits):
    """
    Compute delta visits and % change for each site.
    """

    merged = baseline_visits.merge(
        scenario_visits,
        on="site_id",
        how="left"
    )

    merged["delta_visits"] = merged["visits_scenario"] - merged["visits_baseline"]
    merged["pct_change"] = 100 * merged["delta_visits"] / merged["visits_baseline"]

    return merged
