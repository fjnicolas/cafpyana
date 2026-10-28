from makedf.makedf import *
from analysis_village.nc1p.makedf.make_nc1pdf import *
from analysis_village.nc1p.makedf.make_nc1pblips_df import *
from analysis_village.nc1p.makedf.make_truth_nc1pdf import *

#DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_mcnudf, make_sbndtimingdf, make_stubs]
DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_nc1p_nuslimwgtdf, make_sbndtimingdf, make_stubs]
NAMES = ["evt", "hdr", "pot", "mcnu", "timing", "stubs"]