# Make branching fraction plots in 2HDM and MSSM

This is a small collection of easy plotting scripts, just put here for posterity. They're written for the single purpose of making these plots.

General setup: Requires ROOT, python (+ tqdm package for 2HDM BR plots but that can be commented out)


## 2HDM instructions

* Install most recent version of 2HDMC https://2hdmc.hepforge.org/
* Run br_plots.py, edit the masses/cos(b-a) values scanned and general parameters in the file


## MSSM instructions

Simply makes a nice plot from the BR plot provided by the LHC H WG3

* Download desired MSSM file https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGMSSMNeutral  https://doi.org/10.5281/zenodo.5730270
* Run mssm.py, adjusting input path in file