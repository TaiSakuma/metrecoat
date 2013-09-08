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
process.load('METCorrections_cff')

process.caloMetT1 = cms.EDProducer(
    "CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('caloJetMETcorr', 'type1')
        ),
)   

process.caloMetT1T2 = cms.EDProducer(
    "CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('caloJetMETcorr', 'type1'),
        cms.InputTag('caloMETcorrType2')
    ),
)   

process.pfMetT0rt = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrack'),
    ),
)   

process.pfMetT0rtT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrack'),
        cms.InputTag('pfJetMETcorr', 'type1'),
    ),
)   

process.pfMetT0rtT1T2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrackForTypeIIMET'),
        cms.InputTag('pfJetMETcorr', 'type1'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   


process.pfMetT0rtT2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrackForTypeIIMET'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   

process.pfMetT0pc = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0'),
    ),
)   

process.pfMetT0pcT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0'),
        cms.InputTag('pfJetMETcorr', 'type1')        
    ),
)   

process.pfMetT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1')
    ),
)   

process.pfMetT1T2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   


##____________________________________________________________________________||
process.p = cms.Path(
    process.pfMETcorrType0recoTrack +
    process.pfMETcorrType0recoTrackForTypeIIMET +
    process.pfMETcorrType2 +
    process.pfMetT0rt +
    process.pfMetT0rtT1 +
    process.pfMetT0rtT1T2 +
    process.pfMetT0rtT2 +
    process.pfMetT0pc +
    process.pfMetT0pcT1 +
    process.pfMetT1 +
    process.pfMetT1T2 +
    process.caloMETcorrType2 +
    process.caloMetT1 + 
    process.caloMetT1T2
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_05_corrMET_actual.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
