"""
AWUT Scientific Testbed - Utilities Module

This package provides core utilities for the AWUT testbed:
  - awut_constants: The 4 primitives and derived constants
  - comparison_tools: Compare AWUT vs experimental measurements
  - error_analysis: Statistical error analysis tools
"""

from .awut_constants import (
    ell_PS, tau_PS, f_Red, f_Blue,
    E_tri, Theta_278, eta, Pi_local,
    m_p_m_e_AWUT, print_primitives
)

from .comparison_tools import (
    compare_values,
    print_comparison_table,
    print_summary_table,
    save_comparison_json
)

from .error_analysis import (
    calculate_rms_error,
    analyze_residuals,
    print_residual_analysis,
    compare_models
)

__all__ = [
    # Constants
    'ell_PS', 'tau_PS', 'f_Red', 'f_Blue',
    'E_tri', 'Theta_278', 'eta', 'Pi_local',
    'm_p_m_e_AWUT', 'print_primitives',

    # Comparison tools
    'compare_values', 'print_comparison_table',
    'print_summary_table', 'save_comparison_json',

    # Error analysis
    'calculate_rms_error', 'analyze_residuals',
    'print_residual_analysis', 'compare_models'
]
