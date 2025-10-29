"""
Pytest Configuration and Fixtures

Shared fixtures and configuration for all AWUT testbed tests.
"""

import pytest
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))

# ==============================================================================
# FIXTURES - CONSTANTS
# ==============================================================================

@pytest.fixture
def awut_primitives():
    """The 4 AWUT primitives."""
    from scripts.utils.awut_constants import ell_PS, tau_PS, f_Red, f_Blue
    return {
        'ell_PS': ell_PS,
        'tau_PS': tau_PS,
        'f_Red': f_Red,
        'f_Blue': f_Blue
    }

@pytest.fixture
def tolerance_values():
    """Standard tolerance values for tests."""
    return {
        'mass_ratio_pct': 0.1,          # 0.1% for proton-electron ratio
        'lepton_mass_pct': 0.01,        # 0.01% for lepton masses
        'muon_g2_ppb': 1.0,             # 1 ppb for muon g-2
        'nuclear_binding_MeV': 0.5,     # 0.5 MeV RMS for nuclear binding
        'galaxy_rotation_km_s': 5.0     # 5 km/s RMS for rotation curves
    }

# ==============================================================================
# FIXTURES - DATA
# ==============================================================================

@pytest.fixture
def codata_values():
    """CODATA 2018 recommended values."""
    import codata_2018_values as codata
    return codata

@pytest.fixture
def fermilab_data():
    """Fermilab muon g-2 measurement data."""
    import json
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'fermilab_muon_g2.json')
    with open(data_file, 'r') as f:
        return json.load(f)

# ==============================================================================
# FIXTURES - UTILITIES
# ==============================================================================

@pytest.fixture
def comparison_tools():
    """Comparison tools module."""
    from scripts.utils import comparison_tools
    return comparison_tools

@pytest.fixture
def error_analysis():
    """Error analysis module."""
    from scripts.utils import error_analysis
    return error_analysis

# ==============================================================================
# PYTEST CONFIGURATION
# ==============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
