# S1 Desktop SEM

S1 is an open-source, low-cost scanning electron microscope (SEM) project designed to bring formal engineering rigor and scientific accuracy to the DIY SEM space. Inspired by [Applied Science's DIY SEM](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s), S1 aims to create a reproducible, scientifically valid, and affordable SEM for under $2500 USD, to make nanocharacterization accessible to audiences that weren't able to before. Current finite difference method calculations estimate a 740 nm beam spot size with off-the-shelf components, with sub-500nm resolution as an entirely possible goal when combining DSP methods like deconvolution, frame averaging, and good practices during raster scanning.

Because Picht already supports ions, and because making [custom field-emission tips](https://link.springer.com/article/10.1007/s42452-020-3017-4) is an established process in the scientific open source community, the established hardware processes shown here can very easily be extended to FIB systems, or dual-beam systems with minimal overhead- a mild overhaul in voltages of the einzel lenses, recalculations using Picht, and new engineering for the liquid ion or gas ion source is all that's required, so this project is already building the foundations for an entire nanofabrication platform. You can, for example, for an FIB system, simply lift all the embedded systems hardware, ion column CAD files, and vacuum integrity modules. All you need to do is remove the ET detector and all the frills, replace the tungsten thermionic electrode with a Gallium LMIS or Helium GFIS source (not difficult to make in CAD) and remanufacture.

| Metric            | Estimated     | Achieved | Method                  |
| ----------------- | ---------- | -------- | ----------------------- |
| Beam Spot Size    | <750 nm     | TBD      | Picht calculations for 67x demagnification between crossovers, Pt-Ir 50 μm beam limiting aperture at crossover |
| Vacuum Pressure   | <10⁻⁵ Torr | TBD      | 1e-8 mbar vapor-pressure vacuum oil ([Ultragrade 19](https://www.ajvs.com/edwards-ultragrade-19-hydrocarbon-vacuum-pump-oil-15494)), HV Diffusion Pump      |
| Resolution        | <500 nm       | TBD      | Deconvolution, frame-averaging, contrast-based autofocus, and digital signals processing (DSP)      |

---

## System Overview

S1 is composed of four core modules:

### [Vacuum Integrity](https://github.com/rolypolytoy/diffusion_pump)
- Fully functional high-vacuum system.
- Custom diffusion pump design and integration with COTC rotary vane pumps.
- Image of CAD files:
  
![View](https://github.com/user-attachments/assets/2c7445c5-50e3-48b4-bc69-a5a0268d8c9f)

The C-bend in the flange is in the stead of an optical baffle- the oil vapors will condense inside the pipe rather than go inside the chamber. This is a minor risk and it's not often mitigated in prototype designs, but I've mitigated it by adding it into the piping rather than an entirely separate component.

### [Electron Column](https://github.com/rolypolytoy/S1/blob/main/Electron%20Column/PowerElectronics.md)
- Simulated and finalized using the open-source electrodynamics package [Picht](https://github.com/rolypolytoy/picht/blob/main/examples/sem.py) (which I made!).
- Includes a design for micron-level spot sizes using Wehnelt caps, an electrostatic objective lens, and an electrostatic condenser lens, using full relativistic accuracy and Lorentz force calculations.
- Image of electrons inside the column design (visualized by Picht):
![SEM](https://github.com/user-attachments/assets/8e4bc3db-832a-4892-869d-d16839526ebe)

You can vividly see how the condenser lens converges the diverging beam, and the objective lens produces a focal point ~8 mm beyond its end.
I also used picht to identify that the demagnification between the first and second crossover is approximately 67x, with the first crossover being 4000 micrometers in diameter and the second being 60 micrometers. This means with a 50 micrometer beam-limiting aperture from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/aperture2.aspx) (for less than $80!), you can get 50/67 = 0.74 micrometers of a spot size, or nanometer-level resolution. We might use a larger beam limiting aperture for greater luminosity, but then again, we might not. A radially zoomed-in image better displays how we identified this relationship, and how we precisely identified the crossover point between the two lenses.

![focus](https://github.com/user-attachments/assets/5d8518e4-04b8-4677-aba3-23a68ba41b8d)

We also have a fully functional voltage divider to get from -10kV and 0V to: -7kV, -6.5kV, -5.1kV, -5kV, and 0kV, all the discrete voltage steps required to safely operate the cathode/anode acceleration, and the voltages for the einzel lenses, with proper [power electronics practices](https://github.com/rolypolytoy/S1/blob/main/Electron%20Column/README.md). The voltage divider looks like this:

![circuit (6)](https://github.com/user-attachments/assets/aad040da-3408-4a23-998c-13119db33bba)

And can be made with the cheaply available 1% tolerance multi-resistor kits while falling entirely within their power consumption limits, as well as adds bleeder-resistor-safety natively by using multi-megaohm resistance values to limit currents to the microampere regime.


### Detection, Control, and Embedded Systems
A  low-cost Everhart-Thornley detector is outlined below:

- **Microcontroller**:  
  - [Teensy 4.1](https://www.amazon.in/4-1-iMXRT1062-Development-soldered-Pre-soldered/dp/B0DP6M197Q) (no electrolytic capacitors, which make it safe for vacuum pressures due to no outgassing or capacitor ruptures)
  - Adequate computing power for onboard signal processing, like frame averaging or deconvolution.
  - Works with the Arduino framework which makes coding for it a lot easier.

- **Detector**:  
  - [Plastic scintillator with 425 nm emission](https://www.alibaba.com/product-detail/Polystyrene-Plastic-scintillator-material-equivalent-EJ_1601298622046.html?spm=a2700.7724857.0.0.6c196c9eovIgdM)
  - [Onsemi SiPM with 420 nm peak sensitivity](https://www.mouser.in/ProductDetail/onsemi/MICROFC-30020-SMT-TR1?qs=byeeYqUIh0PslEkIwO7UpQ%3D%3D)

- **Amplification & Shaping**:  
  - **[Cremat CR-110](https://www.amazon.ae/CR-113-R2-1-Charge-Sensitive-preamplifier-Module/dp/B07BCQSBD8)** charge-sensitive preamplifier (µs-long pulses, 7 ns rise time) to read current from the silicon photomultiplier  
  - **[Cremat CR-200-500ns](https://www.amazon.ae/Cremat-Inc-CR-200-500ns-R2-1-Shaping-Amplifier/dp/B07BD28Y7R?)** pulse shaper (500 ns pulses) so the ADC can read from it

- **Data Acquisition**:  
  - The [AD7626BCPZ](https://www.mouser.in/ProductDetail/Analog-Devices/AD7626BCPZ-RL7?qs=%2FtpEQrCGXCwjx1S0Wpoj8A%3D%3D)- a 10 MSPS ADC (exceeds the 2 MSPS requirement for 500 ns pulses, with roughly 5 samples/pulse- good for SNR)

- **Raster Scanning**:  
  - The [AD5754BREZ](https://www.mouser.in/ProductDetail/Analog-Devices/AD5754BREZ?qs=NmRFExCfTkE9WVZYrblgWQ%3D%3D)- a ±10V, 16-bit quad-channel DAC for analog control of the XY raster scan patterns
  - Electrostatic deflection plates for beam movement and magnification

All [component datasheets](https://github.com/rolypolytoy/S1/tree/main/Detection%20%26%20Control) and the full [bill of materials](https://github.com/rolypolytoy/S1/blob/main/Bill%20of%20Materials.docx) are included in this repository.

### Frame, Stage, and CAD
- In progress.
- Parametric CAD models underway for:
  
  - **Mechanical frame**:
    - The assembly is really just going to be a few 15 mm-thick 6063 plates screwed together in HV-safe methods. Full assembly instructions for this coming soon.
      
  - **Sliding vacuum doors**:
    - We plan to use dovetail doors and use a line of Viton at the base + a clamp to make a secure, cheap, and professional HV sliding door. CAD files for this coming soon.
      
  - **Cable feedthroughs**:
    -   Our current approach to making flanges is to, when the frame is being machined, make precise holes in the exterior, pass silicone wires through, and use vacuum-tolerant epoxy. This is expensive, but believe it or not, significantly less expensive than buying feedthroughs for 230VAC, 24VDC, USB, etc, etc. We use [Loctite Stycast-2850](https://in.rsdelivers.com/product/loctite/loctite-stycast-2850-ft-quartkit/loctite-loctite-stycast-2850-ft-quartkit-black-1/2349630)- a state of the art vacuum epoxy, which means this "makeshift" setup is actually more than satisfactory for HV, and really only gets iffy when you get down to UHV. Additionally- silicone doesn't outgas a lot, so using silicone-insulated wires isn't a no-no, but even if it is, taping over it with PTFE tape is an extremely easy (and cheap) workaround which doesn't compromise anything, or introduce any irregularities into the system.
  
  - **Stage platform**:
    - We use a cheap but micron-level accuracy open-loop stage by buying 3 instances of these [1-axis CNC stepper motor setups with 50 mm stroke length](https://ar.aliexpress.com/item/1005007308081154.html), combining it with three instances of the legendary [TM2209 motor driver](https://www.amazon.in/TESSERACT-TMC2209-V2-0-Ultra-Silent-Motherboard/dp/B08QPLL28G) which has 1/256 microstepping, which means we get micron-level resolution in XYZ. This is particularly important for beam clarity because this means we can use autofocus and vary the z-axis, instead of needing to vary the voltage to the objective lens, which makes our power electronics considerably simpler because we can just use static voltage dividers for all our high-voltage components and implement autofocus by modifying the z-axis and checking if the image is in-focus or out of focus.
      
  - Mounting hardware
 
---

## Development Timeline

| Milestone                            | Target Date |
|-------------------------------------|-------------|
| Vacuum, column & ET-Detector design complete   | ✅ Q1 2025   |
| **Release-ready version**           | 🟡 **Q2 2025** |
---

## Estimated Cost

A preliminary bill of materials puts the total project cost at approximately $2200 USD, including:

- High vacuum components
- Beam optics
- Detector electronics
- Embedded control system
- Mechanical frame and assembly

The main cost-savers were making a custom diffusion pump design rather than lifting turbomol pumps from eBay- which also does wonders for reproducibility- as well as using electrostatic lenses rather than electromagnetic lenses, using tungsten thermionic sources, and perhaps most importantly using silicon photomultipliers instead of vacuum-tube photomultipliers. Each one of these changes reduces hundreds, thousands, or tens of thousands of dollars in unit costs using technological advances, without even compromising on performance. We also use only one secondary electron detector instead of SE, BSE, and a lot of redundant detectors. This allows us to make it cheap and high-quality, while still providing feature-complete, crisp imaging.

---
## Checklist of What Remains
Here's what I still need to implement:

- Circuit diagrams for all electrically active component including the electron column and all embedded systems and embedded-adjacent materials.
- Functioning code for the microcontroller to run on, and a companion desktop app that integrates with any OS (I don't want a repeat of the "we keep this terminal on Windows 97" that's common in SEM labs)
- CAD and Assembly files for the mechanical portions
- Assembly and proof of functionality.

---
## Why S1 Is Different

Unlike other DIY SEMs, S1 is:

- Based on first-principles simulations (via Picht), which is a standard step in industrial prototyping and experimental physics research.
- Built with reproducible hardware rather than eBay-lifted parts, or exclusive enterprise hardware. This enables reproducibility, performance, and low cost, a difficult trifecta to nail for both DIY-ers and commercial vendors.
- Fully documented with CAD, BOMs, control logic, and code.
- Designed for educational and research-grade applications rather than seeing whether a DIY SEM can be made, which is a question that's already been answered.
