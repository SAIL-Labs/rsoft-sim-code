import errno
import glob
import os
from shutil import copyfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as sio
from hcipy import *

from make_rsoft_fld_batch import RSOFTPSF


class femsimPSF(RSOFTPSF):
    def __init__(self, femsim_result_dir="", prefix=""):
        self.femsim_result_dir = femsim_result_dir
        self.prefix = prefix

        self.listoffiles = glob.glob(self.femsim_result_dir + self.prefix + "_ex*.m*")

    def makePSF(self, makePSFInputDict: dict, makePSFOptions=None):
        raise NotImplementedError
        pass

    def prepareBATFiles(
        self,
        outpath="./",
        filePrefix="Mode",
        extraPlots=False,
        makeBatFile=False,
        saveAllData=False,
        indFile="bptmp.ind",
        outPrefix="BPScan",
        numBatfiles=1,
        shouldCopyFiles=False,
    ):
        allOutfiles = []
        allData = []
        try:
            os.makedirs(outpath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        for ind, modefilepath in enumerate(self.listoffiles):

            print("Proccessing mode file: " + modefilepath)

            modefile_head_tail = os.path.split(modefilepath)

            if shouldCopyFiles:
                copyfile(
                    modefilepath, outpath + modefile_head_tail[1].replace("_ex", "")
                )

            allOutfiles.append(modefile_head_tail[1].replace("_ex", ""))
            if saveAllData:
                psf_ampl, FLDintens, psf_phase = loadFLD(modefilepath)
                pupil_phase = np.zeros(psf_ampl.size)
                cur_wf = [psf_ampl, psf_phase, pupil_phase]
                allData.append(cur_wf)

        if makeBatFile:
            allOutfilenames = []
            progname = "bsimw32"

            nf = len(allOutfiles)
            batfileLength = nf // numBatfiles
            allBatfileNames = []

            for k in range(numBatfiles):
                startInd = k * batfileLength
                endInd = (k + 1) * batfileLength
                if k == (numBatfiles - 1):
                    curOutfiles = allOutfiles[startInd:]
                else:
                    curOutfiles = allOutfiles[startInd:endInd]
                print(
                    "Making .bat file: " + outpath + outPrefix + "_" + str(k) + ".bat"
                )
                batfile = open(outpath + outPrefix + "_" + str(k) + ".bat", "w")
                allBatfileNames.append(outPrefix + "_" + str(k) + ".bat")
                for launch_file in curOutfiles:
                    cmdStr = (
                        progname
                        + " "
                        + indFile
                        + " prefix="
                        + outPrefix
                        + launch_file
                        + " launch_file="
                        + launch_file
                        + " wait=0\n"
                    )
                    print(cmdStr)
                    batfile.write(cmdStr)
                    allOutfilenames.append(outPrefix + launch_file)
                batfile.close()
            metadatafile = outpath + outPrefix + "_metadata"

            coeffsList = []
            np.savez(
                metadatafile + ".npz",
                allOutfilenames=allOutfilenames,
                coeffsList=self.listoffiles,
                allData=allData,
            )
            sio.savemat(
                metadatafile + ".mat",
                mdict={
                    "allOutfilenames": allOutfilenames,
                    "coeffsList": self.listoffiles,
                    "allData": allData,
                },
            )

            if numBatfiles > 1:
                superbatfile = open(outpath + "runAllBatfiles.bat", "w")
                for batfilename in allBatfileNames:
                    cmdStr = "start cmd /k call " + batfilename + "\n"
                    superbatfile.write(cmdStr)
                superbatfile.close()


def loadFLD(filepath="bptmp.fld"):
    X = pd.read_csv(filepath, skiprows=4, header=None, delim_whitespace=True)
    Xarr = np.asarray(X)
    FLDampl = Xarr[:, ::2]
    FLDintens = Xarr[:, ::2] ** 2
    FLDphase = Xarr[:, 1::2]
    return FLDampl, FLDintens, FLDphase


if __name__ == "__main__":
    hci = femsimPSF(
        femsim_result_dir="/Volumes/silo4/snert/FMF_PL_rsoft/mode solve/OFS-FMF_PL_MM55_T60/",
        prefix="femLantern",
    )
    outpath = "/Volumes/silo4/snert/FMF_PL_rsoft/mode prop/1_FMF_PL_MM55_T60/"
    hci.prepareBATFiles(
        makeBatFile=True,
        saveAllData=True,
        outpath=outpath,
        indFile="lantern55.ind",
        outPrefix="femsimLanternModes_",
        numBatfiles=5,
    )
