# Electron Column Hierarchy
Our electron column uses an off-the-shelf tungsten thermionic filament bought from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx), or from [Agar](https://www.agarscientific.com/agar-filaments), [Microtonano](https://www.microtonano.com/EBS-Tungsten-EM-Filaments.php#a14AE1201B), and [Oxford Instruments](https://estore.oxinst.com/us/products/microscopy-supplies/electron-microscopy/filaments/zid51-1625-0153) for $10/filament.

We'll use the information Agar gives on its thermionic sources to model low-ev (0.5 eV-ish) electrons boiling off at 2800 K using the Picht software package, and create a full electrostatic lens design using:

- -100V biased Wehnelt Cylinder.
- A Tungsten Thermionic source of a 60 micrometers cathode radius, and 25 micrometers initial beam spread radially

An electrostatic condenser lens, and an electrostatic objective lens- we're building off the [Applied Science SEM proof-of-concept](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) which already uses electrostatic lenses, but we use much higher voltages, and einzel lenses instead of cylindrical lenses, and simulate the column in its entirety.

The full CAD design of the electron column post-design is incoming, but all the geometric data's fully available in the design, which already accounts for being inside an enclosed vacuum chamber due to its Dirichlet boundary conditions.

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


## Beam Assembly (CAD)

We'll use Al 6063 for the electrostatic components, and soft iron cores for the magnetic lenses. CAD files are in save.step, and are auto-generated by Picht.