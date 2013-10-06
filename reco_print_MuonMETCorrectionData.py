#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
import math
import json
import re
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = './reco_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():
    
    print '%4s'  % 'run',
    print '%5s'  % 'event',
    print '%27s' % 'module',
    print '%12s' % 'label',
    print '%4s'  % 'type',
    print '%10s' % 'x',
    print '%10s' % 'y',
    print '%10s' % 'pt',
    print
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handleValueMap = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")

    # handleMuons = Handle("std::vector<reco::Muon>") 

    ValueMaps = (
        ("muonMETValueMapProducer",   "muCorrData", "METP", handleValueMap),
        ("muonTCMETValueMapProducer", "muCorrData", "METP", handleValueMap)    
        )


    firstEvent = True
    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        # event.getByLabel("muons", handleMuons)

        # ROOT.reco.MuonRef
        # It is not clear how to initialize ROOT.reco.MuonRef with reco::Muon.
        # in C++ (e.g. RecoMET/METAlgorithms/src/TCMETAlgo.cc),
        #|| event.getByToken(muonToken_ , muonHandle_);
        #|| event.getByToken(muonDepValueMapToken_, muonDepValueMapHandle_);
        #|| for(unsigned int i = 0; i < muonHandle_->size(); ++i)
        #||   {
        #||     reco::MuonRef muonRef(muonHandle_, i);
        #||     reco::MuonMETCorrectionData muCorrData = (*muonDepValueMapHandle_)[muonRef]
        #||   }
        #
        # The equivalent code in FWLite.Python doesn't work
        # First, Handle doesn't have size().
        # use Handle.product().size instead
        #|| for i in range(handleMuons.product().size()):
        #||    muonref = ROOT.reco.MuonRef(handleMuons, i) # <- error, cannot instantiate in this way
        #>>> TypeError: none of the 12 overloaded methods succeeded. Full details:
        #
        # However, ROOT.reco.MuonRef can be instantiated with no argument.
        #|| print ROOT.reco.MuonRef()
        #>>> <ROOT.edm::Ref<vector<reco::Muon>,reco::Muon,edm::refhelper::FindUsingAdvance<vector<reco::Muon>,reco::Muon> > object at 0x11757afa0>
        #
        # Second, ValueMap has no attribute '__getitem__' (probably equivalent
        # of operator[]) so even if ROOT.reco.MuonRef can be initialized. cannot
        # retrieve reco::MuonMETCorrectionData from the ValueMap
        #|| event.getByLabel(("muonMETValueMapProducer",   "muCorrData", "METP"), handleValueMap)
        #|| valuemap = handleValueMap.product()
        #|| print valuemap[ROOT.reco.MuonRef()] # <-- error
        #>>> TypeError: 'edm::ValueMap<reco::MuonMETCorrectionData>' object has no attribute '__getitem__'

        for ValueMap in ValueMaps:
            handle = ValueMap[3]
            event.getByLabel(ValueMap[0:3], handle)
            valuemap = handle.product()

            for i in range(valuemap.size()):
                muonMETCorrectionData = valuemap.get(i)
                print '%4d'    % run,
                print '%5d'    % eventId,
                print '%27s'   % ValueMap[0],
                print '%12s'   % ValueMap[1],
                print '%4d'    % muonMETCorrectionData.type(),
                print '%10.3f' % muonMETCorrectionData.x(),
                print '%10.3f' % muonMETCorrectionData.y(),
                print '%10.3f' % muonMETCorrectionData.pt(),
                print


##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##____________________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle

##____________________________________________________________________________||
if __name__ == '__main__':
    main()
