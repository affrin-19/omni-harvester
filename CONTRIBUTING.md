# Contributing to Omni-Harvester

We welcome engineering contributions, validation datasets, hardware characterization reports, and firmware improvements.

## Contribution Guidelines

1. **Bug Reports & Issues**: Open an issue detailing circuit conditions, component tolerances, or simulator discrepancies.
2. **Pull Requests**:
   - For hardware modifications: Provide revised SPICE netlists, simulation plots, and updated BOM references.
   - For firmware: Follow C++17/Embedded C guidelines, minimize RAM allocation, and verify zero heap fragmentation.
   - For physical modeling: Add unit tests under `tests/` validating your mathematical derivations.
3. **Commit Standards**: Use Conventional Commits (`feat(pmu): ...`, `fix(sim): ...`, `docs(bom): ...`).

## Local Development Workflow

```bash
# Clone the repository
git clone https://github.com/affrin-19/omni-harvester.git
cd omni-harvester

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install simulation and testing dependencies
pip install -r simulation/requirements.txt

# Run simulation test suite
pytest tests/ -v

# Generate physical benchmark curves
python simulation/plot_results.py
```
