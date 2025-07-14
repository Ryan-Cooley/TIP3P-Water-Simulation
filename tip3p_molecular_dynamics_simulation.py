from openmm.app import *
from openmm import *
from openmm.unit import *
import sys

# Load AMBER files
print("Loading AMBER files...")
prmtop = AmberPrmtopFile('waterbox1.prmtop')
inpcrd = AmberInpcrdFile('waterbox1.inpcrd')
print("AMBER files loaded.")

# Create a system
print("Creating system...")
system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer, constraints=HBonds)
print("System created.")

# Create an integrator for dynamics
print("Creating integrator...")
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
print("Integrator created.")

# Create a simulation object
print("Creating simulation object...")
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)
print("Simulation object created and positions set.")

# Minimize the energy
print("Minimizing energy...")
simulation.minimizeEnergy()
print("Energy minimization complete.")

# Equilibration phase (without recording data)
equilibration_steps = 50000  # 100 ps of equilibration
print(f"Starting equilibration phase for {equilibration_steps} steps...")
simulation.step(equilibration_steps)
print("Equilibration phase complete.")

# Reset reporters for the production run
print("Resetting reporters for the production run...")
simulation.reporters.clear()
simulation.reporters.append(StateDataReporter(sys.stdout, 1000, step=True, potentialEnergy=True, temperature=True))
simulation.reporters.append(DCDReporter('trajectory1.dcd', 1000))
print("Reporters set for production run.")

# Production run: Now the data is recorded
production_steps = 10000000  # 20,000 ps (20 ns) of production
print(f"Starting production run for {production_steps} steps...")
simulation.step(production_steps)
print("Production run complete.")