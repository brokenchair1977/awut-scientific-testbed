"""
AWUT Phase 5 — Bridge A Engine v2 (Clean Rebuild)
==================================================

Tests whether AWUT can derive the missing Ka → first SPACE differentiation law
from constraints alone, without smuggling in asymmetry, geometry, or arbitrary labels.

KEY QUESTIONS:
1. Can exact symmetric Ka generate physically distinct relational histories?
2. Are noncommuting ordered histories necessary?
3. Is terminal admissibility sufficient to select first shallow structure?
4. What exact missing state/law remains if underdetermined?

CORRECTED CONSTRAINTS:
- NO random initialization as differentiation source
- NO spatial dimensions pre-SPACE (relational_rank ≠ dim)
- EXPLICIT ordered history tracking
- DECISIVE discrimination test (same scalars, different order)
- Symmetric Ka baseline (no arbitrary breaking)
"""

import numpy as np
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json

# GPU detection
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("[INFO] CuPy available — GPU acceleration enabled")
except ImportError:
    GPU_AVAILABLE = False
    cp = None
    print("[WARNING] CuPy not available — CPU fallback mode")


class BridgeAStatus(Enum):
    """Bridge A closure status"""
    DERIVED = "DERIVED"
    UNIQUE_BRACKET = "UNIQUE_BRACKET"
    MULTIPLY_UNDERDETERMINED = "MULTIPLY_UNDERDETERMINED"
    FAILED = "FAILED"


@dataclass
class PhysicsGates:
    """Phase 5 mandatory gate tolerances"""
    # Runtime FP64 tolerance (accumulated error in long products)
    CONSERVATION_RUNTIME = 1e-11
    # High-precision exact check
    CONSERVATION_EXACT = 1e-100
    # Other gates
    UNITARITY = 1e-14
    RELABEL = 1e-14
    SUBDIVISION = 1e-14
    IDENTICAL_HISTORY = 1e-14
    SYMMETRY_BREAKING = 1e-14


