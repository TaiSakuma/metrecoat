
##____________________________________________________________________________||
from PhysicsTools.PatAlgos.patTemplate_cfg import *

##____________________________________________________________________________||
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.inputFiles = '/store/data/Run2012C/SingleMu/AOD/22Jan2013-v1/20000/000A8B8E-2875-E211-BC1E-00259073E3D6.root',
options.outputFile = 'patTuple_runMEtUncertainties.root'
options.maxEvents = -1
options.parseArguments()

##____________________________________________________________________________||
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
process.MessageLogger.cerr.FwkReport.reportEvery = 10

##____________________________________________________________________________||
from PhysicsTools.PatAlgos.tools.coreTools import *
runOnData(process)

##____________________________________________________________________________||
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJetCollection(process, cms.InputTag('ak5PFJets'),
                    doJTA        = True,
                    doBTagging   = False,
                    jetCorrLabel = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])),
                    doType1MET   = True,
                    genJetCollection=cms.InputTag("ak5GenJets"),
                    doJetID      = True,
                    )

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.globaltag = 'FT_53_V21_AN4::All'

##____________________________________________________________________________||
from PhysicsTools.PatUtils.tools.metUncertaintyTools import runMEtUncertainties
runMEtUncertainties(process)


##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
process.p = cms.Path(
    process.patDefaultSequence
)

##____________________________________________________________________________||
process.out.fileName = cms.untracked.string(options.outputFile)
process.out.outputCommands = cms.untracked.vstring(
    'keep *',
    # 'drop *',
    # 'keep patMETs_patMETs__PAT',
    ) 

##____________________________________________________________________________||
