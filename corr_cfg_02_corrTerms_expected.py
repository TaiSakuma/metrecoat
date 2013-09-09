import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:corr_inputs.root', 
options.outputFile = 'corr_terms_expected.root'
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
process.corrPfMetType1 = cms.EDProducer(
    "PFJetMETcorrInputProducer",
    src = cms.InputTag('ak5PFJets'),
    offsetCorrLabel = cms.string("ak5PFL1Fastjet"),
    jetCorrLabel = cms.string("ak5PFL1FastL2L3"), # NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for Data
    jetCorrEtaMax = cms.double(9.9),
    type1JetPtThreshold = cms.double(10.0),
    skipEM = cms.bool(True),
    skipEMfractionThreshold = cms.double(0.90),
    skipMuons = cms.bool(True),
    skipMuonSelection = cms.string("isGlobalMuon | isStandAloneMuon")
)

process.pfCandMETcorr = cms.EDProducer(
    "PFCandMETcorrInputProducer",
    src = cms.InputTag('pfCandsNotInJet')
)

process.pfchsMETcorr = cms.EDProducer(
    "PFchsMETcorrInputProducer",
    src = cms.InputTag('offlinePrimaryVertices'),
    goodVtxNdof = cms.uint32(4),
    goodVtxZ = cms.double(24)
)

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.pfMETCorrectionType0_cfi")
process.corrPfMetType0PfCand = cms.EDProducer(
    "Type0PFMETcorrInputProducer",
    srcPFCandidateToVertexAssociations = cms.InputTag('pfCandidateToVertexAssociation'),
    srcHardScatterVertex = cms.InputTag('selectedPrimaryVertexHighestPtTrackSumForPFMEtCorrType0'),
    correction = cms.PSet(
        formula = cms.string("-([0] + [1]*x)*(1.0 + TMath::Erf(-[2]*TMath::Power(x, [3])))"),
        par0 = cms.double(0.),
        par1 = cms.double(-0.703151),
        par2 = cms.double(0.0303531),
        par3 = cms.double(0.909209)
    ),
    minDz = cms.double(0.2) # [cm], minimum distance required between pile-up vertices and "hard scatter" vertex
)

##____________________________________________________________________________||
# process.load("JetMETCorrections.Type1MET.caloMETCorrections_cff")
process.corrCaloMetType1 = cms.EDProducer(
    "CaloJetMETcorrInputProducer",
    src = cms.InputTag('ak5CaloJets'),
    jetCorrLabel = cms.string("ak5CaloL2L3"), # NOTE: use "ak5CaloL2L3" for MC / "ak5CaloL2L3Residual" for Data
    jetCorrEtaMax = cms.double(9.9),
    type1JetPtThreshold = cms.double(20.0),
    skipEM = cms.bool(True),
    skipEMfractionThreshold = cms.double(0.90),
    srcMET = cms.InputTag('corMetGlobalMuons')
)

process.muonCaloMETcorr = cms.EDProducer(
    "MuonMETcorrInputProducer",
    src = cms.InputTag('muons'),
    srcMuonCorrections = cms.InputTag('muonMETValueMapProducer', 'muCorrData')
)

##____________________________________________________________________________||
process.p = cms.Path(
    process.ak5PFJetsPtrs +
    process.particleFlowPtrs +
    process.pfCandsNotInJetPtrs +
    process.pfCandsNotInJet +
    process.corrPfMetType1 +
    process.pfCandMETcorr +
    process.pfchsMETcorr +
    process.corrCaloMetType1 +
    process.muonCaloMETcorr +
    process.type0PFMEtCorrectionPFCandToVertexAssociation +
    process.corrPfMetType0PfCand
)

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
processDumpFile = open('processDump-corr_cfg_02_corrTerms_expected.py', 'w')
print >> processDumpFile, process.dumpPython()

##____________________________________________________________________________||
