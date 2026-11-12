nc1p_g4_systematics = [
    "reinteractions_piminus_Geant4",
    "reinteractions_piplus_Geant4",
    "reinteractions_proton_Geant4",
    "reinteractions_neutron_Geant4",
]

nc1p_g4_systematics_2save = [
    "reinteractions_proton_Geant4",
    "reinteractions_neutron_Geant4",
]

nc1p_bnb_syst2save = [
    'expskin_Flux',
    'nucleonqexsec_Flux',
    'piplus_Flux'
]

nc1p_genie_syst2save = [
    'GENIEReWeight_SBN_v1_multisigma_MaNCEL',
    'GENIEReWeight_SBN_v1_multisigma_EtaNCEL',
    'GENIEReWeight_SBN_v1_multisigma_MaNCRES',
    'GENIEReWeight_SBN_v1_multisigma_ZExpA1CCQE',
    'GENIEReWeight_SBN_v1_multisigma_DecayAngMEC',
    'GENIEReWeight_SBN_v1_multisigma_FrCEx_N',
]


nc1p_genie_syst2save_NCMA = [
    'GENIEReWeight_SBN_v1_multisigma_MaNCEL',
]

nc1p_genie_syst2save_DecAngleMEC = [
    'GENIEReWeight_SBN_v1_multisigma_DecayAngMEC'
]

nc1p_syststosave = {
    "Flux": nc1p_bnb_syst2save,
    "G4": nc1p_g4_systematics_2save,
    "GENIE": nc1p_genie_syst2save
}