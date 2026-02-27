# Review Feedback & Suggestions Log

**Date:** 2026-02-27
**Status:** Open for discussion
**Repositories:** stdgrimmsim, stdvoidsim
**Branch:** `dev` (created in both repositories)

---

## Overview

This document summarizes 10 feedback points and suggestions received during review of the
stdgrimmsim and stdvoidsim catalog repositories. Both are thematic extensions of the stdpopsim
framework for population genetics simulation -- stdgrimmsim focusing on Germanic folklore/fairy
tales and stdvoidsim on Lovecraftian entities. They share identical architecture (Species,
DemographicModel, Population, Genome classes) built on msprime/SLiM.

---

## 1. Repository Purpose & Differentiation

**Feedback:** The distinction and intended use cases of the two repositories (stdgrimmsim vs
stdvoidsim) are not yet clear enough.

**Identified potential use cases:**
- **ML Training Data:** Generating diverse, easily accessible variant datasets for training
  machine learning methods in population genetics (likely stdgrimmsim).
- **Extreme/Unusual Scenarios:** Providing atypical demographic scenarios for stress-testing
  inference methods (likely stdvoidsim, possibly also stdgrimmsim).
- **Comparability & Reproducibility:** Enabling reproducible benchmarking studies without being
  constrained by real organism data availability (likely stdgrimmsim).
- **Additional use cases** to be defined.

**Current state:** Both READMEs describe themselves as simulation catalogs but do not clearly
articulate which use case each repository primarily serves, or why a user would choose one over
the other.

**Action items:**
- [ ] Define a clear mission statement for each repository.
- [ ] Clarify in both READMEs: which use case does this repo serve?
- [ ] Consider whether one repo focuses on "realistic-but-fictional" scenarios (stdgrimmsim)
      while the other focuses on "extreme/edge-case" scenarios (stdvoidsim).
- [ ] Document the relationship between the two repos explicitly.

---

## 2. Catalog Extensibility & Community Contributions

**Feedback:** Can external users add populations and demographic models? Could one of the
repositories serve as documentation for training datasets from other papers (which often use
fictional organisms)?

**Current state:** Both repos have a fixed catalog structure. Each species lives in its own
directory under `catalog/` with `species.py`, `genome_data.py`, and `demographic_models.py`.
Adding a new species requires creating this directory structure and registering it. There are
no documented contribution guidelines or acceptance criteria.

**Key consideration:** If the catalogs become extensible, they could serve as a centralized
registry for fictional training datasets used across the population genetics ML community.
This would require:
- Formal acceptance/quality criteria for new entries.
- Contribution guidelines (CONTRIBUTING.md).
- A review process for submitted species/models.
- Standardized metadata for provenance (which paper, which study, what parameters).

**Action items:**
- [ ] Decide whether catalogs should be extensible (open) or curated (closed).
- [ ] If extensible: draft acceptance criteria and contribution guidelines.
- [ ] If extensible: consider adding metadata fields for paper/study provenance.
- [ ] Evaluate which repository is more suitable as the "community catalog."

---

## 3. Design Rationale for Populations & Demographic Models

**Feedback:** The design process behind how populations and demographic models were created is
not transparent. Is there a systematic approach? Different complexity levels should be clearly
separated and made accessible.

**Current state in stdgrimmsim (32 species, 150+ models):**
- Species have varying numbers of chromosomes (e.g., ZweBerg: 7 + mitogenome).
- Demographic models range from single-population constant-size to multi-population split
  models with bottlenecks, migration, and size changes.
- No explicit documentation on the design rationale or complexity taxonomy.

**Current state in stdvoidsim (40 species, 80+ models):**
- Similar range of model complexities.
- Some models have elaborate multi-epoch histories (e.g., ShoNig's AntarcticRevolt_1D31
  with 4 epochs).
- No complexity classification system.

**Proposed complexity taxonomy:**
- **Level 1 -- Constant size:** Single population, constant Ne (simplest baseline).
- **Level 2 -- Size changes:** Single population with bottlenecks or expansions.
- **Level 3 -- Population splits:** Two or more populations diverging from an ancestor.
- **Level 4 -- Migration:** Split populations with ongoing gene flow.
- **Level 5 -- Complex:** Multiple epochs, admixture, changing migration rates, etc.

**Action items:**
- [ ] Document the design rationale: how were species parameters chosen?
- [ ] Introduce a complexity classification for demographic models.
- [ ] Tag each model with its complexity level in metadata.
- [ ] Ensure each complexity level is well-represented across the catalog.
- [ ] Consider generating a summary table (species x model complexity) for users.

---

## 4. Decoupling Species from Demographic Models

**Feedback:** Should species and demographic models (regions/environments) be independent and
freely combinable? E.g., species like Dwarfs, Dragons, Fairies combined with environments
like Mountains, Rivers, Woods to create "Mountain Dwarfs," "River Fairies," etc.

