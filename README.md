Material for the Molecular Dynamics (MD) simulations exercise in the Protein Science course.

> Open the ```MD_Protein_Science.ipynb``` and read its contents before the exercise!

# Downloading the git repository to desktop

```git clone https://github.com/au-mbg/protein_science.git ~/Desktop/``` 

```cd ~/Desktop/protein_science```

# Activating conda environment to run Jupyter Notebook

```module load miniconda3```

```conda activate /sw/common/miniconda3/envs/MD```

You should see ```(MD)``` pop up at the beginning of your terminal line. This means that you are now in the conda environment called ```MD```.

```jupyter-lab MD_Protein_Science.ipynb```

If you want to exit the notebook for any reason, in the terminal window press ```CTRL+C```. You will be asked if you want it to shut down (answer ```y```).

# File structure

The two folders contain the same simulation runs, but with different atom selections:

1) Insulin\_w\_solvent: included protein + solvent
	- Insulin is centered in the middle of the simulation box

2) Insulin: only the protein

	- Insulin is centered in the middle of the simulation box, and its rotational and translational motions have been removed

There are two sets of simulations:

1) INS1

	- coordinate file: INS1.pdb

	- trajectory file: INS1.xtc

2) INS2

	- coordinate file: INS2.pdb
	
	- trajectory file: INS2.pdb

