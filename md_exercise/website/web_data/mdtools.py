"""Ready-made functions for the MD analysis exercise (web version of the insulin exercise).

Uses only numpy, so it runs in the browser. The results match mdtraj
(checked by SCRIPTS/validate_web_analysis.py in the course preparation folder).

    pdb_1 = load_pdb("INS1")            starting structure (one frame)
    t_1 = load_trajectory("INS1")       all frames; t_1.time is in ps
    ca = select(name="CA")              atom selection, as in PyMOL: chain, resnum, resname, name
    show_atoms(ca)                      print the selected atoms
    rmsd(t_1, reference=pdb_1, atoms=ca)
    rmsf(t_1, reference=pdb_1, atoms=ca)
    distance(t_1, atom_A, atom_B)
    residue_labels(ca)                  e.g. ["A1", "A2", ..., "B30"], for plot axes

All distances are in nm. Data files (INS1.npz, INS2.npz, atoms.csv) are read from the folder of this module.
"""
import csv
import os

import numpy as np

_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS = ("INS1", "INS2")


def _read_atoms():
    with open(os.path.join(_DIR, "atoms.csv"), newline="") as f:
        rows = list(csv.DictReader(f))
    return {
        "name": np.array([r["name"] for r in rows]),
        "element": np.array([r["element"] for r in rows]),
        "resname": np.array([r["resname"] for r in rows]),
        "resnum": np.array([int(r["resnum"]) for r in rows]),
        "chain": np.array([r["chain"] for r in rows]),
    }


_ATOMS = _read_atoms()
_N_ATOMS = len(_ATOMS["name"])
_N_RESIDUES = len(set(zip(_ATOMS["chain"], _ATOMS["resnum"])))


class Structure:
    """A single structure (the .pdb file): coordinates of all atoms."""

    def __init__(self, name, xyz):
        self.name = name
        self.xyz = xyz

    def __repr__(self):
        return f"<Structure {self.name}: {_N_ATOMS} atoms, {_N_RESIDUES} residues>"


class Trajectory:
    """An MD trajectory: coordinates of all atoms in every frame, and the time of each frame (ps)."""

    def __init__(self, name, xyz, time):
        self.name = name
        self.xyz = xyz
        self.time = time

    @property
    def n_frames(self):
        return len(self.xyz)

    def __repr__(self):
        return f"<Trajectory {self.name}: {self.n_frames} frames, {_N_ATOMS} atoms, {_N_RESIDUES} residues>"


class Selection:
    """A set of atoms, made with select()."""

    def __init__(self, indices, description):
        self.indices = np.asarray(indices, dtype=int)
        self.description = description

    def __len__(self):
        return len(self.indices)

    def __repr__(self):
        return f"<Selection {self.description}: {len(self)} atoms>"


def _load(name):
    if name not in SYSTEMS:
        raise ValueError(f"Unknown system {name!r}. Choose one of: {', '.join(SYSTEMS)}.")
    return np.load(os.path.join(_DIR, f"{name}.npz"))


def load_pdb(name):
    """Load the starting structure of a system, e.g. load_pdb("INS1")."""
    return Structure(name, _load(name)["structure"].astype(np.float64))


def load_trajectory(name):
    """Load the trajectory of a system, e.g. load_trajectory("INS1")."""
    data = _load(name)
    return Trajectory(name, data["xyz"], data["time"].astype(np.float64))


def select(chain=None, resnum=None, resname=None, name=None):
    """Select atoms, as in PyMOL. Each argument is one value or a list of values; all given ones must match.

    Examples: select(name="CA"), select(chain="B", resnum=1, name="N"), select(chain="B", resnum=[1, 2, 3])
    Residues are numbered within each chain, as in the PDB file and in PyMOL (A1-A21, B1-B30).
    """
    criteria = {"chain": chain, "resnum": resnum, "resname": resname, "name": name}
    mask = np.ones(_N_ATOMS, dtype=bool)
    used = []
    for key, value in criteria.items():
        if value is None:
            continue
        values = list(value) if isinstance(value, (list, tuple, range, np.ndarray)) else [value]
        mask &= np.isin(_ATOMS[key], values)
        used.append(f"{key}={value!r}")
    description = ", ".join(used) if used else "all atoms"
    if not mask.any():
        raise ValueError(f"No atoms match {description}. Check the spelling (atom names are in capitals, "
                         f"e.g. 'CA'; chains are 'A' and 'B') and the residue numbers (A1-A21, B1-B30).")
    return Selection(np.flatnonzero(mask), description)


def _label(i):
    return f"{_ATOMS['chain'][i]}{_ATOMS['resnum'][i]}"


