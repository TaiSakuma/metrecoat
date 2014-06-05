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
parser.add_option('-e', '--expectedPath', default = './reco_expected.root', action = 'store', type = 'string')
parser.add_option('-a', '--actualPath', default = './reco_actual.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)

sys.argv = args

##____________________________________________________________________________||
class METProducerTest(unittest.TestCase):

    def setUp(self):
        self.exEvents = Events([options.expectedPath])
        self.acEvents = Events([options.actualPath])

        self.exHandleGenMETs = Handle("std::vector<reco::GenMET>") 
        self.exHandlePFMETs = Handle("std::vector<reco::PFMET>") 
        self.exHandleCaloMETs = Handle("std::vector<reco::CaloMET>") 
        self.exHandleMETs = Handle("std::vector<reco::MET>") 
        self.exHandlePFClusterMETs = Handle("std::vector<reco::PFClusterMET>") 

        self.acHandleGenMETs = Handle("std::vector<reco::GenMET>") 
        self.acHandlePFMETs = Handle("std::vector<reco::PFMET>") 
        self.acHandleCaloMETs = Handle("std::vector<reco::CaloMET>") 
        self.acHandleMETs = Handle("std::vector<reco::MET>") 
        self.acHandlePFClusterMETs = Handle("std::vector<reco::PFClusterMET>") 

        self.exHandleMuonMETCorrectionData = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")
        self.acHandleMuonMETCorrectionData = Handle("edm::ValueMap<reco::MuonMETCorrectionData>")

    def test_n_events(self):
        self.assertEqual(self.exEvents.size(), self.acEvents.size())

    def test_recoPFMETs_pfMet(self):
        exLabel = ("pfMet" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandlePFMETs
        acHandle = self.acHandlePFMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoPFMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoPFMETs_pfMetWithSignificance(self):
        exLabel = ("pfMetWithSignificance" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandlePFMETs
        acHandle = self.acHandlePFMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoPFMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoPFMETs_pfChMet(self):
        exLabel = ("pfChMet" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandlePFMETs
        acHandle = self.acHandlePFMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoPFMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetTrue(self):
        exLabel = ("genMetTrue" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetCalo(self):
        exLabel = ("genMetCalo" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetCaloAndNonPrompt(self):
        exLabel = ("genMetCaloAndNonPrompt" ,"" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_genMetIC5GenJets(self):
        exLabel = ("genMetIC5GenJets", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMet(self):
        exLabel = ("tcMet", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetCST(self):
        exLabel = ("tcMetCST", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetRft2(self):
        exLabel = ("tcMetRft2", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetVedu(self):
        exLabel = ("tcMetVedu", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetPvtx(self):
        exLabel = ("tcMetPvtx", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetWithPFclusters(self):
        exLabel = ("tcMetWithPFclusters", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMet(self):
        exLabel = ("caloMet", "" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMetWithSignificance(self):
        exLabel = ("caloMetWithSignificance", "" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMetBEFO(self):
        exLabel = ("caloMetBEFO", "" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMetBE(self):
        exLabel = ("caloMetBE", "" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMetBEO(self):
        exLabel = ("caloMetBEO", "" ,"METP")
        acLabel = exLabel
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_caloMetM(self):
        exLabel = ("corMetGlobalMuons", "" ,"METP")
        acLabel = ("caloMetM", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)

    def test_recoPFClusterMETs_pfClusterMet(self):
        exLabel = ("pfClusterMet", "", "METP")
        acLabel = exLabel
        exHandle = self.exHandlePFClusterMETs
        acHandle = self.acHandlePFClusterMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(exLabel, acLabel, exHandle, acHandle, candidateAssertMethods)


    def test_muonMETValueMapProducer(self):
        exLabel = ("muonMETValueMapProducer", "muCorrData", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMuonMETCorrectionData
        acHandle = self.acHandleMuonMETCorrectionData
        self.assert_valuemap_MuonMETCorrectionData(exLabel, acLabel, exHandle, acHandle)

    def test_muonTCMETValueMapProducer(self):
        exLabel = ("muonTCMETValueMapProducer", "muCorrData", "METP")
        acLabel = exLabel
        exHandle = self.exHandleMuonMETCorrectionData
        acHandle = self.acHandleMuonMETCorrectionData
        self.assert_valuemap_MuonMETCorrectionData(exLabel, acLabel, exHandle, acHandle)


    def assert_collection(self, exLabel, acLabel, exHandle, acHandle, candidateAssertMethods):

        exEventIter = self.exEvents.__iter__()
        acEventIter = self.acEvents.__iter__()

        nevents = min(self.exEvents.size(), self.acEvents.size())
        for i in range(nevents):
            exEvent = exEventIter.next()
            acEvent = acEventIter.next()

            exEvent.getByLabel(exLabel, exHandle)
            exMETs = exHandle.product()
            exMET = exMETs.front()

            acEvent.getByLabel(acLabel, acHandle)
            acMETs = acHandle.product()

            self.assertEqual(acMETs.size(), 1)
            acMET = acMETs.front()

            for method in candidateAssertMethods:
                getattr(self, method)(acMET, exMET)

    def assert_recoPFMET(self, actual, expected):
        # double
        self.assertEqual(actual.photonEtFraction()        , expected.photonEtFraction()        )
        self.assertAlmostEqual(actual.photonEt()          , expected.photonEt()                , 10)
        self.assertEqual(actual.neutralHadronEtFraction() , expected.neutralHadronEtFraction() )
        self.assertAlmostEqual(actual.neutralHadronEt()   , expected.neutralHadronEt()         , 10)
        self.assertEqual(actual.electronEtFraction()      , expected.electronEtFraction()      )
        self.assertAlmostEqual(actual.electronEt()        , expected.electronEt()              , 10)
        self.assertEqual(actual.chargedHadronEtFraction() , expected.chargedHadronEtFraction() )
        self.assertAlmostEqual(actual.chargedHadronEt()   , expected.chargedHadronEt()         , 10)
        self.assertEqual(actual.muonEtFraction()          , expected.muonEtFraction()          )
        self.assertAlmostEqual(actual.muonEt()            , expected.muonEt()                  , 10)
        self.assertEqual(actual.HFHadronEtFraction()      , expected.HFHadronEtFraction()      )
        self.assertAlmostEqual(actual.HFHadronEt()        , expected.HFHadronEt()              , 10)
        self.assertEqual(actual.HFEMEtFraction()          , expected.HFEMEtFraction()          )
        self.assertAlmostEqual(actual.HFEMEt()            , expected.HFEMEt()                  , 10)

    def assert_recoGenMET(self, actual, expected):
        # double
        self.assertAlmostEqual(actual.NeutralEMEtFraction()    , expected.NeutralEMEtFraction()  , 7)
        self.assertAlmostEqual(actual.NeutralEMEt()            , expected.NeutralEMEt()          , 7)
        self.assertAlmostEqual(actual.ChargedEMEtFraction()    , expected.ChargedEMEtFraction()  , 7)
        self.assertAlmostEqual(actual.ChargedEMEt()            , expected.ChargedEMEt()          , 7)
        self.assertAlmostEqual(actual.NeutralHadEtFraction()   , expected.NeutralHadEtFraction() , 7)
        self.assertAlmostEqual(actual.NeutralHadEt()           , expected.NeutralHadEt()         , 7)
        self.assertAlmostEqual(actual.ChargedHadEtFraction()   , expected.ChargedHadEtFraction() , 7)
        self.assertAlmostEqual(actual.ChargedHadEt()           , expected.ChargedHadEt()         , 7)
        self.assertAlmostEqual(actual.MuonEtFraction()         , expected.MuonEtFraction()       , 7)
        self.assertAlmostEqual(actual.MuonEt()                 , expected.MuonEt()               , 7)
        self.assertAlmostEqual(actual.InvisibleEtFraction()    , expected.InvisibleEtFraction()  , 7)
        self.assertAlmostEqual(actual.InvisibleEt()            , expected.InvisibleEt()          , 7)

    def assert_recoCaloMET(self, actual, expected):

        # double
        self.assertEqual(actual.maxEtInEmTowers()    , expected.maxEtInEmTowers()    )
        self.assertEqual(actual.maxEtInHadTowers()   , expected.maxEtInHadTowers()   )
        self.assertAlmostEqual(actual.etFractionHadronic() , expected.etFractionHadronic(), 7)
        self.assertAlmostEqual(actual.emEtFraction()       , expected.emEtFraction()      , 7)
        self.assertAlmostEqual(actual.hadEtInHB()          , expected.hadEtInHB()         , 7)
        self.assertAlmostEqual(actual.hadEtInHO()          , expected.hadEtInHO()         , 7)
        self.assertAlmostEqual(actual.hadEtInHE()          , expected.hadEtInHE()         , 7)
        self.assertAlmostEqual(actual.hadEtInHF()          , expected.hadEtInHF()         , 7)
        self.assertAlmostEqual(actual.emEtInEB()           , expected.emEtInEB()          , 7)
        self.assertAlmostEqual(actual.emEtInEE()           , expected.emEtInEE()          , 7)
        self.assertAlmostEqual(actual.emEtInHF()           , expected.emEtInHF()          , 7)
        self.assertAlmostEqual(actual.metSignificance()    , expected.metSignificance()   , 7)
        self.assertAlmostEqual(actual.CaloSETInpHF()       , expected.CaloSETInpHF()      , 7)
        self.assertAlmostEqual(actual.CaloSETInmHF()       , expected.CaloSETInmHF()      , 7)
        self.assertAlmostEqual(actual.CaloMETInpHF()       , expected.CaloMETInpHF()      , 7)
        self.assertAlmostEqual(actual.CaloMETInmHF()       , expected.CaloMETInmHF()      , 7)
        self.assertAlmostEqual(actual.CaloMETPhiInpHF()    , expected.CaloMETPhiInpHF()   , 7)
        self.assertAlmostEqual(actual.CaloMETPhiInmHF()    , expected.CaloMETPhiInmHF()   , 7)

    def assert_recoMET(self, actual, expected):

        # double
        self.assertAlmostEqual(actual.sumEt()     , expected.sumEt()          , 10)
        self.assertAlmostEqual(actual.mEtSig()    , expected.mEtSig()         , 10)
        self.assertEqual(actual.significance()    , expected.significance()   )
        self.assertEqual(actual.e_longitudinal()  , expected.e_longitudinal() )

        self.assertEqual(actual.dmEx().size()    , expected.dmEx().size())
        for a, e in zip(actual.dmEx(), expected.dmEx()):
            self.assertEqual(a , e)

        self.assertEqual(actual.dmEy().size()     , expected.dmEy().size())
        for a, e in zip(actual.dmEy(), expected.dmEy()):
            self.assertEqual(a , e)

        self.assertEqual(actual.dsumEt().size()   , expected.dsumEt().size())
        for a, e in zip(actual.dsumEt(), expected.dsumEt()):
            self.assertEqual(a , e)

        self.assertEqual(actual.mEtCorr().size(), expected.mEtCorr().size())
        for a, e in zip(actual.mEtCorr(), expected.mEtCorr()):
            # self.assertEqual(a.mex          , e.mex)
            # self.assertEqual(a.mey          , e.mey)
            # self.assertEqual(a.sumet        , e.sumet)
            # self.assertEqual(a.significance , e.significance)
            pass

        actualSigMatrix = actual.getSignificanceMatrix()
        expectedSigMatrix = expected.getSignificanceMatrix()
        self.assertEqual(actualSigMatrix.GetNrows(), expectedSigMatrix.GetNrows())
        self.assertEqual(actualSigMatrix.GetNcols(), expectedSigMatrix.GetNcols())
        self.assertEqual(actualSigMatrix.GetNoElements(), expectedSigMatrix.GetNoElements())
        for irow in range(actualSigMatrix.GetNrows()):
            for icol in range(actualSigMatrix.GetNcols()):
                self.assertEqual(actualSigMatrix(irow, icol), expectedSigMatrix(irow, icol))

    def assert_recoLeafCandidate(self, actual, expected):

        # size_t
        self.assertEqual(actual.numberOfDaughters()     , expected.numberOfDaughters()     )
        self.assertEqual(actual.numberOfMothers()       , expected.numberOfMothers()       )
        
        # int
        self.assertEqual(actual.charge()                , expected.charge()                )
        self.assertEqual(actual.threeCharge()           , expected.threeCharge()           )

        # double
        self.assertEqual(actual.p()                     , expected.p()                     )
        self.assertEqual(actual.energy()                , expected.energy()                )
        self.assertEqual(actual.et()                    , expected.et()                    )
        self.assertEqual(actual.mass()                  , expected.mass()                  )
        self.assertEqual(actual.massSqr()               , expected.massSqr()               )
        self.assertEqual(actual.mt()                    , expected.mt()                    )
        self.assertEqual(actual.mtSqr()                 , expected.mtSqr()                 )
        self.assertEqual(actual.px()                    , expected.px()                    )
        self.assertEqual(actual.py()                    , expected.py()                    )
        self.assertEqual(actual.pz()                    , expected.pz()                    )
        self.assertAlmostEqual(actual.pt(), expected.pt(), 5)
        self.assertEqual(actual.phi()                   , expected.phi()                   )
        self.assertEqual(actual.theta()                 , expected.theta()                 )
        self.assertEqual(actual.eta()                   , expected.eta()                   )
        # self.assertEqual(actual.rapidity()              , expected.rapidity()              )
        # self.assertEqual(actual.y()                     , expected.y()                     )
        self.assertEqual(actual.vx()                    , expected.vx()                    )
        self.assertEqual(actual.vy()                    , expected.vy()                    )
        self.assertEqual(actual.vz()                    , expected.vz()                    )

        # int
        self.assertEqual(actual.pdgId()                 , expected.pdgId()                 )
        self.assertEqual(actual.status()                , expected.status()                )

        # bool
        self.assertEqual(actual.longLived()             , expected.longLived()             )
        self.assertEqual(actual.massConstraint()        , expected.massConstraint()        )

        # double
        self.assertEqual(actual.vertexChi2()            , expected.vertexChi2()            )
        self.assertEqual(actual.vertexNdof()            , expected.vertexNdof()            )
        self.assertEqual(actual.vertexNormalizedChi2()  , expected.vertexNormalizedChi2()  )

        # bool
        self.assertEqual(actual.hasMasterClone()        , expected.hasMasterClone()        )
        self.assertEqual(actual.hasMasterClonePtr()     , expected.hasMasterClonePtr()     )
        self.assertEqual(actual.isElectron()            , expected.isElectron()            )
        self.assertEqual(actual.isMuon()                , expected.isMuon()                )
        self.assertEqual(actual.isStandAloneMuon()      , expected.isStandAloneMuon()      )
        self.assertEqual(actual.isGlobalMuon()          , expected.isGlobalMuon()          )
        self.assertEqual(actual.isTrackerMuon()         , expected.isTrackerMuon()         )
        self.assertEqual(actual.isCaloMuon()            , expected.isCaloMuon()            )
        self.assertEqual(actual.isPhoton()              , expected.isPhoton()              )
        self.assertEqual(actual.isConvertedPhoton()     , expected.isConvertedPhoton()     )
        self.assertEqual(actual.isJet()                 , expected.isJet()                 )


    def assert_valuemap_MuonMETCorrectionData(self, exLabel, acLabel, exHandle, acHandle):

        exEventIter = self.exEvents.__iter__()
        acEventIter = self.acEvents.__iter__()

        nevents = min(self.exEvents.size(), self.acEvents.size())
        for i in range(nevents):
            exEvent = exEventIter.next()
            acEvent = acEventIter.next()

            exEvent.getByLabel(exLabel, exHandle)
            exMuonMETCorrectionData = exHandle.product()

            acEvent.getByLabel(acLabel, acHandle)
            acMuonMETCorrectionData = acHandle.product()

            self.assertEqual(acMuonMETCorrectionData.size(), exMuonMETCorrectionData.size())

            for i in range(exMuonMETCorrectionData.size()):
                expected = exMuonMETCorrectionData.get(i)
                actual = acMuonMETCorrectionData.get(i)
                self.assertEqual(actual.type()  , expected.type()  )
                self.assertEqual(actual.corrX() , expected.corrX() )
                self.assertEqual(actual.corrY() , expected.corrY() )
                self.assertEqual(actual.x()     , expected.x()     )
                self.assertEqual(actual.y()     , expected.y()     )
                self.assertEqual(actual.pt()    , expected.pt()    )

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
