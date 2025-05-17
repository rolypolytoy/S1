# S1 Desktop SEM

S1 is an open-source, low-cost scanning electron microscope (SEM) project designed to bring formal engineering rigor and scientific accuracy to the DIY SEM space. Inspired by [Applied Science's DIY SEM](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s), S1 aims to create a reproducible, scientifically valid, and affordable SEM for under $2500 USD, to make nanocharacterization accessible to audiences that weren't able to before.

Because Picht already supports ions, and because making [custom field-emission tips](https://link.springer.com/article/10.1007/s42452-020-3017-4) is an established process in the scientific open source community, the established hardware processes shown here can very easily be extended to FIB systems, or dual-beam systems with minimal overhead- a mild overhaul in voltages of the einzel lenses, recalculations using Picht, and new engineering for the liquid ion or gas ion source is all that's required, so this project is already building the foundations for an entire nanofabrication platform. You can, for example, for an FIB system, simply lift all the embedded systems hardware, ion column CAD files, and vacuum integrity modules. All you need to do is remove the ET detector and all the frills, replace the tungsten thermionic electrode with a Gallium LMIS or Helium GFIS source (not difficult to make in CAD) and remanufacture.

| Metric            | Estimated     | Achieved | Method                  |
| ----------------- | ---------- | -------- | ----------------------- |
| Ultimate Resolution    | <1 μm     | TBD      | Picht simulation |
| Vacuum Pressure   | <10⁻⁵ Torr | TBD      | 1e-8 mbar vapor-pressure vacuum oil ([Ultragrade 19](https://www.ajvs.com/edwards-ultragrade-19-hydrocarbon-vacuum-pump-oil-15494)), HV Diffusion Pump      |

---

## System Overview

S1 is composed of four core modules:

### [Vacuum Integrity](https://github.com/rolypolytoy/S1/tree/main/Vacuum%20Integrity)
- Fully functional high-vacuum system.
- Custom diffusion pump design and integration with COTC rotary vane pumps.
- Image of CAD files:
  
![View](https://github.com/user-attachments/assets/2c7445c5-50e3-48b4-bc69-a5a0268d8c9f)

The C-bend in the flange is in the stead of an optical baffle- the oil vapors will condense inside the pipe rather than go inside the chamber. This is a minor risk and it's not often mitigated in prototype designs, but I've mitigated it by adding it into the piping rather than an entirely separate component.

### [Electron Column](https://github.com/rolypolytoy/S1/blob/main/Electron%20Column)
- Simulated and finalized using the open-source electrodynamics package [Picht](https://rolypolytoy.github.io/picht/auto_examples/example_sem_simulation.html#sphx-glr-auto-examples-example-sem-simulation-py).
- Includes a design for micron-level spot sizes using Wehnelt caps, an objective lens, and a condenser lens.
- Image of electrons inside the column design:
![SEM](https://github.com/user-attachments/assets/9d305eb8-6272-438c-818d-5dedf85e9984)
![SEM_E_Field](https://github.com/user-attachments/assets/be48b182-462a-47cc-afe4-e381d410c67e)
![SEM_B_Field](https://github.com/user-attachments/assets/79333714-5cc1-45cf-8f2c-398a004bda60)

### Detection, Control, and Embedded Systems
I'm on this part at the moment. 
A  low-cost Everhart-Thornley detector is outlined below:

- **Microcontroller**:  
  - [Teensy 4.1](https://www.amazon.in/4-1-iMXRT1062-Development-soldered-Pre-soldered/dp/B0DP6M197Q) (no electrolytic capacitors, which make it safe for vacuum pressures due to no outgassing or capacitor ruptures)
  - Adequate computing power for onboard signal processing, like frame averaging or deconvolution.
  - Works with the Arduino framework which makes coding for it a lot easier.

- **Detector Stuff**:  
  - [Plastic scintillator with 425 nm emission](https://www.alibaba.com/product-detail/Polystyrene-Plastic-scintillator-material-equivalent-EJ_1601298622046.html?spm=a2700.7724857.0.0.6c196c9eovIgdM)
  - [Onsemi SiPM with 420 nm peak sensitivity](https://www.mouser.in/ProductDetail/onsemi/MICROFC-30020-SMT-TR1?qs=byeeYqUIh0PslEkIwO7UpQ%3D%3D)
  - [Cremat CR-110](https://www.amazon.ae/CR-113-R2-1-Charge-Sensitive-preamplifier-Module/dp/B07BCQSBD8) charge-sensitive preamplifier (µs-long pulses, 7 ns rise time) to read current from the silicon photomultiplier  
  - [Cremat CR-200-500ns](https://www.amazon.ae/Cremat-Inc-CR-200-500ns-R2-1-Shaping-Amplifier/dp/B07BD28Y7R?) pulse shaper (500 ns pulses) so the ADC can read from it
  - The [AD7626BCPZ](https://www.mouser.in/ProductDetail/Analog-Devices/AD7626BCPZ-RL7?qs=%2FtpEQrCGXCwjx1S0Wpoj8A%3D%3D)- a 10 MSPS ADC (exceeds the 2 MSPS requirement for 500 ns pulses, with roughly 5 samples/pulse- good for SNR)
  - The [AD5754BREZ](https://www.mouser.in/ProductDetail/Analog-Devices/AD5754BREZ?qs=NmRFExCfTkE9WVZYrblgWQ%3D%3D)- a ±10V, 16-bit quad-channel DAC for analog control of the XY raster scan patterns
  - Electrostatic deflection plates for beam movement and magnification
  - Should probably mention what driver I'm going to use for the NEMA 11 motors on the stages and how I'll drive the V_SOURCE for all of these and where the application and .ino code for these is. Coming soon, not to worry.

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
---

## Development Timeline

| Milestone                            | Target Date |
|-------------------------------------|-------------|
| Vacuum, column & ET-Detector design complete   | ✅ Q1 2025   |
| **Release-ready version**           | 🟡 **Q2 2025** |
---

---
## Checklist of What Remains
Here's what I still need to implement:

- Functioning code for the microcontroller to run on, and a companion desktop app that integrates with any OS
- CAD files for the mechanical portions
- Assembly and proof of functionality.
