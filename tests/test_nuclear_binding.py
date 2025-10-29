"""
Tests for Nuclear Binding Energies Derivation

Validates that AWUT predictions have RMS error < 0.5 MeV across sample nuclei.
"""

import pytest
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


@pytest.mark.slow
@pytest.mark.integration
def test_nuclear_binding_rms_within_tolerance(tolerance_values):
    """Test that RMS error with wobble correction is within 0.5 MeV."""
    from scripts.utils.error_analysis import calculate_rms_error
    import numpy as np

    # This test requires running the full calculation
    # Import the calculation functions
    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    sys.path.insert(0, script_dir)

    # Import from the script module
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "nuclear_script",
        os.path.join(script_dir, '04_nuclear_binding_energies.py')
    )
    nuclear_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nuclear_module)

    # Load test nuclei
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'ame2020_nuclei.csv')
    df = pd.read_csv(data_file)

    # Sample nuclei
    selected = ['He-4', 'C-12', 'O-16', 'Ca-40', 'Fe-56', 'Pb-208']
    df_sample = df[df['nucleus'].isin(selected)]

    # Calculate AWUT predictions with wobble
    predictions = []
    measurements = []

    for _, row in df_sample.iterrows():
        B_awut = nuclear_module.calculate_awut_binding_with_wobble(
            row['A'], row['Z'], row['N']
        )
        predictions.append(B_awut)
        measurements.append(row['binding_energy_MeV'])

    # Calculate RMS error
    predictions = np.array(predictions)
    measurements = np.array(measurements)
    rms_error = calculate_rms_error(predictions, measurements)

    # Check tolerance
    tolerance = tolerance_values['nuclear_binding_MeV']
    assert rms_error < tolerance, (
        f"Nuclear binding RMS error {rms_error:.3f} MeV exceeds tolerance {tolerance} MeV"
    )


@pytest.mark.unit
def test_wobble_correction_improves_accuracy():
    """Test that wobble correction improves accuracy."""
    from scripts.utils.error_analysis import calculate_rms_error
    import numpy as np
    import importlib.util

    # Import calculation functions
    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    spec = importlib.util.spec_from_file_location(
        "nuclear_script",
        os.path.join(script_dir, '04_nuclear_binding_energies.py')
    )
    nuclear_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nuclear_module)

    # Load test nuclei
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'ame2020_nuclei.csv')
    df = pd.read_csv(data_file)

    selected = ['He-4', 'O-16', 'Ca-40', 'Fe-56']
    df_sample = df[df['nucleus'].isin(selected)]

    # Calculate with and without wobble
    predictions_base = []
    predictions_wobble = []
    measurements = []

    for _, row in df_sample.iterrows():
        B_base = nuclear_module.calculate_awut_binding_base(row['A'], row['Z'], row['N'])
        B_wobble = nuclear_module.calculate_awut_binding_with_wobble(row['A'], row['Z'], row['N'])

        predictions_base.append(B_base)
        predictions_wobble.append(B_wobble)
        measurements.append(row['binding_energy_MeV'])

    # Calculate RMS errors
    rms_base = calculate_rms_error(np.array(predictions_base), np.array(measurements))
    rms_wobble = calculate_rms_error(np.array(predictions_wobble), np.array(measurements))

    # Wobble should improve accuracy
    assert rms_wobble < rms_base, (
        "Wobble correction should improve accuracy"
    )


@pytest.mark.unit
def test_magic_nuclei_special_treatment():
    """Test that doubly magic nuclei get special treatment."""
    import importlib.util

    script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    spec = importlib.util.spec_from_file_location(
        "nuclear_script",
        os.path.join(script_dir, '04_nuclear_binding_energies.py')
    )
    nuclear_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nuclear_module)

    # Pb-208 is doubly magic (Z=82, N=126)
    wobble_pb208 = nuclear_module.calculate_wobble_correction(208, 82, 126)

    # Regular nucleus
    wobble_regular = nuclear_module.calculate_wobble_correction(208, 80, 128)

    # Magic nucleus should have different (likely higher) wobble factor
    # due to shell closure bonus
    assert wobble_pb208 != wobble_regular, (
        "Doubly magic nucleus should have different wobble factor"
    )


@pytest.mark.integration
def test_nuclear_binding_script_runs():
    """Test that the full script runs without errors."""
    import subprocess

    script_path = os.path.join(
        os.path.dirname(__file__), '..', 'scripts', '04_nuclear_binding_energies.py'
    )

    result = subprocess.run(
        ['python', script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Script failed with return code {result.returncode}"
    )
