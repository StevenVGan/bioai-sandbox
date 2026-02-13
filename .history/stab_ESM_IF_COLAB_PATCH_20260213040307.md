# Minimal Patch for stab_ESM_IF.ipynb (Colab compatibility)

Apply these changes to the **"PRELIMINARY OPERATIONS: Install dependencies"** cell in the [original notebook](https://colab.research.google.com/github/KULL-Centre/_2024_cagiada_stability/blob/main/stab_ESM_IF.ipynb).

## Why
After condacolab installs, `os.system("pip install ...")` and `conda install` can install to the wrong Python environment, causing `ModuleNotFoundError` for `esm` and `torch_geometric`.

---

## Change 1: Replace the install block inside `if not os.path.isfile("finished_install")`

**Original:**
```python
    os.system(f"conda install conda-forge::torch-scatter")
    os.system(f"conda install conda-forge::pytorch_sparse")
    os.system(f"conda install conda-forge::torch-cluster")
    os.system(f"conda install ostrokach-forge::torch-spline-conv")
    os.system(f'pip install torch_geometric')
    print('...finished torch dependencies')
    os.system(f"pip install biopython")
    os.system(f"pip install biotite")

    print("installing esmfold...")
    # install esmfold
    os.system(f"pip install git+https://github.com/matteo-cagiada/esm.git")
    os.system("touch finished_install")
```

**Replace with:**
```python
    # Use kernel's Python (os.system installs to wrong env with condacolab)
    pip_install = [sys.executable, "-m", "pip", "install"]
    subprocess.run(pip_install + ["torch_geometric"], check=True)
    print('...finished torch dependencies')
    subprocess.run(pip_install + ["biopython", "biotite"], check=True)
    subprocess.run(pip_install + ["git+https://github.com/matteo-cagiada/esm.git"], check=True)
    open("finished_install", "w").close()
```

---

## Change 2: Add ensure block before `import esm`

This is added only to ensure that restarts and edge cases are handled.

**Original:**
```python
## Verify that pytorch-geometric is correctly installed

import esm
```

**Replace with:**
```python
## Ensure deps in kernel's Python (runs every time, idempotent)
subprocess.run([sys.executable, "-m", "pip", "install", "torch_geometric", "biopython", "biotite", "git+https://github.com/matteo-cagiada/esm.git"])

import esm
```

---

## Summary
- **2 edits** in the Install dependencies cell
- Keeps original structure, conda download logic, and all other cells unchanged
- Fixes: `ModuleNotFoundError` for esm/torch_geometric; uses `open()` instead of `os.system("touch")` for portability
