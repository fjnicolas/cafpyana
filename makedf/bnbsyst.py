from . import getsyst
import pandas as pd

# Regen systematic variations
regen_systematics = [
    'expskin_Flux',
    'horncurrent_Flux',
    'kminus_Flux',
    'kplus_Flux',
    'kzero_Flux',
    'nucleoninexsec_Flux',
    'nucleonqexsec_Flux',
    'nucleontotxsec_Flux',
    'piminus_Flux',
    'pioninexsec_Flux',
    'pionqexsec_Flux',
    'piontotxsec_Flux',
    'piplus_Flux'
]

def bnbsyst(f, nuind, multisim_nuniv=250, slim=False, systematics=None, slim_systs2save=None):
    if systematics is None:
        systematics = regen_systematics
    bnbwgtdf = getsyst.getsyst(f, systematics, nuind, multisim_nuniv=multisim_nuniv, slim=slim, slimname="Flux", slim_systs2save=slim_systs2save)

    if slim:  # keep only the multiplied "Flux.univ_" columns and the ones in slim_systs2save
        flux_cols = [c for c in bnbwgtdf.columns if c[0] == "Flux"]
        if slim_systs2save is not None:
            flux_cols += [c for c in bnbwgtdf.columns if c[0] in slim_systs2save]
        bnbwgtdf = bnbwgtdf[flux_cols]
        
    return bnbwgtdf

