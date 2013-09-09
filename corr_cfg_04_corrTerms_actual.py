import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:corr_inputs.root', 
options.outputFile = 'corr_terms_actual.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process = cms.Process("CORR")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
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
    outputCommands = cms.untracked.vstring('keep *')
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
process.corrPfMetType1 = process.pfJetMETcorr.clone()
process.pfCandMETcorr = process.pfCandMETcorr.clone()
process.pfchsMETcorr = process.pfchsMETcorr.clone()

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.pfMETCorrectionType0_cfi")
process.corrPfMetType0PfCand = process.pfMETcorrType0.clone()

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.caloMETCorrections_cff")
process.corrCaloMetType1 = process.caloJetMETcorr.clone()

##____________________________________________________________________________||
process.corrCaloMetType2 = cms.EDProducer(
    "Type2CorrectionProducer",
    srcUnclEnergySums = cms.VInputTag(
        cms.InputTag('corrCaloMetType1', 'type2'),
        cms.InputTag('muonCaloMETcorr') # NOTE: use 'muonCaloMETcorr' for 'corMetGlobalMuons', do **not** use it for 'met' !!
        ),
    type2CorrFormula = cms.string("A + B*TMath::Exp(-C*x)"),
    type2CorrParameter = cms.PSet(
        A = cms.double(2.0),
        B = cms.double(1.3),
        C = cms.double(0.1)
        )
    )

process.corrPfMetType2 = cms.EDProducer(
    "Type2CorrectionProducer",
    srcUnclEnergySums = cms.VInputTag(
        cms.InputTag('corrPfMetType1', 'type2'),
        cms.InputTag('corrPfMetType1', 'offset'),
        cms.InputTag('pfCandMETcorr')
    ),
    type2CorrFormula = cms.string("A"),
    type2CorrParameter = cms.PSet(
        A = cms.double(1.4)
        )
    )

process.corrPfMetType0RecoTrack = cms.EDProducer(
    "ScaleCorrMETData",
    src = cms.InputTag('pfchsMETcorr', 'type0'),
    scaleFactor = cms.double(1 - 0.6)
    )

process.corrPfMetType0RecoTrackForType2 = cms.EDProducer(
    "ScaleCorrMETData",
    src = cms.InputTag('corrPfMetType0RecoTrack'),
    scaleFactor = cms.double(1.4)
    )

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.pfMETsysShiftCorrections_cfi")
process.corrPfMetShiftXY = process.pfMEtSysShiftCorr.clone()

# process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc

##____________________________________________________________________________||
process.correctionTermsPfMetType1Type2 = cms.Sequence(
    process.ak5PFJetsPtrs +
    process.particleFlowPtrs +
    process.pfCandsNotInJetPtrs +
    process.pfCandsNotInJet +
    process.pfCandMETcorr +
    process.corrPfMetType1 +
    process.corrPfMetType2
    )

process.correctionTermsPfMetType0RecoTrack = cms.Sequence(
    process.pfchsMETcorr +
    process.corrPfMetType0RecoTrack +
    process.corrPfMetType0RecoTrackForType2
    )

process.correctionTermsPfMetType0PFCandidate = cms.Sequence(
    process.type0PFMEtCorrectionPFCandToVertexAssociation +
    process.corrPfMetType0PfCand
    )

process.correctionTermsPfMetShiftXY = cms.Sequence(
    process.selectedVerticesForMEtCorr *
    process.corrPfMetShiftXY
    )

process.correctionTermsCaloMet = cms.Sequence(
    process.corrCaloMetType1 +
    process.muonCaloMETcorr +
    process.corrCaloMetType2
    )

##____________________________________________________________________________||
process.p = cms.Path(
    process.correctionTermsPfMetType1Type2 +
    process.correctionTermsPfMetType0RecoTrack +
    process.correctionTermsPfMetType0PFCandidate +
    process.correctionTermsPfMetShiftXY +
    process.correctionTermsCaloMet
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_04_corrTerms_actual.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
