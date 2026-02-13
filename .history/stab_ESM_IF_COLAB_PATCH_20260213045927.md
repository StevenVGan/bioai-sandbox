# Minimal Patch for stab_ESM_IF.ipynb - Colab compatibility

This patch changes the **"PRELIMINARY OPERATIONS: Install dependencies"** cell in the [original colab notebook](https://colab.research.google.com/github/KULL-Centre/_2024_cagiada_stability/blob/main/stab_ESM_IF.ipynb). It fixes `ModuleNotFoundError` for `esm` and `torch_geometric`.

## Why
After condacolab installs, `os.system("pip install ...")` and `conda install` can install to the wrong Python environment, causing `ModuleNotFoundError` for `esm` and `torch_geometric`.

---

## Notes before applying

**PRELIMINARY OPERATIONS: Install condalab** – This cell installs the correct Python environment for the notebook. If running this cell leads to a disconnect and reconnect, that is normal because there is a kernel restart at the end. If unsure, run the cell again; it should print `✨🍰✨ Everything looks OK!`

---

## IMPORTANT: Replace the install block in dependencies

In the following block **PRELIMINARY OPERATIONS: Install dependencies**, replace the install block inside `if not os.path.isfile("finished_install")` with the code below.

**Instructions:**
1. Double-click the cell to open the code editor.
2. Delete the original install block (from the first `os.system` through `os.system("touch finished_install")`). Keep the `print("installing libs...")` line above it.
3. Paste the new code block (**tab-indentation required**).
4. Run the cell.

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
    print("installing esmfold...")
    subprocess.run(pip_install + ["git+https://github.com/matteo-cagiada/esm.git"], check=True)
    open("finished_install", "w").close()
```

---

## Expected output of the patched cell

In the **PRELIMINARY OPERATIONS: Install dependencies** cell, when this patch runs successfully, you should see something like the following output:

```
installing libs...
...finished torch dependencies
installing esmfold...
importing the model
/usr/local/lib/python3.12/dist-packages/esm/pretrained.py:216: UserWarning: Regression weights not found, predicting contacts will not produce correct results.
  warnings.warn(
--> Installations succeeded
CPU times: user 12.1 s, sys: 2.81 s, total: 14.9 s
Wall time: 1min 2s
```

- The **Regression weights** warning is harmless (ESM-IF does not use contact prediction).
- Wall time becomes **faster than the expected 5–10 min** (e.g. ~1 min).

---

## Tested results

Validated with values based on the [spreadsheet](https://docs.google.com/spreadsheets/d/1YSJu_euKUw86p6bActGAkdPi9reAlioDhHiQMEwVjFA/edit?gid=0#gid=0):

| Input | ΔG (likelihoods sum) | ΔG (kcal/mol) |
|-------|----------------------|---------------|
| YP_009724390.1_ref_RBD_AF2 (AlphaFold2 model 4, rank 1) | 91.75509978423361 | 10.171060613370988 |
| YP_009724390.1_ref_RBD_SWISS (SWISS-MODEL) | 87.47504538903013 | 9.725362356565233 |

Both results closely match the original spreadsheet.