import numpy as np
from picht import ElectronOptics, ElectrodeConfig, MagneticLensConfig, Export
import matplotlib.pyplot as plt

system = ElectronOptics(nr=200, nz=400, axial_size=0.1, radial_size=0.1)
system.solve_fields()

#Electron Gun's Beam.
trajectories = system.simulate_beam(
    energy_eV= 9800,  
    start_z=0.0456210,
    r_range=(0.04996, 0.050004),
    angle_range=(-0.15, 0.15),
    num_particles=10, 
    simulation_time=6e-9
)

figure = system.visualize_system(
    trajectories=trajectories)

plt.show()

#exporter = Export(system)
#exporter.cad_export()
