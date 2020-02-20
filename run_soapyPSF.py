#%%
from soapyPSF import soapyPSF
import numpy as np

# Aperture radius:
RADIUS = 3.9
# Lens focal length (m)
# for f=4.5mm lens:
f = 12.7
# Image half-height (m)
h = 100e-6
# Output image size /2
FOV_PIXELS = 1024

theta = np.arctan(h / f) / np.pi * 180 * 60 * 60  # in arcsec
PIXSCALE = theta / FOV_PIXELS
output_size_data = h * 1e6

#%%
s = soapyPSF()
s.runAOSim(simconfig="sh_8x8_openloop.yaml")

#%%
makePSFInputDict = {"coeffs": 99}
s.makePSF(makePSFInputDict)
s.saveToRSoft(outfile="PSFOut_soapy", size_data=output_size_data)

# #%%
# inputdict = []
# for loopitter in range(0, 2):
#     inputdict.append({"coeffs": loopitter})
# outpath = "/Volumes/silo4/snert/FMF_PL_rsoft/sweep/9_atmos/"
# s.makeMultiplePSFs(
#     inputdict,
#     None,
#     makeBatFile=True,
#     saveAllData=True,
#     outpath=outpath,
#     size_data=output_size_data,
#     indFile="lantern55.ind",
#     outPrefix="soapysim_",
#     numBatfiles=8,
#     trimLeadingCoeffnames="seq",
# )


# %%
