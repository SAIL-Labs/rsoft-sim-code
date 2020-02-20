#%%
import numpy as np
import matplotlib.pyplot as plt

# import zernikePSF.zernikePSF
from zernikePSF import zernikePSF, zernikeoptions

#%%
# At 1550nm, airy radius = l/d = 71 arcsec

# Aperture radius:
RADIUS = 3.5e-3
# Lens focal length (m)
# for f=4.5mm lens:
f = 18e-3
# Image half-height (m)
h = 100e-6
# Output image size /2
FOV_PIXELS = 1024

theta = np.arctan(h / f) / np.pi * 180 * 60 * 60  # in arcsec
PIXSCALE = theta / FOV_PIXELS
output_size_data = h * 1e6
#%%
# coeffs = [20, 0, 0, 0.2, 0.1, 0.05, -0.01, -0.03]  # 'Mixed Zernike Set 01'
coeffs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
np.random.seed(0)
coeffs = np.random.normal(0, scale=0.1, size=16)
z = zernikePSF(radius=RADIUS, pixscale=PIXSCALE, FOV_pixels=FOV_PIXELS)

options = zernikeoptions()
options["show"] = True
options["extraPlots"] = True
type(options)
inputs = {"coeffs": coeffs}
z.makePSF(inputs, options)
z.saveToRSoft(outfile="PSFOut", size_data=output_size_data)

#%%
x = np.matrix(np.identity(10).reshape((10, 10))) * 0.1
coeffsList = x.tolist()
coeffsList.append(np.zeros(10).tolist())
# z.makeMultiplePSFs(coeffsList, makeBatFile=False)

np.random.seed(0)
x = np.matrix(np.random.normal(0, scale=0.1, size=48).reshape(3, 16))
coeffsList = x.tolist()
inputdict = []
for coeffs in coeffsList:
    inputdict.append({"coeffs": coeffs})

outpath = "/Volumes/silo4/snert/FMF_PL_rsoft/test/"
z.makeMultiplePSFs(
    inputdict,
    zernikeoptions(),
    makeBatFile=True,
    saveAllData=True,
    outpath=outpath,
    size_data=output_size_data,
    indFile="lantern55.ind",
    outPrefix="randset_",
    numBatfiles=3,
    trimLeadingCoeffnames="seq",
)
