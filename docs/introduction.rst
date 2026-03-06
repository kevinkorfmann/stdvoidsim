.. _sec_introduction:

============
Introduction
============

This is the documentation for ``stdvoidsim``, a library of population
genetic simulation models for Lovecraftian entities and eldritch horrors.

Purpose
-------

``stdvoidsim`` is a *fork catalog* of ``stdpopsim``: it shares the same API and
simulation engines but replaces the species catalog with 40 fictional creatures
from H.P. Lovecraft's Cthulhu Mythos.

**Primary use case:** stress-testing inference methods and probing the limits
of identifiability under extreme demographic scenarios.

Species span deliberately non-standard parameter ranges designed to break
methods that only work in "well-behaved" regimes:

- **Generation time:** 0.01 years (Fire Vampires) to 10^6 years (Azathoth) ---
  8 orders of magnitude.
- **Effective population size:** Ne = 1 (Azathoth) to Ne = 10^6 (Fire Vampires, Zoogs).
- **Ploidy:** diploid to hexaploid (Shoggoth).
- **Scenarios:** extreme bottlenecks, deep dormancy, asymmetric migration.

See also: `stdgrimmsim <https://github.com/kevinkorfmann/stdgrimmsim>`_ --- the
companion catalog for ML training with plausible German-folklore demographies
(32 species, 134 models across 4 complexity levels).


Species categories
------------------

The 40 species are grouped into Mythos-inspired categories:

- **Outer Gods & Great Old Ones** (9 species): Azathoth, Cthulhu, Father Dagon,
  Hastur, Nyarlathotep, Shub-Niggurath, Tsathoggua, Yog-Sothoth, Chaugnar Faugn.

- **Servitor Races & Engineered Species** (7 species): Shoggoth, Star-Spawn,
  Dark Young, Formless Spawn, Hunting Horror, Fire Vampire, Byakhee.

- **Ancient Civilizations** (5 species): Elder Things, Great Race of Yith,
  Flying Polyps, Mi-Go, Serpent People.

- **Amphibious & Aquatic** (2 species): Deep Ones, Colour Out of Space.

- **Subterranean Horrors** (5 species): Ghouls, Gugs, Ghasts, Dholes, Wamps.

- **Dreamlands Creatures** (6 species): Nightgaunts, Shantaks, Moon-Beasts,
  Zoogs, Cats of Ulthar, Leng Spiders.

- **Interdimensional & Temporal** (2 species): Hounds of Tindalos,
  Dimensional Shamblers.

- **Arctic & Desert** (2 species): Gnoph-Keh, Sand Dwellers.

- **Human-Adjacent Horrors** (2 species): Tcho-Tcho, Rat-Things.

Every species has exactly two models (one single-population, one multi-population),
yielding 82 demographic models total.


First steps
-----------

 - Head to the :ref:`Installation <sec_installation>` page to get ``stdvoidsim``
   installed on your computer.

 - Skim the :ref:`Catalog <sec_catalog>` to see all 40 species and 82 demographic
   models.

 - Read the :ref:`Tutorials <sec_tutorial>` to see some examples of ``stdvoidsim``
   in action.


Citations
---------

``stdvoidsim`` is built on the ``stdpopsim`` framework. If you use the simulation
framework, please cite:

  - Jeffrey R Adrion et al. (2020),
    *A community-maintained standard library of population genetic models*,
    eLife 9:e54967; doi: https://doi.org/10.7554/eLife.54967

  - M Elise Lauterbur et al. (2023),
    *Expanding the stdpopsim species catalog, and lessons learned for realistic genome simulations*,
    eLife 12:RP84874; doi: https://doi.org/10.7554/eLife.84874


Licence and usage
-----------------

``stdvoidsim`` is available under the GPLv3 public license.
The terms of this license can be read
`here <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.
