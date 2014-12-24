
##____________________________________________________________________________||
from PhysicsTools.PatAlgos.patTemplate_cfg import *


##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_AODSIM_532_numEvent100.root', 
options.outputFile = 'patTuple_runMEtUncertainties.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process.options.allowUnscheduled = cms.untracked.bool(True)

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")
process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
process.MessageLogger.cerr.FwkReport.reportEvery = 10

##____________________________________________________________________________||
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJetCollection(process,
                    jetSource = cms.InputTag('ak4PFJets'),
                    jetCorrections = ('AK4PF', ['L1FastJet', 'L2Relative', 'L3Absolute'], '')
                    )

##____________________________________________________________________________||
from PhysicsTools.PatUtils.tools.runType1PFMEtUncertainties import runType1PFMEtUncertainties
runType1PFMEtUncertainties(process,
                           addToPatDefaultSequence = False,
                           jetCollection = "selectedPatJets",
                           electronCollection = "selectedPatElectrons",
                           muonCollection = "selectedPatMuons",
                           tauCollection = "selectedPatTaus")


##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.out.fileName = cms.untracked.string(options.outputFile)

##____________________________________________________________________________||
