# Electron Column Hierarchy
Our electron column uses an off-the-shelf tungsten thermionic filament bought from Ted Pella (https://www.tedpella.com/apertures-and-filaments_html/tungsten-filaments.aspx, 10 tungsten-rhenium filaments go for $244, for a unit cost of $24/filament).

Ted Pella provides precise beam emission characteristics for its W thermionic filaments on this website. The most important piece of information is that its effective source radius is 15000 nm, or 15 micrometers wide.

We'll use this initially to profile low-ev electrons boiling off at 2800 K using the Picht software package, and create a full electrostatic lens design using:

-100V biased Wehnelt Cylinders.

An electrostatic condenser lens, and an electrostatic objective lens- we're building off the Applied Science SEM proof-of-concept (https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) which already uses electrostatic lenses, but we use much higher voltages, and einzel lenses instead of cylindrical lenses, and simulate the column in its entirety.

The full parameters of the beam simulation can be found at https://github.com/rolypolytoy/picht/blob/main/examples/sem.py and at the documentation of Picht, but we've found a system which enables micron-level spot size, with 67x demagnification between the first crossover and the focal point which is ~8mm downstream of the final einzel lens. If we buy a 200 micrometers beam limiting aperture at Ted Pella (for only $99 USD!!!) https://www.tedpella.com/apertures-and-filaments_html/aperture3.aspx, we can get 200/67 = 3 micrometers of a spot size, which is tremendous for a DIY system. Whether we actually get this degree of resolution on a DIY system remains to be seen, but counterintuitively we might be able to push it below micrometer-resolution with DSP techniques like deconvolution and frame-averaging- if we have a good enough raster scanner.

For power supplies I'll use an electrostatic power supply rated for 10kV (https://ar.aliexpress.com/item/1005003518403820.html) with voltage dividers and 15 kV rated silicone-jacket wiring, similarly rated diodes, and vet all designs through electrical engineers before production.

The full CAD design of the electron column post-design is incoming, but all the geometric data's fully available in the design, which already accounts for being inside an enclosed vacuum chamber due to its Dirichlet boundary conditions.

## Power Electronics

**[230 VAC to 10kV converter](https://ar.aliexpress.com/item/1005003518403820.html):**
This is a relatively safe and low-cost component used in industry often. It has a <2cm discharge distance due to its plastic protection, so we'll keep a 4cm distance for a safety factor of >2X. It's intended to connect with mains, so we'll use a [mains relay](https://www.amazon.in/CLUB-BOLLYWOOD-Channel-Optocoupler-Insulation/dp/B0C2PT1KRB) to enable PWM-pin controlled switching of the mains voltage that powers the 10kV power source, as well as [heat shrink tubes](https://www.amazon.in/Rpi-shop-Polyolefin-Insulated-Multicolour/dp/B08S3TP2Q6) and [mains-rated wiring](https://www.amazon.in/TWC-Lite-Single-Black-Electrical/dp/B0B7GG46KJ) for the pre-AC-to-DC stage. We'll also use [10kV rated wire](https://ar.aliexpress.com/item/1005001839936748.html?gatewayAdapt=glo2ara) and keep >2x safety factors in terms of discharge distance from these, post-DC amplification, as well as [69kV-rated electrical tape](https://www.amazon.in/3M-70-Self-Fusing-Silicone-Electrical/dp/B0029Z5RSY) (multiple applications at critical places) at junctions.

**Voltage Divider Circuit:**
From the 10kV initial voltage, we need the following discrete voltage steps according to the electron column design:

- -5000V
- -5100V
- -6500V
- -7000V
- 0V (ground)

We can make a voltage divider circuit, as well as add safety features, before we rout the voltage to the einzel lenses, Wehnelt Cylinders, etc. We can actually make one series circuit such that it gives us all of these voltages from 10kV using precisely chosen values of resistors rated for at least 15kV, and at least one diodes for surge protection.


