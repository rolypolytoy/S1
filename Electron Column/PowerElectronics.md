# Electron Column Hierarchy
Our electron column uses an off-the-shelf tungsten thermionic filament bought from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx), where 10 tungsten-rhenium filaments go for $244, for a unit cost of $24/filament).

We'll use the information Ted Pella gives on its thermionic sources to model low-ev (10 eV-ish) electrons boiling off at 2800 K using the Picht software package, and create a full electrostatic lens design using:

- -100V biased Wehnelt Cylinder.
- A Tungsten Thermionic source of a 60 micrometers cathode radius, and 15 micrometers beam emittance spot
- A 5kV accelerating voltage
- 7kV and 6.5kV condenser and objective lenses with proper fringing accounted for

An electrostatic condenser lens, and an electrostatic objective lens- we're building off the [Applied Science SEM proof-of-concept](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) which already uses electrostatic lenses, but we use much higher voltages, and einzel lenses instead of cylindrical lenses, and simulate the column in its entirety.

The full parameters of the beam simulation can be found at [Picht](https://github.com/rolypolytoy/picht/blob/main/examples/sem.py), but to summarize we've found a system which enables micron-level spot size, with 67x demagnification between the first crossover and the focal point which is ~8mm downstream of the final einzel lens. If we buy a 200 micrometers [beam limiting aperture](https://www.tedpella.com/apertures-and-filaments_html/aperture3.aspx) (for only $99 USD!!!), we can get 200/67 = 3 micrometers of a spot size, which is tremendous for a DIY system. Whether we actually get this degree of resolution on a DIY system remains to be seen, but counterintuitively we might be able to push it below micrometer-resolution with DSP techniques like deconvolution and frame-averaging- if we have a good enough raster scanner.

The full CAD design of the electron column post-design is incoming, but all the geometric data's fully available in the design, which already accounts for being inside an enclosed vacuum chamber due to its Dirichlet boundary conditions.

## Power Electronics

Disclaimer: Do not do anything related to any voltages close to or above mains if your design isn't vetted by both electrical engineers and electricians. Don't do anything stupid, for your own sake, and it's always better to have too much clearance distances, put too much tape, use too many safety practices, or just not engage with power electronics than end up dead. Electricity will kill you if you don't respect it, which is why more than half of the design decisions we make are about safety to a pedantic degree. Cheap, low-cost and open-source doesn't mean unsafe or without industry-standard practices.

**[230 VAC to 10kV converter](https://ar.aliexpress.com/item/1005003518403820.html):**
This is a relatively safe and low-cost component used in industry. It has a <2cm discharge distance due to its plastic protection, so we'll keep a 4cm distance for a safety factor of >2X. It's intended to connect with mains, so we'll use a [mains relay](https://www.amazon.in/CLUB-BOLLYWOOD-Channel-Optocoupler-Insulation/dp/B0C2PT1KRB) to enable PWM-pin controlled switching of the mains voltage that powers the 10kV power source, as well as [heat shrink tubes](https://www.amazon.in/Rpi-shop-Polyolefin-Insulated-Multicolour/dp/B08S3TP2Q6) and [mains-rated wiring](https://www.amazon.in/TWC-Lite-Single-Black-Electrical/dp/B0B7GG46KJ) for the pre-AC-to-DC stage. We'll also use [10kV rated wire](https://ar.aliexpress.com/item/1005001839936748.html?gatewayAdapt=glo2ara) post-amplification and keep >2x safety factors in terms of discharge distance from these, as well as [69kV-rated electrical tape](https://www.amazon.in/3M-70-Self-Fusing-Silicone-Electrical/dp/B0029Z5RSY) (multiple applications at critical places) at junctions. The DC power supply allows us to use 0V and -10kV depending on how we set up the polarities, and we'll use exactly this setup for our applications. 

**Voltage Divider Circuit:**
From the 10kV initial voltage, we need the following discrete voltage steps according to the electron column design:

- 0V, or the positive terminal proper, routed to the anode, the walls, and the side electrodes in the einzel lenses
- -5000V, routed to the cathode
- -5100V, routed to the Wehnelt cap
- -6500V, routed to the objective lens' middle electrode
- -7000V, routed to the condenser lens' middle electrode
  
We can make a voltage divider circuit, as well as add safety features, before we rout the voltage to the einzel lenses, Wehnelt Cylinders, etc. We can actually make one series circuit such that it gives us all of these voltages from 10kV using precisely chosen values of resistors rated for at least 15kV and 50W, and at least one diode for surge protection. We need to make sure to properly tape the 3M electrical around all the resistors and the active to ensure absolutely no discharge happens, but though we've accounted for safe practices, we need to obtain the resistors and make a valid diagram for it.

In other words, from -10kV we need to first subtract 3000V, then 500V, then 1400V, then 100V, then 5000V, and so we need these ratios in Ohms from 15kV-rated resistors. We need 30:5:14:10:50 ratio resistors, in other words.


