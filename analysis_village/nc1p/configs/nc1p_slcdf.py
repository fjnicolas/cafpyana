from makedf.makedf import *
from analysis_village.nc1p.makedf.make_nc1pdf import *

DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_mcnudf, make_sbndtimingdf]
NAMES = ["evt", "hdr", "pot", "mcnu", "timing" ]