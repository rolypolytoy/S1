# S1 Desktop SEM
S1 is an open-source, low-cost scanning electron microscope (SEM) project that builds upon DIY efforts with formal engineering principles. It aims to create a reproducible, scientifically accurate SEM that costs under $2500 USD—making nanoscale imaging accessible to researchers, hobbyists, and educators.

It builds upon Applied Science's DIY SEM (https://www.youtube.com/watch?v=VdjYVF4a6iU&t=467s) to produce a low-cost, reproducible, accurate Desktop SEM using formal engineering practices, computational physics, and a workflow with the rigor of scientific instrumentation without the cost.

## Design

The main four modules that are being designed are:

**Vacuum Integrity:** Complete. Diffusion Pump design and rotary vane pump are fully obtainable, with more complete instructions at https://github.com/rolypolytoy/diffusion_pump.

**Electron Column:** Complete. The actual design of an SEM column is completed at and with the help of Picht (https://github.com/rolypolytoy/picht/blob/main/examples/sem.py).

**Detection, Control and Embedded:** In progress. Datasheets for all components are in the folder. The broad, top-level design is this:
Teensy 4.1 as the MCU. The Teensy 4.1 has no electrolytic capacitors and it's powerful enough for image processing which makes it really good for using in vacuum conditions. Electrolytic capacitors tend to burst under vacuum so the fact that Teensies use only ceramic capacitors is a must-have.
A DIY Everhart-Thornley detector, made by plastic scintillator parts that excite at 425 nm from AliExpress, combined with a onsemi low-noise silicon photomultiplier for single-digit dollars instead of thousands of dollars for a vacuum tube photomultiplier. Its peak excitation voltage is 420 nm, which is nearly perfect for this. I use a Cremat CR-110 charge sensitive preamplifier with microsecond pulses, followed by a CR-200-500ns pulse shaper for 500 nanosecond pulses whenever electrons are detected by it, and I'm using a 10 MSPS ADC to detect this, which is more than the 2 MSPS baseline sampling speed required to detect 500 ns pulses. A +-10V 16-bit DAC will be used for raster scanning, and electrostatic plates will be used to deflect beams in the X and Y direction to provide variable magnification and digital control over the raster scanning.

Datasheets for all the components I've picked are included in the folder, and the bill of materials includes all of these.

**Frame, Stage and CAD:** In progress.

## Assembly
Upcoming. A preliminary bill of materials, with an estimated cost of around $2200 USD is shown.

