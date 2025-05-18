# Electron Column Hierarchy
Our electron column uses an off-the-shelf tungsten thermionic filament bought from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx), or from [Agar](https://www.agarscientific.com/agar-filaments), [Microtonano](https://www.microtonano.com/EBS-Tungsten-EM-Filaments.php#a14AE1201B), and [Oxford Instruments](https://estore.oxinst.com/us/products/microscopy-supplies/electron-microscopy/filaments/zid51-1625-0153) for $10/filament.

We'll use the information Agar gives on its thermionic sources to model low-ev (0.5 eV-ish) electrons boiling off at 2800 K using the Picht software package, and create a full electrostatic lens design using:

- -200V biased Wehnelt Cylinder.
- A Tungsten Thermionic source with a 60 micrometers cathode radius, and 25 micrometers initial beam spread radially

The most prohibitive components are the filaments (which might cost $100 total for a pack of 10) and the beam limiting aperture ($70 bucks at the most).

We're building off the [Applied Science SEM proof-of-concept](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) but we're using electromagnetic lenses instead.

**Disclaimer:** Do not do anything related to any voltages close to or above mains if your design hasn't been thoroughly vetted by both electrical engineers and electricians, and assembled with full propriety. Don't do anything stupid, for your own sake, and it's always better to have too much clearance distances, put too much tape, use too many safety practices, or just not engage with power electronics than end up dead. Electricity will kill you if you don't respect it, which is why more than half of the design decisions we make are about safety to a pedantic degree. Cheap, low-cost and open-source doesn't mean unsafe or without industry-standard practices. If you don't have power electronics expertise, it's honestly safer to just not mess around with this and look at this as a speculative exercise entirely, because dealing with the power electronics is actually harder than the design process of the electron column just because of how much everything becomes conductor-like at high voltages. Vacuum interiors mitigate this, but you don't design for vacuums but for normal operation because it might be turned on even when it's in air.

## Power Electronics

**[230 VAC to 10kV converter](https://ar.aliexpress.com/item/1005003518403820.html):**
This is a relatively safe and low-cost component used in industry. It has a <2cm discharge distance due to its plastic protection, so we'll keep a 4cm distance for a safety factor of >2X. It's intended to connect with mains, so we'll use a [mains relay](https://www.amazon.in/CLUB-BOLLYWOOD-Channel-Optocoupler-Insulation/dp/B0C2PT1KRB) to enable PWM-pin controlled switching of the mains voltage that powers the 10kV power source, as well as [heat shrink tubes](https://www.amazon.in/Rpi-shop-Polyolefin-Insulated-Multicolour/dp/B08S3TP2Q6) and [mains-rated wiring](https://www.amazon.in/TWC-Lite-Single-Black-Electrical/dp/B0B7GG46KJ) for the pre-AC-to-DC stage. We'll also use [10kV rated wire](https://ar.aliexpress.com/item/1005001839936748.html?gatewayAdapt=glo2ara) post-amplification and keep >2x safety factors in terms of discharge distance from these, as well as [69kV-rated electrical tape](https://www.amazon.in/3M-70-Self-Fusing-Silicone-Electrical/dp/B0029Z5RSY) (multiple applications at critical places) at junctions. The DC power supply allows us to use 0V and -10kV depending on how we set up the polarities, and we'll use exactly this setup for our applications. 

**Voltage Divider Circuit:**
From the 10kV initial voltage, we need the following discrete voltage steps according to the electron column design:

- 0V, or the positive terminal proper, routed to the anode, the walls, and the side electrodes in the einzel lenses
- -9800V, routed to the cathode
- -10000V, routed to the Wehnelt cap
  
We can make a voltage divider circuit, as well as add safety features, before we rout the voltage to the einzel lenses, Wehnelt Cylinders, etc. We can actually make one series circuit such that it gives us all of these voltages from 10kV using precisely chosen values of resistors, and at least one diode for surge protection. We need to make sure to properly tape the 3M electrical around all the resistors and the active to ensure absolutely no discharge happens, but though we've accounted for safe practices, we need to obtain the resistors and make a valid diagram for it.

In other words, from -10kV we need to first subtract 200V, then 9800V, and so we need these ratios in resistance. If we use 1% tolerance resistors at high resistance values in the megaohm range to limit power to below the 0.25W per resistor limit as well as use resistance values commonly found in the ubiquitous [metal-film-oxide resistor kits](https://www.amazon.in/AVS-Components-Tolerance-Assortment-Electronics/dp/B0D6LRXK5P). Make sure to get the 1% tolerance variants, though, and post-assembly to douse it in epoxy resin.

Kits have 2 MOhm resistors, and we can construct a 98 MOhm resistor in series by combining 4 2 MOhm resistors, 6 5.6 MOhm resistors, and 12 4.7 MOhm resistors. The maximum power across a resistor will be (V = IR so peak current is I = V/R, 10kV/100MOhm = 0.1 mA) $I^2R$ across the largest resistance value which in our case is the 5.6 MOhm resistor, whose resistance will be 0.056 Watts. Their limits are 0.250W so a 5x safety margin should cover it. All the other resistors will have less power across them by definition.

Again- ensure you use proper practices for the 10kV rated wiring (which is the only wiring you should be using here), tape-insulate EVERYTHING, and make the diagram as follows. We now have distinct voltages for the reference voltages required to make the beam column design as shown in the simulations. Once we've set this up via soldering, etc etc, prior to even switching it on, we'll coat it in [epoxy resin](https://www.amazon.in/DYNAMIC-EDGE-Hardener-Long-Lasting-Non-Toxic/dp/B0CWZ8G5CM) to nullify current leakage effects and make it even more safe. This and the 3M silicone tape are key to HV insulation.

## Column Design
General specs:
Our source is at r = 50 mm and z = 55 mm. The Wehnelt cylinder is from r = 30 mm to r = 60 mm, the anode is from r = 90 mm to r = 91 mm, the condenser lens is from r = 130 mm to r = 180 mm and the objective lens is from r = 200 mm to r = 250 mm. The boundary conditions are Dirichlet (0V, grounded metal) at r = 0 mm, r = 100 mm, as well as at z = 0 mm and z = 400 mm, so the chamber's size is effectively a grounded cylinder with inner radius of 100 mm and height of 400 mm.

### First Crossover
The first crossover happens between the Wehnelt Cap and the Condenser lens. The focus is from z = 69.836 mm to z = 70.282 mm, and from r = 49.98 mm to r = 50.02 mm, for an approximate virtual source size of 400 micrometers. Subpar considering our actual source was 25 micrometers, but not unexpected when using a homebrew designed Wehnelt cylinder rather than proper conic-tapered ones.

![image](https://github.com/user-attachments/assets/005ae277-5550-434e-8544-37a0e33c7f4c)

### Second Crossover
The second crossover happens between the Condenser and the Objective lens, from z = 189.29 mm to z = 189.51 mm, and from r = 50.00 mm to r = 50.03 mm for an approximate beam spot size of 20 micrometers. This is considerably, considerably better than the first crossover. At z = 185 mm the beam spans from r = 50.6 mm to r = 49.4mm for a beam spot size of 1.2 mm. If I use a beam-limiting aperture of 200 micrometers in diameter, I should in theory get 1/36 of the beam through (area is 1/36th of the beam, assuming uniform current density rather than the real pseudo-Gaussian which would mean the fraction is more than 1/36). I can get more conservative and shrink the aperture size but I don't want to because these calculations may be up to +-5 mm off from reality, and so a bigger aperture gives me more leeway in that regards, because we have only one aperture and can afford it. Even at the beam's peak width of 8 mm, we only get to ~1/1600th of the beam's current which is still entirely reasonable of a current even with a thermionic source. So, we're probably good beam-limiting aperture wise, regardless of if we're before or after the focal point. It would be better if we were before because this is intended use but even if we're after we'll get the "shrinking effect" we want, and if it's perfectly aligned we get a sixfold reduction in final spot size.
![image](https://github.com/user-attachments/assets/4bfba258-7fad-41a8-a3d2-7c1545e2495a)

### Focal Point
The final focal point is just over 18 mm after the end of the objective lens, which both gives us more than +-10 mm of leeway in our final focal spot estimate (basically +-20mm which is obscenely generous) but also is within the normal range of values in SEMs. Since we'll be using autofocus in our DSP while varying the z-axis in our 3-axis stage, not knowing the precise focal point is a-okay. The estimates of spot size are from z = 268.26 mm to 268.56, and from r = 49.985 mm to r = 50.021 mm, for about the same spot size as our objective lens. Of course, this is with the sixfold reduction in size, so we're likely in the 3-5 micron range. With DSP (deconvolution and image averaging are really good here) it's not unrealistic to think we're on the cusp of nm-level resolution, or at least that nothing bars us from doing so. Additionally, with a simple swap of a more aggressive aperture if we confirm high beam current with this design, we can most likely get nm-level resolution with this design alone. Preliminary analysis from simulations looks extremely promising. 

![image](https://github.com/user-attachments/assets/902d1fab-3882-4569-8469-6fcd89683e81)

## Hardware
We'll use Al 6063 for the electrostatic components, and silicon steel for the magnetic lenses. CAD files are in save.step, and are auto-generated by Picht.

Aluminium 6063 is conductive enough for the applications we need and M19 (the grade of silicon steel we need) has a saturation flux density of around 1.6 Tesla at around 400 A/m of field strength, which is a relative permeability of around 3100. [Source](https://www.researchgate.net/figure/Magnetization-curves-of-electrical-steels-grade-M4-and-M19_fig1_286116205).

Our condenser lenses have field strengths of 400 A/m and 500 A/m which should give us fluxes of around 1.6 and 1.8 T-ish respectively for flux density. So our relative permeability of the condenser lens is 3183 and of the objective lens is 2865. Note that above 1000 permeabilities I've anecdotally observed changing permeability doesn't change trajectories much and MMF is the limiting factor- something about how the fields are rather than merely their peak strength. Still, these are the numbers I used in the simulation.

Apart for the -10kV Wehnelt cylinder, -9.8kV cathode, and grounded anode, there are several other electric components we need to handle. Using our AD5754 DAC- again, it's quad channel and +-10V- we can pretty much entirely control digitally, the voltage across the thermionic filament. It needs to be biased to -9.8kV, needs a voltage of up to 10V across it. So, we've got thermionic emission covered, we've got the electron gun covered, do we have the lenses covered? We need two 40 mm ID, 50 mm OD, 50 mm height cylinders of M19 which is ~0.541 kg, which should in raw materials cost $1.65, and even with a 20x markup for say, cutting and finishing, is $20. Really breaking the bank here. By the way, in simulations I changed mu_r from 4000 to 1000 to reflect variabilities that stem from saturation, and it really doesn't seem to affect the beam trajectories a lot (+-1mm at the most). MMF does, though. A lot. Counterintuitive but I trust Poisson and Laplace more than I trust my intuition. Since I simulate electromagnets as magnetostatic objects and don't add a separate coil/core geometry, this might deviate from real life, but I don't think it'll be by a significant amount at least in the beam's path.

We need 200 ampere-turns on the condenser lens and 250 ampere-turns on the objective lens, pretty much. We'll give 2 A of current, do 100 turns on the condenser lens and 125 on the objective lens, and that's our full electron optics system. We'll use 20 meters of 14 AWG enameled copper wire to minimize power dissipation losses from heating so we don't need any cooling at all. We'll get exactly 2A by measuring the exact length of wire used in each case, finding the exact resistance, and I'll use the Teensy 4.1's DAC1 and DAC2 for this purpose (we can precisely program the values after the fact for every machine so this is a non-issue and 0 to 3.3V is more than enough range, the resistance of 3.2 * 0.05 * 250 meters of 14 AWG wire (a bit over pi times the diameter of the core times number turns to get the length) is 0.33 Ohms.)

Well, that's all there is to it. Electron column's fully done. 

Of course, I'll make sure to add knobs for the voltage of the electrons and the MMF of each lens so I can adjust things on the fly.
