from makedf.makedf import *
from pyanalib.pandas_helpers import *
from makedf.util import *
from analysis_village.nc1p.configs.nc1p_systematiclist import *

import sys


def make_nc1p_nucvdf(f):
    return make_mcnudf(f)

def make_nc1p_nuslimwgtdf(f):

    hdrdf = make_mchdrdf(f)
    ismc = hdrdf.ismc.iloc[0]

    if (ismc == 1):
        return make_mcnudf(f, include_weights=True, slim=True,  wgt_types=["genie","g4","bnb"], g4_systematics=nc1p_g4_systematics, slim_systs2save=nc1p_syststosave)
    else:
        return make_mcnudf(f)
        

def make_nc1p_nufullwgtdf(f):

    hdrdf = make_mchdrdf(f)
    ismc = hdrdf.ismc.iloc[0]
    if (ismc == 1):
        return make_mcnudf(f, include_weights=True, slim=False, g4_systematics=nc1p_g4_systematics)
    else:
        return make_mcnudf(f)