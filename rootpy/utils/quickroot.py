# Copyright 2012 the rootpy developers
# distributed under the terms of the GNU General Public License
"""
Quickly load ROOT symbols without causing slow finalSetup()

The main principle is that appropriate dictionaries need to be loaded.
"""
from __future__ import absolute_import

import ROOT

from .. import log; log = log[__name__]
from .module_facade import Facade

__all__ = []

# Quick's __name__ needs to be the ROOT module for this to be transparent.
# The below is one way of obtaining such a function
Quick = eval("lambda symbol: module._root.LookupRootEntity(symbol)",
             ROOT.__dict__)

_gSystem = Quick("gSystem")
Load = _gSystem.Load

# It is not vital to list _all_ symbols in here, just enough that a library
# will be loaded by the time it is needed.
SYMBOLS = dict(
    Hist="TH1 TGraph TGraphAsymmErrors",
    Tree="TCut TTree",
    Gui="TPad TCanvas",
    Graf="TLegend TLine TEllipse",
    Physics="TVector2 TVector3 TLorentzVector TRotation TLorentzRotation",
    Matrix="TMatrixT",
    RooStats="RooStats RooMsgService",
    RooFit="RooFit RooWorkspace",
)

# Mapping of symbols to libraries which need to be loaded
SYMBOLS_TO_LIB = dict(
    (sym, lib) for lib, syms in SYMBOLS.iteritems() for sym in syms.split())

# If you encounter problems with particular symbols, add them to this set.
SLOW = set("".split())

@Facade(__name__, expose_internal=False)
class QuickROOT(object):
    def __getattr__(self, symbol):
        if symbol in SLOW:
            log.warning(
                "Tried to quickly load {0} which is always slow".format(symbol))

        lib = SYMBOLS_TO_LIB.get(symbol, None)
        if lib:
            # Load() doesn't cost anything if the library is already loaded
            libname = "lib{0}".format(lib)
            if libname not in _gSystem.GetLibraries():
                regex = "^duplicate entry .* for level 0; ignored$"
                with log["/ROOT.TEnvRec.ChangeValue"].ignore(regex):
                    if Load(libname) == 0:
                        log.debug("Loaded {0} (required by {1})".format(
                            libname, symbol))
                    else:
                        raise RuntimeError(
                            "Unable to load {0} (required by {1})".format(
                                libname, symbol))

        return Quick(symbol)
