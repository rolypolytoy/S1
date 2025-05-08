# Vacuum Integrity

To reach the <1e-5 torr pressures required to operate a thermionic tungsten source, we need a roughing pump and a high vacuum pump.

Roughing pumps can be bought quite cheaply on amazon for about $70, and can pump down to the 1e-2 torr order of magnitude, which is good enough as a backing pump for most high-vacuum pumps. For example, you can use: https://www.amazon.com/Orion-Motor-Tech-Conditioner-Servicing/dp/B08P1W6Z8D, or just search 'vacuum pump' and look for the micron rating on it. This one is 37.5 microns, which converts to around 3e-2 torr, which is good enough for diffusion pumps.

Most pumps of this kind have an around 1/4th inch diameter outlet, and so you can buy 1/4th inch ID vinyl tubing like at https://www.amazon.com/Flexible-Lightweight-Plastic-Chemical-Resistant/dp/B09Y5R8SSL. 

Finally- FCStd files for the Diffusion Pump are uploaded here and at https://github.com/rolypolytoy/diffusion_pump. It's already built to be integrated with 1/4th inch vinyl pipes, so simply slip the pipe around the machined diffusion pump. 

For the o-ring, buy 130 mm ID, 2 mm thickness O-rings to seal the flange between the diffusion pump and the connector to the vacuum pump. Nitrile should work fine, for example at https://www.amazon.com/uxcell-Rings-Nitrile-125-2mm-Diameter/dp/B07HGCCHNZ.

The holes on the side of the flanges are around 6.4 mm in diameter, so use 8 M6 to tighten, once the O-ring is inside the groove, and the connector has been welded to the frame. 