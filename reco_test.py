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

    def test_n_events(self):
        self.assertEqual(self.exEvents.size(), self.acEvents.size())

    def test_recoPFMETs_pfMet(self):
        label = ("pfMet" ,"" ,"METP")
        exHandle = self.exHandlePFMETs
        acHandle = self.acHandlePFMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoPFMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetTrue(self):
        label = ("genMetTrue" ,"" ,"METP")
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetCalo(self):
        label = ("genMetCalo" ,"" ,"METP")
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoGenMETs_genMetCaloAndNonPrompt(self):
        label = ("genMetCaloAndNonPrompt" ,"" ,"METP")
        exHandle = self.exHandleGenMETs
        acHandle = self.acHandleGenMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoGenMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_genMetIC5GenJets(self):
        label = ("genMetIC5GenJets", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMet(self):
        label = ("tcMet", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetCST(self):
        label = ("tcMetCST", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetRft2(self):
        label = ("tcMetRft2", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetVedu(self):
        label = ("tcMetVedu", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_tcMetWithPFclusters(self):
        label = ("tcMetWithPFclusters", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoMETs_htMetAK5(self):
        label = ("htMetAK5", "", "METP")
        exHandle = self.exHandleMETs
        acHandle = self.acHandleMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    # def test_recoMETs_htMetAK7(self):
    #     label = ("htMetAK7", "", "METP")
    #     exHandle = self.exHandleMETs
    #     acHandle = self.acHandleMETs
    #     candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
    #     self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    # def test_recoMETs_htMetKT4(self):
    #     label = ("htMetKT4", "", "METP")
    #     exHandle = self.exHandleMETs
    #     acHandle = self.acHandleMETs
    #     candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
    #     self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    # def test_recoMETs_htMetKT6(self):
    #     label = ("htMetKT6", "", "METP")
    #     exHandle = self.exHandleMETs
    #     acHandle = self.acHandleMETs
    #     candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
    #     self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    # def test_recoMETs_htMetIC5(self):
    #     label = ("htMetIC5", "", "METP")
    #     exHandle = self.exHandleMETs
    #     acHandle = self.acHandleMETs
    #     candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
    #     self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_met(self):
        label = ("met", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metHO(self):
        label = ("metHO", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metNoHF(self):
        label = ("metNoHF", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metNoHFHO(self):
        label = ("metNoHFHO", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metOpt(self):
        label = ("metOpt", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metOptHO(self):
        label = ("metOptHO", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metOptNoHF(self):
        label = ("metOptNoHF", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_metOptNoHFHO(self):
        label = ("metOptNoHFHO", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoCaloMETs_corMetGlobalMuons(self):
        label = ("corMetGlobalMuons", "" ,"METP")
        exHandle = self.exHandleCaloMETs
        acHandle = self.exHandleCaloMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoCaloMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoPFClusterMETs_pfClusterMet(self):
        label = ("pfClusterMet", "", "METP")
        exHandle = self.exHandlePFClusterMETs
        acHandle = self.acHandlePFClusterMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)

    def test_recoPFMETs_pfChargedMET(self):
        label = ("pfChargedMET" ,"" ,"METP")
        exHandle = self.exHandlePFMETs
        acHandle = self.acHandlePFMETs
        candidateAssertMethods = ('assert_recoLeafCandidate', 'assert_recoMET', 'assert_recoPFMET')
        self.assert_collection(label, exHandle, acHandle, candidateAssertMethods)


    def assert_collection(self, label, exHandle, acHandle, candidateAssertMethods):

        exEventIter = self.exEvents.__iter__()
        acEventIter = self.acEvents.__iter__()

        nevents = min(self.exEvents.size(), self.acEvents.size())
        for i in range(nevents):
            exEvent = exEventIter.next()
            acEvent = acEventIter.next()

            exEvent.getByLabel(label, exHandle)
            exMETs = exHandle.product()
            exMET = exMETs.front()

            acEvent.getByLabel(label, acHandle)
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
        self.assertEqual(actual.NeutralEMEtFraction()    , expected.NeutralEMEtFraction()   )
        self.assertEqual(actual.NeutralEMEt()            , expected.NeutralEMEt()           )
        self.assertEqual(actual.ChargedEMEtFraction()    , expected.ChargedEMEtFraction()   )
        self.assertEqual(actual.ChargedEMEt()            , expected.ChargedEMEt()           )
        self.assertEqual(actual.NeutralHadEtFraction()   , expected.NeutralHadEtFraction()  )
        self.assertEqual(actual.NeutralHadEt()           , expected.NeutralHadEt()          )
        self.assertEqual(actual.ChargedHadEtFraction()   , expected.ChargedHadEtFraction()  )
        self.assertEqual(actual.ChargedHadEt()           , expected.ChargedHadEt()          )
        self.assertEqual(actual.MuonEtFraction()         , expected.MuonEtFraction()        )
        self.assertEqual(actual.MuonEt()                 , expected.MuonEt()                )
        self.assertEqual(actual.InvisibleEtFraction()    , expected.InvisibleEtFraction()   )
        self.assertEqual(actual.InvisibleEt()            , expected.InvisibleEt()           )

    def assert_recoCaloMET(self, actual, expected):

        # double
        self.assertEqual(actual.maxEtInEmTowers()    , expected.maxEtInEmTowers()    )
        self.assertEqual(actual.maxEtInHadTowers()   , expected.maxEtInHadTowers()   )
        self.assertAlmostEqual(actual.etFractionHadronic() , expected.etFractionHadronic(), 15 )
        self.assertAlmostEqual(actual.emEtFraction()       , expected.emEtFraction()      , 15 )
        self.assertEqual(actual.hadEtInHB()          , expected.hadEtInHB()          )
        self.assertEqual(actual.hadEtInHO()          , expected.hadEtInHO()          )
        self.assertEqual(actual.hadEtInHE()          , expected.hadEtInHE()          )
        self.assertEqual(actual.hadEtInHF()          , expected.hadEtInHF()          )
        self.assertEqual(actual.emEtInEB()           , expected.emEtInEB()           )
        self.assertEqual(actual.emEtInEE()           , expected.emEtInEE()           )
        self.assertEqual(actual.emEtInHF()           , expected.emEtInHF()           )
        self.assertEqual(actual.metSignificance()    , expected.metSignificance()    )
        self.assertEqual(actual.CaloSETInpHF()       , expected.CaloSETInpHF()       )
        self.assertEqual(actual.CaloSETInmHF()       , expected.CaloSETInmHF()       )
        self.assertEqual(actual.CaloMETInpHF()       , expected.CaloMETInpHF()       )
        self.assertEqual(actual.CaloMETInmHF()       , expected.CaloMETInmHF()       )
        self.assertEqual(actual.CaloMETPhiInpHF()    , expected.CaloMETPhiInpHF()    )
        self.assertEqual(actual.CaloMETPhiInmHF()    , expected.CaloMETPhiInmHF()    )

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

        self.assertEqual(actual.dSignificance().size()  , expected.dSignificance().size())
        for a, e in zip(actual.dSignificance(), expected.dSignificance()):
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
