import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:reco_inputs.root', 
options.outputFile = 'reco_actual.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("METP")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")

##____________________________________________________________________________||
process.load("RecoMET.Configuration.RecoGenMET_cff")
process.load("RecoMET.Configuration.RecoMET_cff")
process.load("RecoMET.Configuration.RecoPFMET_cff")


process.load("RecoMET.METProducers.HTMET_cfi")
process.load("RecoMET.METProducers.pfChargedMET_cfi")

##____________________________________________________________________________||
process.load("RecoMET/METProducers/PFClusterMET_cfi")

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
        'keep *_*_*_METP'
        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
# process.pfMet.globalThreshold = cms.double(5.0)

##____________________________________________________________________________||
process.p = cms.Path(
    process.genMetCalo *
    process.genMetCaloAndNonPrompt * 
    process.genMetTrue *
    process.genMetIC5GenJets *
    process.met *
    process.metNoHF *
    process.metHO *
    process.metNoHFHO *
    process.metOpt *
    process.metOptNoHF *
    process.metOptHO *
    process.metOptNoHFHO *
    # process.htMetKT4 *
    process.htMetKT6 *
    # process.htMetIC5 *
    process.htMetAK5 * 
    # process.htMetAK7 *
    process.corMetGlobalMuons *
    process.tcMet *
    process.tcMetWithPFclusters *
    process.pfMet*
    process.pfClusterMet *
    process.particleFlowForChargedMET *
    process.pfChargedMET
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-reco_cfg_03_actual.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
