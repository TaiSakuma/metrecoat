import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:corr_terms_actual.root', 
options.outputFile = 'corr_met_actual.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("TEST")

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
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *', 'keep *_*_*_CORR', 'keep *_*_*_TEST')
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctedMet_cff")

##____________________________________________________________________________||
process.p = cms.Path(
    process.pfMetT0rt +
    process.pfMetT0rtT1 +
    process.pfMetT0rtT1T2 +
    process.pfMetT0rtT2 +
    process.pfMetT0pc +
    process.pfMetT0pcT1 +
    process.pfMetT1 +
    process.pfMetT1T2 +
    process.caloMetT1 + 
    process.caloMetT1T2 + 
    process.pfMetT0rtTxy + 
    process.pfMetT0rtT1Txy + 
    process.pfMetT0rtT1T2Txy + 
    process.pfMetT0rtT2Txy +
    process.pfMetT0pcTxy +
    process.pfMetT0pcT1Txy +
    process.pfMetT1Txy+ 
    process.pfMetT1T2Txy
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_04_corrMET_actual.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
