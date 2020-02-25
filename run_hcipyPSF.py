#%%
import numpy as np

from hcipyPSF import hcipyPSF

hci = hcipyPSF(radius=0.3)
makePSFInputDict = {"coeffs": 0}
hci.makePSF(makePSFInputDict)
hci.saveToRSoft(outfile="PSFOut_hcipy_test", size_data=hci.physicalsize * 1e6 / 2)

#%%
inputdict = []
for loopitter in range(0, 100):
    inputdict.append({"coeffs": loopitter * 0.0025})
outpath = "/Volumes/silo4/snert/FMF_PL_rsoft/sweep/10_atmos_hci/"
hci.makeMultiplePSFs(
    inputdict,
    None,
    makeBatFile=True,
    saveAllData=True,
    outpath=outpath,
    size_data=hci.physicalsize * 1e6 / 2,
    indFile="lantern55.ind",
    outPrefix="hcipysim_",
    numBatfiles=5,
    trimLeadingCoeffnames="seq",
)


# %%
