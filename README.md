# S1 Desktop SEM

S1 is an open-source, low-cost, high-performance scanning electron microscope (SEM) project, which doubles as a reasonably accurate e-beam lithography machine, because why not?

| Metric            | Estimated     | Achieved | Method                  |
| ----------------- | ---------- | -------- | ----------------------- |
| Ultimate Resolution    |<<100nm     | TBD      | Reconstructing the Paper |
| Vacuum Pressure   | <10⁻⁵ Torr | TBD      | HV Diffusion Pump, Embedded Pressure Gauge.|

---

## System Overview

### Vacuum Integrity
![View](https://github.com/user-attachments/assets/2c7445c5-50e3-48b4-bc69-a5a0268d8c9f)

[Roughing pumps](https://www.amazon.com/Orion-Motor-Tech-Conditioner-Servicing/dp/B08P1W6Z8D) can be bought quite cheaply on amazon for about $70, and can pump down to the 1e-2 torr order of magnitude, which is good enough as a backing pump for most high-vacuum pumps. This one is 37.5 microns, which converts to around 3e-2 torr, which is good enough for diffusion pumps.

Most pumps of this kind have an around 1/4th inch diameter outlet, and so you can buy 1/4th inch ID [vinyl tubing](https://www.amazon.com/Flexible-Lightweight-Plastic-Chemical-Resistant/dp/B09Y5R8SSL). 

Finally- FCStd files for the Diffusion Pump are uploaded [here](https://github.com/rolypolytoy/S1/blob/main/Vacuum%20Integrity) and at the [Diffusion Pump](https://github.com/rolypolytoy/diffusion_pump) project. It's already built to be integrated with 1/4th inch vinyl pipes, so simply slip the pipe around the machined diffusion pump. We also use KF25 flanges and conventional water cooling with a pump, to ensure it stays cold.

For the O-ring, buy 130 mm ID, 2 mm thickness [Nitrile O-rings](https://www.amazon.com/uxcell-Rings-Nitrile-125-2mm-Diameter/dp/B07HGCCHNZ) to seal the flange between the diffusion pump and the connector to the vacuum pump.

The holes on the side of the flanges are around 6.4 mm in diameter, so use 8 M6 to tighten, once the O-ring is inside the groove, and the connector has been welded to the frame. 

We'll use the [KJL 704](https://www.agarscientific.com/vacuum-diffusion-pump-fluids) diffusion pump oil for 125.77 pounds from agar scientific, which has an untrapped ultimate vacuum of 1e-7 to 1e-8 torr and trapped of 1e-11 torr. Kurt J Lesker also sells 500 ccs directly for [120 dollars](https://www.lesker.com/newweb/fluids/diffpumpoils-silicone-kjlc/), and so this is really good cost-price.

The nichrome wire I'm using can heat up to 800W so we're good in terms of heating since resistive heating implements are the only implements with 100% efficiency, and 800W is more than enough to heat a diffusion pump of this size and we're using a [server fan](https://www.amazon.in/Delta-Electronics-AFB1212GHE-CF00-120x120x-connector/dp/B004X2M2GG) with 241 CFM- it's noisy but it's better than a water cooling system I know that, so about 200W of dissipation might be viable.

We'll use dovetail sliding doors, nitrile tubing, and screw clamps for the sliding door.

### Embedded Systems

All power sources are kept outside and funneled in- this is because power supplies have electrolytic capacitors that will 100% burst in a vacuum. All our embedded stuff is designed to have none of this.

The power supply comes from mains through a plug, and we have a [10kVDC](https://ar.aliexpress.com/item/1005003518403820.html) power source, as well as a [60VDC](https://www.amazon.in/Adjustable-05-60Volt-Variable-Converter-600Watts/dp/B0F3KJ5VNP) power source that connects w/mains.

- **Microcontroller**:  
  - [Teensy 4.1](https://www.amazon.in/4-1-iMXRT1062-Development-soldered-Pre-soldered/dp/B0DP6M197Q) (no electrolytic capacitors, which make it safe for vacuum pressures due to no outgassing or capacitor ruptures)
  - Works with the Arduino framework with [Teensyduino](https://www.pjrc.com/teensy/td_download.html).

- **Electron Detector**:  
  - [Plastic scintillator with 425 nm emission](https://www.alibaba.com/product-detail/Polystyrene-Plastic-scintillator-material-equivalent-EJ_1601298622046.html?spm=a2700.7724857.0.0.6c196c9eovIgdM). It's a 10mmx10mmx1mm cuboid.
  - [Onsemi SiPM with 420 nm peak sensitivity](https://www.mouser.in/ProductDetail/onsemi/MICROFC-30035-SMT-TR?qs=byeeYqUIh0Mh9KJVNOFZEA%3D%3D). I've taken the CAD file for this and put it in the CAD folder. Its rise time is 0.6nS, and at 420nM it has over 40% of particles detected. It has a 300 ps pulse with a 600 ps pulse width. It has several white papers on its characteristics. In [this one](https://www.onsemi.com/pub/collateral/and9770-d.pdf) we can see its breakdown voltage is ~24.6 V and in [this one](https://www.onsemi.com/download/white-papers/pdf/tnd6262-d.pdf) we can see its recommended overvoltage is 5.0V so 30VDC is a very, very good voltage and we can make it with the 60V power supply with a basic voltage divider. They have either a fast pulse or a normal pulse mode, we'll use normal pulse mode. 
  - [Cremat CR-110](https://www.amazon.ae/CR-113-R2-1-Charge-Sensitive-preamplifier-Module/dp/B07BCQSBD8) charge-sensitive preamplifier (µs-long pulses, 7 ns rise time) to read current from the silicon photomultiplier, and it needs a +-10V (12V total) power supply. The pulses from this are 7ns in terms of rise time and decay slower. 
  - [Cremat CR-200-500ns](https://www.amazon.ae/Cremat-Inc-CR-200-500ns-R2-1-Shaping-Amplifier/dp/B07BD28Y7R?) pulse shaper (500 ns pulses) so the ADC can read from it. Needs the same power as the CR-110. Shapes it into Gaussian pulses and amplifies it a bit more post-CSA so this should be in the hundreds of mV/low V range, but regardless will be within the ADC's 16 bits of range.
  - The [AD7626BCPZ](https://www.mouser.in/ProductDetail/Analog-Devices/AD7626BCPZ-RL7?qs=%2FtpEQrCGXCwjx1S0Wpoj8A%3D%3D)- a 10 MSPS ADC (exceeds the 2 MSPS requirement for 500 ns pulses, with roughly 5 samples/pulse- good for SNR). So, we can quite easily sample at 2MHz with this signal processing pipeline which is good enough for electron microscopy. Uses LVDS so we'll definitely need a chip for it which is [this one](https://www.mouser.in/ProductDetail/Texas-Instruments/DS90CR286ATDGGRQ1?qs=8%2FmU9qzJpL9GnwtExKjdYg%3D%3D). So we have a functional design for an electron detection pipeline at fast enough speeds for our needs.

I'll obviously use a blue LED on the photomultiplier-cremat-ADC setup to see if it works before assembling the ET detector.

Some auxiliary setup information not in the CAD: 
The first two condenser lenses must have 920 turns and the objective lens 600 turns in a solenoidal arrangement inside the housing. 

The EE bit is done, all that remains is the embedded system code & companion app (Teensyduino and QT via PySide6, Pyintaller, PyUSB, PySERIAL on pypi respectively).


### CAD
I found an [old paper](https://github.com/rolypolytoy/S1/blob/main/SEM_Design.pdf) which outlines how to design a 10-nm resolution SEM with exact current, current densities (so of course we can reconstruct the gauge they used, which I did, and it's 14 AWG), condenser 1, 2, and objective lens specs, beam column design, full ray tracing with commercial FEM, and so the design work has been done already. Of course this means all the work we did in the electron column is useless but honestly basically guaranteeing nm-scale resolution is worthwhile. Even if we don't get 10 nm resolution, it's going to get sub-micron resolution. The condenser lens 1 is centered at 80mm below the Wehnelt cap aperture (at 100.45mm). The second condenser lens is centered at 165mm below, or at -64mm-ish. Final focus is at 301mm, and the assembly of the objective lens must end at 290mm. This is all, as per the latest CAD file, is entirely valid and so the dimensions are all entirely correct. 

Additionally I've finished the CAD for the electron column including the Wehnelt cylinder, anodes, and lenses. There wasn't information on the pole piece bore size in the SEM paper so I found a patent for a magnetic lens design and it showed that the normal range was from 1 mm to 3 mm, so I've taken a 4 mm bore diameter for the condenser lenses and 1 mm for the objective lens (US5563415A if you're looking for it, but I have the pdf in the repo regardless). It expired in 2015- [proof here](https://patents.google.com/patent/US5563415A/en?oq=5%2c563%2c415), so we're entirely able to use it. In general there are a lot of US patents on electromagnetic lenses [here](https://patents.google.com/?q=H01J37%2f141).

Another expired patent I found really useful is a full design of an SEM that expired in 1992: [US3924126A](https://patents.google.com/patent/US3924126A/en?q=H01J37%2f141). It's not as useful as the paper because it doesn't include full dimensions, but it's a sanity check and it has some useful information about alignment, some dimensions that weren't mentioned in the paper, and aperture-related info. So, another good source.

For the pole piece: one internal piece, one external piece, attached w/screws. 3A current, 2.8A current, 1.1 A current. 14 AWG wire. Center of condenser lens at 80mm, Focal position 1 at approx. 100mm, Center of Condenser 2 at 164mm, Focal position 2 at approximately 170 mm, center of Objective at 295mm and focal position at 315 mm. 1000 micrometer beam-limiting aperture at 80mm, 100 micrometer beam-limiting aperture at 200mm. Luckily all the apertures are 'inside' the lenses so we don't have to worry about them when constructing the structural parts.

A 500 micrometer aperture as the condenser aperture at 60 mm and a 200 micrometer aperture as the objective aperture at 280 mm.

We also need ~500m of 14 AWG aluminium wire which is either insulated or enameled, for as cheap as possible, which is roughly 14.5 USD, and definitely under 100

Every exterior of the EM lens should be in 4 pieces, and the pole piece as 1. Design the CAD files of these next. Scanning coils (solenoid), stigmators (octupole), and alignment coils (quadrupole) also necessary using 14AWG Al wire where relevant.

For the yoke of the magnetic lenses we'll use electrical steel, and for the pole piece we'll use 99.95% iron (electropolished and nickelplated ofc).

Make a singular CAD Assembly file with all details.

I've fully reconstructed the specs from the paper. Here's an exploded view of all the non-structural components- you can see the housing, pole pieces, Wehnelt caps etc etc:

![image](https://github.com/user-attachments/assets/4a40d4dd-cda8-497b-803c-708da79b92bd)

Non-exploded view of the frame with diffusion pump attached:

![image](https://github.com/user-attachments/assets/2bdacd55-febc-4bbf-9263-7d457ce1202e)

View of all the analog & power electronics via a circuit schematic: 

![Circuit](https://github.com/user-attachments/assets/b6a56f7b-11ab-403d-b466-1370241eb6ef)


This is in the repo as Column.FCStd, of course. All the sizes are exactly as taken down to the mm from the paper, and I've made structural components for everything as well. The baseline weight of the frame is ~32 kg and if made of Al 6061 should cost on the order of $100, and the full frame w/sliding doors (metal to metal seal w/ambient air pressure pushing on it) is in Frame.FCStd.
      
  - **Cable feedthroughs**:
    -   Our current approach to making flanges is to, when the frame is being machined, make precise holes in the exterior, pass silicone wires through, and use vacuum-tolerant epoxy. This is expensive, but believe it or not, significantly less expensive than buying feedthroughs for 230VAC, 24VDC, USB, etc, etc. We use [Loctite Stycast-2850](https://in.rsdelivers.com/product/loctite/loctite-stycast-2850-ft-quartkit/loctite-loctite-stycast-2850-ft-quartkit-black-1/2349630)- a state of the art vacuum epoxy, which means this "makeshift" setup is actually more than satisfactory for HV, and really only gets iffy when you get down to UHV. Additionally- silicone doesn't outgas a lot, so using silicone-insulated wires isn't a no-no, but even if it is, taping over it with PTFE tape is an extremely easy (and cheap) workaround which doesn't compromise anything, or introduce any irregularities into the system.
  
  - **Stage platform**:
    - We use a cheap but micron-level accuracy open-loop stage by buying 3 instances of these [1-axis CNC stepper motor setups with 50 mm stroke length](https://ar.aliexpress.com/item/1005007308081154.html), combining it with three instances of the legendary [TM2209 motor driver](https://www.amazon.in/TESSERACT-TMC2209-V2-0-Ultra-Silent-Motherboard/dp/B08QPLL28G) which has 1/256 microstepping, which means we get micron-level resolution in XYZ. This is particularly important for beam clarity because this means we can use autofocus and vary the z-axis, instead of needing to vary the voltage to the objective lens, which makes our power electronics considerably simpler because we can just use static voltage dividers for all our high-voltage components and implement autofocus by modifying the z-axis and checking if the image is in-focus or out of focus. 

In-House Manufacturing for Al 6061 parts (via manual milling and lathes, for critical vacuum chamber bits sanding with 220 to 3000-grit), Polypropylene (via manual milling and lathing with up to 2000 grit), Soft Iron Yokes (via manual milling and lathing, surface finishing with 220 to 2000 grit), Pole Pieces from 99.95% iron (manual milling/lathing, then electropolishing then nickel plating). Before and after assembly clean everything with isopropyl then acetone, in a cleanroom-esque environment with nitrile gloves and basic PPE.


29/5/2025: I've begun looking for the 500 meters of 14/16 AWG Aluminium wire and the CAD components. Stuff's coming together. I'll keep updating this when there's more progress on this end. From what I can tell, getting electropolishing and nickel plating isn't going to be particularly challenging and since our tolerances are more surface finishes than actual manufacturing tolerances it's going to be easy enough to do 'in house'.

30/5/2025: Ordered every non-structural component, will see how things begin to come together. Ultimately, went easier than I expected. Thanks Agar Scientific, Mouser, Amazon, and AliExpress. Still need to find a supplier for 3N-4N soft iron and 500 meters of aluminum wire. I talked to a guy who sells the latter and he laughed me out for such a 'small quantity' asking me to get at least 50 kg (read: 10 km of wire) or not waste his time. You win some, you lose some. I'll provide updates as everything comes in.

31/5/2025: Teensy 4.1's already arrived, as have a few other miscellaneous things. It's fortuitous it arrived so quickly because it means I can troubleshoot my setup and understand the flow of this MCU well. I already have an Arduino kit, I'll solder headers onto it and in general prepare for the full setup prematurely.

12/6/2025: Several things have arrived. All the 3D printed parts are fabricated to within tolerances. The 10kV HV sources have also arrived, as have the ADC, DAC, SiPM, and Cremat signals processing modules. Still no electrical steel, but we've found a supplier for 500 meters of copper wire and ~200 meters have already arrived, with 300 more to go. Soft iron's also found (4N, from AliExpress once more). Progress is progressing.

19/6/2025: We're using soft iron ingots and melting and casting them, so the final supplier issue (on the materials side) is done, and we're officially to assembly. Like a hydra though, there's another issue- the Cremat CR-113 hasn't shipped and they've refunded it, and only the CR-200-500ns has shipped. So we're going to have to make a CSA with an op-amp in a differentiator setup in an SIP package. Doable with KiCAD, and it'll honestly be lower cost and higher perf, so I'm glad it happened. Maybe I'll remake the CSA + pulse shaper in one package, or make a full MCU + signals processing PCB instead of the whole Teensy, DAC, ADC, SiPM, signals processing as modules thing. For a prototype a difficult setup is fine but for production, definitely not. In more good news though- DRDO's [SSPL](https://www.drdo.gov.in/drdo/labs-and-establishments/solid-state-physics-laboratory-sspl), a SOTA government research laboratory in materials science, and Miranda House from Delhi University, are tentatively going to be beta-testers for it when the prototype is assembled, so there's already some steady footing in that direction.

5/7/2025: Bled over into early Q3 2025, which is unfortunate. But the frame is made! Onto machining the internals and assembling the embedded systems stuff. Looks really good so far. Fixed the Cremat CR-113 issue- made a bespoke CSA with 750x higher gain (better for low-current filaments) and half the cost of the 113. I call it [Lightning In A Bottle](https://github.com/rolypolytoy/lightning-in-a-bottle) because it's really good (the op-amp I used is the best on the market), cheaper than the CR-113 by >50%, and bottling charge is basically exactly what a charge integrator is. It's a better name than Cremat anyways. It's already ordered and should arrive in under 2 weeks from PCBPower, they've got all the parts on hand so no waiting around. I also learnt analog design as a side quest so it's probably good that Cremat refunded me.

---

## Development Timeline

| Milestone                            | Target Date |
|-------------------------------------|-------------|
| Full design complete   | ✅ Q1 2025   |
| **Release-ready version (BEHIND TARGET!!!! WE NEED TO GRIND!!!!!!!!)**           | 🟡 **Q2 2025** |
---

---
## Assembly Instructions

I'll update this with photos and instructions the further I get along in the process.

SEM frame:
![SEM](https://github.com/user-attachments/assets/1885e2d8-4cab-4043-ba80-9ec8d7d393e2)

3D printed parts:

![1000135306](https://github.com/user-attachments/assets/020caf3e-acb4-474d-b333-ca8ebe55a649)

- Machine it and get it functioning
- Get e-beam lithography tested and functional to <25 nm resolution.
