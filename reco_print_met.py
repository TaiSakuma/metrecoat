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
    print '%10s' % 'met.pt',
    print '%7s'  % 'met.phi',
    print '%10s' % 'met.signif',
    print '%10s' % 'met.px',
    print '%10s' % 'met.py',
    print '%10s' % 'met.pz',
    print '%10s' % 'met.pt2',
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
        ("genMetCalo"             ,"" ,"METP" ,handleGenMETs   ),
        ("genMetCaloAndNonPrompt" ,"" ,"METP" ,handleGenMETs   ),
        ("genMetTrue"             ,"" ,"METP" ,handleGenMETs   ),
        ("pfMet"                  ,"" ,"METP" ,handlePFMETs    ),
        ("corMetGlobalMuons"      ,"" ,"METP" ,handleCaloMETs  ),
        ("met"                    ,"" ,"METP" ,handleCaloMETs  ),
        ("metHO"                  ,"" ,"METP" ,handleCaloMETs  ),
        ("metNoHF"                ,"" ,"METP" ,handleCaloMETs  ),
        ("metNoHFHO"              ,"" ,"METP" ,handleCaloMETs  ),
        ("metOpt"                 ,"" ,"METP" ,handleCaloMETs  ),
        ("metOptHO"               ,"" ,"METP" ,handleCaloMETs  ),
        ("metOptNoHF"             ,"" ,"METP" ,handleCaloMETs  ),
        ("metOptNoHFHO"           ,"" ,"METP" ,handleCaloMETs  ),
        ("htMetAK5"               ,"" ,"METP" ,handleMETs      ),
        # ("htMetAK7"               ,"" ,"METP" ,handleMETs      ),
        # ("htMetIC5"               ,"" ,"METP" ,handleMETs      ),
        # ("htMetKT4"               ,"" ,"METP" ,handleMETs      ),
        ("htMetKT6"               ,"" ,"METP" ,handleMETs      ),
        ("tcMet"                  ,"" ,"METP" ,handleMETs      ),
        ("tcMetCST"               ,"" ,"METP" ,handleMETs      ),
        ("tcMetRft2"              ,"" ,"METP" ,handleMETs      ),
        ("tcMetVedu"              ,"" ,"METP" ,handleMETs      ),
        ("tcMetWithPFclusters"    ,"" ,"METP" ,handleMETs      ),
        ("pfChargedMET"           ,"" ,"METP" ,handlePFMETs    ),
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

            print '%4d'    % run,
            print '%5d'    % eventId,
            print '%25s'   % METCollection[0],
            print '%7s'    % METCollection[2],
            print '%10.3f' % met.pt(),
            print '%7.2f' % (met.phi()/math.pi*180.0),
            print '%10.3f' % met.significance(),
            print '%10.3f' % met.px(),
            print '%10.3f' % met.py(),
            print '%10.3f' % met.pz(),
            print '%10.3f' % math.sqrt(met.px()**2 + met.py()**2),
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
