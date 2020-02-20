import soapy
from make_rsoft_fld_batch import RSOFTPSF
import numpy as np


class structtype:
    pass


class AltSim(soapy.Sim):
    def __init__(self, *args, **kwargs):
        super(AltSim, self).__init__(*args, **kwargs)

    def aoloop(self):
        """
        Main AO Loop

        Runs a WFS iteration, reconstructs the phase, runs DMs and finally the science cameras. Also makes some nice output to the console and can add data to the Queue for the GUI if it has been requested. Repeats for nIters.
        """

        # self.iters = 0
        # self.correct = 1
        self.go = True

        # # Circular buffers to hold loop iteration correction data
        # self.slopes = np.zeros((self.config.sim.totalWfsData))
        # self.closedCorrection = []
        # self.openCorrection = []
        # self.dmCommands = np.zeros(self.config.sim.totalActs)
        # self.finalscrn = {}

        try:
            while self.iters < self.config.sim.nIters:
                if self.go:
                    self.loopFrame()
                    scrnsum = self.scrns[0] * 0.0
                    for scrn in self.scrns.values():
                        scrnsum = scrnsum + scrn
                    self.finalscrn[self.iters] = scrnsum
                    # self.iters += 1
                else:
                    break
        except KeyboardInterrupt:
            self.go = False
            # logger.info("\nSim exited by user\n")

        # Finally save data after loop is over.
        self.saveData()
        self.finishUp()


class soapyPSF(RSOFTPSF):
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

    def makePSF(self, makePSFInputDict: dict, makePSFOptions=None):
        loopitter = makePSFInputDict["coeffs"]
        self.complex_psf = self.sim.scieFieldInst[0][loopitter, :, :]

        self.psf = self.sim.sciImgsInst[0][0, :, :]
        self.wf = structtype()
        self.wf.amplitude = self.complex_psf.real
        self.wf.phase = np.angle(self.complex_psf)

        self.osys_obj = None
        self.pupil_wf = self.sim.finalscrn[loopitter]

    def runAOSim(self, simconfig="o_loop.yaml"):
        self.sim = soapy.Sim(simconfig)
        self.sim.aoinit()
        self.sim.makeIMat()
        self.sim.aoloop()

        # self.SciImgReal = s.sim.scieFieldInst[0]
        # self.SciImgImag = s.sim.scieFieldInst[0]


if __name__ == "__main__":
    s = soapyPSF()
    s.runAOSim()

    makePSFInputDict = {"coeffs": 0}
    s.makePSF(makePSFInputDict)

