from makedf.makedf import *
from pyanalib.pandas_helpers import *
from makedf.util import *

import sys

ENERGY_TO_CHARGE = 0.584 / 23.6e-9   # MeV → electrons

BLIPS_SIZE_COL_NAME = ('rec', 'blips', 'size', '', '')
BLIPS_DX_COL_NAME   = ('rec', 'blips', 'dX', '', '')
BLIPS_DYZ_COL_NAME  = ('rec', 'blips', 'dYZ', '', '')
BLIPS_CHARGE_COL_NAME = ('rec', 'blips', 'charge', '', '')
BLIPS_ENERGY_COL_NAME = ('rec', 'blips', 'energy', '', '')
BLIPS_ENERGYPSTAR_COL_NAME = ('rec', 'blips', 'energyPSTAR', '', '')
BLIPS_CHARGE_SIZE_RATIO_COL_NAME = ('rec', 'blips', 'charge_size_ratio', '', '')
BLIPS_ENERGYPSTAR_SIZE_RATIO_COL_NAME = ('rec', 'blips', 'energy_size_ratio', '', '')

def add_blip_calorimetry_variables(df):
    """
    Add derived blip columns to a single DataFrame with flat column names.

    New columns
    -----------
    rec.blips.size              : sqrt(dX² + dYZ²)
    rec.blips.charge            : energy * charge_conversion
    rec.blips.charge_size_ratio : charge / size
    rec.blips.energy_size_ratio : energy / size
    """

    df[BLIPS_SIZE_COL_NAME] = np.sqrt(
        df[BLIPS_DX_COL_NAME]  ** 2 +
        df[BLIPS_DYZ_COL_NAME] ** 2
    )

    df[BLIPS_CHARGE_COL_NAME] = df[BLIPS_ENERGY_COL_NAME] * ENERGY_TO_CHARGE
    df[BLIPS_CHARGE_SIZE_RATIO_COL_NAME] = df[BLIPS_CHARGE_COL_NAME] / df[BLIPS_SIZE_COL_NAME]
    return df


def rewrite_blip_energyPSTAR(df):
    """
    Overwrite rec.blips.energyPSTAR using spline interpolation from charge.
    Values outside the calibration range are set to 0.
    """

    splines_charge_xV = [5.62012, 7.5217, 9.22644, 10.7891, 12.2458, 14.9232, 17.364, 19.6304, 21.7613, 23.7802, 25.7044, 27.5476, 31.8909, 35.949, 39.788, 43.4516, 46.9648, 50.3587, 53.6611, 56.8741, 63.0742, 69.0801, 74.8993, 80.575, 86.1498, 91.7055, 97.1671, 102.615, 108.013, 113.441, 118.862, 124.317, 129.767, 135.294, 163.462, 193.083, 224.394, 257.526, 292.434, 329.105, 367.443, 407.39, 491.813, 581.821, 677.162, 777.008, 881.301, 989.983, 1102.24, 1218.42, 1338.49, 1461.65, 1588.63, 1719.02, 1852.79, 1989.92, 2724.66, 3537.17, 4419.21, 5369.11, 6382.82, 7452.57, 8577.23, 9758.68, 11242.9, 12272.8, 13874.3, 14979.2, 16110.6, 16688.6, 17866, 19069.3, 19680.1, 20925.4, 24147.3, 27525.1, 31049.9, 34728.2, 38532.3, 42455.5, 46518.8, 50719.2, 55031.4, 59453.7, 83220.8, 109496, 137981, 168490,  234878, 270445, 307528, 385847, 468873, 556297, 647608, 742473, 840596, 941610, 1.04538e+06, 1.1517e+06, 1.26037e+06, 1.37111e+06, 1.48395e+06, 1.59864e+06, 1.71474e+06, 2.32002e+06, 2.95591e+06, 3.61505e+06, 4.29229e+06]
    splines_energy_xV= [0.001, 0.0015, 0.002, 0.0025, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.3, 3.5, 3.8, 4, 4.2, 4.3, 4.5, 4.7, 4.8, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 12.5, 15, 17.5, 20, 25, 27.5, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 125, 150, 175, 200]

    df[BLIPS_ENERGYPSTAR_COL_NAME] = np.interp(
        df[BLIPS_CHARGE_COL_NAME],
        splines_charge_xV,
        splines_energy_xV,
        left=0,
        right=0,
    )

    df[BLIPS_ENERGYPSTAR_COL_NAME] = df[BLIPS_ENERGYPSTAR_COL_NAME]
    df[BLIPS_ENERGYPSTAR_SIZE_RATIO_COL_NAME] = df[BLIPS_ENERGYPSTAR_COL_NAME] / df[BLIPS_SIZE_COL_NAME]
    
    return df