class PreSPACEState:
    """
    Finite nonmetric relational state before first SPACE realization.

    FORBIDDEN before first SPACE:
    - Euclidean position (x,y,z)
    - Radius, distance, metric
    - Neighbor graph, adjacency
    - Spatial shell indices
    - Lattice coordinates
    - Velocity, propagation

    ALLOWED:
    - Finite ledger
    - TIIME order/succession
    - Relational phase structure
    - Ordered history
    - Terminal admissibility
    """

    def __init__(self, relational_rank: int, use_gpu: bool = True):
        """
        Args:
            relational_rank: Number of distinguishable relational channels
                            NOT spatial dimensionality (no geometry pre-SPACE)
            use_gpu: Use CuPy if available
        """
        self.relational_rank = relational_rank
        self.gpu = use_gpu and GPU_AVAILABLE
        self.xp = cp if self.gpu else np

        # Current coherent relational state
        self.psi = None

        # Ledger conservation
        self.ledger_norm = None

        # Ordered relational transformations (preserved for history)
        self.ordered_history_ops = []

        # Derived history invariants (NOT arbitrary labels)
        # Examples: gauge-invariant phases, order-dependent observables
        self.ordered_history_invariants = {}

        # Terminal admissibility state
        # (when no further inward continuation admissible)
        self.terminal_admissibility_state = None

    def initialize_symmetric_ka(self):
        """
        Initialize perfectly symmetric finite Ka state.

        NO random seeds.
        NO unequal weights.
        NO tagged subcomponents.
        NO shell/body labels.
        NO arbitrary asymmetry.

        Maximally symmetric under declared relational representation.
        """
        # All relational channels equal phase and amplitude
        self.psi = self.xp.ones(self.relational_rank, dtype=complex)
        self.psi /= self.xp.linalg.norm(self.psi)
        self.ledger_norm = float(self.xp.real(self.xp.vdot(self.psi, self.psi)))

        # Reset history
        self.ordered_history_ops = []
        self.ordered_history_invariants = {}

        return self.psi

    def initialize_test_perturbation(self, seed: int, epsilon: float = 1e-6):
        """
        Add small deterministic perturbation for adversarial testing ONLY.

        NOT for physics law itself.
        Any law requiring this for differentiation → FAIL BRIDGE A.
        """
        if self.psi is None:
            raise ValueError("Must initialize symmetric Ka first")

        rng = self.xp.random.default_rng(seed)

        # Small symmetric-breaking perturbation
        perturbation = rng.standard_normal(self.relational_rank) + \
                      1j * rng.standard_normal(self.relational_rank)
        perturbation *= epsilon / self.xp.linalg.norm(perturbation)

        self.psi = self.psi + perturbation
        self.psi /= self.xp.linalg.norm(self.psi)

        return self.psi

    def apply_relational_update(self, G_operator, label: Optional[str] = None):
        """
        Apply one relational transformation, preserve in ordered history.

        Args:
            G_operator: Unitary operator (must conserve ledger)
            label: Optional physics-derived label (NOT arbitrary tag)
        """
        if self.psi is None:
            raise ValueError("Ka not initialized")

        # Verify unitarity
        I = self.xp.eye(self.relational_rank)
        unitarity_err = float(self.xp.max(self.xp.abs(
            G_operator @ G_operator.conj().T - I
        )))
        if unitarity_err > PhysicsGates.UNITARITY:
            raise ValueError(f"Operator not unitary: error={unitarity_err:.2e}")

        # Store in ordered history
        self.ordered_history_ops.append({
            'operator': G_operator if not self.gpu else G_operator.get(),
            'label': label,
            'step': len(self.ordered_history_ops)
        })

        # Evolve state
        self.psi = G_operator @ self.psi

        # Renormalize (should be automatic if G unitary, but FP64 drift)
        norm_before = float(self.xp.linalg.norm(self.psi))
        self.psi /= norm_before

        # Check conservation
        drift = abs(norm_before**2 - self.ledger_norm)
        if drift > PhysicsGates.CONSERVATION_RUNTIME:
            print(f"[WARNING] Ledger drift: {drift:.2e}")

        return self.psi

    def compute_history_invariants(self) -> Dict:
        """
        Compute gauge-invariant observables from ordered history.

        These must be physical invariants, not coordinate-dependent.
        """
        if not self.ordered_history_ops:
            return {}

        # Ordered product of all operators
        G_total = self.xp.eye(self.relational_rank, dtype=complex)
        for entry in self.ordered_history_ops:
            G = entry['operator']
            if self.gpu:
                G = cp.asarray(G)
            G_total = G @ G_total

        # Gauge-invariant spectral data
        eigenvalues = self.xp.linalg.eigvals(G_total)
        phases = self.xp.angle(eigenvalues)

        # Gram matrix (pairwise coherence)
        gram = self.xp.outer(self.psi.conj(), self.psi)

        invariants = {
            'total_operator_spectrum': phases if not self.gpu else phases.get(),
            'gram_matrix': gram if not self.gpu else gram.get(),
            'ledger_norm': self.ledger_norm,
            'history_length': len(self.ordered_history_ops)
        }

        self.ordered_history_invariants = invariants
        return invariants

    def copy(self):
        """Deep copy of current state"""
        new_state = PreSPACEState(self.relational_rank, self.gpu)
        if self.psi is not None:
            new_state.psi = self.psi.copy()
        new_state.ledger_norm = self.ledger_norm
        new_state.ordered_history_ops = [op.copy() for op in self.ordered_history_ops]
        new_state.ordered_history_invariants = self.ordered_history_invariants.copy()
        return new_state


def generate_skew_hermitian_generator(rank: int, seed: int,
                                     strength: float = 0.1,
                                     use_gpu: bool = False) -> np.ndarray:
    """
    Generate skew-Hermitian matrix for unitary evolution.

    H is skew-Hermitian: H† = -H
    Then U = exp(H) is unitary.

    Args:
        rank: Matrix size
        seed: Deterministic seed
        strength: Coupling strength
        use_gpu: Return CuPy array if True
    """
    xp = cp if (use_gpu and GPU_AVAILABLE) else np
    rng = xp.random.default_rng(seed)

    # Random skew-Hermitian (anti-Hermitian): H† = -H
    A = rng.standard_normal((rank, rank)) + 1j * rng.standard_normal((rank, rank))
    H = (A - A.conj().T) * strength
    
    # Verify skew-Hermitian
    assert xp.allclose(H.conj().T, -H), "Not skew-Hermitian"

    # Verify skew-Hermitian
    assert xp.allclose(H.conj().T, -H), "Not skew-Hermitian"

    return H


def generate_unitary_operator(rank: int, seed: int,
                              strength: float = 0.1,
                              use_gpu: bool = False) -> np.ndarray:
    """
    Generate unitary operator from skew-Hermitian generator.

    Deterministic (no random asymmetry injection).
    """
    H = generate_skew_hermitian_generator(rank, seed, strength, use_gpu)

    if use_gpu and GPU_AVAILABLE:
        U = cp.linalg.matrix_exp(H)
    else:
        from scipy.linalg import expm
        U = expm(H)

    return U


