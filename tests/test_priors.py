"""Tests for the prior sampling system."""

import numpy as np
import pytest

import stdvoidsim
from stdvoidsim.priors import (
    LogNormalPrior,
    LogUniformPrior,
    PriorConfig,
    _EXTREME,
    _rescale_demography,
)


class TestLogNormalPrior:
    def test_sample_scalar(self):
        prior = LogNormalPrior(median=100, sigma=0.3)
        rng = np.random.default_rng(42)
        val = prior.sample(rng)
        assert isinstance(val, float)
        assert val > 0

    def test_sample_array(self):
        prior = LogNormalPrior(median=100, sigma=0.3)
        rng = np.random.default_rng(42)
        vals = prior.sample(rng, size=1000)
        assert vals.shape == (1000,)


class TestLogUniformPrior:
    def test_sample_in_range(self):
        prior = LogUniformPrior(low=1, high=100)
        rng = np.random.default_rng(42)
        vals = prior.sample(rng, size=10_000)
        assert np.all(vals >= 1)
        assert np.all(vals <= 100)


class TestExtremeSpecies:
    def test_extreme_count(self):
        assert len(_EXTREME) == 9

    def test_extreme_species_exist(self):
        catalog_ids = {sp.id for sp in stdvoidsim.all_species()}
        for sid in _EXTREME:
            assert sid in catalog_ids


class TestGetPrior:
    def test_all_species(self):
        for sp in stdvoidsim.all_species():
            prior = stdvoidsim.get_prior(sp.id)
            assert prior.species_id == sp.id
            assert prior.cluster in ("extreme", "non-extreme")

    def test_unknown_species_raises(self):
        with pytest.raises(ValueError, match="Unknown species"):
            stdvoidsim.get_prior("NonExistent")

    def test_extreme_uses_loguniform(self):
        prior = stdvoidsim.get_prior("AzaPri")
        assert prior.cluster == "extreme"
        assert isinstance(prior.generation_time, LogUniformPrior)
        assert isinstance(prior.time_scale, LogUniformPrior)

    def test_non_extreme_uses_lognormal(self):
        prior = stdvoidsim.get_prior("DagHyd")
        assert prior.cluster == "non-extreme"
        assert isinstance(prior.generation_time, LogNormalPrior)
        assert isinstance(prior.time_scale, LogNormalPrior)

    def test_has_time_and_migration_scale(self):
        prior = stdvoidsim.get_prior("DagHyd")
        rng = np.random.default_rng(42)
        params = prior.sample(rng)
        assert "time_scale" in params
        assert "migration_scale" in params

    def test_point_estimates_match_species(self):
        for sp in stdvoidsim.all_species():
            prior = stdvoidsim.get_prior(sp.id)
            if prior.cluster == "non-extreme":
                assert prior.generation_time.median == sp.generation_time
            else:
                assert prior.generation_time.low <= sp.generation_time
                assert prior.generation_time.high >= sp.generation_time

    def test_adaptive_sigma_long_gen_time(self):
        prior = stdvoidsim.get_prior("DhoGno")  # gen_time=200
        assert prior.generation_time.sigma == 0.8

    def test_adaptive_sigma_small_ne(self):
        prior = stdvoidsim.get_prior("DimSha")  # Ne=3000
        assert prior.population_size.sigma == 0.8

    def test_reproducibility(self):
        prior = stdvoidsim.get_prior("DagHyd")
        p1 = prior.sample(np.random.default_rng(123))
        p2 = prior.sample(np.random.default_rng(123))
        for k in p1:
            assert p1[k] == p2[k]


class TestRescaleDemography:
    def test_rescale_ne(self):
        import msprime
        d = msprime.Demography()
        d.add_population(name="A", initial_size=1000)
        d.add_population_parameters_change(time=100, initial_size=500, population="A")
        d2 = _rescale_demography(d, ne_scale=2.0, time_scale=1.0, migration_scale=1.0)
        assert d2.populations[0].initial_size == 2000
        assert d2.events[0].initial_size == 1000


class TestEndToEnd:
    def test_simulation(self):
        import warnings
        warnings.filterwarnings("ignore")
        species = stdvoidsim.get_species("DagHyd")
        model = species.get_demographic_model("InnsmouthDecline_1M27")
        engine = stdvoidsim.get_engine("msprime")
        prior = stdvoidsim.get_prior("DagHyd")
        rng = np.random.default_rng(42)

        params = prior.sample(rng)
        dm = prior.rescale_demography(model, params)
        contig = prior.build_contig(species, params, length=10_000)
        ts = engine.simulate(dm, contig, samples={"DeepOnes": 5},
                             seed=rng.integers(2**31))
        assert ts.num_trees > 0
