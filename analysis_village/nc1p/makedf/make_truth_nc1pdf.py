from makedf.makedf import *
from pyanalib.pandas_helpers import *
from makedf.util import *

import sys, os

def make_nc1p_nuslimwgtdf(f):
    return make_mcnudf(f, include_weights=True, slim=True,  wgt_types=["genie","g4"])

def make_nc1p_nuwgtdf(f):
    return make_mcnudf(f, include_weights=True, slim=False)