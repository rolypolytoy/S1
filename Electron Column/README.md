# Electron Column Hierarchy
Our electron column uses an off-the-shelf tungsten thermionic filament bought from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx), or from [Agar](https://www.agarscientific.com/agar-filaments), [Microtonano](https://www.microtonano.com/EBS-Tungsten-EM-Filaments.php#a14AE1201B), and [Oxford Instruments](https://estore.oxinst.com/us/products/microscopy-supplies/electron-microscopy/filaments/zid51-1625-0153) for $10/filament.

We'll use the information Agar gives on its thermionic sources to model low-ev (10 eV-ish) electrons boiling off at 2800 K using the Picht software package, and create a full electrostatic lens design using:

- -100V biased Wehnelt Cylinder.
- A Tungsten Thermionic source of a 60 micrometers cathode radius, and 25 micrometers initial beam spread radially
- A 5kV accelerating voltage
- 7.5kV and 10kV condenser and objective lenses with proper fringing accounted for

An electrostatic condenser lens, and an electrostatic objective lens- we're building off the [Applied Science SEM proof-of-concept](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) which already uses electrostatic lenses, but we use much higher voltages, and einzel lenses instead of cylindrical lenses, and simulate the column in its entirety.

The full CAD design of the electron column post-design is incoming, but all the geometric data's fully available in the design, which already accounts for being inside an enclosed vacuum chamber due to its Dirichlet boundary conditions.

**Disclaimer:** Do not do anything related to any voltages close to or above mains if your design hasn't been thoroughly vetted by both electrical engineers and electricians, and assembled with full propriety. Don't do anything stupid, for your own sake, and it's always better to have too much clearance distances, put too much tape, use too many safety practices, or just not engage with power electronics than end up dead. Electricity will kill you if you don't respect it, which is why more than half of the design decisions we make are about safety to a pedantic degree. Cheap, low-cost and open-source doesn't mean unsafe or without industry-standard practices. If you don't have power electronics expertise, it's honestly safer to just not mess around with this and look at this as a speculative exercise entirely, because dealing with the power electronics is actually harder than the design process of the electron column just because of how much everything becomes conductor-like at high voltages. Vacuum interiors mitigate this, but you don't design for vacuums but for normal operation because it might be turned on even when it's in air.

## Power Electronics

**[230 VAC to 10kV converter](https://ar.aliexpress.com/item/1005003518403820.html):**
This is a relatively safe and low-cost component used in industry. It has a <2cm discharge distance due to its plastic protection, so we'll keep a 4cm distance for a safety factor of >2X. It's intended to connect with mains, so we'll use a [mains relay](https://www.amazon.in/CLUB-BOLLYWOOD-Channel-Optocoupler-Insulation/dp/B0C2PT1KRB) to enable PWM-pin controlled switching of the mains voltage that powers the 10kV power source, as well as [heat shrink tubes](https://www.amazon.in/Rpi-shop-Polyolefin-Insulated-Multicolour/dp/B08S3TP2Q6) and [mains-rated wiring](https://www.amazon.in/TWC-Lite-Single-Black-Electrical/dp/B0B7GG46KJ) for the pre-AC-to-DC stage. We'll also use [10kV rated wire](https://ar.aliexpress.com/item/1005001839936748.html?gatewayAdapt=glo2ara) post-amplification and keep >2x safety factors in terms of discharge distance from these, as well as [69kV-rated electrical tape](https://www.amazon.in/3M-70-Self-Fusing-Silicone-Electrical/dp/B0029Z5RSY) (multiple applications at critical places) at junctions. The DC power supply allows us to use 0V and -10kV depending on how we set up the polarities, and we'll use exactly this setup for our applications. 

**Voltage Divider Circuit:**
From the 10kV initial voltage, we need the following discrete voltage steps according to the electron column design:

- 0V, or the positive terminal proper, routed to the anode, the walls, and the side electrodes in the einzel lenses
- -5000V, routed to the cathode
- -5100V, routed to the Wehnelt cap
- -7500V, routed to the objective lens' middle electrode
- -10000V, routed to the condenser lens' middle electrode
  
We can make a voltage divider circuit, as well as add safety features, before we rout the voltage to the einzel lenses, Wehnelt Cylinders, etc. We can actually make one series circuit such that it gives us all of these voltages from 10kV using precisely chosen values of resistors, and at least one diode for surge protection. We need to make sure to properly tape the 3M electrical around all the resistors and the active to ensure absolutely no discharge happens, but though we've accounted for safe practices, we need to obtain the resistors and make a valid diagram for it.

In other words, from -10kV we need to first subtract 2500V, then 2400V, then 100V, then 5000V, and so we need these ratios in resistance (25:24:1:50). If we use 1% tolerance resistors at high resistance values in the megaohm range to limit power to below the 0.25W per resistor limit as well as use resistance values commonly found in the ubiquitous [metal-film-oxide resistor kits](https://www.amazon.in/AVS-Components-Tolerance-Assortment-Electronics/dp/B0D6LRXK5P). Make sure to get the 1% tolerance variants, though, and post-assembly to wrap this with the 3M silicone electrical tape for proper insulation.

Kits commonly have 1 MOhm, 2MOhm, 4.7MOhm and 5.6MOhm values of resistors as well as some other common values, which are all the building blocks we'll use. Make a 25 MOhm resistor using 1 5.6 MOhm resistor, two 4.7MOhm resistors and five 2MOhm resistors. You can make a 24 MOhm resistor using a 1 5.6 MOhm resistor, two 4.7MOhm resistors, four 2 MOhm resistors and 1 1MOhm resistor. For the next stage just use a 1MOhm resistor. Make a 50 MOhm resistor using 3 5.6 MOhm resistor, 6 4.7 MOhm resistors, 2 2 MOhm resistors and 1 1MOhm resistor. Wire them up like this to make a voltage divider -10kV -> 25MOhm ->  24MOhm -> 1MOhm -> 50MOhm -> 0V

This makes a voltage divider circuit like so: 
![voltagedivider](https://github.com/user-attachments/assets/ce32a2be-ea33-4567-9234-9e5978b3aea0)

I'd recommend first creating the geometry of them, [soldering](https://www.amazon.in/Electronic-Spices-Starter-60watt-Soldering/dp/B098XTZJYQ) them together with a high-quality [tin solder](https://www.amazon.in/Solder-Soldering-Electronic-Electrical-Components/dp/B0B3D8NLMB). The net current will be 10kV/50 MOhm = 0.2 mA or 200 microamperes, with the power dissipation across the most energetic resistor of $I^2R$ = $0.04 * 5.6 = 0.224$, which is below their operating power of 0.25W, which means our system should work entirely functionally. We've also created bleeding across all of this, which is tremendously good practice for power electronics because nor electrostatic lenses, nor accelerating electrodes require particularly high operating currents, and >100 microamperes is more than enough for functional operation. 

Again- ensure you use proper practices for the 10kV rated wiring (which is the only wiring you should be using here), tape-insulate EVERYTHING, and make the diagram as follows. We now have distinct voltages for the reference voltages required to make the beam column design as shown in the simulations. Once we've set this up via soldering, etc etc, prior to even switching it on, we'll coat it in [epoxy resin](https://www.amazon.in/DYNAMIC-EDGE-Hardener-Long-Lasting-Non-Toxic/dp/B0CWZ8G5CM) to nullify current leakage effects and make it even more safe. This and the 3M silicone tape are key to HV insulation.

## Column Design
I've already designed my column using [Picht](https://github.com/rolypolytoy/S1/blob/main/Electron%20Column/sem.py) with visual results of focusing behavior that's shown in many places. Using the pre-verified design as a baseline, we can build it out using parametric CAD software, as well as sufficient insulation to prevent arcing.

Let's examine the image in more detail:
![SEM](https://github.com/user-attachments/assets/77c80e26-aec4-40b3-aa98-369c81665102)


You can regenerate it using [this code](https://rolypolytoy.github.io/picht/auto_examples/example_sem_simulation.html#sphx-glr-auto-examples-example-sem-simulation-py).

**First Crossover**

If you zoom into the focal points using Matplotlib (its visualization features reign supreme) you can find spherical aberrations that you couldn't in the top-level view. Zooming into the first crossover point between the Wehnelt Cylinder and the condenser lens we find this:
![FirstCrossover](https://github.com/user-attachments/assets/52d47ffe-41ff-4afd-877e-bd703b1337fd)

Focal length: From 40.65 mm to 40.89 mm, with focal diameter/spot size of 240 micrometers and a center of focus at 40.77 mm.

**Second Crossover**

![SecondCrossover](https://github.com/user-attachments/assets/eb8d4675-ada9-4a6b-abb3-cbfc5ae6cdfb)

Focal length: From 140.10 mm to 140.39 mm, with focal diameter/spot size of 290 micrometers and a center of focus at 140.25 mm.


**Final Focus**
![Focus](https://github.com/user-attachments/assets/0ec8ab87-5951-41c6-90cf-71778c42e120)

Focal length: From 201.52 mm to 203.02 mm, with focal diameter/spot size of 1500 micrometers and a center of focus at 202.27mm.

## Beam Assembly (CAD)
Now, we need to make the beam assembly based on this validated design. We'll use aluminium 6063 for any electrically active components (to minimize the final weight of the desktop SEM). We also need a machinable insulator material- PTFE is great for this because it has at the **lowest end** a dielectric strength of [20kV/mm](https://polyfluoroltd.com/blog/the-insane-electrical-properties-of-ptfe-and-how-to-interpret-them/), which means 1 mm thick insulation with PTFE will have a 2x safety factor with even the most high-voltage differential einzel lens, which is our objective lens with a middle voltage of -10kV with the other two electrodes at ground. [PTFE's](https://en.wikipedia.org/wiki/Materials_for_use_in_vacuum#Plastics) also completely fine to use in HV conditions, and is [machinable](https://fluorocarbon.co.uk/resources/blog/a-guide-to-machining-ptfe/) though with some expansion/creep issues, which is fine because no critical positioning aspects are affected by PTFE. We'll use machined shoulders to make a column using the dimensions from the SEM analysis we've done so far.

According to [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx) the diameter of the AEI tungsten filament's ceramic base is 12 mm, with the pin diameters being 1 mm and the center distance of the pins being 6.45 mm. 

We can thus design the CAD components for the column with all of this in mind. 
