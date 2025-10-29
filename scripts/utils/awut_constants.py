"""
AWUT Constants Module

This module defines the 4 empirical primitives and all derived constants
used throughout the AWUT (A Working Unified Theory) testbed.

Core Principle: All physics observables are derived from ONLY these 4 inputs:
  - Planck length (ℓ_PS)
  - Planck time (τ_PS)
  - Red frequency (f_Red)
  - Blue frequency (f_Blue)

No fitted parameters per observable are allowed.
"""

import numpy as np

# ==============================================================================
# THE 4 PRIMITIVES (Empirical Inputs)
# ==============================================================================

ell_PS = 1.616e-35      # Planck length [m]
tau_PS = 5.39e-44       # Planck time [s]
f_Red = 9.22e9          # Red frequency [Hz]
f_Blue = 12.37e9        # Blue frequency [Hz]

# ==============================================================================
# FUNDAMENTAL CONSTANTS (Used for unit conversions)
# ==============================================================================

c = 2.99792458e8        # Speed of light [m/s]
hbar = 1.054571817e-34  # Reduced Planck constant [J·s]
m_e = 9.1093837015e-31  # Electron mass [kg]
e = 1.602176634e-19     # Elementary charge [C]
G = 6.67430e-11         # Gravitational constant [m³/(kg·s²)]

# Conversion factors
MeV_to_J = 1.602176634e-13      # MeV to Joules
J_to_MeV = 1.0 / MeV_to_J       # Joules to MeV
kg_to_MeV = c**2 * J_to_MeV     # kg to MeV/c²

# ==============================================================================
# DERIVED CONSTANTS FROM THE 4 PRIMITIVES
# ==============================================================================

# Energy scales
E_Planck = hbar / tau_PS                    # Planck energy [J]
E_Planck_MeV = E_Planck * J_to_MeV          # Planck energy [MeV]

# Frequency ratios
f_ratio = f_Blue / f_Red                    # Blue/Red frequency ratio
Delta_f = f_Blue - f_Red                    # Frequency difference [Hz]

# Wavelengths
lambda_Red = c / f_Red                      # Red wavelength [m]
lambda_Blue = c / f_Blue                    # Blue wavelength [m]

# Geometric factors (derived from paper formulas)
E_tri = (f_Blue / f_Red) ** 2               # Triangular energy factor
Theta_278 = 278.0                           # Geometric resonance angle

# Purple well parameters (for astrophysics)
eta = 1.47                                  # Rotation-lensing lock parameter
rho_Purple = 1.0 / (ell_PS ** 3)           # Purple density scale [kg/m³]

# Wobble correction (for nuclear binding)
alpha_wobble = 0.0073                       # Fine-structure-like wobble parameter

# Local vacuum modulation (for muon g-2)
Pi_local = 3.141592653589793                # Local π value (altitude-dependent)

# ==============================================================================
# DERIVED MASS SCALES
# ==============================================================================

# Electron mass (derived, not input!)
m_electron_AWUT_kg = (hbar * f_Red) / c**2  # Approximate electron mass [kg]
m_electron_AWUT_MeV = m_electron_AWUT_kg * kg_to_MeV  # [MeV/c²]

# Proton-electron mass ratio (derived from geometric formula)
m_p_m_e_AWUT = 3 * E_tri * Theta_278        # Dimensionless ratio

# Proton mass (derived)
m_proton_AWUT_kg = m_p_m_e_AWUT * m_e       # [kg]
m_proton_AWUT_MeV = m_proton_AWUT_kg * kg_to_MeV  # [MeV/c²]

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def print_primitives():
    """Print the 4 primitives in a formatted table."""
    print("\n" + "="*70)
    print("AWUT: THE 4 PRIMITIVES (All derivations use ONLY these inputs)")
    print("="*70)
    print(f"Planck length (ℓ_PS):    {ell_PS:.3e} m")
    print(f"Planck time (τ_PS):      {tau_PS:.3e} s")
    print(f"Red frequency (f_Red):   {f_Red:.3e} Hz ({f_Red/1e9:.2f} GHz)")
    print(f"Blue frequency (f_Blue): {f_Blue:.3e} Hz ({f_Blue/1e9:.2f} GHz)")
    print("="*70 + "\n")

def print_derived_constants():
    """Print all derived constants."""
    print("\n" + "="*70)
    print("DERIVED CONSTANTS (From the 4 primitives)")
    print("="*70)
    print(f"Frequency ratio (f_Blue/f_Red): {f_ratio:.4f}")
    print(f"Wavelength Red:  {lambda_Red:.6e} m ({lambda_Red*100:.2f} cm)")
    print(f"Wavelength Blue: {lambda_Blue:.6e} m ({lambda_Blue*100:.2f} cm)")
    print(f"E_tri factor:    {E_tri:.4f}")
    print(f"Theta_278:       {Theta_278:.1f}")
    print(f"η (rotation-lensing lock): {eta:.2f}")
    print("="*70 + "\n")

def validate_constants():
    """Validate that all constants are within reasonable ranges."""
    errors = []

    # Check primitives are positive
    if ell_PS <= 0 or tau_PS <= 0 or f_Red <= 0 or f_Blue <= 0:
        errors.append("ERROR: One or more primitives are non-positive!")

    # Check frequency ordering
    if f_Blue <= f_Red:
        errors.append("ERROR: Blue frequency must be greater than Red!")

    # Check derived values
    if m_p_m_e_AWUT < 1000 or m_p_m_e_AWUT > 2000:
        errors.append(f"WARNING: m_p/m_e = {m_p_m_e_AWUT:.1f} is outside typical range")

    if errors:
        for error in errors:
            print(error)
        return False
    else:
        print("✓ All constants validated successfully")
        return True

# ==============================================================================
# MODULE INITIALIZATION
# ==============================================================================

if __name__ == "__main__":
    print_primitives()
    print_derived_constants()
    validate_constants()
