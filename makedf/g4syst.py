from . import getsyst

g4_systematics = [
    "reinteractions_piminus_Geant4",
    "reinteractions_piplus_Geant4",
    "reinteractions_proton_Geant4"
]

def g4syst(f, nuind, systematics=None):
    if systematics is None:
        systematics = g4_systematics
    return getsyst.getsyst(f, systematics, nuind)