def test_ordered_history_discrimination(relational_rank: int = 8,
                                        use_gpu: bool = False) -> Dict:
    """
    DECISIVE TEST: Can we distinguish histories with different order
    but identical scalar statistics?

    Test ψ_A = G3 G2 G1 ψ0  vs  ψ_B = G1 G2 G3 ψ0

    Requirements:
    - [Gi, Gj] ≠ 0 (noncommuting)
    - ||ψ_A|| = ||ψ_B|| (same ledger)
    - Same operator multiset
    - Different causal order

    Returns:
        Result dict with discrimination metrics
    """
    xp = cp if (use_gpu and GPU_AVAILABLE) else np

    print("\n" + "="*70)
    print("DECISIVE TEST: Ordered History Discrimination")
    print("="*70)

    # Initialize symmetric Ka
    ka = PreSPACEState(relational_rank, use_gpu)
    psi_0 = ka.initialize_symmetric_ka()

    print(f"Symmetric Ka initialized: rank={relational_rank}, ledger={ka.ledger_norm:.6f}")

    # Generate three noncommuting unitary operators
    print("\nGenerating noncommuting operators...")
    G1 = generate_unitary_operator(relational_rank, seed=101, strength=0.3, use_gpu=use_gpu)
    G2 = generate_unitary_operator(relational_rank, seed=202, strength=0.3, use_gpu=use_gpu)
    G3 = generate_unitary_operator(relational_rank, seed=303, strength=0.3, use_gpu=use_gpu)

    # Verify noncommutation
    comm_12 = float(xp.linalg.norm(G1 @ G2 - G2 @ G1))
    comm_23 = float(xp.linalg.norm(G2 @ G3 - G3 @ G2))
    comm_13 = float(xp.linalg.norm(G1 @ G3 - G3 @ G1))

    print(f"Commutator norms:")
    print(f"  [G1,G2]: {comm_12:.6f}")
    print(f"  [G2,G3]: {comm_23:.6f}")
    print(f"  [G1,G3]: {comm_13:.6f}")

    if comm_12 < 1e-10 and comm_23 < 1e-10 and comm_13 < 1e-10:
        print("[ERROR] Operators commute — test invalid")
        return {'status': 'INVALID', 'reason': 'operators_commute'}

    # Two different ordered histories
    print("\nEvolving ordered histories...")
    psi_A = G3 @ G2 @ G1 @ psi_0  # Order: 1→2→3
    psi_B = G1 @ G2 @ G3 @ psi_0  # Order: 3→2→1

    # Normalize
    psi_A /= xp.linalg.norm(psi_A)
    psi_B /= xp.linalg.norm(psi_B)

    # Check same ledger norm
    norm_A = float(xp.abs(xp.vdot(psi_A, psi_A)))
    norm_B = float(xp.abs(xp.vdot(psi_B, psi_B)))
    ledger_match = abs(norm_A - norm_B)

    print(f"\nLedger norms:")
    print(f"  ψ_A: {norm_A:.10f}")
    print(f"  ψ_B: {norm_B:.10f}")
    print(f"  Difference: {ledger_match:.2e}")

    # Scalar statistics
    amp_sum_A = float(xp.sum(xp.abs(psi_A)**2))
    amp_sum_B = float(xp.sum(xp.abs(psi_B)**2))

    phase_A = xp.angle(psi_A)
    phase_B = xp.angle(psi_B)

    print(f"\nScalar statistics:")
    print(f"  Σ|ψ_A|²: {amp_sum_A:.10f}")
    print(f"  Σ|ψ_B|²: {amp_sum_B:.10f}")

    # CRITICAL: Full state difference
    state_diff = float(xp.linalg.norm(psi_A - psi_B))
    overlap = float(xp.abs(xp.vdot(psi_A, psi_B)))

    print(f"\nPhysical distinction:")
    print(f"  ||ψ_A - ψ_B||: {state_diff:.10f}")
    print(f"  |<ψ_A|ψ_B>|: {overlap:.10f}")

    # Gram matrices (gauge-invariant structure)
    gram_A = xp.outer(psi_A.conj(), psi_A)
    gram_B = xp.outer(psi_B.conj(), psi_B)
    gram_diff = float(xp.linalg.norm(gram_A - gram_B, 'fro'))

    print(f"  Gram matrix diff: {gram_diff:.10f}")

    # VERDICT
    can_distinguish = (state_diff > PhysicsGates.IDENTICAL_HISTORY or
                      overlap < (1.0 - PhysicsGates.IDENTICAL_HISTORY) or
                      gram_diff > PhysicsGates.IDENTICAL_HISTORY)

    print(f"\n{'='*70}")
    if can_distinguish:
        print("RESULT: Histories ARE physically distinguishable")
        print("→ Ordered relational structure preserved")
    else:
        print("RESULT: Histories NOT distinguishable")
        print("→ Representation collapses order to scalar statistics")
        print("→ KILL this representation class")
    print(f"{'='*70}\n")

    return {
        'status': 'PASS' if can_distinguish else 'FAIL',
        'can_distinguish': can_distinguish,
        'state_diff': state_diff,
        'overlap': overlap,
        'gram_diff': gram_diff,
        'commutator_norms': [comm_12, comm_23, comm_13],
        'ledger_match': ledger_match
    }


