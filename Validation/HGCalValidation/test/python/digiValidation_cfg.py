###############################################################################
# Way to use this:
#   cmsRun digiValidation_cfg.py geometry=D92
#
#   Options for geometry D88, D92, D93
#
###############################################################################
import FWCore.ParameterSet.Config as cms
import os, sys, imp, re
import FWCore.ParameterSet.VarParsing as VarParsing

####################################################################
### SETUP OPTIONS
options = VarParsing.VarParsing('standard')
options.register('geometry',
                 "D88",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "geometry of operations: D88, D92, D93")

### get and parse the command line arguments
options.parseArguments()

print(options)

####################################################################
# Use the options

if (options.geometry == "D88"):
    from Configuration.Eras.Era_Phase2C11M9_cff import Phase2C11M9
    process = cms.Process('testHGCalDigiLocal',Phase2C11M9)
    process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
    fileName = 'file:DigiValD88.root'
elif (options.geometry == "D92"):
    from Configuration.Eras.Era_Phase2C11M9_cff import Phase2C11M9
    process = cms.Process('testHGCalDigiLocal',Phase2C11M9)
    process.load('Configuration.Geometry.GeometryExtended2026D92Reco_cff')
    fileName = 'file:DigiValD92.root'
else:
    from Configuration.Eras.Era_Phase2C11M9_cff import Phase2C11M9
    process = cms.Process('testHGCalDigiLocal',Phase2C11M9)
    process.load('Configuration.Geometry.GeometryExtended2026D93Reco_cff')
    fileName = 'file:DigiValD93.root'

print("Output file: ", fileName)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedGauss_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T21', '')

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet()

# Production Info
process.configurationMetadata = cms.untracked.PSet(
	version    = cms.untracked.string('$Revision: 1.20 $'),
	annotation = cms.untracked.string('SingleMuonPt10_cfi nevts:10'),
	name       = cms.untracked.string('Applications')
	)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
					      splitLevel                   = cms.untracked.int32(0),
					      eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
					      outputCommands               = process.FEVTDEBUGHLTEventContent.outputCommands,
					      fileName                     = cms.untracked.string(fileName),
					      dataset                      = cms.untracked.PSet(
	filterName = cms.untracked.string(''),
	dataTier   = cms.untracked.string('GEN-SIM-DIGI-RAW')
	),
					      SelectEvents                 = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step'))
					      )

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")

process.generator = cms.EDProducer("FlatRandomPtGunProducer",
   PGunParameters = cms.PSet(
	MaxPt  = cms.double(10.01),
	MinPt  = cms.double(9.99),
	PartID = cms.vint32(13),
	MaxEta = cms.double(2.50),
	MaxPhi = cms.double(3.14159265359),
	MinEta = cms.double(1.75),
	MinPhi = cms.double(-3.14159265359)
	),
   Verbosity       = cms.untracked.int32(0),
   psethack        = cms.string('single electron pt 10'),
   AddAntiParticle = cms.bool(True),
   firstRun        = cms.untracked.uint32(1)
)

process.mix.digitizers = cms.PSet(process.theDigitizersValid)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Output definition
process.ValidationOutput = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *', 'keep *_MEtoEDMConverter_*_*'),
    fileName = cms.untracked.string('file:output_digiVal_test.root'),
)

process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.MEtoEDMConverter_cfi")

process.load("Validation.HGCalValidation.digiValidation_cff")

## path and endpath deffinition 
process.p1 = cms.Path(process.hgcalDigiValidationEE+
		      process.hgcalDigiValidationHEF+
		      process.hgcalDigiValidationHEB)
process.p2 = cms.Path(process.MEtoEDMConverter)
process.output_step = cms.EndPath(process.ValidationOutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,
				process.simulation_step,process.digitisation_step,
				process.L1simulation_step,process.digi2raw_step,
				process.endjob_step,process.p1,process.p2,process.output_step)

# filter all path with the production filter sequence
for path in process.paths:
        getattr(process,path)._seq = process.generator * getattr(process,path)._seq
	
for label, prod in process.producers_().items():
        if prod.type_() == "OscarMTProducer":
            # ugly hack
            prod.__dict__['_TypedParameterizable__type'] = "OscarProducer"
