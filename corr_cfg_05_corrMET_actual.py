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
# process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
# process.load("JetMETCorrections.Type1MET.caloMETCorrections_cff")

##____________________________________________________________________________||
process.load('METCorrections_cff')

process.pfType0CorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrack'),
    ),
)   

process.pfType0p1CorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrack'),
        cms.InputTag('pfJetMETcorr', 'type1'),
    ),
)   

process.pfType0p1p2CorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrackForTypeIIMET'),
        cms.InputTag('pfJetMETcorr', 'type1'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   


process.pfType0p2CorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0recoTrackForTypeIIMET'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   

process.pfType0pfcCorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0'),
    ),
)   

process.pfType0pfcp1CorrectedMet = cms.EDProducer(
    "CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfMETcorrType0'),
        cms.InputTag('pfJetMETcorr', 'type1')        
    ),
)   


##____________________________________________________________________________||
process.p = cms.Path(
    process.pfMETcorrType0recoTrack +
    process.pfMETcorrType0recoTrackForTypeIIMET +
    process.pfMETcorrType2 +
    process.pfType1CorrectedMet +
    process.pfType1p2CorrectedMet +
    process.pfType0CorrectedMet +
    process.pfType0p1CorrectedMet +
    process.pfType0p1p2CorrectedMet +
    process.pfType0p2CorrectedMet +
    process.pfType0pfcCorrectedMet +
    process.pfType0pfcp1CorrectedMet +
    process.caloMETcorrType2 +
    process.caloType1CorrectedMet +
    process.caloType1p2CorrectedMet 
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
process.MessageLogger.categories.extend(["GetManyWithoutRegistration","GetByLabelWithoutRegistration"])
_messageSettings = cms.untracked.PSet(
                reportEvery = cms.untracked.int32(1),
                            optionalPSet = cms.untracked.bool(True),
                            limit = cms.untracked.int32(10000000)
                        )

process.MessageLogger.cerr.GetManyWithoutRegistration = _messageSettings
process.MessageLogger.cerr.GetByLabelWithoutRegistration = _messageSettings

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_05_corrMET_actual.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
