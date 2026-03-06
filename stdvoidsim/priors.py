"""
Prior distributions over species parameters for training-data generation.

Each species has LogNormal or LogUniform priors over six parameters:
generation_time, population_size, mutation_rate, recombination_rate,
time_scale, and migration_scale.

Extreme species (Azathoth, Yog-Sothoth, etc.) use LogUniform priors spanning
four orders of magnitude.  Non-extreme species use LogNormal priors with
σ that widens for unusual generation times or small Ne.

Usage::

    import stdvoidsim
    import numpy as np

    species = stdvoidsim.get_species("DagHyd")
    model   = species.get_demographic_model("InnsmouthDecline_1M27")
    engine  = stdvoidsim.get_engine("msprime")
    prior   = stdvoidsim.get_prior("DagHyd")
    rng     = np.random.default_rng(42)

    params     = prior.sample(rng)
    demography = prior.rescale_demography(model, params)
    contig     = prior.build_contig(species, params, length=100_000)
    ts = engine.simulate(demography, contig,
                         samples={"DeepOnes": 20}, seed=rng.integers(2**31))
"""

import copy
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


def _rescale_demography(demography, ne_scale, time_scale, migration_scale):
    """Return a deep copy of an msprime.Demography with rescaled parameters."""
    import msprime

    d = copy.deepcopy(demography)

    for pop in d.populations:
        if pop.initial_size is not None:
            pop.initial_size *= ne_scale

    if d.migration_matrix is not None:
        d.migration_matrix = d.migration_matrix * migration_scale

    for ev in d.events:
        if hasattr(ev, "time") and ev.time is not None:
            ev.time *= time_scale
        if isinstance(ev, msprime.PopulationParametersChange):
            if ev.initial_size is not None:
                ev.initial_size *= ne_scale
        if isinstance(ev, msprime.MigrationRateChange):
            if ev.rate is not None:
                ev.rate *= migration_scale

    return d


class PriorConfig:
    """Prior configuration for a single species."""

    def __init__(self, species_id, cluster, generation_time, population_size,
                 mutation_rate, recombination_rate, time_scale,
                 migration_scale):
        self.species_id = species_id
        self.cluster = cluster
        self.generation_time = generation_time
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.recombination_rate = recombination_rate
        self.time_scale = time_scale
        self.migration_scale = migration_scale

    def sample(self, rng, size=None):
        """Sample parameters from the prior.

        Returns dict with keys: generation_time, population_size,
        mutation_rate, recombination_rate, time_scale, migration_scale.
        """
        return {
            "generation_time": self.generation_time.sample(rng, size),
            "population_size": self.population_size.sample(rng, size),
            "mutation_rate": self.mutation_rate.sample(rng, size),
            "recombination_rate": self.recombination_rate.sample(rng, size),
            "time_scale": self.time_scale.sample(rng, size),
            "migration_scale": self.migration_scale.sample(rng, size),
        }

    def rescale_demography(self, demographic_model, params):
        """Return a rescaled DemographicModel from sampled parameters."""
        from . import get_species

        sp = get_species(self.species_id)
        ne_scale = params["population_size"] / sp.population_size
        rescaled_msp = _rescale_demography(
            demographic_model.model,
            ne_scale=ne_scale,
            time_scale=params["time_scale"],
            migration_scale=params["migration_scale"],
        )
        dm_copy = copy.copy(demographic_model)
        dm_copy.model = rescaled_msp
        return dm_copy

    def build_contig(self, species, params, length):
        """Build a contig with sampled mutation and recombination rates."""
        return species.get_contig(
            length=length,
            mutation_rate=params["mutation_rate"],
            recombination_rate=params["recombination_rate"],
        )

    def __repr__(self):
        return (
            f"PriorConfig(species_id={self.species_id!r}, "
            f"cluster={self.cluster!r})"
        )


# ── Species groups ────────────────────────────────────────────────────
_EXTREME = [
    "AzaPri", "YogSot", "CthGre", "DagGod", "TsaGod",
    "ChaFau", "NyaAza", "FirVam", "ColOos",
]
_EXTREME_SET = set(_EXTREME)


def get_prior(species_id):
    """Return the PriorConfig for a species."""
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
            time_scale=LogUniformPrior(0.1, 10.0),
            migration_scale=LogUniformPrior(0.1, 10.0),
        )

    # Non-extreme: adaptive σ
    cluster = "non-extreme"
    sig_g = 0.8 if sp.generation_time > 100 else 0.5
    sig_ne = 0.8 if sp.population_size < 5000 else 0.5

    return PriorConfig(
        species_id=species_id,
        cluster=cluster,
        generation_time=LogNormalPrior(sp.generation_time, sig_g),
        population_size=LogNormalPrior(sp.population_size, sig_ne),
        mutation_rate=LogNormalPrior(mu_est, 0.5),
        recombination_rate=LogNormalPrior(r_est, 0.5),
        time_scale=LogNormalPrior(1.0, 0.5),
        migration_scale=LogNormalPrior(1.0, 0.5),
    )
