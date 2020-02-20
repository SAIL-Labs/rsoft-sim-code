import logging
import poppy
import numpy as np
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
import scipy.io as sio

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
from make_rsoft_fld_batch import RSOFTPSF

# logging.basicConfig(level=logging.DEBUG)


class zernikeoptions(dict):
    def __init__(self):
        self["show"] = False
        self["units"] = "microns"
        self["extraPlots"] = False


class zernikePSF(RSOFTPSF):
    def __init__(self, radius=1.0, wavelength=1500e-9, pixscale=0.01, FOV_pixels=128):
        # RADIUS = 1.0 # meters
        # WAVELENGTH = 1500e-9 # meters
        # PIXSCALE = 0.01 # arcsec / pix
        # FOV = 1 # arcsec
        # NWAVES = 1.0
        # FOV_PIXELS = 128
        self.radius = radius
        self.wavelength = wavelength
        self.pixscale = pixscale
        # self.FOV = 1
        self.FOV_pixels = FOV_pixels

    def makePSF(self, makePSFInputDict: dict, makePSFOptions: zernikeoptions):
        coeffs = makePSFInputDict["coeffs"]
        show = makePSFOptions["show"]
        units = makePSFOptions["units"]
        extraPlots = makePSFOptions["extraPlots"]

        if units is "microns":
            coeffs = np.asarray(coeffs) * 1e-6

        osys = poppy.OpticalSystem()
        circular_aperture = poppy.CircularAperture(radius=self.radius)
        osys.add_pupil(circular_aperture)
        thinlens = poppy.ZernikeWFE(radius=self.radius, coefficients=coeffs)
        osys.add_pupil(thinlens)
        # osys.add_detector(pixelscale=self.pixscale, fov_arcsec=self.FOV)
        osys.add_detector(pixelscale=self.pixscale, fov_pixels=self.FOV_pixels)

        if extraPlots:
            plt.figure(1)
        # psf_with_zernikewfe, final_wf = osys.calc_psf(wavelength=self.wavelength, display_intermediates=show,
        #                                               return_final=True)
        psf_with_zernikewfe, all_wfs = osys.calc_psf(
            wavelength=self.wavelength,
            display_intermediates=show,
            return_intermediates=True,
        )
        final_wf = all_wfs[-1]
        pupil_wf = all_wfs[1]

        if extraPlots:
            psf = psf_with_zernikewfe
            psfImage = psf[0].data
            # plt.figure(2)
            # plt.clf()
            # poppy.display_psf(psf, normalize='peak', cmap='viridis', scale='linear', vmin=0, vmax=1)
            plt.figure(3)

            wf = final_wf
            wf = pupil_wf

            plt.clf()
            plt.pause(0.001)
            plt.subplot(1, 2, 1)
            plt.imshow(wf.amplitude ** 2)
            plt.title("Amplitude ^2")
            plt.colorbar()
            plt.subplot(1, 2, 2)
            plt.imshow(wf.phase)
            plt.title("Phase")
            plt.colorbar()
            plt.tight_layout()
            poppy.display_psf(psf_with_zernikewfe, title="PSF")

        self.psf = psf_with_zernikewfe
        self.wf = final_wf
        self.complex_psf = self.wf.amplitude * np.exp(1j * self.wf.phase)
        self.osys_obj = osys
        self.pupil_wf = pupil_wf

    def makeCoeffsRange(self, input=None):
        # Input is tuple (no., start, end, numsteps)
        if input is None:
            print("0: Piston")
            print("1: Tip")
            print("2: Tilt")
            print("3: Defocus")
            print("4: Astig 1")
            print("5: Astig 2")
            print("6: Coma 1")
            print("7: Coma 2")
            print("8: Trefoil 1")
            print("9: Trefoil 2")
            print("10: Spherical")
            return

        nsteps = input[3]
        curCoeff = np.linspace(input[1], input[2], nsteps)
        coeffsList = []
        maxCoeffs = input[0] + 1
        for k in range(input[3]):
            cur = np.zeros(maxCoeffs)
            cur[input[0]] = curCoeff[k]
            coeffsList.append(cur)

        return coeffsList

