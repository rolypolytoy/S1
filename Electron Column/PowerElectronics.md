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

**Disclaimer:** Do not do anything related to any voltages close to or above mains if your design hasn't been thoroughly vetted by both electrical engineers and electricians, and assembled with full propriety. Don't do anything stupid, for your own sake, and it's always better to have too much clearance distances, put too much tape, use too many safety practices, or just not engage with power electronics than end up dead. Electricity will kill you if you don't respect it, which is why more than half of the design decisions we make are about safety to a pedantic degree. Cheap, low-cost and open-source doesn't mean unsafe or without industry-standard practices. If you don't have power electronics expertise, it's honestly safer to just not mess around with this and look at this as a speculative exercise entirely, because dealing with the power electronics is actually harder than the design process of the electron column just because of how much everything becomes conductor-like at high voltages. Vacuum interiors mitigate this, but you don't design for vacuums but for normal operation because it might be turned on even when it's in air.

## Power Electronics

**[230 VAC to 10kV converter](https://ar.aliexpress.com/item/1005003518403820.html):**
This is a relatively safe and low-cost component used in industry. It has a <2cm discharge distance due to its plastic protection, so we'll keep a 4cm distance for a safety factor of >2X. It's intended to connect with mains, so we'll use a [mains relay](https://www.amazon.in/CLUB-BOLLYWOOD-Channel-Optocoupler-Insulation/dp/B0C2PT1KRB) to enable PWM-pin controlled switching of the mains voltage that powers the 10kV power source, as well as [heat shrink tubes](https://www.amazon.in/Rpi-shop-Polyolefin-Insulated-Multicolour/dp/B08S3TP2Q6) and [mains-rated wiring](https://www.amazon.in/TWC-Lite-Single-Black-Electrical/dp/B0B7GG46KJ) for the pre-AC-to-DC stage. We'll also use [10kV rated wire](https://ar.aliexpress.com/item/1005001839936748.html?gatewayAdapt=glo2ara) post-amplification and keep >2x safety factors in terms of discharge distance from these, as well as [69kV-rated electrical tape](https://www.amazon.in/3M-70-Self-Fusing-Silicone-Electrical/dp/B0029Z5RSY) (multiple applications at critical places) at junctions. The DC power supply allows us to use 0V and -10kV depending on how we set up the polarities, and we'll use exactly this setup for our applications. 

**Voltage Divider Circuit:**
From the 10kV initial voltage, we need the following discrete voltage steps according to the electron column design:

- 0V, or the positive terminal proper, routed to the anode, the walls, and the side electrodes in the einzel lenses
- -5000V, routed to the cathode
- -5100V, routed to the Wehnelt cap
- -6500V, routed to the objective lens' middle electrode
- -7000V, routed to the condenser lens' middle electrode
  
We can make a voltage divider circuit, as well as add safety features, before we rout the voltage to the einzel lenses, Wehnelt Cylinders, etc. We can actually make one series circuit such that it gives us all of these voltages from 10kV using precisely chosen values of resistors, and at least one diode for surge protection. We need to make sure to properly tape the 3M electrical around all the resistors and the active to ensure absolutely no discharge happens, but though we've accounted for safe practices, we need to obtain the resistors and make a valid diagram for it.

In other words, from -10kV we need to first subtract 3000V, then 500V, then 1400V, then 100V, then 5000V, and so we need these ratios in Ohms from 15kV-rated resistors. We need 30:5:14:1:50 ratio resistors, in other words. If we use 1% tolerance resistors at high resistance values in the megaohm range to limit power to below the 0.25W per resistor limit as well as use resistance values commonly found in the ubiquitous [metal-film-oxide resistor kits](https://www.amazon.in/AVS-Components-Tolerance-Assortment-Electronics/dp/B0D6LRXK5P). Make sure to get the 1% tolerance variants, though, and post-assembly to wrap this with the 3M silicone electrical tape for proper insulation.

Kits commonly have 1 MOhm, 2MOhm, 4.7MOhm and 5.6MOhm values of resistors as well as some other common values, which are all the building blocks we'll use. You can build a 15 MOhm resistor by adding  1 5.6 MOhm and 2 4.7 MOhm resistors in series, which is a bit tedious but honestly not tremendously so. You can then build a 2.5 MOhm resistor with a 2 MOhm resistor, 2 150kOhm resistors, and 2 100kOhm resistors. A 7 MOhm resistor with 3 2 MOhm resistors and 1 MOhm resistor. A 0.5 MOhm resistor using a 470kOhm and 2 15 kOhm resistors. Finally, one 25 MOhm resistor using 2 4.7 MOhm resistors, 1 5.6MOhm resistor, and 5 2 MOhm resistors. I'd recommend first creating the geometry of them, [soldering](https://www.amazon.in/Electronic-Spices-Starter-60watt-Soldering/dp/B098XTZJYQ) them together with a high-quality [tin solder](https://www.amazon.in/Solder-Soldering-Electronic-Electrical-Components/dp/B0B3D8NLMB). The net current will be 10kV/54.5 MOhm = 183.49 µA, with the power dissipation across the most energetic resistor of $$V^2/R = (183.49 microamps * 5.6 MOhm)^2/50 Mohm) = 0.021 Watts$$ which is well, well below their operating limit of 0.25W. We've also created bleeding across all of this, which is tremendously good practice for power electronics because nor electrostatic lenses, nor accelerating electrodes require particularly high operating currents, and >100 microamperes is more than enough for functional operation. 

Wire it such that the arrangement is -10kV terminal -> 15 MOhm -> 2.5 MOhm -> 7 MOhm -> 0.5 MOhm -> 25 MOhm -> 0V terminal in a series circuit, with the voltage divider looking like:

![circuit (6)](https://github.com/user-attachments/assets/8271819e-8a73-4d14-948c-81e136f0b9ac)<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Circuit Diagram, cdlibrary.dll 4.0.0.0 -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" width="320" height="360" xmlns="http://www.w3.org/2000/svg">
	<text x="238" y="320" style="font-family:Arial;font-size:12px;text-anchor:start" dominant-baseline="middle" transform="rotate(0, 238, 320)">0V</text>
	<line x1="220" y1="320" x2="227" y2="320" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="230" cy="320" rx="3" ry="3" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<text x="238" y="270" style="font-family:Arial;font-size:12px;text-anchor:start" dominant-baseline="middle" transform="rotate(0, 238, 270)">-5kV</text>
	<line x1="220" y1="270" x2="227" y2="270" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="230" cy="270" rx="3" ry="3" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<text x="238" y="210" style="font-family:Arial;font-size:12px;text-anchor:start" dominant-baseline="middle" transform="rotate(0, 238, 210)">-5.1 kV</text>
	<line x1="220" y1="210" x2="227" y2="210" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="230" cy="210" rx="3" ry="3" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<text x="238" y="150" style="font-family:Arial;font-size:12px;text-anchor:start" dominant-baseline="middle" transform="rotate(0, 238, 150)">-6.5kV</text>
	<line x1="220" y1="150" x2="227" y2="150" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="230" cy="150" rx="3" ry="3" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<text x="238" y="90" style="font-family:Arial;font-size:12px;text-anchor:start" dominant-baseline="middle" transform="rotate(0, 238, 90)">-7kV</text>
	<line x1="220" y1="90" x2="227" y2="90" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="230" cy="90" rx="3" ry="3" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<line x1="140" y1="90" x2="220" y2="90" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="150" x2="220" y2="150" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="210" x2="220" y2="210" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="270" x2="220" y2="270" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="320" x2="220" y2="320" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="50" y1="320" x2="140" y2="320" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="50" y1="200" x2="50" y2="320" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="50" y1="30" x2="140" y2="30" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="50" y1="30" x2="50" y2="150" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="270" x2="140" y2="275" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="315" x2="140" y2="320" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 140,275 L 140,277 L 133,280 L 147,286 L 133,292 L 147,298 L 133,304 L 147,310 L 140,313 L 140,315" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<text x="126" y="295" style="font-family:Arial;font-size:11px;text-anchor:end" dominant-baseline="middle" transform="rotate(0, 126, 295)">25 MΩ</text>
	<line x1="140" y1="210" x2="140" y2="220" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="260" x2="140" y2="270" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 140,220 L 140,222 L 133,225 L 147,231 L 133,237 L 147,243 L 133,249 L 147,255 L 140,258 L 140,260" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<text x="126" y="240" style="font-family:Arial;font-size:11px;text-anchor:end" dominant-baseline="middle" transform="rotate(0, 126, 240)">500 kΩ</text>
	<line x1="140" y1="140" x2="140" y2="155" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="195" x2="140" y2="210" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 140,155 L 140,157 L 133,160 L 147,166 L 133,172 L 147,178 L 133,184 L 147,190 L 140,193 L 140,195" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<text x="126" y="175" style="font-family:Arial;font-size:11px;text-anchor:end" dominant-baseline="middle" transform="rotate(0, 126, 175)">7 MΩ</text>
	<line x1="140" y1="90" x2="140" y2="95" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="135" x2="140" y2="140" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 140,95 L 140,97 L 133,100 L 147,106 L 133,112 L 147,118 L 133,124 L 147,130 L 140,133 L 140,135" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<text x="126" y="115" style="font-family:Arial;font-size:11px;text-anchor:end" dominant-baseline="middle" transform="rotate(0, 126, 115)">2.5 MΩ</text>
	<line x1="140" y1="30" x2="140" y2="40" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<line x1="140" y1="80" x2="140" y2="90" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 140,40 L 140,42 L 133,45 L 147,51 L 133,57 L 147,63 L 133,69 L 147,75 L 140,78 L 140,80" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<text x="126" y="60" style="font-family:Arial;font-size:11px;text-anchor:end" dominant-baseline="middle" transform="rotate(0, 126, 60)">15 MΩ</text>
	<line x1="50" y1="200" x2="50" y2="191" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="50" cy="175" rx="16" ry="16" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<line x1="50" y1="159" x2="50" y2="150" style="stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<path d="M 50,175 M 50,185 L 50,177 M 46,181 L 54,181 M 46,167 L 54,167" style="fill-opacity:0;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-linecap:square;stroke-width:2" />
	<ellipse cx="140" cy="90" rx="2" ry="2" style="fill-opacity:1;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<ellipse cx="140" cy="150" rx="2" ry="2" style="fill-opacity:1;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<ellipse cx="140" cy="210" rx="2" ry="2" style="fill-opacity:1;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<ellipse cx="140" cy="270" rx="2" ry="2" style="fill-opacity:1;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
	<ellipse cx="140" cy="320" rx="2" ry="2" style="fill-opacity:1;fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);stroke-width:2" />
</svg>

This is pretty good.

