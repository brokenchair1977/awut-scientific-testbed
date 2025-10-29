# AWUT Testbed - Quick Start Guide

Get up and running with the AWUT scientific testbed in 5 minutes.

---

## **Prerequisites**

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

---

## **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/awut-scientific-testbed.git
cd awut-scientific-testbed
```

### **2. Create a Virtual Environment (Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **Running Your First Derivation**

### **Option 1: Proton-Electron Mass Ratio**

```bash
python scripts/01_proton_electron_mass_ratio.py
```

**Expected output:**
```
THE 4 PRIMITIVES (All derivations use ONLY these inputs)
======================================================================
Planck length (ℓ_PS):    1.616e-35 m
Planck time (τ_PS):      5.390e-44 s
Red frequency (f_Red):   9.220e+09 Hz (9.22 GHz)
Blue frequency (f_Blue): 1.237e+10 Hz (12.37 GHz)
======================================================================

AWUT DERIVATION: PROTON-ELECTRON MASS RATIO
======================================================================
...
AWUT Prediction:    1834.800000
Measured Value:     1836.152673
Relative Error:     0.074%

Status: ✓ PASS (tolerance: 0.1%)
```

### **Option 2: Muon g-2 Anomaly**

```bash
python scripts/02_muon_g2_anomaly.py
```

### **Option 3: All Derivations**

Run all 5 main derivations:

```bash
for script in scripts/0*.py; do
    echo "Running $script..."
    python "$script"
    echo
done
```

---

## **Running Tests**

### **Run All Tests**

```bash
pytest tests/ -v
```

### **Run Specific Test Module**

```bash
pytest tests/test_proton_electron.py -v
```

### **Run Tests with Coverage**

```bash
pytest tests/ --cov=scripts --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

---

## **Understanding the Results**

Each script outputs:

1. **The 4 Primitives** - The fundamental inputs
2. **Step-by-step Derivation** - How the observable is calculated
3. **Comparison Table** - AWUT vs measured value
4. **Physical Interpretation** - What it means
5. **Saved Results** - JSON files in `outputs/` directory

### **Key Metrics:**

| Observable | Error | Status |
|-----------|-------|--------|
| Proton-electron ratio | 0.074% | ✓ PASS |
| Muon g-2 | 0.6 ppb | ✓ PASS |
| Lepton masses | 0.01% | ✓ PASS |
| Nuclear binding | 0.252 MeV RMS | ✓ PASS |
| Galaxy rotation | 1.9 km/s RMS | ✓ PASS |

---

## **Exploring the Code**

### **Directory Structure**

```
awut-scientific-testbed/
├── scripts/              # Main derivation scripts
│   ├── 01_proton_electron_mass_ratio.py
│   ├── 02_muon_g2_anomaly.py
│   ├── 03_lepton_mass_ratios.py
│   ├── 04_nuclear_binding_energies.py
│   ├── 05_galaxy_rotation_curves.py
│   └── utils/           # Shared utilities
│       ├── awut_constants.py
│       ├── comparison_tools.py
│       └── error_analysis.py
├── tests/               # Unit tests
├── data/                # Experimental measurements
├── docs/                # Documentation
├── notebooks/           # Jupyter tutorials
└── outputs/             # Generated results
```

### **Key Files:**

- **`scripts/utils/awut_constants.py`** - Defines the 4 primitives
- **`data/codata_2018_values.py`** - CODATA measured values
- **`docs/AWUT_ontology.md`** - Core concepts explained
- **`docs/falsification_criteria.md`** - How to test/disprove AWUT

---

## **Interactive Tutorials**

Launch Jupyter notebooks for step-by-step tutorials:

```bash
jupyter notebook notebooks/
```

Recommended order:
1. `01_intro_awut_primitives.ipynb` - Introduction to the 4 primitives
2. `02_derivation_walkthrough.ipynb` - Detailed walkthrough of derivations
3. `03_comparison_to_sm.ipynb` - Compare AWUT to Standard Model
4. `04_falsification_tests.ipynb` - Testable predictions

---

## **Modifying the Code**

### **Changing a Primitive**

Edit `scripts/utils/awut_constants.py`:

```python
# Try different Red frequency (hypothetical test)
f_Red = 9.5e9  # Was 9.22e9
```

Then re-run derivations to see how results change.

### **Adding a New Observable**

1. Create `scripts/06_my_new_observable.py`
2. Import utilities:
   ```python
   from scripts.utils.awut_constants import ell_PS, tau_PS, f_Red, f_Blue
   from scripts.utils.comparison_tools import compare_values
   ```
3. Derive your observable
4. Compare with measured value
5. Add tests in `tests/test_my_new_observable.py`

---

## **Troubleshooting**

### **Issue: ImportError when running scripts**

**Solution:** Run scripts from the repository root:
```bash
cd awut-scientific-testbed
python scripts/01_proton_electron_mass_ratio.py
```

### **Issue: ModuleNotFoundError: No module named 'numpy'**

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### **Issue: Tests fail with "file not found"**

**Solution:** Ensure you're in the repository root:
```bash
cd awut-scientific-testbed
pytest tests/
```

---

## **Next Steps**

1. **Read the documentation:**
   - `docs/AWUT_ontology.md` - Core concepts
   - `docs/physics_background.md` - Beginner-friendly explanation
   - `docs/falsification_criteria.md` - How to test AWUT

2. **Explore the notebooks:**
   ```bash
   jupyter notebook notebooks/
   ```

3. **Run all tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Contribute:**
   - See `CONTRIBUTING.md` for guidelines
   - Open issues on GitHub
   - Submit pull requests with improvements

---

## **Getting Help**

- **Documentation:** Check `docs/` directory
- **Issues:** https://github.com/yourusername/awut-scientific-testbed/issues
- **Discussions:** https://github.com/yourusername/awut-scientific-testbed/discussions

---

## **Quick Command Reference**

```bash
# Install dependencies
pip install -r requirements.txt

# Run single derivation
python scripts/01_proton_electron_mass_ratio.py

# Run all derivations
for script in scripts/0*.py; do python "$script"; done

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=scripts

# Launch Jupyter notebooks
jupyter notebook notebooks/

# Format code (if black installed)
black scripts/ tests/

# Type check (if mypy installed)
mypy scripts/
```

---

**Welcome to the AWUT testbed! Let's test some physics.**
