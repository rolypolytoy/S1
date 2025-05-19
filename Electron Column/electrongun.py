import numpy as np
from picht import ElectronOptics, ElectrodeConfig, MagneticLensConfig, Export
import matplotlib.pyplot as plt

system = ElectronOptics(nr=1000, nz=4000, axial_size=0.4, radial_size = 0.01)

#Electron Gun- Finished.
wehnelt1 = ElectrodeConfig(
    start=0,
    width=300,
    ap_start=200,
    ap_width=600,
    outer_diameter = 1000,
    voltage=-10000
)
wehnelt2 = ElectrodeConfig(
    start=300,
    width=50,
    ap_start=450,
    ap_width=100,
    outer_diameter = 1000,
    voltage=-10000
)
system.add_electrode(wehnelt1)
system.add_electrode(wehnelt2)
anode = ElectrodeConfig(
    start=450,
    width = 10,
    ap_start=480,
    ap_width=40,
    outer_diameter = 1000,
    voltage=0
)
cathode = ElectrodeConfig(
    start=248,
    width = 2,
    ap_start=500,
    ap_width=0,
    outer_diameter = 6,
    voltage=-9800
)
system.add_electrode(anode)
system.add_electrode(cathode)
#Electron Gun- Finished.
"""
system.solve_fields()

trajectories = system.simulate_beam(
    energy_eV= 0.5,  
    start_z=0.025,
    r_range=(0.0049875, 0.0050125),
    angle_range=(-2, 2),
    num_particles=10, 
    simulation_time=1e-7
)

#approximable as a pointlike source at r ≈ 0.0456210 from z = 0.00491882 to z = 0.00500278, from +0.12708460 radians to -0.14790062, at 9.8 keV. approx 80 microns virtual source.
#basically- is at r = 0.0456210, with an 80 micron virtual spot size, 9.8 keV energy, and +-0.15 radians spot.

figure = system.visualize_system(
    trajectories=trajectories)

plt.show()
"""
exporter = Export(system)
exporter.cad_export()
