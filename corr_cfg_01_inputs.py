import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = '/store/relval/CMSSW_7_0_0_pre3/RelValTTbar/GEN-SIM-RECO/PU_PRE_ST62_V8-v1/00000/18B6C0B5-C114-E311-8127-02163E007A38.root', 
options.outputFile = 'corr_inputs.root'
options.maxEvents = 100
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("INPU")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    # SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep recoGenMETs_*_*_*',
        'keep recoCaloMETs_*_*_*',
        'keep recoMETs_*_*_*',
        'keep recoPFMETs_*_*_*',
        'keep recoPFCandidates_particleFlow__*',
        'keep recoPFJets_ak5PFJets__*',
        'keep double_kt6PFJets_rho_*',
        'keep recoVertexs_offlinePrimaryVertices__*',
        'keep recoTracks_generalTracks__*',
        'keep recoTrackExtras_generalTracks__*',
        'keep recoTrackExtras_electronGsfTracks__*',
        'keep recoConversions_allConversions__*',
        'keep recoCaloJets_ak5CaloJets__*',
        'keep recoMuons_muons__*',
        'keep *_muonMETValueMapProducer_muCorrData_*',
        'keep recoVertexCompositeCandidates_generalV0Candidates_Kshort_*',
        'keep recoVertexCompositeCandidates_generalV0Candidates_Lambda_*',
        'keep recoGsfTracks_electronGsfTracks__*',
        'keep recoBeamSpot_offlineBeamSpot__*',
        'keep recoGsfElectrons_gsfElectrons__*',
        'keep recoGsfElectronCores_gsfElectronCores__*',
        'keep *TrackingRecHit*_generalTracks__*',
        'keep recoElectronSeeds_electronMergedSeeds__*',
        'keep recoTracks_conversionStepTracks__*',
        'keep recoTracks_ckfInOutTracksFromConversions__*',
        'keep recoTracks_ckfOutInTracksFromConversions__*',
        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_01_inputs.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
