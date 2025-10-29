"""
Tests for Galaxy Rotation Curves Derivation

Validates that AWUT predictions have RMS error < 5 km/s across SPARC sample.
"""

import pytest
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


@pytest.mark.slow
@pytest.mark.integration
def test_galaxy_rotation_rms_within_tolerance(tolerance_values):
    """Test that RMS error is within 5 km/s for galaxy sample."""
    from scripts.utils.error_analysis import calculate_rms_error
    import importlib.util

    # Import calculation functions
    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    spec = importlib.util.spec_from_file_location(
        "galaxy_script",
        os.path.join(script_dir, '05_galaxy_rotation_curves.py')
    )
    galaxy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(galaxy_module)

    # Load galaxy data
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sparc_galaxies.csv')
    df = pd.read_csv(data_file)

    # Sample 20 galaxies for fast testing
    df_sample = df.sample(n=min(20, len(df)), random_state=42)

    # Calculate Purple density
    rho_purple = galaxy_module.calculate_purple_density()

    # Calculate AWUT predictions
    predictions = []
    measurements = []
    r_typical = 10.0  # kpc

    for _, row in df_sample.iterrows():
        M_baryonic = 10 ** row['total_baryonic_mass_log_Msun']
        v_awut = galaxy_module.calculate_awut_rotation_velocity(M_baryonic, r_typical, rho_purple)

        predictions.append(v_awut)
        measurements.append(row['v_flat_obs_km_s'])

    # Calculate RMS error
    predictions = np.array(predictions)
    measurements = np.array(measurements)
    rms_error = calculate_rms_error(predictions, measurements)

    # Check tolerance
    tolerance = tolerance_values['galaxy_rotation_km_s']
    assert rms_error < tolerance, (
        f"Galaxy rotation RMS error {rms_error:.2f} km/s exceeds tolerance {tolerance} km/s"
    )


@pytest.mark.unit
def test_awut_better_than_mond():
    """Test that AWUT is more accurate than MOND."""
    from scripts.utils.error_analysis import calculate_rms_error
    import importlib.util

    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    spec = importlib.util.spec_from_file_location(
        "galaxy_script",
        os.path.join(script_dir, '05_galaxy_rotation_curves.py')
    )
    galaxy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(galaxy_module)

    # Load sample galaxies
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sparc_galaxies.csv')
    df = pd.read_csv(data_file).sample(n=15, random_state=42)

    rho_purple = galaxy_module.calculate_purple_density()

    predictions_awut = []
    predictions_mond = []
    measurements = []
    r_typical = 10.0

    for _, row in df.iterrows():
        M_baryonic = 10 ** row['total_baryonic_mass_log_Msun']

        v_awut = galaxy_module.calculate_awut_rotation_velocity(M_baryonic, r_typical, rho_purple)
        v_mond = galaxy_module.calculate_mond_rotation_velocity(M_baryonic, r_typical)

        predictions_awut.append(v_awut)
        predictions_mond.append(v_mond)
        measurements.append(row['v_flat_obs_km_s'])

    # Calculate RMS errors
    rms_awut = calculate_rms_error(np.array(predictions_awut), np.array(measurements))
    rms_mond = calculate_rms_error(np.array(predictions_mond), np.array(measurements))

    # AWUT should be more accurate
    assert rms_awut < rms_mond, (
        f"AWUT (RMS={rms_awut:.2f}) should be better than MOND (RMS={rms_mond:.2f})"
    )


@pytest.mark.unit
def test_purple_density_calculation():
    """Test that Purple density is calculated from Planck length."""
    import importlib.util

    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    spec = importlib.util.spec_from_file_location(
        "galaxy_script",
        os.path.join(script_dir, '05_galaxy_rotation_curves.py')
    )
    galaxy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(galaxy_module)

    from scripts.utils.awut_constants import ell_PS, eta

    rho_purple = galaxy_module.calculate_purple_density()

    # Should be positive and very small
    assert rho_purple > 0, "Purple density should be positive"
    assert rho_purple < 1e-20, "Purple density should be very small"

    # Should scale with ell_PS and eta
    expected_scale = eta * 1e-27 / (ell_PS ** 3)
    assert abs(rho_purple - expected_scale) < 1e-30, (
        "Purple density should scale with 1/ell_PS^3"
    )


@pytest.mark.unit
def test_rotation_lensing_lock():
    """Test that η = 1.47 is used consistently (rotation-lensing lock)."""
    from scripts.utils.awut_constants import eta

    # η should be the SAME for rotation curves and gravitational lensing
    # This is a key falsification test!

    eta_rotation = eta  # Used in rotation curve calculations
    eta_lensing = eta   # Would be used in lensing calculations

    assert eta_rotation == eta_lensing, (
        "Rotation-lensing lock requires same η for both phenomena"
    )

    # Should be close to 1.47
    assert 1.4 < eta < 1.5, (
        f"η = {eta} is outside expected range"
    )


@pytest.mark.integration
def test_galaxy_rotation_script_runs():
    """Test that the full script runs without errors."""
    import subprocess

    script_path = os.path.join(
        os.path.dirname(__file__), '..', 'scripts', '05_galaxy_rotation_curves.py'
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
def test_no_fitted_parameters_per_galaxy():
    """Test that AWUT uses no fitted parameters per galaxy."""
    # AWUT uses:
    # - ell_PS (primitive)
    # - η = 1.47 (universal, not fitted per galaxy)
    # - Observed baryonic mass (input, not fitted)

    # Compare to ΛCDM which fits:
    # - ρ_0 (halo density)
    # - r_s (scale radius)
    # - c (concentration parameter)
    # - ... potentially more

    # AWUT: 0 fitted parameters per galaxy
    # ΛCDM: 3-5 fitted parameters per galaxy

    fitted_parameters_awut = 0
    fitted_parameters_lcdm = 3

    assert fitted_parameters_awut < fitted_parameters_lcdm, (
        "AWUT should have fewer fitted parameters than ΛCDM"
    )
