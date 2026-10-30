# Material for the Molecular Dynamics (MD) simulations exercise in the Protein Science course

The exercise has two parts:

1) **Visualisation**: you look at the simulations in **PyMOL**. For this, you need the simulation files, which you download in step 2 below.
2) **Analysis**: you analyse the simulations with Python, **directly on the exercise web page**. Nothing needs to be installed.

The instructions for both parts are on the exercise web page: **https://au-mbg.github.io/protein_science/md_exercise/**

Follow the steps below before you start.

# Step 1: Open a terminal

The commands can be run in Terminal window.

Open a terminal by right-clicking on the desktop and selecting "Open Terminal" (or press CTRL+ALT+t).

# Step 2: Download the exercise files

Go to the Desktop folder:

```cd ~/Desktop```

Download (clone) the course repository from GitHub. This creates a folder called ```protein_science``` on your desktop:

```git clone https://github.com/au-mbg/protein_science.git```

Go into the folder of the MD exercise:

```cd protein_science/md_exercise```

Check that you are in the right folder:

```ls```

You should see, among others, the folder ```Insulin_solvent``` and this file, ```README.md```.

**If the folder ```protein_science``` already exists**, ```git clone``` gives an error. Instead, go into the folder and update it:

```cd ~/Desktop/protein_science/md_exercise```

```git pull```

## File structure

The folder **Insulin\_solvent** contains the simulation systems: insulin (protein) + solvent (water and ions).

There are two sets of simulations:

1) **INS1_solvent**

	- coordinate file: INS1_solvent.pdb

	- trajectory file: INS1_solvent.xtc

2) **INS2_solvent**

	- coordinate file: INS2_solvent.pdb
	
	- trajectory file: INS2_solvent.xtc

# Step 3: Open the exercise web page

Open the link: https://au-mbg.github.io/protein_science/md_exercise/

The web page has three parts, listed in the menu on the left:

- **Overview**: the aims of the exercise
- **1) Visualisation**: the PyMOL part
- **2) Analysis**: the Python part.

The Python code runs on the web page itself. Click **Run Code** on each code box, in order from top to bottom. The first time, Python needs up to a minute to load in the browser.

Keep the web page open during the whole exercise.

# Step 4: Open PyMOL

In the same terminal (you must still be in the ```md_exercise``` folder; check with ```ls``` as in step 2), run:

```pymol```

PyMOL should be started from the ```md_exercise``` folder, because the commands in the exercise (e.g. ```load Insulin_solvent/INS1_solvent.pdb```) load the files from there.

PyMOL commands are typed into the command line of the PyMOL window (the line starting with ```PyMOL>```), not into the terminal.

# Alternative: the exercise as a Jupyter Notebook

The same exercise is also available as a Jupyter Notebook (```MD_Protein_Science.ipynb```). Use it only if you are told to.

Open a new tab in the terminal by pressing CTRL+SHIFT+t, go to the ```md_exercise``` folder, and activate the conda environment:

```cd ~/Desktop/protein_science/md_exercise```

```module load miniconda3```

```conda activate /sw/common/miniconda3/envs/MD```

You should see ```(MD)``` pop up at the beginning of your terminal line. This means that you are now in the conda environment called ```MD```.

```jupyter-lab MD_Protein_Science.ipynb```

If you want to exit the notebook for any reason, in the terminal window press ```CTRL+C```. You will be asked if you want it to shut down (answer ```y```).

# Ending the exercise

After you are done with the exercises, log out of your account. **Do NOT turn off the machines!**
