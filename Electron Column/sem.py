import numpy as np
from picht import IonOpticsSystem, ElectrodeConfig
import matplotlib.pyplot as plt

system = IonOpticsSystem(nr=100, nz=400, axial_size=0.4, radial_size = 0.1)


#Wehnelt Cylinders- responsible for the first crossover
wehnelt1 = ElectrodeConfig(
    start=0,
    width=30,
    ap_start=30,
    ap_width=40,
    outer_diameter = 50,
    voltage=-5150 #biased at -150V in relation to the cathode
)
wehnelt2 = ElectrodeConfig(
    start=30,
    width=5,
    ap_start=45,
    ap_width=10,
    outer_diameter = 50,
    voltage=-5150 #biased at -150V in relation to the cathode
)
system.add_electrode(wehnelt1)
system.add_electrode(wehnelt2)

#Anode- +5000V in relation to the cathode, to provide acceleration
anode = ElectrodeConfig(
    start=50,
    width = 2,
    ap_start=49,
    ap_width=2,
    outer_diameter = 50,
    voltage=0
)
#Cathode- represents the thermionic tungsten filament electrons boil off from
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

#Condenser Lens- In between the first and second crossover point, provides initial focusing
system.add_einzel_lens(
    position= 70.0,
    width=70.0,
    aperture_center=50.0,
    aperture_width=48.0,
    outer_diameter=50.0,
    focus_voltage=-7500
)

#A Beam-Limiting Aperture comes between the lenses to add a demagnification ratio

#Objective Lens- Provides final focusing mere millimeters after its end
system.add_einzel_lens(
    position= 141.0,
    width=58.0,
    aperture_center=50.0,
    aperture_width=48.0,
    outer_diameter=50.0,
    focus_voltage=-10000
)

potential = system.solve_fields()

#Notice how we initialize it at only 0.5 eV- the acceleration happens from the field lines between the cathode and anode
trajectories = system.simulate_beam(
    energy_eV= 0.5,  
    start_z=0.025, #We begin at z = 0.025, or 25 grid units in the z-direction so that there's a bit of Wehnelt Cylinder behind this
    r_range=(0.0499875, 0.0500125), #25 micron thick beam, which is a realistic amount given by the manufacturer
    angle_range=(-2, 2), #very high initial angular divergence to mimic thermionic emission + Coulomb repulsion pre-acceleration
    num_particles=10, #the time it takes to compute scales o(n)-ish with this
    simulation_time=1e-8 #empirically found value for when the full simulation completes
)

figure = system.visualize_system(
    trajectories=trajectories)

plt.show()
