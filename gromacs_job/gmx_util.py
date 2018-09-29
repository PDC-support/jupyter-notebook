import os
import subprocess
import numpy as np

class Atom(object):

    """The Atom class contains atomic information including atom
    name, residue name, residue ID, and Cartesian coordinates"""

    def __init__(self, name, resname, resid, x, y, z):

        """Initializes an atom with name, residue name, residue ID,
        and Cartesian coordinates"""

        self.name = name
        self.resname = resname
        self.resid = resid
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):

        """String representation for an atom"""

        return "%-4s %8.3f %8.3f %8.3f %5s (%d)" \
                % (self.name, self.x, self.y, self.z,
                   self.resname, self.resid)

def load_gmx():

    """Load GROMACS environmental variables"""

    gmx_root = "/pdc/vol/gromacs/2018.3/amd64_co7/haswell_openmpi"

    os.environ["GMXBIN"]   = gmx_root + "/bin"
    os.environ["GMXLDLIB"] = gmx_root + "/lib"
    os.environ["GMXMAN"]   = gmx_root + "/man"
    os.environ["GMXDATA"]  = gmx_root + "/share"

    os.environ["LD_LIBRARY_PATH"] = gmx_root + "/lib:" + os.environ["LD_LIBRARY_PATH"] 
    os.environ["PATH"]            = gmx_root + "/bin:" + os.environ["PATH"]
    os.environ["MANPATH"]         = gmx_root + "/man:" + os.environ["MANPATH"]

def get_prop(prop, deffnm):

    """Extract system property (Temperature, Pressure, Potential, or Density)
    from a GROMACS energy (edr) file. Returns lists of time and property."""

    assert prop in ["Temperature", "Pressure", "Potential", "Density"]

    # echo Potential | gmx_seq energy -f npt.edr

    ps = subprocess.Popen(("echo", prop), stdout=subprocess.PIPE)
    command = "gmx_seq energy -f %s.edr" % deffnm
    output = subprocess.check_output(command.split(), stdin=ps.stdout)
    ps.wait()

    # read xvg and return x & y

    x = []
    y = []

    f_ener = open("energy.xvg", 'r')
    for line in f_ener:
        if line[0] == '#' or line[0] == '@':
            continue
        content = line.split()
        x.append(float(content[0]))
        y.append(float(content[1]))
    f_ener.close()

    return x,y

def get_rmsd(target, deffnm):

    """Calculate RMSD of Protein, Backbone, or SideChain from a molecular
    dynamics simulation trajectory. Returns lists of time and RMSD."""

    assert target in ["Protein", "Backbone", "SideChain"]

    # echo Protein Protein | gmx_seq rms -f npt.xtc -s topol.tpr

    ps = subprocess.Popen(("echo", target, target), stdout=subprocess.PIPE)
    command = "gmx_seq rms -f %s.xtc -s topol.tpr" % deffnm
    output = subprocess.check_output(command.split(), stdin=ps.stdout)
    ps.wait()

    # read xvg and return x & y

    x = []
    y = []

    f_ener = open("rmsd.xvg", 'r')
    for line in f_ener:
        if line[0] == '#' or line[0] == '@':
            continue
        content = line.split()
        x.append(float(content[0]))
        y.append(float(content[1]))
    f_ener.close()

    return x,y

def get_pdb(target, deffnm):

    """Extract pdb of System, Protein, or Water from a GROMACS trajectory (xtc)
    file"""

    assert target in ["System", "Protein", "Water"]

    # echo System | gmx_seq trjconv -f npt.xtc -s topol.tpr -o npt.pdb

    ps = subprocess.Popen(("echo", target), stdout=subprocess.PIPE)
    command = "gmx_seq trjconv -f %s.xtc -s topol.tpr -o %s.pdb" % (deffnm, deffnm)
    command += " -dt 10 -pbc mol"
    output = subprocess.check_output(command.split(), stdin=ps.stdout)
    ps.wait()

def read_pdb(time, deffnm):

    """Read a pdb frame at a given time. Returns a list of atoms."""

    # read pdb frame at a given time and return a list of atoms

    time_found = False
    atoms = []

    f_pdb = open("%s.pdb" % deffnm, 'r')

    for line in f_pdb:

        if "t=" in line:
            if time_found:
                print("Frame found at time %f" % time)
                f_pdb.close()
                return atoms
            atoms = []
            t = float(line.split("t=")[1].split("step=")[0])
            if t == float(time):
                time_found = True
            if t > float(time):
                print("Frame NOT found at time %f" % time)
                f_pdb.close()
                return []

        if line[0:4] == "ATOM":
            name = line[12:16]
            resname = line[17:20]
            resid = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            atoms.append(Atom(name,resname,resid,x,y,z))

    print("Frame NOT found at time %f" % time)
    f_pdb.close()
    return []