**Current state:** Species and demographic models are tightly coupled. Each species directory
contains its own `demographic_models.py`. For example:
- `ZweBerg/demographic_models.py` defines `BlackForest_1D12` and `HarzBlackForest_2D12`
- The demographic models reference populations specific to that species.

**Proposed architecture (modular approach):**
```
catalog/
  species/           # Biological parameters only
    ZweBerg/         # genome, mutation rate, recombination rate, generation time
    DraFeu/
    FeeFlu/
  environments/      # Demographic models only (region-based)
    Mountains/       # bottleneck + expansion demographic history
    Rivers/          # isolation-by-distance along a river
    Woods/           # metapopulation in fragmented habitat
  combinations/      # Pre-configured species+environment pairings
    MountainDwarfs/  # ZweBerg + Mountains
    RiverFairies/    # FeeFlu + Rivers
```

**Trade-offs:**
- **Pro:** Much more flexible; N species x M environments = N*M combinations without
  N*M manual definitions. Better for ML training (parameter space exploration).
- **Pro:** Cleaner separation of concerns; biological vs. environmental parameters.
- **Con:** Significant architectural refactor of the catalog system.
- **Con:** Not all species-environment combinations may be biologically meaningful.
- **Con:** Breaks compatibility with stdpopsim's catalog structure.

**Action items:**
- [ ] Decide whether to pursue full decoupling, partial decoupling, or keep current structure.
- [ ] If decoupling: design the API for combining species + environment at runtime.
- [ ] If decoupling: determine which repository gets this architecture (likely one, not both).
- [ ] Prototype the modular approach with 2-3 species and 2-3 environments.

---

## 5. Parameter Distributions Instead of Fixed Values

**Feedback:** For some species, instead of fixed parameters (mutation rate, recombination rate,
population size, etc.), provide prior distributions or confidence intervals. This would be more
useful for ML training, where models need to learn across parameter uncertainty.

**Current state:** All species define fixed scalar values. For example in ZweBerg:
- `generation_time=25`
- `population_size=80_000`
- Mutation/recombination rates defined per chromosome in `genome_data.py`.

**Proposed approach:**
```python
# Instead of:
population_size = 80_000

# Allow:
population_size = ParameterDistribution(
    point_estimate=80_000,
    distribution="lognormal",
    mean=np.log(80_000),
    sigma=0.5,
    ci_95=(30_000, 200_000),
    source="Estimated from folklore genealogies"
)
```

**Implementation options:**
1. **Minimal wrapper:** A thin Python wrapper that samples parameters from distributions
   before passing them to the existing simulation machinery.
2. **stdpopsim extension:** Extend the Species/DemographicModel classes to accept
   distribution objects alongside scalar values.
3. **External config:** Define distributions in YAML/JSON config files that a helper
   script reads to generate simulation parameter sets.

**Trade-offs:**
- **Pro:** Enables proper Bayesian-style training of ML methods.
- **Pro:** More honestly represents parameter uncertainty.
- **Con:** Requires at minimum a wrapper layer on top of current infrastructure.
- **Con:** Increases complexity for users who just want a single simulation.

**Action items:**
- [ ] Decide on implementation approach (wrapper vs. extension vs. config).
- [ ] Define which parameters should have distributions (mutation rate, recombination
      rate, Ne, generation time, migration rates).
- [ ] Prototype with 1-2 species.
- [ ] Document how users sample from distributions for training pipelines.

---

## 6. Workload & Collaboration

**Feedback:** Both primary contributors have limited bandwidth due to professorship setup,
grant applications, and other commitments. Proposal to involve Hannah Goetsch (postdoc with
population genetics background, transitioning to ML) to help with structuring species and
models.

**Key questions to resolve:**
- Should the project remain small (2 contributors) or expand?
- What specific tasks could Hannah contribute to without extensive onboarding?
  - Structuring species and models (taxonomy, complexity levels).
  - Designing the modular species/environment system.
  - Writing contribution guidelines and documentation.
  - Implementing parameter distributions for ML training.
- How to manage collaboration (regular meetings, async via GitHub issues, etc.)?

**Action items:**
- [ ] Decide on involving Hannah Goetsch.
- [ ] If yes: define scope of her contributions and onboarding needs.
- [ ] Set up project management (GitHub issues, milestones).
- [ ] Establish a realistic timeline given bandwidth constraints.

---

## 7. Authorship

**Feedback:** Authorship allocation is unclear. Current primary contributor has done most work
as both first and last author role, but cannot hold both positions. Need to clarify what
arrangement works best.

**Considerations:**
- First author: typically did the most hands-on work.
- Last author: typically the senior/supervising researcher.
- For software papers: contribution roles (CRediT taxonomy) may be more appropriate.
- If Hannah joins, authorship order needs to account for her contributions.

**Action items:**
- [ ] Primary contributor to decide preferred authorship position.
- [ ] Discuss CRediT roles as an alternative to strict ordering.
- [ ] Revisit if team composition changes (e.g., Hannah joining).