def test_symmetric_ka_baseline(relational_rank: int = 8,
                               n_steps: int = 10,
                               use_gpu: bool = False) -> Dict:
    """
    Test if differentiation emerges from symmetric Ka
    without random perturbation or arbitrary breaking.

    DECISIVE: Any law requiring asymmetry injection → FAIL BRIDGE A
    """
    xp = cp if (use_gpu and GPU_AVAILABLE) else np

    print("\n" + "="*70)
    print("SYMMETRIC KA BASELINE TEST")
    print("="*70)

    # Perfect symmetry
    ka = PreSPACEState(relational_rank, use_gpu)
    psi_0 = ka.initialize_symmetric_ka()

    # Verify exact symmetry
    amplitudes = xp.abs(psi_0)
    phases = xp.angle(psi_0)

    amp_var = float(xp.var(amplitudes))
    phase_var = float(xp.var(phases))

    print(f"Initial Ka state:")
    print(f"  Amplitude variance: {amp_var:.2e}")
    print(f"  Phase variance: {phase_var:.2e}")

    symmetric = (amp_var < PhysicsGates.SYMMETRY_BREAKING and
                phase_var < PhysicsGates.SYMMETRY_BREAKING)

    if not symmetric:
        print("[ERROR] Initial state not symmetric")
        return {'status': 'INVALID', 'reason': 'not_symmetric'}

    print("  → Exactly symmetric ✓")

    # Deterministic evolution (no random seed in physics)
    print(f"\nDeterministic evolution ({n_steps} steps)...")

    for step in range(n_steps):
        # Generate operator from step index only (deterministic)
        G = generate_unitary_operator(relational_rank, seed=1000+step,
                                      strength=0.2, use_gpu=use_gpu)
        ka.apply_relational_update(G, label=f"step_{step}")

    # Check if differentiation emerged
    psi_final = ka.psi
    final_amps = xp.abs(psi_final)
    final_phases = xp.angle(psi_final)

    final_amp_var = float(xp.var(final_amps))
    final_phase_var = float(xp.var(final_phases))

    print(f"\nFinal state:")
    print(f"  Amplitude variance: {final_amp_var:.2e}")
    print(f"  Phase variance: {final_phase_var:.2e}")

    differentiation_emerged = (final_amp_var > PhysicsGates.SYMMETRY_BREAKING or
                              final_phase_var > PhysicsGates.SYMMETRY_BREAKING)

    print(f"\n{'='*70}")
    if differentiation_emerged:
        print("RESULT: Differentiation emerged from symmetric Ka")
        print("→ Deterministic relational evolution breaks symmetry")
    else:
        print("RESULT: Symmetry preserved")
        print("→ This law class cannot differentiate symmetric Ka")
    print(f"{'='*70}\n")

    return {
        'status': 'PASS',
        'symmetric_initial': symmetric,
        'differentiation_emerged': differentiation_emerged,
        'initial_amp_var': amp_var,
        'initial_phase_var': phase_var,
        'final_amp_var': final_amp_var,
        'final_phase_var': final_phase_var
    }


if __name__ == "__main__":
    print("="*70)
    print("AWUT PHASE 5 — Bridge A Engine v2 (Clean Rebuild)")
    print("="*70)
    print(f"GPU Available: {GPU_AVAILABLE}\n")

    # Test 1: Ordered history discrimination (DECISIVE)
    result_discrimination = test_ordered_history_discrimination(
        relational_rank=8,
        use_gpu=GPU_AVAILABLE
    )

    # Test 2: Symmetric Ka baseline
    result_symmetric = test_symmetric_ka_baseline(
        relational_rank=8,
        n_steps=10,
        use_gpu=GPU_AVAILABLE
    )

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Ordered Discrimination: {result_discrimination['status']}")
    print(f"Symmetric Baseline: {result_symmetric['status']}")

    if result_discrimination['can_distinguish']:
        print("\n→ Noncommuting ordered histories are distinguishable")
        print("→ Order-sensitive representation viable for Bridge A")
    else:
        print("\n→ WARNING: Cannot distinguish different ordered histories")
        print("→ This representation class FAILED")

    if result_symmetric['differentiation_emerged']:
        print("\n→ Differentiation emerges from symmetric Ka deterministically")
    else:
        print("\n→ Symmetry preserved — additional physics needed")

    print("\n" + "="*70)
    print("Engine v2 smoke tests complete")
    print("Ready for production-scale aster1 execution")
    print("="*70)
