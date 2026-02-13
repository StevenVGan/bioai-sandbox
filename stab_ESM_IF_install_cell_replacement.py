# Replace the "PRELIMINARY OPERATIONS: Install dependencies" cell with this content.
# Copy everything below the line into the cell in Colab.

# ========== PASTE FROM HERE ==========

#@title PRELIMINARY OPERATIONS: Install dependencies

#@markdown Run the cell to install all the extra necessaries packages (~15 mins), including:
#@markdown - ESM-IF (library and parameters)
#@markdown - Torch libraries: torch-scatter,-sparse,-cluster,spline-conv,-geometric
#@markdown - Python libraries: biopython, biotite

%%time
import os,time,subprocess,re,sys,shutil
from google.colab import files
import torch
import numpy as np
import pandas as pd

def format_pytorch_version(version):
  return version.split('+')[0]

def format_cuda_version(version):
  return 'cu' + version.replace('.', '')

TORCH_version = torch.__version__
TORCH = format_pytorch_version(TORCH_version)
CUDA_version = torch.version.cuda
CUDA = format_cuda_version(CUDA_version)

IF_model_name = "esm_if1_gvp4_t16_142M_UR50.pt"

if not os.path.isfile(IF_model_name):
  # download esmfold params
  os.system("apt-get install aria2 -qq")
  os.system(f"aria2c -x 16 https://sid.erda.dk/share_redirect/eIZVVNEd8B --out={IF_model_name} &")

  if not os.path.isfile("finished_install"):
    # install libs (use kernel's Python - os.system installs to wrong env with condacolab)
    print("installing libs...")
    pip_install = [sys.executable, "-m", "pip", "install"]
    subprocess.run(pip_install + ["torch_geometric"], check=True)
    print('...finished torch dependencies')
    subprocess.run(pip_install + ["biopython", "biotite"], check=True)
    subprocess.run(pip_install + ["git+https://github.com/matteo-cagiada/esm.git"], check=True)
    open("finished_install", "w").close()

    #wait for Params to finish downloading...
    while not os.path.isfile(IF_model_name):
      time.sleep(5)
    if os.path.isfile(f"{IF_model_name}.aria2"):
      print("downloading params...")
    while os.path.isfile(f"{IF_model_name}.aria2"):
      time.sleep(5)

## Ensure deps in kernel's Python (runs every time, idempotent)
subprocess.run([sys.executable, "-m", "pip", "install", "torch_geometric", "biopython", "biotite", "git+https://github.com/matteo-cagiada/esm.git"])

import esm

from esm.inverse_folding.util import load_structure, extract_coords_from_structure,CoordBatchConverter
from esm.inverse_folding.multichain_util import extract_coords_from_complex,_concatenate_coords,load_complex_coords


print("importing the model")

model, alphabet = esm.pretrained.load_model_and_alphabet(IF_model_name)
model.eval().cuda().requires_grad_(False)

print("--> Installations succeeded")
