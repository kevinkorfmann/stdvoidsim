# stdvoidsim

[![PyPI version](https://img.shields.io/pypi/v/stdvoidsim)](https://pypi.org/project/stdvoidsim/)
[![PyPI downloads](https://img.shields.io/pypi/dm/stdvoidsim)](https://pypi.org/project/stdvoidsim/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/stdvoidsim)](https://pypi.org/project/stdvoidsim/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Docs](https://github.com/kevinkorfmann/stdvoidsim/actions/workflows/docs.yml/badge.svg?branch=main)](https://stdvoidsim.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/kevinkorfmann/stdvoidsim/graph/badge.svg)](https://codecov.io/gh/kevinkorfmann/stdvoidsim)

**Install:** `pip install stdvoidsim` · **Docs:** [stdvoidsim.readthedocs.io](https://stdvoidsim.readthedocs.io/en/latest/)

A community-maintained library of population genetic simulation models for
**Lovecraftian entities and eldritch horrors**.

**40 species · 80 demographic models** spanning extreme parameter space.

> See also: [**stdgrimmsim**](https://github.com/kevinkorfmann/stdgrimmsim) — the companion catalog for ML training with plausible German-folklore demographies.

## Purpose

`stdvoidsim` is a *fork catalog* of [stdpopsim](https://stdpopsim.org): it shares the same API and simulation engines (msprime, SLiM) but replaces the species catalog with fictional taxa from H.P. Lovecraft's Cthulhu Mythos.

**Primary use case: stress-testing inference methods** and probing the limits of identifiability under extreme demographic scenarios.

Species span deliberately non-standard parameter ranges designed to break methods that only work in "well-behaved" regimes:

- **Generation time:** 0.01 years (Fire Vampires) to 10^6 years (Azathoth) — 8 orders of magnitude
- **Effective population size:** Ne = 1 (Azathoth) to Ne = 10^6 (Fire Vampires, Zoogs)
- **Ploidy:** diploid to hexaploid (Shoggoth)
- **Scenarios:** extreme bottlenecks, deep dormancy, asymmetric migration

| | stdvoidsim | stdgrimmsim |
|---|---|---|
| **Focus** | Stress-testing & identifiability limits | Diverse training data & benchmarking |
| **Species** | 40 (Cthulhu Mythos) | 32 (German folklore) |
| **Models** | 80 (1- and 2-population) | 150 (1- to 4-population) |
| **Parameter range** | Extreme (Ne=1 to 10^6, gen. time 0.01–10^6 yr) | Moderate, plausible |
| **Ploidy** | Diploid to hexaploid | All diploid |

## Available Species

### Outer Gods & Great Old Ones

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| AzaPri | *Azathoth primordia* | Blind Idiot God | 1 | 1M yr | 2 |
| CthGre | *Cthulhu greatoldone* | Great Cthulhu | 500 | 10K yr | 4 |
| DagGod | *Dagonus maximus* | Father Dagon | 50 | 50K yr | 4 |
| HasKin | *Hastur carcosensis* | King in Yellow | 2,000 | 50 yr | 2 |
| NyaAza | *Nyarlathotep azathothspawn* | Crawling Chaos | 1,000 | 1 yr | 2 |
| ShbNig | *Shubniggurath fertilitas* | Black Goat of the Woods | 100,000 | 25 yr | 2 |
| TsaGod | *Tsathoggua somnolentis* | Tsathoggua | 100 | 50K yr | 2 |
| YogSot | *Yogsothoth dimensionalis* | The Key and the Gate | 10 | 100K yr | 2 |
| ChaFau | *Chaugnarus faugnis* | Chaugnar Faugn | 200 | 10K yr | 2 |

### Servitor Races & Engineered Species

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| ShoNig | *Shoggoth nigrumplasma* | Shoggoth | 100,000 | 0.5 yr | 6 |
| StarSp | *Starspawn cthulhidae* | Star-Spawn of Cthulhu | 10,000 | 5K yr | 4 |
| DarYou | *Obscurus silvanus* | Dark Young | 35,000 | 50 yr | 3 |
| ForSpa | *Informis generatus* | Formless Spawn | 25,000 | 10 yr | 2 |
| HunTin | *Venator obscurus* | Hunting Horror | 15,000 | 20 yr | 2 |
| FirVam | *Igneus vampirus* | Fire Vampire | 1,000,000 | 0.01 yr | 1 |
| BybWor | *Byakhee voidwing* | Byakhee | 200,000 | 10 yr | 2 |

### Ancient Civilizations

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| EldThi | *Elderium antarcticae* | Elder Thing | 10,000 | 1K yr | 2 |
| YitGre | *Yithianus temporalis* | Great Race of Yith | 50,000 | 500 yr | 2 |
| FlyPol | *Polypus volantis* | Flying Polyp | 20,000 | 2K yr | 2 |
| SerHum | *Serpentis valusiensis* | Serpent Person | 40,000 | 50 yr | 2 |
| MiGFun | *Migo fungoides* | Fungi from Yuggoth | 500,000 | 5 yr | 2 |

### Amphibious & Aquatic

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| DagHyd | *Dagonus hydridae* | Deep One | 50,000 | 100 yr | 2 |
| ColOos | *Chromatis extraspatiala* | Colour Out of Space | 10,000 | 0.1 yr | 1 |

### Subterranean Horrors

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| GhoFee | *Ghoulish necrophagus* | Ghoul | 30,000 | 20 yr | 2 |
| GugsUn | *Gugus underworldis* | Gug | 25,000 | 30 yr | 2 |
| GhaShe | *Ghastus cavernicola* | Ghast | 80,000 | 3 yr | 2 |
| DhoGno | *Dholos subterraneus* | Dhole | 15,000 | 200 yr | 2 |
| WamUnd | *Degeneratus subterraneus* | Wamp | 20,000 | 10 yr | 2 |

### Dreamlands Creatures

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| NigMan | *Nightgauntus mantaformis* | Nightgaunt | 75,000 | 5 yr | 2 |
| SanDre | *Shantakus dreamlandis* | Shantak | 60,000 | 15 yr | 2 |
| MooFun | *Lunaris bestialis* | Moon-Beast | 45,000 | 8 yr | 2 |
| ZooGul | *Zoogus sylvaticus* | Zoog | 500,000 | 2 yr | 2 |
| CatUlt | *Felis ultharensis* | Cat of Ulthar | 100,000 | 5 yr | 2 |
| LenSpi | *Araneus lengensis* | Leng Spider | 20,000 | 10 yr | 2 |

### Interdimensional & Temporal

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| HouFir | *Houndus tindalosi* | Hound of Tindalos | 5,000 | 500 yr | 2 |
| DimSha | *Dimensius shambleris* | Dimensional Shambler | 3,000 | 100 yr | 2 |

### Arctic & Desert

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| GnpKeh | *Gnophkehus arcticus* | Gnoph-Keh | 12,000 | 40 yr | 2 |
| SanDwl | *Arenicola abyssalis* | Sand Dweller | 40,000 | 15 yr | 2 |

### Human-Adjacent Horrors

| ID | Species | Common Name | Ne | Gen Time | Ploidy |
|--------|-------------------------------|--------------------------|----------|----------|--------|
| TsaCho | *Tsathoggua choriensis* | Tcho-Tcho | 70,000 | 25 yr | 2 |
| RatThi | *Rattus magicus* | Rat-Thing | 50,000 | 1 yr | 2 |

## Quick Start

```python
import stdvoidsim

# Get the Deep One species
species = stdvoidsim.get_species("DagHyd")

# Use the Innsmouth Decline demographic model (3-epoch history)
model = species.get_demographic_model("InnsmouthDecline_1M27")

# Set up a generic contig of 100kb
contig = species.get_contig(length=100_000)

# Simulate with msprime
engine = stdvoidsim.get_engine("msprime")
ts = engine.simulate(model, contig, samples={"DeepOnes": 20}, seed=42)

print(f"Trees: {ts.num_trees}, Mutations: {ts.num_mutations}")
```

## CLI Usage

```bash
# List all available species
stdvoidsim --help

# Deep Ones: 3-epoch decline-then-expansion
stdvoidsim DagHyd -d InnsmouthDecline_1M27 -o deep_ones.trees -L 100000 DeepOnes:10

# Shoggoth: 4-epoch revolt history (hexaploid, 0.5-yr generation time)
stdvoidsim ShoNig -d AntarcticRevolt_1D31 -o shoggoths.trees -L 50000 Shoggoth:20

# Cthulhu: deep dormancy (10,000-yr generation time)
stdvoidsim CthGre -d DeepSlumber_1R28 -o cthulhu.trees -L 50000 Rlyeh:5
```

## Installation

```bash
pip install stdvoidsim
```

From source (editable):

```bash
pip install -e .
```

### SLiM engine (optional)

SLiM supports ploidy 1 or 2 only. Species with higher ploidy (e.g. Cthulhu ploidy 4, Shoggoth ploidy 6) must use msprime.

```bash
stdvoidsim DagHyd -d InnsmouthDecline_1M27 -e slim -o deep_ones.trees -L 10000 DeepOnes:10
```

### Development with uv

```bash
make install    # editable install + dev/CI dependencies
make test       # run test suite
make test-cov   # run tests with coverage
make quick-sim  # run quick simulation check
```

## Citation

This project is a fork of [stdpopsim](https://stdpopsim.org). If you use the simulation framework, please cite:

* [Adrion, et al. (2020)](https://doi.org/10.7554/eLife.54967) — A community-maintained standard library of population genetic models.
* [Lauterbur, et al. (2023)](https://doi.org/10.7554/eLife.84874) — Expanding the stdpopsim species catalog.

*"Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn."*
