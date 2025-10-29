"""
CODATA 2018 Recommended Values

Official values from the Committee on Data for Science and Technology (CODATA)
2018 adjustment of fundamental physical constants.

Reference: https://physics.nist.gov/cuu/Constants/
DOI: 10.1103/RevModPhys.93.025010

All values include uncertainty estimates.
"""

# ==============================================================================
# FUNDAMENTAL CONSTANTS
# ==============================================================================

# Speed of light (exact, defined value)
c = {
    "value": 299792458.0,
    "uncertainty": 0.0,
    "unit": "m/s",
    "relative_uncertainty": 0.0,
    "source": "CODATA 2018 (exact)"
}

# Planck constant (exact, defined value since 2019)
h = {
    "value": 6.62607015e-34,
    "uncertainty": 0.0,
    "unit": "J·s",
    "relative_uncertainty": 0.0,
    "source": "CODATA 2018 (exact)"
}

# Reduced Planck constant
hbar = {
    "value": 1.054571817e-34,
    "uncertainty": 0.0,
    "unit": "J·s",
    "relative_uncertainty": 0.0,
    "source": "CODATA 2018 (exact, derived from h)"
}

# Elementary charge (exact, defined value since 2019)
e = {
    "value": 1.602176634e-19,
    "uncertainty": 0.0,
    "unit": "C",
    "relative_uncertainty": 0.0,
    "source": "CODATA 2018 (exact)"
}

# ==============================================================================
# PARTICLE MASSES
# ==============================================================================

# Electron mass
m_electron = {
    "value": 9.1093837015e-31,
    "uncertainty": 2.8e-40,
    "unit": "kg",
    "relative_uncertainty": 3.0e-10,
    "source": "CODATA 2018"
}

# Electron mass in MeV/c²
m_electron_MeV = {
    "value": 0.51099895000,
    "uncertainty": 1.5e-10,
    "unit": "MeV/c²",
    "relative_uncertainty": 3.0e-10,
    "source": "CODATA 2018"
}

# Proton mass
m_proton = {
    "value": 1.67262192369e-27,
    "uncertainty": 5.1e-37,
    "unit": "kg",
    "relative_uncertainty": 3.1e-10,
    "source": "CODATA 2018"
}

# Proton mass in MeV/c²
m_proton_MeV = {
    "value": 938.27208816,
    "uncertainty": 2.9e-7,
    "unit": "MeV/c²",
    "relative_uncertainty": 3.1e-10,
    "source": "CODATA 2018"
}

# Neutron mass
m_neutron = {
    "value": 1.67492749804e-27,
    "uncertainty": 9.5e-37,
    "unit": "kg",
    "relative_uncertainty": 5.7e-10,
    "source": "CODATA 2018"
}

# Neutron mass in MeV/c²
m_neutron_MeV = {
    "value": 939.56542052,
    "uncertainty": 5.4e-7,
    "unit": "MeV/c²",
    "relative_uncertainty": 5.7e-10,
    "source": "CODATA 2018"
}

# Muon mass
m_muon = {
    "value": 1.883531627e-28,
    "uncertainty": 4.2e-36,
    "unit": "kg",
    "relative_uncertainty": 2.2e-8,
    "source": "CODATA 2018"
}

# Muon mass in MeV/c²
m_muon_MeV = {
    "value": 105.6583745,
    "uncertainty": 2.4e-6,
    "unit": "MeV/c²",
    "relative_uncertainty": 2.2e-8,
    "source": "CODATA 2018"
}

# Tau mass (from PDG, not in CODATA)
m_tau_MeV = {
    "value": 1776.86,
    "uncertainty": 0.12,
    "unit": "MeV/c²",
    "relative_uncertainty": 6.8e-5,
    "source": "PDG 2024"
}

# ==============================================================================
# MASS RATIOS
# ==============================================================================

# Proton-to-electron mass ratio
m_p_m_e = {
    "value": 1836.15267343,
    "uncertainty": 0.00000011,
    "unit": "dimensionless",
    "relative_uncertainty": 6.0e-11,
    "source": "CODATA 2018"
}

# Muon-to-electron mass ratio
m_mu_m_e = {
    "value": 206.7682830,
    "uncertainty": 0.0000046,
    "unit": "dimensionless",
    "relative_uncertainty": 2.2e-8,
    "source": "CODATA 2018"
}

# Tau-to-electron mass ratio
m_tau_m_e = {
    "value": 3477.23,
    "uncertainty": 0.23,
    "unit": "dimensionless",
    "relative_uncertainty": 6.6e-5,
    "source": "PDG 2024"
}

# ==============================================================================
# ELECTROMAGNETIC PROPERTIES
# ==============================================================================

# Fine-structure constant
alpha = {
    "value": 7.2973525693e-3,
    "uncertainty": 1.1e-12,
    "unit": "dimensionless",
    "relative_uncertainty": 1.5e-10,
    "source": "CODATA 2018"
}

# Inverse fine-structure constant
alpha_inv = {
    "value": 137.035999084,
    "uncertainty": 2.1e-8,
    "unit": "dimensionless",
    "relative_uncertainty": 1.5e-10,
    "source": "CODATA 2018"
}

# Electron g-factor
g_e = {
    "value": -2.00231930436256,
    "uncertainty": 3.5e-13,
    "unit": "dimensionless",
    "relative_uncertainty": 1.7e-13,
    "source": "CODATA 2018"
}

# Muon g-factor (see fermilab_muon_g2.json for latest measurement)
g_mu = {
    "value": -2.0023318418,
    "uncertainty": 1.3e-9,
    "unit": "dimensionless",
    "relative_uncertainty": 6.3e-10,
    "source": "CODATA 2018 (older measurement)"
}

# ==============================================================================
# GRAVITATIONAL CONSTANT
# ==============================================================================

G = {
    "value": 6.67430e-11,
    "uncertainty": 1.5e-15,
    "unit": "m³/(kg·s²)",
    "relative_uncertainty": 2.2e-5,
    "source": "CODATA 2018"
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_value(constant_dict):
    """Extract just the numerical value from a constant dictionary."""
    return constant_dict["value"]

def get_uncertainty(constant_dict):
    """Extract just the uncertainty from a constant dictionary."""
    return constant_dict["uncertainty"]

def print_constant(name, constant_dict):
    """Print a formatted constant with uncertainty."""
    val = constant_dict["value"]
    unc = constant_dict["uncertainty"]
    unit = constant_dict["unit"]
    src = constant_dict["source"]

    if unc == 0:
        print(f"{name}: {val} {unit} (exact, {src})")
    else:
        print(f"{name}: {val} ± {unc} {unit} ({src})")

# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CODATA 2018 RECOMMENDED VALUES")
    print("="*70 + "\n")

    print("--- Fundamental Constants ---")
    print_constant("Speed of light", c)
    print_constant("Planck constant", h)
    print_constant("Elementary charge", e)

    print("\n--- Particle Masses ---")
    print_constant("Electron mass", m_electron_MeV)
    print_constant("Proton mass", m_proton_MeV)
    print_constant("Muon mass", m_muon_MeV)

    print("\n--- Mass Ratios ---")
    print_constant("Proton/electron mass ratio", m_p_m_e)
    print_constant("Muon/electron mass ratio", m_mu_m_e)

    print("\n--- Electromagnetic Properties ---")
    print_constant("Fine-structure constant", alpha)

    print()
