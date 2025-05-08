# S1 Desktop SEM

S1 is an open-source, low-cost scanning electron microscope (SEM) project designed to bring formal engineering rigor and scientific accuracy to the DIY SEM space. Inspired by [Applied Science's DIY SEM](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s), S1 aims to create a reproducible, scientifically valid, and affordable SEM for under $2500 USD, to make nanocharacterization accessible to audiences that weren't able to before. Current finite difference method calculations estimate a 740 nm beam spot size with off-the-shelf components, with sub-500nm resolution as an entirely possible goal when combining DSP methods like deconvolution, frame averaging, and good practices during raster scanning.

---

## System Overview

S1 is composed of four core modules:

### Vacuum Integrity
- Fully functional high-vacuum system.
- Custom diffusion pump design and integration with COTC rotary vane pumps.
- CAD files and instructions available at: [Diffusion Pump](https://github.com/rolypolytoy/diffusion_pump)
- Image of CAD files:
![View](https://github.com/user-attachments/assets/2c7445c5-50e3-48b4-bc69-a5a0268d8c9f)

### Electron Column
- Simulated and finalized using the open-source electrodynamics package [Picht](https://github.com/rolypolytoy/picht/blob/main/examples/sem.py) (which I made!).
- Includes a design for micron-level spot sizes using Wehnelt caps, an electrostatic objective lens, and an electrostatic condenser lens, using full relativistic accuracy and Lorentz force calculations.
- Image of electrons inside the column design (visualized by Picht):
![SEM](https://github.com/user-attachments/assets/8e4bc3db-832a-4892-869d-d16839526ebe)

You can vividly see how the condenser lens converges the diverging beam, and the objective lens produces a focal point ~8 mm beyond its end.
I also used picht to identify that the demagnification between the first and second crossover is approximately 67x, with the first crossover being 4000 micrometers in diameter and the second being 60 micrometers. This means with a 50 micrometer beam-limiting aperture from [Ted Pella](https://www.tedpella.com/apertures-and-filaments_html/aperture2.aspx) (for less than $80!), you can get 50/67 = 0.74 micrometers of a spot size, or nanometer-level resolution. We might use a larger beam limiting aperture for greater luminosity, but then again, we might not. A radially zoomed-in image better displays how we identified this relationship, and how we precisely identified the crossover point between the two lenses.

![focus](https://github.com/user-attachments/assets/5d8518e4-04b8-4677-aba3-23a68ba41b8d)


### Detection, Control, and Embedded Systems
A  low-cost Everhart-Thornley detector is outlined below:

- **Microcontroller**:  
  - [Teensy 4.1](https://www.amazon.in/4-1-iMXRT1062-Development-soldered-Pre-soldered/dp/B0DP6M197Q) (no electrolytic capacitors, which make it safe for vacuum pressures)
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
  - Mechanical frame
  - Sliding vacuum doors
  - Cable feedthroughs
  - Stage platform
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

## Why S1 Is Different

Unlike other DIY SEMs, S1 is:

- Based on first-principles simulations (via Picht), which is a standard step in industrial prototyping and experimental physics research.
- Built with reproducible hardware rather than eBay-lifted parts, or exclusive enterprise hardware. This enables reproducibility, performance, and low cost, a difficult trifecta to nail for both DIY-ers and commercial vendors.
- Fully documented with CAD, BOMs, control logic, and code.
- Designed for educational and research-grade applications rather than seeing whether a DIY SEM can be made, which is a question that's already been answered.
