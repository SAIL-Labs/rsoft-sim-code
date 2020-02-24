import matplotlib.pyplot as plt
import numpy as np
from hcipy import *

from make_rsoft_fld_batch import RSOFTPSF


class hcipyPSF(RSOFTPSF):
    def __init__(
        self,
        radius=0.3,
        wavelength=1550e-9,
        pixscale=1e-6,
        FOV_pixels=128,
        xq=0.1,
        outer_scale=20,
        velocity=10,
    ):
        # RADIUS = 1.0 # meters
        # WAVELENGTH = 1500e-9 # meters
        # PIXSCALE = 0.01 # um
        # FOV = 1 # arcsec
        # NWAVES = 1.0
        # FOV_PIXELS = 128
        self.radius = radius
        self.wavelength = wavelength
        self.pixscale = pixscale
        # self.FOV = 1
        self.FOV_pixels = FOV_pixels

        self.pupil_grid = make_pupil_grid(256, radius * 2)
        self.focal_grid = make_focal_grid(
            4, self.FOV_pixels, spatial_resolution=pixscale
        )
        self.prop = FraunhoferPropagator(
            self.pupil_grid, self.focal_grid, focal_length=10 * self.radius * 2
        )
        self.aperture = circular_aperture(self.radius * 2)(self.pupil_grid)

        self.fried_parameter = fried_parameter
        self.outer_scale = outer_scale  # meter
        self.velocity = velocity  # meter/sec
        layers = make_standard_atmospheric_layers(self.pupil_grid, self.outer_scale)
        self.atmos = MultiLayerAtmosphere(layers, scintilation=False)

        self.wavefront = Wavefront(self.aperture, wavelength)

    def set_fried_parameter(self, fried_parameter, wavelength=550e-9):
        self.atmos.Cn_squared = Cn_squared_from_fried_parameter(
            fried_parameter, wavelength
        )

    def makePSF(self, makePSFInputDict: dict, makePSFOptions=None):
        loopitter = makePSFInputDict["coeffs"]
        self.atmos.t = loopitter

        img = self.prop(self.atmos(self.wavefront))

        self.complex_psf = np.asarray(img.electric_field.shaped, dtype=np.complex128)
        self.physicalsize = self.FOV_pixels * 2 * self.pixscale

        self.psf = np.asarray(img.intensity.shaped)
        self.psf = self.psf / self.psf.max()

        self.wf.amplitude = self.complex_psf.real
        self.wf.phase = np.angle(self.complex_psf)

        self.osys_obj = None
        self.pupil_wf = np.asarray(self.atmos.phase_for(self.wavelength).shaped)


if __name__ == "__main__":
    hci = hcipyPSF(radius=0.3)
    makePSFInputDict = {"coeffs": 0}
    hci.makePSF(makePSFInputDict)
    hci.saveToRSoft(outfile="PSFOut_hcipy", size_data=hci.physicalsize * 1e6 / 2)
