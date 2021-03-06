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
parser.add_option('-i', '--inputPath', default = './corr_terms_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():
    
    print '%6s'  % 'run',
    print '%9s'  % 'event',
    print '%35s' % 'module',
    print '%10s' % 'label',
    print '%10s' % 'mex',
    print '%10s' % 'mey',
    print

    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handleCorrMETData = Handle("CorrMETData") 

    inputTags = (
        ("pfCandMETcorr",                   "",       "CORR",   handleCorrMETData),
        ("pfchsMETcorr",                    "type0",  "CORR",   handleCorrMETData),
        ("muonCaloMETcorr",                 "",       "CORR",   handleCorrMETData),
        ("corrPfMetType1",                  "offset", "CORR",   handleCorrMETData),
        ("corrPfMetType1",                  "type1",  "CORR",   handleCorrMETData),
        ("corrPfMetType1",                  "type2",  "CORR",   handleCorrMETData),
        ("corrPfMetType0PfCand",            "",       "CORR",   handleCorrMETData),
        ("corrCaloMetType1",                "offset", "CORR",   handleCorrMETData),
        ("corrCaloMetType1",                "type1",  "CORR",   handleCorrMETData),
        ("corrCaloMetType1",                "type2",  "CORR",   handleCorrMETData),
        ("corrCaloMetType2",                "",       "CORR",   handleCorrMETData),
        ("corrPfMetShiftXY",                "",       "CORR",   handleCorrMETData),
        ("corrPfMetType0RecoTrack",         "",       "CORR",   handleCorrMETData),
        ("corrPfMetType0RecoTrackForType2", "",       "CORR",   handleCorrMETData),
        ("corrPfMetType2",                  "",       "CORR",   handleCorrMETData),
        )

    firstEvent = True
    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

                           
        for inputTag in inputTags:
            handle = inputTag[3]
            event.getByLabel(inputTag[0:3], handle)
            obj = handle.product()

            print '%6d'    % run,
            print '%9d'    % eventId,
            print '%35s'   % inputTag[0],
            print '%10s'   % inputTag[1],
            print '%10.3f' % obj.mex,
            print '%10.3f' % obj.mey,
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
