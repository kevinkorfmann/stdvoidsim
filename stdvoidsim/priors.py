"""
Prior distributions over species parameters for training-data generation.

Each species has LogNormal or LogUniform priors over four parameters:
generation_time, population_size, mutation_rate, and recombination_rate.

Extreme species (Azathoth, Yog-Sothoth, etc.) use LogUniform priors spanning
four orders of magnitude.  Non-extreme species use LogNormal priors with
σ that widens for unusual generation times or small Ne.

Usage::

    import stdvoidsim
    import numpy as np

    prior = stdvoidsim.get_prior("DagHyd")
    rng = np.random.default_rng(42)

    # Single draw
    params = prior.sample(rng)

    # Multiple draws
    params = prior.sample(rng, size=1000)
    # params["generation_time"]  -> np.array of shape (1000,)
"""

import math
import numpy as np


class LogNormalPrior:
    """LogNormal prior with given median and log-space standard deviation."""

    def __init__(self, median, sigma):
        self.median = median
        self.sigma = sigma

    def sample(self, rng, size=None):
        mu_log = math.log(self.median)
        return rng.lognormal(mu_log, self.sigma, size=size)

    def __repr__(self):
        return f"LogNormalPrior(median={self.median:.4g}, sigma={self.sigma})"


class LogUniformPrior:
    """LogUniform prior on [low, high]."""

    def __init__(self, low, high):
        self.low = low
        self.high = high

    def sample(self, rng, size=None):
        log_low = math.log(self.low)
        log_high = math.log(self.high)
        u = rng.uniform(log_low, log_high, size=size)
        return np.exp(u)

    def __repr__(self):
        return f"LogUniformPrior(low={self.low:.4g}, high={self.high:.4g})"


class PriorConfig:
    """Prior configuration for a single species."""

    def __init__(self, species_id, cluster, generation_time, population_size,
                 mutation_rate, recombination_rate):
        self.species_id = species_id
        self.cluster = cluster
        self.generation_time = generation_time
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.recombination_rate = recombination_rate

    def sample(self, rng, size=None):
        """Sample parameters from the prior.

        Parameters
        ----------
        rng : numpy.random.Generator
            Random number generator (e.g. ``np.random.default_rng(42)``).
        size : int, optional
            Number of samples.  If None, returns scalar values.

        Returns
        -------
        dict
            Keys: ``generation_time``, ``population_size``,
            ``mutation_rate``, ``recombination_rate``.
        """
        return {
            "generation_time": self.generation_time.sample(rng, size),
            "population_size": self.population_size.sample(rng, size),
            "mutation_rate": self.mutation_rate.sample(rng, size),
            "recombination_rate": self.recombination_rate.sample(rng, size),
        }

    def __repr__(self):
        return (
            f"PriorConfig(species_id={self.species_id!r}, "
            f"cluster={self.cluster!r})"
        )


# ── Species groups ────────────────────────────────────────────────────
# Extreme species: LogUniform priors spanning [0.01*v, 100*v]
_EXTREME = [
    "AzaPri", "YogSot", "CthGre", "DagGod", "TsaGod",
    "ChaFau", "NyaAza", "FirVam", "ColOos",
]

# Non-extreme: LogNormal with adaptive σ
_EXTREME_SET = set(_EXTREME)


def get_prior(species_id):
    """Return the PriorConfig for a species.

    Parameters
    ----------
    species_id : str
        Species identifier (e.g. ``"DagHyd"``).

    Returns
    -------
    PriorConfig
    """
    from . import get_species, all_species

    all_ids = {sp.id for sp in all_species()}
    if species_id not in all_ids:
        raise ValueError(
            f"Unknown species {species_id!r}. "
            f"Known species: {sorted(all_ids)}"
        )

    sp = get_species(species_id)
    chroms = [
        c for c in sp.genome.chromosomes
        if "mito" not in c.id and "chaos" not in c.id and "void" not in c.id
    ]
    mu_est = chroms[0].mutation_rate
    r_est = chroms[0].recombination_rate

    if species_id in _EXTREME_SET:
        cluster = "extreme"
        return PriorConfig(
            species_id=species_id,
            cluster=cluster,
            generation_time=LogUniformPrior(
                0.01 * sp.generation_time, 100 * sp.generation_time
            ),
            population_size=LogUniformPrior(
                max(0.01 * sp.population_size, 1),
                100 * sp.population_size,
            ),
            mutation_rate=LogUniformPrior(0.01 * mu_est, 100 * mu_est),
            recombination_rate=LogUniformPrior(0.01 * r_est, 100 * r_est),
        )

    # Non-extreme: adaptive σ
    cluster = "non-extreme"
    sig_g = 0.8 if sp.generation_time > 100 else 0.5
    sig_ne = 0.8 if sp.population_size < 5000 else 0.5
    sig_mu = 0.5
    sig_r = 0.5

    return PriorConfig(
        species_id=species_id,
        cluster=cluster,
        generation_time=LogNormalPrior(sp.generation_time, sig_g),
        population_size=LogNormalPrior(sp.population_size, sig_ne),
        mutation_rate=LogNormalPrior(mu_est, sig_mu),
        recombination_rate=LogNormalPrior(r_est, sig_r),
    )
