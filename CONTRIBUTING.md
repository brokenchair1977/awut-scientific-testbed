# Contributing to AWUT Scientific Testbed

Thank you for considering contributing to the AWUT testbed! This document provides guidelines for contributions.

---

## **How to Contribute**

### **1. Reporting Bugs**

If you find a bug:
- Check if it's already reported in [Issues](https://github.com/yourusername/awut-scientific-testbed/issues)
- If not, open a new issue with:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and OS
  - Full error traceback

### **2. Suggesting Enhancements**

For feature requests or improvements:
- Open an issue with the `enhancement` label
- Describe the proposed feature
- Explain why it would be useful
- Provide example use cases

### **3. Contributing Code**

#### **Process:**

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/awut-scientific-testbed.git
   cd awut-scientific-testbed
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

---

## **Code Style Guidelines**

### **Python Style**

Follow PEP 8 with these specifics:

- **Line length:** 100 characters max
- **Indentation:** 4 spaces (no tabs)
- **Docstrings:** Use triple quotes `"""` for all functions and classes
- **Type hints:** Encouraged but not required

**Example:**

```python
def calculate_mass_ratio(f_blue: float, f_red: float) -> float:
    """
    Calculate mass ratio from frequency ratio.

    Args:
        f_blue: Blue bubble frequency in Hz
        f_red: Red bubble frequency in Hz

    Returns:
        Mass ratio (dimensionless)
    """
    return (f_blue / f_red) ** 2
```

### **Formatting Tools**

Use `black` for automatic formatting:

```bash
pip install black
black scripts/ tests/
```

### **Naming Conventions**

- **Variables:** `snake_case`
- **Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`

---

## **Testing Guidelines**

### **Writing Tests**

All new functionality must include tests.

**Test file structure:**

```python
import pytest

@pytest.mark.unit
def test_basic_calculation():
    """Test that basic calculation works correctly."""
    result = my_function(input_value)
    assert result == expected_value

@pytest.mark.integration
def test_full_derivation():
    """Test that full derivation script runs."""
    # Integration test code
```

### **Running Tests**

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/ -m "unit"

# Run only integration tests
pytest tests/ -m "integration"

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

### **Test Coverage**

Aim for:
- New functions: 90%+ coverage
- Bug fixes: Test that reproduces the bug

---

## **Documentation Guidelines**

### **Code Documentation**

Every function should have a docstring:

```python
def derive_observable(primA, primB, primC):
    """
    Derive an observable from AWUT primitives.

    This function calculates the observable using geometric
    resonance from the three primitives provided.

    Args:
        primA (float): First primitive value
        primB (float): Second primitive value
        primC (float): Third primitive value

    Returns:
        float: Derived observable value

    Raises:
        ValueError: If any primitive is negative
    """
    if primA < 0 or primB < 0 or primC < 0:
        raise ValueError("All primitives must be positive")

    return (primA * primB) / primC
```

### **Markdown Documentation**

When adding to `docs/`:
- Use clear headings
- Include examples
- Add links to related docs
- Keep language accessible

---

## **Adding New Derivations**

To add a new observable derivation:

### **1. Create the Script**

Create `scripts/06_your_observable.py`:

```python
#!/usr/bin/env python3
"""
AWUT Derivation: Your Observable

Brief description of what this derives.

Key Formula:
    observable = formula_here

Expected Result:
    AWUT:     value
    Measured: value
    Error:    percentage

Status: ✓ PASS or ✗ FAIL
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.utils.awut_constants import ell_PS, tau_PS, f_Red, f_Blue
from scripts.utils.comparison_tools import compare_values, print_comparison_table

def derive_your_observable():
    """Derive the observable from AWUT primitives."""
    # Your calculation here
    return calculated_value

def main():
    """Main execution function."""
    awut_value = derive_your_observable()

    # Get measured value (add to data/ if needed)
    measured_value = get_measured_value()

    # Compare
    result = compare_values(
        observable_name="Your Observable",
        awut_value=awut_value,
        measured_value=measured_value,
        units="appropriate_units",
        tolerance_pct=0.1
    )

    print_comparison_table(result)

    return result['status'] == 'PASS'

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

### **2. Add Tests**

Create `tests/test_your_observable.py`:

```python
import pytest

@pytest.mark.unit
def test_your_observable_within_tolerance(tolerance_values):
    """Test that AWUT prediction is within tolerance."""
    # Import your derivation function
    awut_value = derive_your_observable()
    measured_value = get_measured_value()

    error_pct = abs(awut_value - measured_value) / measured_value * 100

    assert error_pct < tolerance_values['your_observable_pct']
```

### **3. Add Data**

If needed, add measured values to `data/`:
- `data/your_data_source.csv` for datasets
- `data/your_data_source.py` for Python dictionaries
- `data/your_data_source.json` for JSON format

### **4. Update Documentation**

- Add entry to `docs/AWUT_ontology.md`
- Update `README.md` with new observable
- Add notebook if complex: `notebooks/your_observable.ipynb`

---

## **Proposing Theoretical Changes**

AWUT is a scientific theory. Changes to core theory require:

### **1. Mathematical Justification**

- Show derivation from the 4 primitives
- Explain physical interpretation
- Compare to existing formulations

### **2. Experimental Support**

- Cite published measurements
- Show error analysis
- Compare to Standard Model

### **3. Falsifiability**

- Provide testable predictions
- Specify what would falsify your modification
- Suggest experimental tests

### **4. Community Discussion**

Open a GitHub Discussion before large theoretical changes:
- Title: "Theory Proposal: [Brief Description]"
- Include: Motivation, derivation, predictions, falsification criteria

---

## **Commit Message Guidelines**

Use clear, descriptive commit messages:

**Format:**
```
Type: Brief description (50 chars max)

Longer explanation if needed (wrap at 72 chars).
Include motivation and context.

Fixes #123
```

**Types:**
- `Add:` New feature or file
- `Fix:` Bug fix
- `Refactor:` Code restructuring
- `Docs:` Documentation only
- `Test:` Adding or updating tests
- `Style:` Formatting changes

**Examples:**

```
Add: Derivation for neutron lifetime

Implements AWUT derivation of neutron beta decay lifetime from
the 4 primitives. Compares to PDG 2024 measurement.

Closes #45
```

```
Fix: Nuclear binding wobble calculation

Corrected sign error in pairing term that was causing ~10%
error for odd-odd nuclei.

Fixes #67
```

---

## **Pull Request Checklist**

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] New functionality includes tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main branch
- [ ] PR description explains changes

---

## **Getting Help**

If you need help contributing:

- **GitHub Discussions:** For general questions
- **GitHub Issues:** For specific bugs or features
- **Documentation:** Check `docs/` for detailed info

---

## **Code of Conduct**

### **Our Pledge**

We are committed to providing a welcoming and respectful environment for all contributors.

### **Expected Behavior**

- Be respectful and considerate
- Welcome newcomers
- Focus on constructive criticism
- Accept feedback gracefully

### **Unacceptable Behavior**

- Personal attacks or insults
- Harassment of any kind
- Publishing others' private information
- Other conduct that would be inappropriate in a professional setting

### **Enforcement**

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to [maintainer email]

---

## **License**

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AWUT!**
