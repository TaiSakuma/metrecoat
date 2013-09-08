import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:corr_terms_expected.root', 
options.outputFile = 'corr_met_expected.root'
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
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")

process.pfType0CorrectedMet = process.pfType1CorrectedMet.clone()
process.pfType0CorrectedMet.applyType0Corrections = cms.bool(True)
process.pfType0CorrectedMet.applyType1Corrections = cms.bool(False)

process.pfType0p1CorrectedMet = process.pfType1CorrectedMet.clone()
process.pfType0p1CorrectedMet.applyType0Corrections = cms.bool(True)

process.pfType0p1p2CorrectedMet = process.pfType1p2CorrectedMet.clone()
process.pfType0p1p2CorrectedMet.applyType0Corrections = cms.bool(True)

process.pfType0p2CorrectedMet = process.pfType1p2CorrectedMet.clone()
process.pfType0p2CorrectedMet.applyType0Corrections = cms.bool(True)
process.pfType0p2CorrectedMet.applyType1Corrections = cms.bool(False)


process.pfType0pfcCorrectedMet = process.pfType1CorrectedMet.clone()
process.pfType0pfcCorrectedMet.srcType1Corrections = cms.VInputTag(
    cms.InputTag('pfMETcorrType0'),
)

process.pfType0pfcp1CorrectedMet = process.pfType1CorrectedMet.clone()
process.pfType0pfcp1CorrectedMet.srcType1Corrections = cms.VInputTag(
    cms.InputTag('pfMETcorrType0'),
    cms.InputTag('pfJetMETcorr', 'type1')        
)

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.caloMETCorrections_cff")


##____________________________________________________________________________||
process.p = cms.Path(
    process.pfType1CorrectedMet +
    process.pfType1p2CorrectedMet +
    process.pfType0CorrectedMet +
    process.pfType0p1CorrectedMet +
    process.pfType0p1p2CorrectedMet +
    process.pfType0p2CorrectedMet +
    process.pfType0pfcCorrectedMet +
    process.pfType0pfcp1CorrectedMet +
    process.caloType1CorrectedMet +
    process.caloType1p2CorrectedMet
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_03_corrMET_expected.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
