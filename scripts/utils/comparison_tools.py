"""
Comparison Tools Module

Provides utilities for comparing AWUT predictions with:
  - Experimental measurements (CODATA, PDG, Fermilab, etc.)
  - Standard Model predictions (QED, lattice QCD)
  - Alternative theories (MOND, ΛCDM)

Key functions:
  - compare_values(): Compare AWUT vs measured with error analysis
  - print_comparison_table(): Formatted output
  - calculate_sigma_deviation(): Statistical significance
  - save_comparison_json(): Export results
"""

import numpy as np
import json
from typing import Dict, Tuple, Optional

# ==============================================================================
# CORE COMPARISON FUNCTIONS
# ==============================================================================

def calculate_error(awut_value: float, measured_value: float) -> Tuple[float, float]:
    """
    Calculate absolute and relative error between AWUT and measurement.

    Args:
        awut_value: AWUT theoretical prediction
        measured_value: Experimental measurement

    Returns:
        (absolute_error, relative_error_percent)
    """
    abs_error = awut_value - measured_value
    rel_error_pct = (abs_error / measured_value) * 100
    return abs_error, rel_error_pct

def calculate_sigma_deviation(awut_value: float,
                               measured_value: float,
                               measurement_uncertainty: float) -> float:
    """
    Calculate how many standard deviations AWUT prediction differs from measurement.

    Args:
        awut_value: AWUT prediction
        measured_value: Experimental value
        measurement_uncertainty: Experimental uncertainty (1σ)

    Returns:
        Number of sigma deviation
    """
    if measurement_uncertainty == 0:
        return np.inf if awut_value != measured_value else 0.0

    return abs(awut_value - measured_value) / measurement_uncertainty

def compare_values(observable_name: str,
                   awut_value: float,
                   measured_value: float,
                   measurement_uncertainty: float = 0.0,
                   sm_value: Optional[float] = None,
                   units: str = "",
                   tolerance_pct: float = 0.1) -> Dict:
    """
    Comprehensive comparison between AWUT prediction and measurement.

    Args:
        observable_name: Name of the physical observable
        awut_value: AWUT theoretical prediction
        measured_value: Experimental measurement
        measurement_uncertainty: Experimental uncertainty (1σ)
        sm_value: Standard Model prediction (optional)
        units: Physical units of the observable
        tolerance_pct: Tolerance for pass/fail (default 0.1%)

    Returns:
        Dictionary with comparison results
    """
    abs_error, rel_error_pct = calculate_error(awut_value, measured_value)
    sigma_dev = calculate_sigma_deviation(awut_value, measured_value, measurement_uncertainty)

    status = "PASS" if abs(rel_error_pct) < tolerance_pct else "FAIL"

    result = {
        "observable": observable_name,
        "awut_prediction": awut_value,
        "measured_value": measured_value,
        "measurement_uncertainty": measurement_uncertainty,
        "absolute_error": abs_error,
        "relative_error_percent": rel_error_pct,
        "sigma_deviation": sigma_dev,
        "units": units,
        "status": status,
        "tolerance_percent": tolerance_pct
    }

    # Add Standard Model comparison if provided
    if sm_value is not None:
        sm_abs_error, sm_rel_error_pct = calculate_error(sm_value, measured_value)
        sm_sigma_dev = calculate_sigma_deviation(sm_value, measured_value, measurement_uncertainty)

        result["sm_prediction"] = sm_value
        result["sm_relative_error_percent"] = sm_rel_error_pct
        result["sm_sigma_deviation"] = sm_sigma_dev
        result["awut_improvement_factor"] = abs(sm_rel_error_pct / rel_error_pct) if rel_error_pct != 0 else np.inf

    return result

# ==============================================================================
# FORMATTING AND OUTPUT
# ==============================================================================