def show_atoms(atoms):
    """Print the selected atoms: chain + residue number, residue name, atom name."""
    _check_selection(atoms, "atoms")
    print(f"{len(atoms)} atom(s) selected ({atoms.description}):")
    for i in atoms.indices[:20]:
        print(f"  {_label(i):>4} {_ATOMS['resname'][i]} {_ATOMS['name'][i]}")
    if len(atoms) > 20:
        print(f"  ... and {len(atoms) - 20} more")


def residue_labels(atoms):
    """Chain + residue number of each selected atom, e.g. ["A1", ..., "B30"] for select(name="CA")."""
    _check_selection(atoms, "atoms")
    return [_label(i) for i in atoms.indices]


def _check_trajectory(obj, arg):
    if isinstance(obj, Structure):
        raise TypeError(f"'{arg}' must be a trajectory (e.g. t_1), but you gave the structure {obj.name}. "
                        f"Load the trajectory with load_trajectory().")
    if not isinstance(obj, Trajectory):
        raise TypeError(f"'{arg}' must be a trajectory (e.g. t_1), not {type(obj).__name__}.")


def _check_reference(obj):
    if isinstance(obj, Trajectory):
        raise TypeError(f"The reference must be a single structure (e.g. pdb_1 or pdb_2), but you gave the "
                        f"trajectory {obj.name} with {obj.n_frames} frames.")
    if not isinstance(obj, Structure):
        raise TypeError(f"The reference must be a structure (e.g. pdb_1 or pdb_2), not {type(obj).__name__}.")


def _check_selection(obj, arg):
    if not isinstance(obj, Selection):
        raise TypeError(f"'{arg}' must be an atom selection made with select(), not {type(obj).__name__}.")


def _superpose(xyz, reference, fit):
    """Rotate and translate every frame so that the atoms `fit` best match the reference (Kabsch).

    Returns the moved coordinates of all atoms and the RMSD of the fit atoms."""
    x = xyz[:, fit].astype(np.float64)
    x_c = x.mean(axis=1, keepdims=True)
    y = reference[fit]
    y_c = y.mean(axis=0)
    x0, y0 = x - x_c, y - y_c
    h = np.einsum("fai,aj->fij", x0, y0)
    u, s, vt = np.linalg.svd(h)
    d = np.sign(np.linalg.det(u @ vt))
    s[:, -1] *= d
    u[:, :, -1] *= d[:, None]
    rot = u @ vt
    moved = np.einsum("fai,fij->faj", xyz - x_c, rot) + y_c
    msd = ((x0 ** 2).sum(axis=(1, 2)) + (y0 ** 2).sum() - 2 * s.sum(axis=1)) / len(fit)
    return moved, np.sqrt(np.clip(msd, 0, None))


def rmsd(trajectory, reference, atoms):
    """RMSD (nm) of each frame to the reference structure, using the selected atoms.

    Each frame is first superimposed onto the reference (on the same atoms). Returns one value per frame."""
    _check_trajectory(trajectory, "trajectory")
    _check_reference(reference)
    _check_selection(atoms, "atoms")
    return _superpose(trajectory.xyz, reference.xyz, atoms.indices)[1]


def rmsf(trajectory, reference, atoms):
    """RMSF (nm) of each selected atom: its fluctuation around its average position.

    The frames are first superimposed onto the reference structure (on the selected atoms).
    Returns one value per selected atom."""
    _check_trajectory(trajectory, "trajectory")
    _check_reference(reference)
    _check_selection(atoms, "atoms")
    moved = _superpose(trajectory.xyz[:, atoms.indices], reference.xyz[atoms.indices],
                       np.arange(len(atoms)))[0]
    return np.sqrt(((moved - moved.mean(axis=0)) ** 2).sum(axis=2).mean(axis=0))


def distance(trajectory, atom_A, atom_B):
    """Distance (nm) between two atoms in each frame. Each selection must contain exactly one atom."""
    _check_trajectory(trajectory, "trajectory")
    for arg, sel in (("atom_A", atom_A), ("atom_B", atom_B)):
        _check_selection(sel, arg)
        if len(sel) != 1:
            found = ", ".join(f"{_label(i)} {_ATOMS['name'][i]}" for i in sel.indices[:5])
            more = " ..." if len(sel) > 5 else ""
            raise ValueError(f"'{arg}' must contain exactly one atom, but it contains {len(sel)} ({found}{more}). "
                             f"Add chain, resnum and name to select() to narrow it down.")
    a, b = atom_A.indices[0], atom_B.indices[0]
    return np.linalg.norm(trajectory.xyz[:, a] - trajectory.xyz[:, b], axis=1).astype(np.float64)
