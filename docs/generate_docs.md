# 📚 Documentation Generation Guide

This project uses [Sphinx](https://www.sphinx-doc.org/) to generate HTML documentation from Python docstrings.

---

## ⚙️ Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Generate `.rst` Files (Optional)

If you want to regenerate the `.rst` files automatically from your codebase, use:

```bash
sphinx-apidoc -o docs/source/ task_manager/
```

> Replace `task_manager/` with the root folder of your source code, if different.  
> This will generate or update `.rst` files like `modules.rst`, `core.rst`, etc.

---

## 🚀 Build HTML Documentation

### On Windows:

```bash
cd docs
make.bat html
```

### On macOS / Linux:

```bash
cd docs
make html
```

---

## 📂 Output

The generated documentation will be located at:

```
docs/build/html/index.html
```

Open this file in your browser to view the documentation locally.

---

## 🚫 Do Not Commit

Avoid committing the following:

- `docs/build/` – This is a generated folder and should be added to `.gitignore`
- Any temporary or cache files (e.g. `__pycache__`, `.pyc` files)

---

## 📁 Project Structure (Relevant to Docs)

```
docs/
├── build/            ← Generated output (ignored in Git)
├── source/           ← Main Sphinx source files
│   ├── conf.py       ← Sphinx configuration
│   ├── index.rst     ← Main index file
│   ├── *.rst         ← Module-level docs (auto or manually written)
│   ├── _static/      ← Optional custom styles, images
│   └── _templates/   ← Optional HTML templates
```

---

## 💡 Tip

If Sphinx can't find your modules (e.g. `routes`, `services`, etc.), make sure `conf.py` includes the correct path setup:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
```

This ensures that Sphinx can import your code correctly during the build process.
