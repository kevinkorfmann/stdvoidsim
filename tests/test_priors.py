"""Tests for the prior sampling system."""

import numpy as np
import pytest

import stdvoidsim
from stdvoidsim.priors import (
    LogNormalPrior,
    LogUniformPrior,
    PriorConfig,
    _EXTREME,
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
        assert np.all(vals > 0)


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
            assert sid in catalog_ids, f"{sid} not in catalog"


class TestGetPrior:
    def test_all_species(self):
        """get_prior works for every species in the catalog."""
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
        assert isinstance(prior.population_size, LogUniformPrior)
        assert isinstance(prior.mutation_rate, LogUniformPrior)
        assert isinstance(prior.recombination_rate, LogUniformPrior)

    def test_non_extreme_uses_lognormal(self):
        prior = stdvoidsim.get_prior("DagHyd")
        assert prior.cluster == "non-extreme"
        assert isinstance(prior.generation_time, LogNormalPrior)
        assert isinstance(prior.population_size, LogNormalPrior)

    def test_point_estimates_match_species(self):
        """Prior medians/centres must relate to the species point estimates."""
        for sp in stdvoidsim.all_species():
            prior = stdvoidsim.get_prior(sp.id)
            if prior.cluster == "non-extreme":
                assert prior.generation_time.median == sp.generation_time
                assert prior.population_size.median == sp.population_size
            else:
                # LogUniform: check that point estimate is within range
                assert prior.generation_time.low <= sp.generation_time
                assert prior.generation_time.high >= sp.generation_time

    def test_adaptive_sigma_long_gen_time(self):
        """Species with gen_time > 100 get σ=0.8 for generation_time."""
        prior = stdvoidsim.get_prior("DhoGno")  # gen_time=200
        assert prior.generation_time.sigma == 0.8

    def test_adaptive_sigma_short_gen_time(self):
        """Species with gen_time <= 100 get σ=0.5 for generation_time."""
        prior = stdvoidsim.get_prior("GhoFee")  # gen_time=20
        assert prior.generation_time.sigma == 0.5

    def test_adaptive_sigma_small_ne(self):
        """Species with Ne < 5000 get σ=0.8 for population_size."""
        prior = stdvoidsim.get_prior("DimSha")  # Ne=3000
        assert prior.population_size.sigma == 0.8

    def test_reproducibility(self):
        prior = stdvoidsim.get_prior("DagHyd")
        p1 = prior.sample(np.random.default_rng(123))
        p2 = prior.sample(np.random.default_rng(123))
        for k in p1:
            assert p1[k] == p2[k]
