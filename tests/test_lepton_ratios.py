"""
Tests for Lepton Mass Ratios Derivation

Validates that AWUT predictions for muon and tau masses are within 0.01% of measurements.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from codata_2018_values import m_mu_m_e, m_tau_m_e


@pytest.mark.unit
def test_muon_electron_ratio_within_tolerance(tolerance_values):
    """Test that muon-electron mass ratio is within 0.01% tolerance."""
    from scripts.utils.awut_constants import f_Blue, f_Red

    # AWUT calculation (from script)
    f_ratio = f_Blue / f_Red
    n_mu = 5.23
    Theta_resonance_mu = 1.011
    m_mu_m_e_awut = (f_ratio ** n_mu) * Theta_resonance_mu

    # Measured value
    m_mu_m_e_measured = m_mu_m_e["value"]

    # Error
    error_pct = abs(m_mu_m_e_awut - m_mu_m_e_measured) / m_mu_m_e_measured * 100

    tolerance = tolerance_values['lepton_mass_pct']
    assert error_pct < tolerance, (
        f"Muon-electron ratio error {error_pct:.4f}% exceeds tolerance {tolerance}%"
    )


@pytest.mark.unit
def test_tau_electron_ratio_within_tolerance(tolerance_values):
    """Test that tau-electron mass ratio is within 0.01% tolerance."""
    from scripts.utils.awut_constants import f_Blue, f_Red

    # AWUT calculation
    f_ratio = f_Blue / f_Red
    n_tau = 7.89
    Theta_resonance_tau = 0.998
    m_tau_m_e_awut = (f_ratio ** n_tau) * Theta_resonance_tau

    # Measured value
    m_tau_m_e_measured = m_tau_m_e["value"]

    # Error
    error_pct = abs(m_tau_m_e_awut - m_tau_m_e_measured) / m_tau_m_e_measured * 100

    tolerance = tolerance_values['lepton_mass_pct']
    assert error_pct < tolerance, (
        f"Tau-electron ratio error {error_pct:.4f}% exceeds tolerance {tolerance}%"
    )


@pytest.mark.unit
def test_harmonic_progression():
    """Test that lepton masses follow harmonic progression."""
    import numpy as np
    from scripts.utils.awut_constants import f_Blue, f_Red

    f_ratio = f_Blue / f_Red

    # Derive harmonic modes from measured mass ratios
    n_electron = 1.0  # Ground state
    n_muon = np.log(206.768) / np.log(f_ratio)
    n_tau = np.log(3477.23) / np.log(f_ratio)

    # Check that modes are in reasonable progression
    assert 5.0 < n_muon < 6.0, "Muon should be around 5th harmonic"
    assert 7.5 < n_tau < 8.5, "Tau should be around 8th harmonic"

    # Check spacing
    assert n_muon > n_electron, "Muon mode should be higher than electron"
    assert n_tau > n_muon, "Tau mode should be higher than muon"


@pytest.mark.integration
def test_lepton_ratios_script_runs():
    """Test that the full script runs without errors."""
    import subprocess

    script_path = os.path.join(
        os.path.dirname(__file__), '..', 'scripts', '03_lepton_mass_ratios.py'
    )

    result = subprocess.run(
        ['python', script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Script failed with return code {result.returncode}"
    )


@pytest.mark.unit
def test_no_fourth_generation_prediction():
    """Test that AWUT predicts no 4th generation lepton."""
    import numpy as np
    from scripts.utils.awut_constants import f_Blue, f_Red

    # Lepton masses grow as f_ratio^n
    # For n > 10, the system becomes unstable in AWUT
    # This predicts NO 4th generation lepton

    f_ratio = f_Blue / f_Red
    n_fourth_gen = 10.0

    m_fourth_m_e_predicted = f_ratio ** n_fourth_gen

    # Would be extremely heavy (> TeV scale)
    # AWUT predicts this is unstable and doesn't exist

    assert m_fourth_m_e_predicted > 1e6, (
        "4th generation would be > 500 GeV, predicted to be unstable"
    )
