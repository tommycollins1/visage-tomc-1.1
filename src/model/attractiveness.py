"""
Attractiveness functions for ViSAGE 1.1.

Combines:
- size (optional)
- quality (from QualityScore)
- other amenity weights (future extension)
into a single A_j term for spatial interaction.
"""

import numpy as np


def combine_attractiveness(quality_scores,
                           size_ha=None,
                           beta_quality=1.0,
                           beta_size=0.0):
    """
    Combine multiple components into a single attractiveness A_j.

    Parameters
    ----------
    quality_scores : array-like
        Normalised quality scores in [0, 1].
    size_ha : array-like or None
        Site size in hectares (optional). If None, ignored.
    beta_quality : float
        Exponent for quality sensitivity.
    beta_size : float
        Exponent for size sensitivity.

    Returns
    -------
    ndarray
        Attractiveness values A_j (length = n_sites).
    """
    quality_scores = np.asarray(quality_scores)

    # Base: quality component
    A = np.power(quality_scores, beta_quality)

    # Optional: size component
    if size_ha is not None and beta_size != 0.0:
        size_ha = np.asarray(size_ha)
        # Avoid zeros / negatives
        size_ha = np.maximum(size_ha, 1e-6)
        A *= np.power(size_ha, beta_size)

    return A
