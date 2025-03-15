 # Linting Guidelines
## Selected Linter: Flake8
For this project, we have chosen Flake8 as the 
linter due to its effectiveness in enforcing code quality and consistency
### Why Flake8?
* PEP 8 Compliance – Ensures the code follows Python's official style guide.
* Catches Errors Early – Identifies syntax issues, unused imports, and bad formatting.
* Lightweight & Fast – Minimal overhead, making it suitable for large projects
* Highly Configurable – Supports rule customization and per-file exceptions.
* CI/CD Friendly – Can be used in automated pipelines to enforce coding standards.
## Basic Rules and Explanation
Flake8 checks for multiple code quality issues, including:
###  1.Formatting Issues (PEP 8)
* E501: Line too long (>79 characters).
* E302: Expected 2 blank lines before top-level function or class.
### 2. Syntax & Logical Errors
* F401: Imported but unused module.
* F821: Undefined variable.
* F841: Local variable assigned but never used.

### 3. Code Complexity
* C901: Function is too complex (Cyclomatic Complexity check).

#### Note: We allow exceptions in specific files (e.g., __init__.py for F401 warnings).
## Running Flake8
## Run Flake8 Manually
To lint all Python files in the project:

``` 
flake8
```
To check a specific file:
```
flake8 path/to/file.py
```

## MyPy – Static Type Checking
Along with Flake8, we also use Mypy for static type checking. Mypy helps detect type-related bugs before runtime.
### Running Mypy
Run Mypy on the entire project:
```
mypy .
```
Check a specific file:
```
mypy path/to/file.py
```
## Run Both (Flake8 & Mypy)
Instead of running Flake8 and Mypy separately, you can run both at once using the script:
```
python scripts/check_code.py
```
## Pre-Commit Hooks
This project includes pre-commit hooks to enforce code quality before commits.

* Pre-commit hooks run Flake8 automatically when making a commit.
* If any style or syntax issues are found, the commit is blocked until the issues are fixed.

To manually trigger the pre-commit checks, run:
```
pre-commit run --all-files
```

## CI Integration – GitHub Actions
Code quality is enforced automatically through GitHub Actions.

* On every push to main and on pull requests, Flake8 checks are executed.
* If any issues are found, the pipeline fails, ensuring only clean code is merged.