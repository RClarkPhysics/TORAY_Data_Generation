#Time Fitting Script
#This script will take an array of times that the user requests
#TORAY runs to be done at, then it will look at the avaialable times
#discard anything outside of the bounds and match requested points to
#those nearest to them (rounding down when equidistant)

import numpy as np

#Collect data from the  Variables Tree
defaultVars(times = OMFIT['Variables']['times'],
    ShotNum = OMFIT['Variables']['ShotNum']
)

#Collect the ZIPFIT times that we will compare against the requested times
tmp = OMFITmdsValue(
    server='DIII-D', treename='ELECTRONS', shot=OMFIT['Variables']['ShotNum'], TDI='\\ELECTRONS::TOP.PROFILE_FITS.ZIPFIT.ETEMPFIT'
)
time_te = np.atleast_1d(tmp.dim_of(1))

tmp = OMFITmdsValue(
    server='DIII-D', treename='ELECTRONS', shot=OMFIT['Variables']['ShotNum'], TDI='\\ELECTRONS::TOP.PROFILE_FITS.ZIPFIT.EDENSFIT'
)
time_ne = np.atleast_1d(tmp.dim_of(1))
Allowed_time = np.intersect1d(time_te,time_ne)


#Discard times outside of the bounds
Filtered_times = times[times> np.min(Allowed_time)]
Filtered_times = Filtered_times[Filtered_times < np.max(Allowed_time)]

#Make a new array such that the times in Filtered_times match with the closest available time in Allowed_time
Run_times = np.zeros(Filtered_times.shape[0])
for i,t in enumerate(Filtered_times):
    Diff = abs(Allowed_time - t)
    Run_times[i] = Allowed_time[Diff == np.min(Diff)][0]

#Store Run_times
OMFIT['Variables']['Run_times'] = Run_times
