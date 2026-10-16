from makedf.makedf import *
from analysis_village.nc1p.makedf.make_nc1pdf import *
from analysis_village.nc1p.makedf.make_nc1pblips_df import *


#DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_mcnudf, make_sbndtimingdf, make_blipdf_mcnutruthmatched, make_stubs, make_beamopflash_df]
#NAMES = ["evt", "hdr", "pot", "mcnu", "timing", "blips", "stubs", "opflashes"]

DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_mcnudf, make_sbndtimingdf, make_blipdf_mcnutruthmatched, make_stubs, make_opflashdf]
NAMES = ["evt", "hdr", "pot", "mcnu", "timing", "blips", "stubs", "opflashes"]

#DFS = [make_pandora_df_nc1p, make_hdrdf, make_potdf_bnb, make_mcnudf, make_sbndtimingdf, make_blipdf_mcnutruthmatched, make_stubs, make_beamopflash_df, make_alltrueparticlesdf]
#NAMES = ["evt", "hdr", "pot", "mcnu", "timing", "blips", "stubs", "opflashes", "trueparts"]