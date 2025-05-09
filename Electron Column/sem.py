import numpy as np
from picht import IonOpticsSystem, ElectrodeConfig
import matplotlib.pyplot as plt

system = IonOpticsSystem(nr=100, nz=400, axial_size=0.4, radial_size = 0.1)


wehnelt1 = ElectrodeConfig(
    start=0,
    width=30,
    ap_start=30,
    ap_width=40,
    outer_diameter = 50,
    voltage=-5100
)
wehnelt2 = ElectrodeConfig(
    start=30,
    width=5,
    ap_start=45,
    ap_width=10,
    outer_diameter = 50,
    voltage=-5100
)
system.add_electrode(wehnelt1)
system.add_electrode(wehnelt2)
anode = ElectrodeConfig(
    start=50,
    width = 2,
    ap_start=49,
    ap_width=2,
    outer_diameter = 50,
    voltage=0
)
cathode = ElectrodeConfig(
    start=24,
    width = 1,
    ap_start=50,
    ap_width=0,
    outer_diameter = 2,
    voltage=-5000
)

system.add_electrode(anode)
system.add_electrode(cathode)


system.add_einzel_lens(
    position= 70.0,
    width=70.0,
    aperture_center=50.0,
    aperture_width=48.0,
    outer_diameter=50.0,
    focus_voltage=-7200
)
system.add_einzel_lens(
    position= 142.0,
    width=63.0,
    aperture_center=50.0,
    aperture_width=48.0,
    outer_diameter=50.0,
    focus_voltage=-10000
)


potential = system.solve_fields()

trajectories = system.simulate_beam(
    energy_eV= 0.1,  
    start_z=0.025,
    r_range=(0.0499925, 0.0500075),
    angle_range=(-2, 2),
    num_particles=100,
    simulation_time=1e-8
)

figure = system.visualize_system(
    trajectories=trajectories)

plt.show()