def print_comparison_table(result: Dict):
    """
    Print a formatted comparison table for a single observable.

    Args:
        result: Dictionary from compare_values()
    """
    print("\n" + "="*70)
    print(f"Observable: {result['observable']}")
    print("="*70)
    print(f"AWUT Prediction:    {result['awut_prediction']:.10f} {result['units']}")
    print(f"Measured Value:     {result['measured_value']:.10f} {result['units']}")

    if result['measurement_uncertainty'] > 0:
        print(f"Uncertainty:        ±{result['measurement_uncertainty']:.10e} {result['units']}")

    print(f"\nAbsolute Error:     {result['absolute_error']:.10e} {result['units']}")
    print(f"Relative Error:     {result['relative_error_percent']:.6f}%")

    if result['measurement_uncertainty'] > 0:
        print(f"Sigma Deviation:    {result['sigma_deviation']:.2f}σ")

    # Standard Model comparison
    if 'sm_prediction' in result:
        print(f"\n--- Standard Model Comparison ---")
        print(f"SM Prediction:      {result['sm_prediction']:.10f} {result['units']}")
        print(f"SM Relative Error:  {result['sm_relative_error_percent']:.6f}%")
        print(f"AWUT Improvement:   {result['awut_improvement_factor']:.2f}x better")

    # Pass/Fail status
    status_symbol = "✓" if result['status'] == "PASS" else "✗"
    print(f"\nStatus: {status_symbol} {result['status']} (tolerance: {result['tolerance_percent']}%)")
    print("="*70 + "\n")

def print_summary_table(results: list):
    """
    Print a summary table comparing multiple observables.

    Args:
        results: List of result dictionaries from compare_values()
    """
    print("\n" + "="*90)
    print("AWUT TESTBED: SUMMARY OF ALL OBSERVABLES")
    print("="*90)
    print(f"{'Observable':<35} {'Error (%)':<15} {'Sigma':<10} {'Status':<10}")
    print("-"*90)

    for result in results:
        obs_name = result['observable'][:33]
        error_pct = result['relative_error_percent']
        sigma = result['sigma_deviation'] if result['measurement_uncertainty'] > 0 else np.nan
        status = "✓" if result['status'] == "PASS" else "✗"

        sigma_str = f"{sigma:.2f}σ" if not np.isnan(sigma) else "N/A"
        print(f"{obs_name:<35} {error_pct:>12.4f}%   {sigma_str:<10} {status:<10}")

    print("="*90 + "\n")

    # Calculate overall statistics
    pass_count = sum(1 for r in results if r['status'] == "PASS")
    total_count = len(results)
    avg_error = np.mean([abs(r['relative_error_percent']) for r in results])

    print(f"Overall Pass Rate: {pass_count}/{total_count} ({pass_count/total_count*100:.1f}%)")
    print(f"Average Error:     {avg_error:.4f}%")
    print()

# ==============================================================================
# DATA EXPORT
# ==============================================================================

def save_comparison_json(result: Dict, filename: str):
    """
    Save comparison result to JSON file.

    Args:
        result: Dictionary from compare_values()
        filename: Output filename (e.g., "outputs/proton_electron.json")
    """
    # Convert numpy types to native Python types for JSON serialization
    json_result = {}
    for key, value in result.items():
        if isinstance(value, (np.float64, np.float32)):
            json_result[key] = float(value)
        elif isinstance(value, (np.int64, np.int32)):
            json_result[key] = int(value)
        else:
            json_result[key] = value

    with open(filename, 'w') as f:
        json.dump(json_result, f, indent=2)

    print(f"✓ Results saved to {filename}")

def save_summary_json(results: list, filename: str):
    """
    Save summary of all results to JSON file.

    Args:
        results: List of result dictionaries
        filename: Output filename (e.g., "outputs/derivation_results.json")
    """
    # Convert all results
    json_results = []
    for result in results:
        json_result = {}
        for key, value in result.items():
            if isinstance(value, (np.float64, np.float32)):
                json_result[key] = float(value)
            elif isinstance(value, (np.int64, np.int32)):
                json_result[key] = int(value)
            else:
                json_result[key] = value
        json_results.append(json_result)

    # Add summary statistics
    summary = {
        "results": json_results,
        "summary": {
            "total_observables": len(results),
            "passed": sum(1 for r in results if r['status'] == "PASS"),
            "failed": sum(1 for r in results if r['status'] == "FAIL"),
            "average_error_percent": float(np.mean([abs(r['relative_error_percent']) for r in results])),
            "max_error_percent": float(np.max([abs(r['relative_error_percent']) for r in results])),
            "min_error_percent": float(np.min([abs(r['relative_error_percent']) for r in results]))
        }
    }

    with open(filename, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✓ Summary saved to {filename}")

# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == "__main__":
    # Example usage
    result = compare_values(
        observable_name="Proton-Electron Mass Ratio",
        awut_value=1834.8,
        measured_value=1836.15267,
        measurement_uncertainty=0.00027,
        sm_value=None,
        units="dimensionless",
        tolerance_pct=0.1
    )

    print_comparison_table(result)

    # Example with multiple results
    results = [result]
    print_summary_table(results)
