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
process.caloMetT1 = cms.EDProducer(
    "CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrCaloMetType1', 'type1')
        ),
)   

process.caloMetT1T2 = cms.EDProducer(
    "CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrCaloMetType1', 'type1'),
        cms.InputTag('corrCaloMetType2')
    ),
)   

process.pfMetT0rt = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrack'),
    ),
)   

process.pfMetT0rtT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrack'),
        cms.InputTag('corrPfMetType1', 'type1'),
    ),
)   

process.pfMetT0rtT1T2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrackForType2'),
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetType2'),
    ),
)   

process.pfMetT0rtT2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrackForType2'),
        cms.InputTag('corrPfMetType2'),
    ),
)   

process.pfMetT0pc = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0PfCand'),
    ),
)   

process.pfMetT0pcT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0PfCand'),
        cms.InputTag('corrPfMetType1', 'type1')
    ),
)   

process.pfMetT1 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType1', 'type1')
    ),
)   

process.pfMetT1T2 = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetType2'),
    ),
)   

process.pfMetT0rtTxy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrack'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT0rtT1Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrack'),
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT0rtT1T2Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrackForType2'),
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetType2'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT0rtT2Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0RecoTrackForType2'),
        cms.InputTag('corrPfMetType2'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT0pcTxy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0PfCand'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT0pcT1Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType0PfCand'),
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT1Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   

process.pfMetT1T2Txy = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('corrPfMetType1', 'type1'),
        cms.InputTag('corrPfMetType2'),
        cms.InputTag('corrPfMetShiftXY'),
    ),
)   


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
processDumpFile = open('processDump-corr_cfg_03_corrMET_expected.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
