# S1 Desktop SEM

**S1** is an open-source, low-cost scanning electron microscope (SEM) project designed to bring formal engineering rigor and scientific accuracy to the DIY SEM space. Inspired by [Applied Science's DIY SEM](https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s), S1 aims to create a reproducible, scientifically valid, and affordable SEM for under **$2200 USD**—making nanoscale imaging accessible to researchers, educators, and advanced hobbyists.

---

## System Overview

S1 is composed of four core modules:

### Vacuum Integrity
- Fully functional high-vacuum system.
- Custom diffusion pump design and integration with COTC rotary vane pumps.
- CAD files and instructions available at: [Diffusion Pump GitHub Repo](https://github.com/rolypolytoy/diffusion_pump)

### Electron Column
- Simulated and finalized using the open-source electrodynamics package [Picht](https://github.com/rolypolytoy/picht/blob/main/examples/sem.py).
- Includes a design for micron-level spot sizes using Wehnelt caps, an electrostatic objective lens, and an electrostatic condenser lens, using full relativistic accuracy and Lorentz force calculations.

### Detection, Control, and Embedded Systems
A  low-cost detector system is under development:

- **Microcontroller**:  
  - Teensy 4.1 (no electrolytic capacitors, which make it safe for vacuum pressures)
  - Adequate computing power for onboard signal processing, like frame averaging or deconvolution.
  - Works with the Arduino framework which makes coding for it a lot easier.

- **Detector**:  
  - Plastic scintillator with 425 nm emission (AliExpress)
  - Onsemi SiPM with 420 nm peak sensitivity (perfect match)

- **Amplification & Shaping**:  
  - **Cremat CR-110** charge-sensitive preamplifier (µs-long pulses, 7 ns rise time) to read current from the silicon photomultiplier  
  - **Cremat CR-200-500ns** pulse shaper (500 ns pulses) so the ADC can read from it

- **Data Acquisition**:  
  - 10 MSPS ADC (exceeds the 2 MSPS requirement for 500 ns pulses)

- **Raster Scanning**:  
  - ±10V, 16-bit DAC for analog control  
  - Electrostatic deflection plates for beam movement and magnification

All component datasheets and the full bill of materials are included in this repository.

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
| Vacuum and column design complete   | ✅ Q1 2025   |
| **Release-ready version**           | 🟡 **Q2 2025** |
---

## Estimated Cost

A preliminary bill of materials puts the total project cost at approximately **$2200 USD**, including:

- High vacuum components
- Beam optics
- Detector electronics
- Embedded control system
- Mechanical frame and assembly

---

## Why S1 Is Different

Unlike other DIY SEMs, S1 is:

- Based on first-principles simulations (via Picht), which is a standard step in industrial prototyping and experimental physics research.
- Built with modular, reproducible hardware rather than eBay-lifted used parts, or exclusive enterprise hardware. This enables reproducibility, performance, and low cost, a difficult trifecta to nail for both DIY-ers and commercial vendors.
- Fully documented with CAD, BOMs, control logic, and code.
- Designed for educational and research-grade applications.

---

_This is a work-in-progress. Contributions, feedback, and collaborations are welcome._

