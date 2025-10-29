"""
Error Analysis Module

Provides statistical tools for analyzing AWUT prediction errors:
  - RMS (Root Mean Square) error
  - Mean absolute error
  - Chi-squared statistics
  - Residual analysis
  - Error distribution plots

Used for multi-observable studies like nuclear binding energies
and galaxy rotation curves.
"""

import numpy as np
from typing import List, Tuple, Dict
import json

# ==============================================================================
# STATISTICAL ERROR METRICS
# ==============================================================================

def calculate_rms_error(predictions: np.ndarray, measurements: np.ndarray) -> float:
    """
    Calculate Root Mean Square (RMS) error.

    Args:
        predictions: Array of predicted values
        measurements: Array of measured values

    Returns:
        RMS error
    """
    residuals = predictions - measurements
    return np.sqrt(np.mean(residuals**2))

def calculate_mean_absolute_error(predictions: np.ndarray, measurements: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error (MAE).

    Args:
        predictions: Array of predicted values
        measurements: Array of measured values

    Returns:
        MAE
    """
    return np.mean(np.abs(predictions - measurements))

def calculate_relative_errors(predictions: np.ndarray, measurements: np.ndarray) -> np.ndarray:
    """
    Calculate relative errors for each prediction-measurement pair.

    Args:
        predictions: Array of predicted values
        measurements: Array of measured values

    Returns:
        Array of relative errors (as percentages)
    """
    return ((predictions - measurements) / measurements) * 100

def calculate_chi_squared(predictions: np.ndarray,
                          measurements: np.ndarray,
                          uncertainties: np.ndarray) -> Tuple[float, float]:
    """
    Calculate chi-squared statistic and reduced chi-squared.

    Args:
        predictions: Array of predicted values
        measurements: Array of measured values
        uncertainties: Array of measurement uncertainties (1σ)

    Returns:
        (chi_squared, reduced_chi_squared)
    """
    # Avoid division by zero
    valid_mask = uncertainties > 0
    predictions_valid = predictions[valid_mask]
    measurements_valid = measurements[valid_mask]
    uncertainties_valid = uncertainties[valid_mask]

    residuals = predictions_valid - measurements_valid
    chi_squared = np.sum((residuals / uncertainties_valid)**2)

    n_dof = len(predictions_valid)  # degrees of freedom
    reduced_chi_squared = chi_squared / n_dof if n_dof > 0 else np.inf

    return chi_squared, reduced_chi_squared

# ==============================================================================
# RESIDUAL ANALYSIS
# ==============================================================================

def analyze_residuals(predictions: np.ndarray,
                      measurements: np.ndarray,
                      labels: List[str] = None) -> Dict:
    """
    Comprehensive residual analysis.

    Args:
        predictions: Array of predicted values
        measurements: Array of measured values
        labels: Optional labels for each data point

    Returns:
        Dictionary with residual statistics
    """
    residuals = predictions - measurements
    relative_errors = calculate_relative_errors(predictions, measurements)

    analysis = {
        "n_points": len(residuals),
        "rms_error": calculate_rms_error(predictions, measurements),
        "mean_absolute_error": calculate_mean_absolute_error(predictions, measurements),
        "mean_residual": np.mean(residuals),
        "std_residual": np.std(residuals),
        "max_residual": np.max(np.abs(residuals)),
        "mean_relative_error_pct": np.mean(np.abs(relative_errors)),
        "max_relative_error_pct": np.max(np.abs(relative_errors)),
        "residuals": residuals.tolist(),
        "relative_errors_pct": relative_errors.tolist()
    }

    if labels is not None:
        analysis["labels"] = labels

    return analysis

def print_residual_analysis(analysis: Dict):
    """
    Print formatted residual analysis report.

    Args:
        analysis: Dictionary from analyze_residuals()
    """
    print("\n" + "="*70)
    print("RESIDUAL ANALYSIS")
    print("="*70)
    print(f"Number of data points:    {analysis['n_points']}")
    print(f"RMS Error:                {analysis['rms_error']:.6f}")
    print(f"Mean Absolute Error:      {analysis['mean_absolute_error']:.6f}")
    print(f"Mean Residual:            {analysis['mean_residual']:.6f}")
    print(f"Std Dev of Residuals:     {analysis['std_residual']:.6f}")
    print(f"Maximum Residual:         {analysis['max_residual']:.6f}")
    print(f"\nMean Relative Error:      {analysis['mean_relative_error_pct']:.4f}%")
    print(f"Max Relative Error:       {analysis['max_relative_error_pct']:.4f}%")
    print("="*70 + "\n")

# ==============================================================================
# COMPARISON BETWEEN MODELS
# ==============================================================================

def compare_models(predictions_awut: np.ndarray,
                   predictions_other: np.ndarray,
                   measurements: np.ndarray,
                   other_model_name: str = "Other Model") -> Dict:
    """
    Compare AWUT predictions with another model (SM, MOND, ΛCDM, etc.).

    Args:
        predictions_awut: AWUT predicted values
        predictions_other: Other model predicted values
        measurements: Experimental measurements
        other_model_name: Name of the other model

    Returns:
        Dictionary with comparison statistics
    """
    rms_awut = calculate_rms_error(predictions_awut, measurements)
    rms_other = calculate_rms_error(predictions_other, measurements)

    mae_awut = calculate_mean_absolute_error(predictions_awut, measurements)
    mae_other = calculate_mean_absolute_error(predictions_other, measurements)

    improvement_rms = rms_other / rms_awut if rms_awut > 0 else np.inf
    improvement_mae = mae_other / mae_awut if mae_awut > 0 else np.inf

    comparison = {
        "awut_rms_error": rms_awut,
        f"{other_model_name.lower().replace(' ', '_')}_rms_error": rms_other,
        "rms_improvement_factor": improvement_rms,
        "awut_mae": mae_awut,
        f"{other_model_name.lower().replace(' ', '_')}_mae": mae_other,
        "mae_improvement_factor": improvement_mae,
        "better_model": "AWUT" if rms_awut < rms_other else other_model_name
    }

    return comparison

def print_model_comparison(comparison: Dict, model_name: str = "Other Model"):
    """
    Print formatted model comparison report.

    Args:
        comparison: Dictionary from compare_models()
        model_name: Name of the other model
    """
    print("\n" + "="*70)
    print(f"MODEL COMPARISON: AWUT vs {model_name}")
    print("="*70)
    print(f"AWUT RMS Error:           {comparison['awut_rms_error']:.6f}")
    print(f"{model_name} RMS Error:    {comparison[f'{model_name.lower().replace(' ', '_')}_rms_error']:.6f}")
    print(f"RMS Improvement Factor:   {comparison['rms_improvement_factor']:.2f}x")
    print(f"\nAWUT MAE:                 {comparison['awut_mae']:.6f}")
    print(f"{model_name} MAE:          {comparison[f'{model_name.lower().replace(' ', '_')}_mae']:.6f}")
    print(f"MAE Improvement Factor:   {comparison['mae_improvement_factor']:.2f}x")
    print(f"\nBetter Model:             {comparison['better_model']}")
    print("="*70 + "\n")

# ==============================================================================
# DATA EXPORT
# ==============================================================================

def save_error_analysis_json(analysis: Dict, filename: str):
    """
    Save error analysis to JSON file.

    Args:
        analysis: Dictionary from analyze_residuals()
        filename: Output filename
    """
    # Convert numpy types to native Python types
    json_analysis = {}
    for key, value in analysis.items():
        if isinstance(value, (np.float64, np.float32)):
            json_analysis[key] = float(value)
        elif isinstance(value, (np.int64, np.int32)):
            json_analysis[key] = int(value)
        elif isinstance(value, np.ndarray):
            json_analysis[key] = value.tolist()
        else:
            json_analysis[key] = value

    with open(filename, 'w') as f:
        json.dump(json_analysis, f, indent=2)

    print(f"✓ Error analysis saved to {filename}")

# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def quick_error_summary(predictions: np.ndarray,
                        measurements: np.ndarray,
                        name: str = "Observable") -> None:
    """
    Quick one-line error summary for debugging.

    Args:
        predictions: Array of predictions
        measurements: Array of measurements
        name: Name of the observable
    """
    rms = calculate_rms_error(predictions, measurements)
    mae = calculate_mean_absolute_error(predictions, measurements)
    mean_rel_err = np.mean(np.abs(calculate_relative_errors(predictions, measurements)))

    print(f"{name}: RMS={rms:.4f}, MAE={mae:.4f}, Mean Rel Err={mean_rel_err:.4f}%")

# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == "__main__":
    # Example: Nuclear binding energies
    print("Example: Nuclear Binding Energy Analysis\n")

    # Simulated data
    nuclei = ["He-4", "O-16", "Ca-40", "Fe-56", "Pb-208"]
    measurements = np.array([28.30, 127.62, 342.05, 492.25, 1636.44])  # MeV
    predictions_awut = np.array([28.25, 127.70, 341.80, 492.50, 1636.20])
    predictions_sm = np.array([28.10, 127.50, 342.30, 492.00, 1637.00])

    # Residual analysis
    analysis = analyze_residuals(predictions_awut, measurements, nuclei)
    print_residual_analysis(analysis)

    # Model comparison
    comparison = compare_models(predictions_awut, predictions_sm, measurements, "Standard Model")
    print_model_comparison(comparison, "Standard Model")

    # Quick summary
    quick_error_summary(predictions_awut, measurements, "AWUT Nuclear Binding")
