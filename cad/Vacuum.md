# Vacuum Integrity

To reach the <1e-5 torr pressures required to operate a thermionic tungsten source, we need a roughing pump and a high vacuum pump.

[Roughing pumps](https://www.amazon.com/Orion-Motor-Tech-Conditioner-Servicing/dp/B08P1W6Z8D) can be bought quite cheaply on amazon for about $70, and can pump down to the 1e-2 torr order of magnitude, which is good enough as a backing pump for most high-vacuum pumps. This one is 37.5 microns, which converts to around 3e-2 torr, which is good enough for diffusion pumps.

Most pumps of this kind have an around 1/4th inch diameter outlet, and so you can buy 1/4th inch ID [vinyl tubing](https://www.amazon.com/Flexible-Lightweight-Plastic-Chemical-Resistant/dp/B09Y5R8SSL). 

Finally- FCStd files for the Diffusion Pump are uploaded [here](https://github.com/rolypolytoy/S1/blob/main/Vacuum%20Integrity/DiffusionPump.FCStd) and at the [Diffusion Pump](https://github.com/rolypolytoy/diffusion_pump) project. It's already built to be integrated with 1/4th inch vinyl pipes, so simply slip the pipe around the machined diffusion pump. 

For the O-ring, buy 130 mm ID, 2 mm thickness [Nitrile O-rings](https://www.amazon.com/uxcell-Rings-Nitrile-125-2mm-Diameter/dp/B07HGCCHNZ) to seal the flange between the diffusion pump and the connector to the vacuum pump.

The holes on the side of the flanges are around 6.4 mm in diameter, so use 8 M6 to tighten, once the O-ring is inside the groove, and the connector has been welded to the frame. 

To do: improve diffusion pump design, ensure nichrome wire can do 1kW of power and heat it enough for truly good pumping, and have the inverted u-shape and DFM for the pump. I.e. design the cylinder to be holed + screwed rather than anything else and machine/attach the U-bend bit separately.
