import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
caloMETcorrType2 = cms.EDProducer(
    "Type2CorrectionProducer",
    srcUnclEnergySums = cms.VInputTag(
        cms.InputTag('caloJetMETcorr', 'type2'),
        cms.InputTag('muonCaloMETcorr') # NOTE: use 'muonCaloMETcorr' for 'corMetGlobalMuons', do **not** use it for 'met' !!
        ),                              
    type2CorrFormula = cms.string("A + B*TMath::Exp(-C*x)"),
    type2CorrParameter = cms.PSet(
        A = cms.double(2.0),
        B = cms.double(1.3),
        C = cms.double(0.1) 
        )
    )
##____________________________________________________________________________||
caloType1CorrectedMet = cms.EDProducer("CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('caloJetMETcorr', 'type1')
    ),
)   

##____________________________________________________________________________||
caloType1p2CorrectedMet = cms.EDProducer("CorrectedCaloMETProducer2",
    src = cms.InputTag('corMetGlobalMuons'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('caloJetMETcorr', 'type1'),
        cms.InputTag('caloMETcorrType2')
    ),
)   

##____________________________________________________________________________||
pfMETcorrType0recoTrack = cms.EDProducer(
    "ScaleCorrMETData",
    src = cms.InputTag('pfchsMETcorr', 'type0'),
    scaleFactor = cms.double(1 - 0.6)
    )

##____________________________________________________________________________||
pfMETcorrType0recoTrackForTypeIIMET = cms.EDProducer(
    "ScaleCorrMETData",
    src = cms.InputTag('pfMETcorrType0recoTrack'),
    scaleFactor = cms.double(1.4)
    )

##____________________________________________________________________________||
pfMETcorrType2 = cms.EDProducer(
    "Type2CorrectionProducer",
    srcUnclEnergySums = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type2'),
        cms.InputTag('pfJetMETcorr', 'offset'),
        cms.InputTag('pfCandMETcorr')                                    
    ),                              
    type2CorrFormula = cms.string("A"),
    type2CorrParameter = cms.PSet(
        A = cms.double(1.4)
        )
    )

##____________________________________________________________________________||
pfType1CorrectedMet = cms.EDProducer("CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1')
    ),
)   

##____________________________________________________________________________||
pfType1p2CorrectedMet = cms.EDProducer("CorrectedPFMETProducer2",
    src = cms.InputTag('pfMet'),
    srcCorrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1'),
        cms.InputTag('pfMETcorrType2'),
    ),
)   

##____________________________________________________________________________||
producePFMETCorrections = cms.Sequence(
    pfType1CorrectedMet *
    pfType1p2CorrectedMet
)

##____________________________________________________________________________||
