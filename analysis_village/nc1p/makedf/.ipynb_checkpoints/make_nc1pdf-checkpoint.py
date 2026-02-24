from makedf.makedf import *
from pyanalib.pandas_helpers import *
from makedf.util import *

import sys, os


def make_slcdf_withlight(f):
    slcdf = loadbranches(f["recTree"], slcbrancheswithlight)
    slcdf = slcdf.rec
    slc_mcdf = make_mcdf(f, slc_mcbranches, slc_mcprimbranches)
    slc_mcdf.columns = pd.MultiIndex.from_tuples([tuple(["slc", "truth"] + list(c)) for c in slc_mcdf.columns])
    slcdf = multicol_merge(slcdf, slc_mcdf, left_index=True, right_index=True, how="left", validate="one_to_one")

    return slcdf

def make_pandora_df_withlight(f, trkScoreCut=False, trkDistCut=50., cutClearCosmic=False, requireFiducial=False, updatecalo=False, **trkArgs):
    # load
    trkdf = make_trkdf(f, trkScoreCut, **trkArgs)
    if updatecalo:
        # check detector
        det = loadbranches(f["recTree"], ["rec.hdr.det"]).rec.hdr.det
        if (1 == det.unique()):
            det = "SBND"
        else:
            det = "ICARUS"
        #check ismc
        hdrdf = make_mchdrdf(f)
        ismc = hdrdf.ismc.iloc[0]

        chi2_pids = []
        for plane in range(0, 3):
            trkhitdf = make_trkhitdf(f, plane)
            if det == "SBND": ## FIXME
                trkhitdf = trkhitdf[InFV(df = trkhitdf, inzback = 0., det = "SBND_nohighyz")]
            #dqdx_redo = chi2pid.dqdx(trkhitdf, gain=det, calibrate=det, isMC=ismc)
            dedx_redo = chi2pid.dedx(trkhitdf, gain=det, calibrate=det, plane=plane, isMC=ismc)
            dedx_bias = (dedx_redo - trkhitdf.dedx) / trkhitdf.dedx
            trkhitdf["dedx_redo"] = dedx_redo
            #trkhitdf["dqdx_redo"] = dqdx_redo
            #trkhitdf["dedx_bias"] = dedx_bias
            #print(trkhitdf[trkhitdf.rr < 26.].head(50))
            for par in ['muon', 'proton']:
                this_chi2_new, this_chi2_ndof = chi2pid.chi2par(trkhitdf, dedxname="dedx_redo", par=par)
                this_chi2_col = ('pfp', 'trk', 'chi2pid', 'I' + str(plane), 'chi2_' + par + '_new', '')
                this_ndof_col = ('pfp', 'trk', 'chi2pid', 'I' + str(plane), 'ndof_' + par + '_new', '')
                trkdf[this_chi2_col] = this_chi2_new
                trkdf[this_ndof_col] = this_chi2_ndof
                trkdf[this_chi2_col] = trkdf[this_chi2_col].fillna(0.)
                trkdf[this_ndof_col] = trkdf[this_ndof_col].fillna(0)

    slcdf = make_slcdf_withlight(f)

    # merge in tracks
    slcdf = multicol_merge(slcdf, trkdf, left_index=True, right_index=True, how="right", validate="one_to_many")

    # distance from vertex to track start
    slcdf = multicol_add(slcdf, dmagdf(slcdf.slc.vertex, slcdf.pfp.trk.start).rename(("pfp", "dist_to_vertex")))

    if trkDistCut > 0:
        slcdf = slcdf[slcdf.pfp.dist_to_vertex < trkDistCut]
    if cutClearCosmic:
        slcdf = slcdf[slcdf.slc.is_clear_cosmic==0]
    # require fiducial verex
    if requireFiducial:
        slcdf = slcdf[InFV(slcdf.slc.vertex, 50)]

    #print(slcdf.pfp.trk.chi2pid.head(50))
    return slcdf

def make_pandora_df_nc1p(f):
    pandoradf = make_pandora_df_withlight(f, cutClearCosmic=True)
    return pandoradf