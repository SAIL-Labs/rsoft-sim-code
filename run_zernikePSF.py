#%%
import numpy as np
import matplotlib.pyplot as plt

# import zernikePSF.zernikePSF
from zernikePSF import zernikePSF

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
z.makeZernikePSF(coeffs=coeffs, show=True, extraPlots=True)
z.saveToRSoft(outfile="PSFOut", size_data=output_size_data)

#%%
x = np.matrix(np.identity(10).reshape((10, 10))) * 0.1
coeffsList = x.tolist()
coeffsList.append(np.zeros(10).tolist())
# z.makeMultiplePSFs(coeffsList, makeBatFile=False)

np.random.seed(0)
x = np.matrix(np.random.normal(0, scale=0.1, size=48).reshape(3, 16))
coeffsList = x.tolist()

outpath = "/Volumes/silo4/snert/FMF_PL_rsoft/sweep/4_random_set/"
z.makeMultiplePSFs(
    coeffsList,
    makeBatFile=True,
    saveAllData=True,
    outpath=outpath,
    size_data=output_size_data,
    indFile="lantern55.ind",
    outPrefix="randset_",
    numBatfiles=3,
    trimLeadingCoeffnames="seq",
)


# # Test restore:
# outpath = '/Users/bnorris/Dropbox/Win-Mac Share/rsoft/19CorePL/scan1/'
# npzfile = np.load(outpath+'testscans2_metadata.npz')


# psf = makeZernikePSF(coeffs=coeffs, show=True)
# psf = makeZernikePSF(show=True, coeffs=np.random.normal(0, scale=0.05, size=8))

# psfImage = psf[0].data

# plt.figure(2)
# poppy.display_psf(psf, normalize='peak', cmap='gist_heat', scale='log', vmin=1e-7, vmax=1)

# psf, wf = makeZernikePSF(coeffs=coeffs, show=True, return_final=True)


# psfImage = psf[0].data
# plt.figure(2)
# plt.clf()
# poppy.display_psf(psf, normalize='peak', cmap='viridis', scale='linear', vmin=0, vmax=1)
#
# plt.figure(3)
# plt.clf()
# plt.subplot(1, 2, 1)
# plt.imshow(wf.amplitude**2)
# plt.title('Amplitude ^2')
# plt.colorbar()
# plt.subplot(1, 2, 2)
# plt.imshow(wf.phase)
# plt.title('Phase')
# plt.colorbar()
# plt.tight_layout()


# %%
