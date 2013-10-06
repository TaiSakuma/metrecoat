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
    print '%25s' % 'module',
    print '%7s'  % 'process',
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handleValueMap = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")

    handleGenMETs = Handle("std::vector<reco::GenMET>") 
    handlePFMETs = Handle("std::vector<reco::PFMET>") 
    handleCaloMETs = Handle("std::vector<reco::CaloMET>") 
    handleMETs = Handle("std::vector<reco::MET>") 

    handleMuons = Handle("std::vector<reco::Muon>") 

    ValueMaps = (
        ("muonMETValueMapProducer",   "muCorrData", "METP", handleValueMap),
        ("muonTCMETValueMapProducer", "muCorrData", "METP", handleValueMap)    
        )


    firstEvent = True
    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        event.getByLabel("muons", handleMuons)
        print handleMuons.product()
        print [m for m in handleMuons.product()]
        print ROOT.reco.MuonRef
        # for i in range( handleMuons.product().size()):
        #    print ROOT.reco.MuonRef(handleMuons, i)

        for ValueMap in ValueMaps:
            handle = ValueMap[3]
            event.getByLabel(ValueMap[0:3], handle)
            valuemap = handle.product()
            # print valuemap.size()
            # print valuemap.ids()
            # print [valuemap.get(id) for id in valuemap.ids()]
            print dir(valuemap)
            print valuemap.get(0)


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