---

## 8. AI/LLM Usage Transparency

**Feedback:** Some passages and demographic models appear to have been AI-generated. Clarify
the extent of AI usage in writing and model design.

**Relevance:**
- Transparency about AI usage is increasingly expected in academic publications.
- If demographic models were AI-generated, this affects reproducibility claims.
- Some journals now require AI usage disclosure.

**Action items:**
- [ ] Document which parts were AI-assisted (text, code, model parameters, model design).
- [ ] Add an AI usage disclosure section to the paper/documentation.
- [ ] Ensure AI-generated demographic models have been reviewed for biological plausibility.
- [ ] If models were AI-designed: document the prompts/process for reproducibility.

---

## 9. Naming: Grimm vs. Fairytale/Folklore

**Feedback:** The name "stdgrimmsim" is well-received, but the catalog should not be limited
to German fairy tales (Grimm's). Consider including other folklore traditions.

**Current state:** stdgrimmsim contains 32 species, almost exclusively from Germanic folklore:
- German fairy tales: Rumpelstiltskin, Cinderella (Aschenputtel), Frau Holle, etc.
- Germanic mythology: Valkyries, Frost Giants, Erlkoenig, Wild Hunt.
- Regional German folklore: Bavarian, Prussian, Saxon, Pomeranian creatures.
- Some Norse-adjacent: Jotnar (Frost Giants), Valkyries.

**Options:**
1. **Keep Germanic focus:** "Grimm" in the name justifies a Germanic scope. Other traditions
   could go in separate catalogs (e.g., stdfablesim for Aesop, stdyokaisim for Japanese).
2. **Broaden scope:** Allow select non-Germanic folklore while keeping the Grimm name as a
   thematic anchor (Grimm as "fairy tale" in general, not strictly Brothers Grimm).
3. **Rename:** Use a broader name like stdfairytalesim or stdfolkloresim if the scope expands
   significantly.

**Action items:**
- [ ] Decide on scope: strictly Germanic vs. broader folklore.
- [ ] If broadening: which traditions to include? (Celtic, Slavic, Nordic, etc.)
- [ ] If broadening: consider renaming or keep "Grimm" as a brand.
- [ ] Document the naming rationale in the README.

---

## 10. Frau Holle as a Population

**Feedback:** It is unclear why Frau Holle (FraHol) is modeled as a population/species. Frau
Holle is a single character in the fairy tale, not a population of organisms.

**Action items:**
- [ ] Review the FraHol species definition and its demographic models.
- [ ] Clarify the biological/population-genetic interpretation:
  - Is FraHol representing a population of "Holle-like" weather spirits?
  - Is it a single-individual lineage (Ne=1) representing a mythical being?
  - Does it serve a specific simulation purpose (e.g., extreme bottleneck)?
- [ ] Either provide clear justification in the species documentation or reconsider the entry.
- [ ] This relates to point 3: the design rationale should explain choices like this.

---

## Summary of Priority Actions

### High Priority (Architectural Decisions)
1. **Define repository purposes** (Point 1) -- needed before other decisions.
2. **Decide on species/environment decoupling** (Point 4) -- major architectural impact.
3. **Decide on extensibility** (Point 2) -- affects project scope and governance.

### Medium Priority (Design & Implementation)
4. **Design complexity taxonomy** (Point 3) -- improves usability.
5. **Prototype parameter distributions** (Point 5) -- enables ML use case.
6. **Clarify scope: Grimm vs. broader folklore** (Point 9) -- affects catalog content.
7. **Review FraHol and similar edge cases** (Point 10) -- quality control.

### Ongoing / Organizational
8. **Decide on collaboration model** (Point 6) -- affects project velocity.
9. **Settle authorship** (Point 7) -- needed for publication planning.
10. **Document AI usage** (Point 8) -- needed for publication transparency.

---

## Technical Notes

### Current Repository State (2026-02-27)

**stdgrimmsim:**
- Branch: `dev` (created from `main` at commit 77d7628)
- Remote: https://github.com/kevinkorfmann/stdgrimmsim
- 32 species, 150+ demographic models
- Dependencies: msprime>=1.0.4, pyslim>=1.0.4, numpy, attrs

**stdvoidsim:**
- Branch: `dev` (created from `main` at commit 7648a3d)
- Remote: git@github.com:kevinkorfmann/stdvoidsim.git
- 40 species, 80+ demographic models
- Dependencies: same as stdgrimmsim

### Shared Architecture
Both repos follow identical patterns forked from stdpopsim:
- `catalog/<SpeciesID>/species.py` -- species definition
- `catalog/<SpeciesID>/genome_data.py` -- chromosome lengths, assembly metadata
- `catalog/<SpeciesID>/demographic_models.py` -- msprime demographic models
- `species.py` -- global species registry
- `models.py` -- DemographicModel and Population classes
- `genomes.py` -- Genome, Chromosome, Contig classes
