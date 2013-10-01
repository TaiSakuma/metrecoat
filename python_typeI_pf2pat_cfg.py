
##____________________________________________________________________________||
from PhysicsTools.PatAlgos.patTemplate_cfg import *

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = 'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/TTJets_AODSIM_532_numEvent100.root', 
options.outputFile = 'patTuple_typeI_pf2pat.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
process.MessageLogger.cerr.FwkReport.reportEvery = 10

##____________________________________________________________________________||
process.load("PhysicsTools.PatAlgos.patSequences_cff")

##____________________________________________________________________________||
from PhysicsTools.PatAlgos.tools.pfTools import *

##____________________________________________________________________________||
process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
process.producePatPFMETCorrections.replace(
    process.pfCandMETcorr,
    process.type0PFMEtCorrection *
    process.patPFMETtype0Corr *
    process.pfCandMETcorr 
    )

postfix = "PFlow"
jetAlgo="AK5"
usePF2PAT(process, 
          runPF2PAT = True,
          jetAlgo = jetAlgo,
          runOnMC = True,
          postfix = postfix, 
          typeIMetCorrections = True
          )

getattr(process,'patMETs'+postfix).metSource = cms.InputTag("patType1CorrectedPFMet"+postfix)

getattr(process,'patType1CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
    cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
    cms.InputTag("patPFMETtype0Corr"+postfix)
)

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
# process.p = cms.Path(
#     process.type0PFMEtCorrection *
#     process.patDefaultSequence
# )

process.p = cms.Path(
    getattr(process,"patPF2PATSequence"+postfix)
)

##____________________________________________________________________________||
process.out.fileName = cms.untracked.string(options.outputFile)
process.out.outputCommands = cms.untracked.vstring(
    'keep *',
    # 'drop *',
    # 'keep patMETs_patMETs__PAT',
    ) 

##____________________________________________________________________________||
