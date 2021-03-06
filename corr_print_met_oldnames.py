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
parser.add_option('-i', '--inputPath', default = './corr_met_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():
    
    print '%6s'  % 'run',
    print '%9s'  % 'event',
    print '%25s' % 'module',
    print '%10s' % 'met.pt',
    print '%10s' % 'met.px',
    print '%10s' % 'met.py',
    print '%10s'  % 'met.phi',
    print '%10s'  % 'sumet',
    print

    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handleGenMETs = Handle("std::vector<reco::GenMET>") 
    handlePFMETs = Handle("std::vector<reco::PFMET>") 
    handleCaloMETs = Handle("std::vector<reco::CaloMET>") 
    handleMETs = Handle("std::vector<reco::MET>") 

    METCollections = (
        ("caloType1CorrectedMet"    ,"" ,"TEST", handleCaloMETs ),
        ("caloType1p2CorrectedMet"  ,"" ,"TEST", handleCaloMETs ),
        ("pfType0CorrectedMet"      ,"" ,"TEST", handlePFMETs   ),
        ("pfType0p1CorrectedMet"    ,"" ,"TEST", handlePFMETs   ),
        ("pfType0p1p2CorrectedMet"  ,"" ,"TEST", handlePFMETs   ),
        ("pfType0p2CorrectedMet"    ,"" ,"TEST", handlePFMETs   ),
        ("pfType0pfcCorrectedMet"   ,"" ,"TEST", handlePFMETs   ),
        ("pfType0pfcp1CorrectedMet" ,"" ,"TEST", handlePFMETs   ),
        ("pfType1CorrectedMet"      ,"" ,"TEST", handlePFMETs   ),
        ("pfType1p2CorrectedMet"    ,"" ,"TEST", handlePFMETs   ),
        )


    firstEvent = True
    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

                           
        for METCollection in METCollections:
            handle = METCollection[3]
            event.getByLabel(METCollection[0:3], handle)
            met = handle.product().front()

            print '%6d'    % run,
            print '%9d'    % eventId,
            print '%25s'   % METCollection[0],
            print '%10.3f' % met.pt(),
            print '%10.3f' % met.px(),
            print '%10.3f' % met.py(),
            print '%10.2f' % (met.phi()/math.pi*180.0),
            print '%10.2f' % met.sumEt(),
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
