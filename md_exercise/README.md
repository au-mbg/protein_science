Material for the Molecular Dynamics (MD) simulations exercise in the Protein Science course.

Read and execute steps in this document before proceeding to the exercises.

# Downloading the git repository to desktop

Open a Terminal window by right-clicking on the desktop and selecting "Open Terminal."

```cd ~/Desktop```

```git clone https://github.com/au-mbg/protein_science.git``` 

```cd protein_science/md_exercise```

# Activating conda environment to run Jupyter Notebook

```module load miniconda3```

```conda activate /sw/common/miniconda3/envs/MD```

You should see ```(MD)``` pop up at the beginning of your terminal line. This means that you are now in the conda environment called ```MD```.

```jupyter-lab MD_Protein_Science.ipynb```

If you want to exit the notebook for any reason, in the terminal window press ```CTRL+C```. You will be asked if you want it to shut down (answer ```y```).

# Opening PyMOL

Open a new tab in the Terminal by pressing CTRL+SHIFT+t. 

```pymol```

# File structure

The folder **Insulin\_solvent** contains the simulation systems: insulin (protein) + solvent (water and ions).

There are two sets of simulations:

1) **INS1_solvent**

	- coordinate file: INS1_solvent.pdb

	- trajectory file: INS1_solvent.xtc

2) **INS2_solvent**

	- coordinate file: INS2_solvent.pdb
	
	- trajectory file: INS2_solvent.xtc

# Ending the exercise

After you are done with the exercises, log out of your account. **Do NOT turn off the machines!**
