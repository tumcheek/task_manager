import subprocess

subprocess.run(["flake8"])
subprocess.run(["mypy", "."])
