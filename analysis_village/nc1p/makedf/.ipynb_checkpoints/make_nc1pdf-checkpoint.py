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

    if (updatecalo == True):
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
            #if det == "SBND": ## FIXME
            #    trkhitdf = trkhitdf[InFV(df = trkhitdf, inzback = 0., det = "SBND_nohighyz")]
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


    #### Charge in spheres with centers at vtx
    pandora_df = make_pandora_df(f)
    hitdf = make_trkhitdf_plane2(f)
    new_columns = pd.MultiIndex.from_tuples(
        [('pfp', 'trk', 'hit', col, '') for col in hitdf.columns]
    )
    hitdf.columns = new_columns
    pfp_vtxdist_4cm_df = pandora_df[(pandora_df.pfp.dist_to_vertex < 50.) & (pandora_df.slc.is_clear_cosmic == 0)]
    hittrk_matched_df = multicol_merge(hitdf.reset_index(), pfp_vtxdist_4cm_df.reset_index(),
                                       left_on=[('entry', '', '', '', '', ''), ('rec.slc..index', '', '', '', '', ''), ('rec.slc.reco.pfp..index', '', '', '', '', '')],
                                       right_on=[('entry', '', '', '', '', ''), ('rec.slc..index', '', '', '', '', ''), ('rec.slc.reco.pfp..index', '', '', '', '', '')],
                                       how="right")
    hittrk_matched_df = hittrk_matched_df.set_index(["entry", "rec.slc..index", "rec.slc.reco.pfp..index", "rec.slc.reco.pfp.trk.calo.2.points..index"], verify_integrity=True)
    hittrk_matched_df = multicol_add(hittrk_matched_df, dmagdf(hittrk_matched_df.slc.vertex, hittrk_matched_df.pfp.trk.hit).rename(("pfp", "trk", "hit", "dist_to_vertex", "", "")))
    hittrk_matched_df_4cm = hittrk_matched_df[hittrk_matched_df.pfp.trk.hit.dist_to_vertex < 4.]
    hittrk_matched_df_3cm = hittrk_matched_df[hittrk_matched_df.pfp.trk.hit.dist_to_vertex < 3.]
    hittrk_matched_df_2cm = hittrk_matched_df[hittrk_matched_df.pfp.trk.hit.dist_to_vertex < 2.]
    hittrk_matched_df_1cm = hittrk_matched_df[hittrk_matched_df.pfp.trk.hit.dist_to_vertex < 1.]

    sum_integ_4cm = (hittrk_matched_df_4cm.pfp.trk.hit.integral).groupby(level=[0,1]).sum()
    sum_integ_3cm = (hittrk_matched_df_3cm.pfp.trk.hit.integral).groupby(level=[0,1]).sum()
    sum_integ_2cm = (hittrk_matched_df_2cm.pfp.trk.hit.integral).groupby(level=[0,1]).sum()
    sum_integ_1cm = (hittrk_matched_df_1cm.pfp.trk.hit.integral).groupby(level=[0,1]).sum()

    #print(sum_integ_4cm)
    slcdf['sum_integ_4cm'] = sum_integ_4cm
    slcdf['sum_integ_3cm'] = sum_integ_3cm
    slcdf['sum_integ_2cm'] = sum_integ_2cm
    slcdf['sum_integ_1cm'] = sum_integ_1cm


    #print(slcdf.pfp.trk.chi2pid.head(50))
    return slcdf

def make_pandora_df_nc1p(f):
    pandoradf = make_pandora_df_withlight(f, cutClearCosmic=True, updatecalo=True)
    return pandoradf