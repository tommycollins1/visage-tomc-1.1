"""
Ranking comparison visualisations for ViSAGE 1.1.

Compares:
- baseline (distance-only) site visitation
- quality-sensitive site visitation

Outputs:
- table of ranks and rank changes
- optional simple bar plot of top-N sites
"""

import pandas as pd
import matplotlib.pyplot as plt


def build_ranking_comparison(baseline_df, quality_df):
    """
    Build a site-level ranking comparison table.

    Parameters
    ----------
    baseline_df : DataFrame
        Long-form: origin_id, site_id, visits (baseline).
    quality_df : DataFrame
        Long-form: origin_id, site_id, visits (quality-sensitive).

    Returns
    -------
    DataFrame
        site_id, visits_baseline, visits_quality,
        rank_baseline, rank_quality, rank_change
    """
    base = (
        baseline_df.groupby("site_id")["visits"]
        .sum()
        .reset_index()
        .rename(columns={"visits": "visits_baseline"})
    )

    qual = (
        quality_df.groupby("site_id")["visits"]
        .sum()
        .reset_index()
        .rename(columns={"visits": "visits_quality"})
    )

    merged = base.merge(qual, on="site_id", how="outer").fillna(0)

    merged["rank_baseline"] = merged["visits_baseline"].rank(
        method="min", ascending=False
    ).astype(int)

    merged["rank_quality"] = merged["visits_quality"].rank(
        method="min", ascending=False
    ).astype(int)

    merged["rank_change"] = merged["rank_baseline"] - merged["rank_quality"]

    return merged.sort_values("rank_quality")


def plot_top_n_rank_change(ranking_df, top_n=10):
    """
    Simple bar plot of rank changes for top-N quality-ranked sites.
    """
    top = ranking_df.nsmallest(top_n, "rank_quality").copy()
    top = top.sort_values("rank_quality")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(
        top["site_id"].astype(str),
        top["rank_change"],
        color=["green" if x > 0 else "red" if x < 0 else "grey"
               for x in top["rank_change"]],
    )

    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Rank change (baseline − quality)")
    ax.set_ylabel("Site ID")
    ax.set_title(f"Top {top_n} sites: rank change with quality")

    plt.tight_layout()
    plt.show()
