# AWUT Phase 5 — God-Mode Bridge Campaign

**Date:** 2026-09-30  
**Machine:** aster1 (RTX 5070 required)  
**Executor:** Claude  
**Theory Authority:** Phase 4 Core + Brian/ChatGPT theory chat

## Mission

**Can AWUT execute a universe from Ka forward?**

The Phase 4 Core is causally aligned and re-derived. We are no longer asking about internal organization. We are testing executability.

**Primary target:** Bridge A — the missing law that differentiates finite nonmetric Ka and selects the first shallow interface.

**Secondary target:** Bridge B unification — can the same parent rule reduce to post-SPACE rerouting?

## Hard Constraints

- NO GPU → NO EXECUTION. Requires CUDA on aster1.
- DO NOT edit the Core
- DO NOT invent theory to save results
- DO NOT use CODATA/observations to select laws
- Physics gates before numerics
- FP64 precision
- Deterministic seeds

## Bridge A Requirements

Missing law must map:
```
nonmetric differentiated Ka history
    →
first differentiated shallow realization / first interface
```

Pre-SPACE ontology:
- NO: Euclidean position, radius, shells, neighbor graph, distance, metric, velocity, fields, lattice, hidden geometry
- YES: finite ledger, TIIME order, relational state, causal histories (if physically generated), phase relations, conservation, terminal admissibility

## Search Strategy

Test law classes constructible from authorized nonmetric state:

1. **Commuting history** — all G_i G_j = G_j G_i
2. **Noncommuting history** — [G_i, G_j] ≠ 0  
3. **Pure phase/Gram history** — pairwise coherence invariants
4. **Order-holonomy history** — gauge-invariant loops
5. **Terminal-admissibility-dependent** — response changes as inward routes close
6. **Mixed finite history** — combinations, NO added coefficients

## Mandatory Gates (All Must Pass)

A. FINITE — no infinities/singularities  
B. CONSERVATIVE — ledger preserved to FP64  
C. RELABEL INVARIANT — renaming histories changes nothing  
D. SUBDIVISION INVARIANT — splitting identical copies changes nothing  
E. NONMETRIC — no hidden pre-SPACE geometry  
F. NO RANDOM SYMMETRY BREAKING — labels/noise cannot be physical cause  
G. CAUSAL ORDER — preserve distinction when histories differ by order  
H. IDENTICAL-HISTORY CONTROL — identical histories stay identical  
I. DIFFERENTIATION — capable of producing distinct classes from one Ka  
J. TERMINAL CONSISTENCY — Planck Stop is admissibility only, not force  
K. FLIP COMPATIBILITY — output must parent first shallow realization  
L. NO OBSERVATION — no particle values, cosmology, or CODATA

## Key No-Go Test

**Theorem candidate:** Any pre-SPACE law whose state reduces to commutative scalar statistics (total depth, count, mean engagement, mean phase, cumulative exposure) cannot generate robust shell/body differentiation from symmetric Ka.

If proven → minimum viable Bridge A must retain noncommuting/order-sensitive relational information.

## Compute Scale

### Smoke Test
- 1e5 histories
- Quick gate validation

### Gate Test  
- 1e6 histories
- Full invariance checks

### Surviving Law Class
- 1e7+ histories
- Long duration (64-4096 events)

### Finalists
- 1e8+ histories preferred
- Billions of event evaluations
- Convergence studies

### History Lengths
64, 128, 256, 512, 1024, 2048, 4096 events

## GPU Reduction (Do Not Store Raw Universes)

Compute on GPU, reduce to:
- Conservation maxima
- Class counts / recurrence
- History discrimination
- Commutator statistics
- Convergence metrics
- Counterexamples
- Invariance violations

## Adversarial Tests Required

- Physical-history relabeling
- Identical-history subdivision
- Common phase rotation / basis change
- Causal order reversal / shuffling
- Same scalar totals, different histories ← **decisive**
- Same history, different representation
- Longer duration / finer resolution
- Nearly coherent/cancelling states
- Exact symmetric Ka / perturbed equivalent
- No-SPACE controls

## Kill Conditions (Do Not Repair)

1. Requires hidden pre-SPACE geometry
2. Requires arbitrary labels
3. Depends on numerical step count
4. Breaks conservation
5. Depends on representation/basis
6. Fails subdivision invariance
7. Cannot distinguish different causal orders
8. Creates fake differentiation from duplicate labels
9. Requires observed Red/Purple fraction
10. Requires tunable coefficient for stability
11. Only works at one resolution
12. Cannot produce legitimate first shallow state
13. Cannot survive longer histories
14. Produces second fundamental medium

## Success Criteria

**Best:** Single rule forced by constraints, generates first shallow interface, survives Boom, reduces to Bridge B.

**Next-best:** Bridge A closes uniquely, Bridge B separate.

**Next:** Bridge A narrowed to one equivalence class with one precise missing selector.

**Valid negative:** Multiple inequivalent laws remain; prove exactly what physical statement is missing.

## Phase 5 Deliverables

- `BRIDGE_A_REPORT.md` — derivation search results
- `FIRST_SPACE_REPORT.md` — shallow interface generation
- `SURVIVOR_FORMATION_REPORT.md` — Boom overlap / stable classes
- `BRIDGE_AB_UNIFICATION_REPORT.md` — common parent test
- `REROUTING_REPORT.md` — degeneracy resolution
- `NO_GO_THEOREMS.md` — analytical impossibility results
- `COUNTEREXAMPLES.md` — gate failures
- `PHASE5_FINAL_REPORT.md` — answers to 10 questions

## Execution

From aster1 with RTX 5070:
```bash
cd campaign/PHASE5_GODMODE_20260930
python source/run_bridge_a_campaign.py --mode=full --gpu=0
```

Results in `results/`, figures in `figures/`, logs in `logs/`.
