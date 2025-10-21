Material for the Molecular Dynamics (MD) simulations exercise in the Protein Science course.

> Open the ```MD_Protein_Science.ipynb``` and read its contents before the exercise!

# Installing conda environment

In order to run the exercise, we need a correct Python environment that is based on Python 3, and that contains the following packages:

- MDTraj
- Numpy
- Matplotlib

First, try running the following in terminal:

```conda activate MDsims```

If the command throws an error, we need to install the environment ourselves. The installation is handled by the file ```envs.yml```. Run the following commands:

```conda env create -f envs.yml```

(respond ```y``` where necessary)

```conda activate MDsims```

The Notebook can be opened using the following command:

```jupyter-lab MD_Protein_Science.ipynb```

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

