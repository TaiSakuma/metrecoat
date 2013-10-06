#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
import unittest
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-e', '--expectedPath', default = './reco_expected.root', action = 'store', type = 'string')
parser.add_option('-a', '--actualPath', default = './reco_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)

##____________________________________________________________________________||
class METProducerTest(unittest.TestCase):

    def setUp(self):
        self.exEvents = Events([options.expectedPath])
        self.acEvents = Events([options.actualPath])

        self.exHandleValueMap = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")
        self.acHandleValueMap = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")

    def test_n_events(self):
        self.assertEqual(self.exEvents.size(), self.acEvents.size())

    def test_muonMETValueMapProducer(self):
        label = ("muonMETValueMapProducer", "muCorrData", "METP")
        exHandle = self.exHandleValueMap
        acHandle = self.acHandleValueMap
        self.assert_collection(label, exHandle, acHandle)


    def assert_collection(self, label, exHandle, acHandle):

        exEventIter = self.exEvents.__iter__()
        acEventIter = self.acEvents.__iter__()

        nevents = min(self.exEvents.size(), self.acEvents.size())
        for i in range(nevents):
            exEvent = exEventIter.next()
            acEvent = acEventIter.next()

            exEvent.getByLabel(label, exHandle)
            exValuemap = exHandle.product()

            acEvent.getByLabel(label, acHandle)
            acValuemap = acHandle.product()

            self.assertEqual(acValuemap.size(), exValuemap.size())

            for i in range(exValuemap.size()):
                expected = exValuemap.get(i)
                actual = acValuemap.get(i)
                self.assertEqual(actual.type()  , expected.type()  )
                self.assertEqual(actual.corrX() , expected.corrX() )
                self.assertEqual(actual.corrY() , expected.corrY() )
                self.assertEqual(actual.x()     , expected.x()     )
                self.assertEqual(actual.y()     , expected.y()     )
                self.assertEqual(actual.pt()    , expected.pt()    )

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