def flatten_columns_blips(df):
    """Collapse a MultiIndex column into dot-joined flat strings."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [
            '.'.join(str(lvl) for lvl in col if lvl != '').strip('.')
            for col in df.columns
        ]
    return df


def add_blip_mcnu_truthmatching(blips_df, true_particles_df, mcnu_df):
    """
    Enrich a blips DataFrame with matched true-particle and MCNu information.

    Matching rules
    --------------
    true_particles : (__ntuple, entry) + blip.leadG4ID == true_particle.G4ID
    mcnu           : (__ntuple, entry) + rec.blips.true_particles.interaction_id == mcnu.idx

    Added column namespaces
    -----------------------
    rec.blips.true_particles.*
    rec.blips.mcnu.*

    Parameters
    ----------
    blips_df          : blips DataFrame   (index: __ntuple, entry, rec.blips..index)
    true_particles_df : true-particle DF  (index: __ntuple, entry, rec.true_particles..index)
    mcnu_df           : MCNu DataFrame    (index: __ntuple, entry, rec.mc.nu..index, rec.mc.nu.prim..index)

    Returns
    -------
    pd.DataFrame  — blips with all added branches, original index restored.
    """
    
    # ── Flatten & reset indices ───────────────────────────────────────────
    blips_r = flatten_columns_blips(blips_df).reset_index()
    tp_r    = flatten_columns_blips(true_particles_df).reset_index()

    ##

    # ── Step 1: match true_particles → blips ─────────────────────────────
    leadG4ID_col = next(c for c in blips_r.columns if 'leadG4ID' in c)

    # Temp column for -1→NaN so the original leadG4ID column is untouched
    TEMP_KEY = '__merge_g4id__'
    blips_r[TEMP_KEY] = blips_r[leadG4ID_col].replace(-1, pd.NA)

    result = blips_r.merge(
        tp_r,
        left_on=['entry', TEMP_KEY],
        right_on=['entry', 'G4ID'],
        how='left',
    ).drop(columns=[TEMP_KEY])

    tp_data_cols = [c for c in tp_r.columns if c not in ('entry')]
    result = result.rename(columns={
        col: f'rec.blips.true_particles.{col}'
        for col in tp_data_cols
        if col in result.columns
    })

    # ── Step 2: match MCNu → blips ───────────────────────────────────────
    mcnu_r = flatten_columns_blips(mcnu_df).reset_index()

    # Drop prim index level and all prim-branching columns; deduplicate to nu level
    prim_cols = [c for c in mcnu_r.columns if 'prim' in c]
    mcnu_r = (
        mcnu_r
        .drop(columns=prim_cols)
        .drop_duplicates(subset=['entry', 'idx'])
    )

    result = result.merge(
        mcnu_r,
        left_on=['entry', 'rec.blips.true_particles.interaction_id'],
        right_on=['entry', 'idx'],
        how='left',
    )

    mcnu_data_cols = [c for c in mcnu_r.columns if c not in ('__ntuple', 'entry')]
    result = result.rename(columns={
        col: f'rec.blips.mcnu.{col}'
        for col in mcnu_data_cols
        if col in result.columns
    })

    # ── Restore original blip MultiIndex ─────────────────────────────────
    return result.set_index(blips_df.index.names)


def make_blipdf_mcnutruthmatched(f):
    
    blipinfodf = loadbranches(f["recTree"], blipbranches)
    trueblipinfodf = loadbranches(f["recTree"], trueblipbranches)
    fullblipdf = multicol_merge(blipinfodf, trueblipinfodf, left_index=True, right_index=True, how="left", validate="one_to_one")
    #blipclusterinfodf = loadbranches(f["recTree"], blipclusterbranches)
    #fullblipdf = multicol_merge(fullblipdf, blipclusterinfodf, left_index=True, right_index=True, how="left", validate="one_to_one")
    

    # Add derived blip columns

    # Add blip size
    fullblipdf = add_blip_calorimetry_variables(fullblipdf)
    # Rewrite energyPSTAR using spline interpolation from charge
    fullblipdf = rewrite_blip_energyPSTAR(fullblipdf)

    # Add CRT veto branches
    crt_veto_df = make_crtvetodf(f)
    ## Rename CRT veto columns with rec.blips.crt_veto prefix
    crt_veto_df = crt_veto_df.rename(columns=lambda col: f"rec.blips.{col}", level=0)
    fullblipdf = multicol_merge(fullblipdf, crt_veto_df, left_index=True, right_index=True, how="left", validate="one_to_one")

    # Load true_particles and MCNu for matching
    true_particles_df = make_alltrueparticlesdf(f)
    mcnu_df = make_mcnudf(f)


    # Perform blip-truth matching
    fullblipdf = add_blip_mcnu_truthmatching(fullblipdf, true_particles_df, mcnu_df)
    
    return fullblipdf 
    