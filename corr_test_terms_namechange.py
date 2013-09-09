#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
import math
import json
import re
import unittest
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-e', '--expectedPath', default = './corr_terms_expected.root', action = 'store', type = 'string')
parser.add_option('-a', '--actualPath', default = './corr_terms_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)

##____________________________________________________________________________||
class METProducerTest(unittest.TestCase):

    def setUp(self):
        self.exEvents = Events([options.expectedPath])
        self.acEvents = Events([options.actualPath])

        self.exHandleCorrMETData = Handle("CorrMETData") 
        self.acHandleCorrMETData = Handle("CorrMETData") 

        self.nameChangeMap = {
            "pfJetMETcorr"    : "corrPfMetType1",
            "pfMETcorrType0"  : "corrPfMetType0PfCand",
            "caloJetMETcorr"  : "corrCaloMetType1",
            "pfCandMETcorr"   : "pfCandMETcorr",
            "pfchsMETcorr"    : "pfchsMETcorr",
            "muonCaloMETcorr" : "muonCaloMETcorr",
            }


    def test_n_events(self):
        self.assertEqual(self.exEvents.size(), self.acEvents.size())

    def test_pfJetMETcorr_offset(self):
        label = ("pfJetMETcorr",    "offset", "CORR")
        self.assert_CorrMETData(label)

    def test_pfJetMETcorr_type1(self):
        label = ("pfJetMETcorr",    "type1",  "CORR")
        self.assert_CorrMETData(label)

    def test_pfJetMETcorr_type2(self):
        label = ("pfJetMETcorr",    "type2",  "CORR")
        self.assert_CorrMETData(label)

    def test_pfCandMETcorr(self):
        label = ("pfCandMETcorr",   "",       "CORR")
        self.assert_CorrMETData(label)

    def test_pfchsMETcorr_type0(self):
        label = ("pfchsMETcorr",    "type0",  "CORR")
        self.assert_CorrMETData(label)

    def test_pfMETcorrType0(self):
        label = ("pfMETcorrType0",  "",       "CORR")
        self.assert_CorrMETData(label)

    def test_muonCaloMETcorr(self):
        label = ("muonCaloMETcorr", "",       "CORR")
        self.assert_CorrMETData(label)

    def test_caloJetMETcorr_offset(self):
        label = ("caloJetMETcorr",  "offset", "CORR")
        self.assert_CorrMETData(label)

    def test_caloJetMETcorr_type1(self):
        label = ("caloJetMETcorr",  "type1",  "CORR")
        self.assert_CorrMETData(label)

    def test_caloJetMETcorr_type2(self):
        label = ("caloJetMETcorr",  "type2",  "CORR")
        self.assert_CorrMETData(label)

    def assert_CorrMETData(self, label):

        exHandle = self.exHandleCorrMETData
        acHandle = self.acHandleCorrMETData

        exEventIter = self.exEvents.__iter__()
        acEventIter = self.acEvents.__iter__()

        nevents = min(self.exEvents.size(), self.acEvents.size())
        for i in range(nevents):
            exEvent = exEventIter.next()
            acEvent = acEventIter.next()

            exEvent.getByLabel(label, exHandle)
            exCorr = exHandle.product()

            aclabel = list(label)
            aclabel[0] = self.nameChangeMap[aclabel[0]]
            acEvent.getByLabel(aclabel, acHandle)
            acCorr = acHandle.product()

            self.assertAlmostEqual(acCorr.mex, exCorr.mex, 12)
            self.assertAlmostEqual(acCorr.mey, exCorr.mey, 12)
            self.assertAlmostEqual(acCorr.sumet, exCorr.sumet, 12)
            self.assertAlmostEqual(acCorr.significance, exCorr.significance, 12)

##____________________________________________________________________________||
class ROOT_STL_Test(unittest.TestCase):

    def test_vector(self):
        a = ROOT.vector("double")()
        b = ROOT.vector("double")()
        self.assertEqual(a, b)

        a.push_back(2.2)
        self.assertNotEqual(a, b)

        a.push_back(3.5)
        a.push_back(4.2)

        b.push_back(2.2)
        b.push_back(3.5)
        b.push_back(4.2)
        self.assertEqual(a, b)

        a.push_back(2.7)
        b.push_back(8.9)
        self.assertNotEqual(a, b)

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
    unittest.main()
