import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = '/store/relval/CMSSW_7_0_0_pre3/RelValTTbar/GEN-SIM-RECO/PU_PRE_ST62_V8-v1/00000/18B6C0B5-C114-E311-8127-02163E007A38.root', 
options.outputFile = 'reco_inputs.root'
options.maxEvents = 100
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("INPU")

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.load("RecoMET.Configuration.CaloTowersOptForMET_cff")
process.load("RecoMET.Configuration.RecoMET_cff")
process.load("RecoMET.Configuration.RecoHTMET_cff")
process.load("RecoMET.Configuration.RecoGenMET_cff")
process.load("RecoMET.Configuration.GenMETParticles_cff")
process.load("RecoMET.Configuration.RecoPFMET_cff")

process.load("RecoJets.Configuration.CaloTowersRec_cff")

process.load("RecoMET/Configuration/RecoMET_BeamHaloId_cff")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.load('RecoParticleFlow.PFClusterProducer.particleFlowCluster_cff')
process.load('RecoParticleFlow.Configuration.RecoParticleFlow_cff')

process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")

process.load("RecoJets.JetProducers.PFClustersForJets_cff")

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.Generator_cff")

##____________________________________________________________________________||
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep recoGenParticles_genParticles_*_*',
        'keep *_genCandidatesForMET__*',
        'keep *_genParticlesForJets__*',
        'keep *_genParticlesForMETAllVisible__*',
        'keep recoGenJets_iterativeCone5GenJets__*',
        'keep *_towerMaker_*_*',
        'keep *_towerMakerWithHO_*_*',
        'keep *_calotoweroptmaker_*_*',
        'keep *_calotoweroptmakerWithHO_*_*',
        # 'keep recoCaloJets_kt4CaloJets_*_*',
        'keep recoCaloJets_kt6CaloJets_*_*',
        'keep recoCaloJets_ak5CaloJets_*_*',
        # 'keep recoCaloJets_ak7CaloJets_*_*',
        # 'keep recoCaloJets_iterativeCone5CaloJets_*_*',
        'keep *_muonMETValueMapProducer_*_*',
        'keep recoMuons_muons_*_*',
        'keep *_muonTCMETValueMapProducer_muCorrData_*',
        'keep recoTracks_generalTracks_*_*',
        'keep recoGsfElectrons_gsfElectrons_*_*',
        'keep recoGsfElectronCores_gsfElectronCores_*_*',
        'keep recoPFClusters_particleFlowClusterECAL_*_INPU',
        'keep recoPFClusters_particleFlowClusterHCAL_*_INPU',
        'keep recoPFClusters_particleFlowClusterHFHAD_*_INPU',
        'keep recoPFClusters_particleFlowClusterHFEM_*_INPU',
        'keep recoPFCandidates_particleFlow_*_*',
        'keep recoPFJets_ak5PFJets_*_*',
        'keep recoRecoPFClusterRefCandidates_pfClusterRefsForJetsHCAL_*_*',
        'keep recoRecoPFClusterRefCandidates_pfClusterRefsForJetsECAL_*_*',
        'keep recoRecoPFClusterRefCandidates_pfClusterRefsForJets_*_*',
        'keep recoVertexs_offlinePrimaryVertices_*_*',
        )
    )
##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
process.pfType1CorrectedMet.applyType0Corrections = cms.bool(False)
process.pfType1p2CorrectedMet.applyType0Corrections = cms.bool(False)

##____________________________________________________________________________||
process.p = cms.Path(
    process.genJetParticles*
    process.genMETParticles*
    process.calotoweroptmaker*
    process.calotoweroptmakerWithHO*
    process.towerMakerWithHO*
    process.particleFlowCluster*
    process.pfClusterRefsForJetsHCAL*
    process.pfClusterRefsForJetsECAL*
    process.pfClusterRefsForJets
    )

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-reco_cfg_01_inputs.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
