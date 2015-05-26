#FAANG experiment metadata spec

This document describes the specification for all experiment metadata. You can find an overview of our metadata and archival plans in [the overview document](faang_metadata_overview.md). The [sample](faang_sample_metadata.md) and [analysis](faang_analysis_metadata.md) documents are also in this [git repo](https://github.com/FAANG/faang-metadata).

Experiments are expected to fall into two categories 

sequencing experiments, archived in an SRA database (hosted at NCBI, EMBL-EBI and DDBJ). Some of this submissions will be brokered by ArrayExpress.
array experiments, archived in ArrayExpress or GEO. 

##Experiment attributes

These following elements must always be present in any experiment metadata

* Assay Type
	* What class of experiment is being performed? e.g. RNA-Seq or expression array. This is stored as a library strategy attribute in the SRA database model. Terms used should have an equivalent in EFO (child term of [EFO:0002773](http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=EFO&termId=EFO%3A0002773&termName=assay%20by%20instrument)).
* Experiment target
	* What is the experiment trying to find? e.g. Methylated DNA, polyA RNA, total RNA. This should be stored in the experiment attributes for SRA archives using their controlled vocabulary.
* Sample
	* This should be a reference to the Biosample ID for the specimen, purified cell, cultured cell or cell line the experiment was conducted  on
* Sample Storage
	* This should reference how the sample was stored e.g frozen, liquid nitrogen
* Sample to preparation interval / preparation date 
	* This should list how long between the sample being taken and use in the experiment
* Experimental Protocol
	* This should point to a PDF for the protocol stored in a permenant location on the FAANG FTP or website


The metadata group will seek guidance from the assay group on what needs to be recorded here for each assay type.

#Assay specific attributes

Each assay type will require metadata in addition to the core set of common attributes. The initial set proposed is based upon the [IHEC metadata standards](http://ihec-epigenomes.org/research/reference-epigenome-standards/)

##Whole-genome bisulfite sequencing
Assay type: methylation profiling by high throughput sequencing ([EFO:0002761](http://www.ebi.ac.uk/efo/EFO_0002761))

Experiment target: methylated DNA ([SO:0000306](http://www.sequenceontology.org/browser/current_svn/term/SO:0000306))

###Protocols
- EXTRACTION_PROTOCOL The protocol used to isolate the extract material.
- BISULFITE_CONVERSION_PROTOCOL The bisulfite conversion protocol.
- LIBRARY_GENERATION_PCR_PRODUCT_ISOLATION_PROTOCOL The protocol for isolating PCR products used for library generation.

###Attributes

- EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR The type of sonicator used for extraction.
- EXTRACTION_PROTOCOL_SONICATION_CYCLES The number of sonication cycles used for extraction.
- DNA_PREPARATION_INITIAL_DNA_QNTY The initial DNA quantity used in preparation.
- DNA_PREPARATION_FRAGMENT_SIZE_RANGE The DNA fragment size range used in preparation.
- DNA_PREPARATION_ADAPTOR_SEQUENCE The sequence of the adaptor used in preparation.
- DNA_PREPARATION_ADAPTOR_LIGATION_PROTOCOL The protocol used for adaptor ligation.
- DNA_PREPARATION_POST-LIGATION_FRAGMENT_SIZE_SELECTION The fragment size selection after adaptor ligation.
- BISULFITE_CONVERSION_PERCENT The bisulfite conversion percent and how it was determined.
- LIBRARY_GENERATION_PCR_TEMPLATE_CONC The PCR template concentration for library generation.
- LIBRARY_GENERATION_PCR_POLYMERASE_TYPE The PCR polymerase used for library generation
- LIBRARY_GENERATION_PCR_THERMOCYCLING_PROGRAM The thermocycling program used for library generation.
- LIBRARY_GENERATION_PCR_NUMBER_CYCLES The number of PCR cycles used for library generation.
- LIBRARY_GENERATION_PCR_F_PRIMER_SEQUENCE The sequence of the PCR forward primer used for library generation.
- LIBRARY_GENERATION_PCR_R_PRIMER_SEQUENCE The sequence of the PCR reverse primer used for library generation.
- LIBRARY_GENERATION_PCR_PRIMER_CONC The concentration of the PCR primers used for library generation.

##ChIP-seq
Assay type: ChIP-seq ([EFO:0002692](http://www.ebi.ac.uk/efo/EFO_0002692))

Experiment target: variable. Consider child terms of ([SO:0001700](http://www.sequenceontology.org/browser/current_svn/term/SO:0001700)) for histone modifications

###Protocols
- EXTRACTION_PROTOCOL The protocol used to isolate the extract material.
- CHIP_PROTOCOL – The ChIP protocol used.

###Attributes
 
- EXTRACTION_PROTOCOL_TYPE_OF_SONICATOR The type of sonicator used for extraction.
- EXTRACTION_PROTOCOL_SONICATION_CYCLES The number of sonication cycles used for extraction.
- CHIP_PROTOCOL_CHROMATIN_AMOUNT The amount of chromatin used in the ChIP protocol.
- CHIP_PROTOCOL_BEAD_TYPE The type of bead used in the ChIP protocol.
- CHIP_PROTOCOL_BEAD_AMOUNT The amount of beads used in the ChIP protocol.
- CHIP_PROTOCOL_ANTIBODY_AMOUNT The amount of antibody used in the ChIP protocol.
- CHIP_ANTIBODY The specific antibody used in the ChIP protocol.
- CHIP_ANTIBODY_PROVIDER The name of the company, laboratory or person that provided the antibody.
- CHIP_ANTIBODY_CATALOG The catalog from which the antibody was purchased.
- CHIP_ANTIBODY_LOT The lot identifier of the antibody.
- CHIP_PROTOCOL_CROSSLINK_TIME The timespan in which the chromatin is crosslinked
- LIBRARY_GENERATION_FRAGMENT_SIZE_RANGE The fragment size range of the preparation.

##RNA-seq
Assay type: RNA-seq of coding RNA ([EFO:0003738](http://www.ebi.ac.uk/efo/EFO_0003738))

Experiment target: RNA e.g. polyA RNA ([OBI:0000869](http://purl.obolibrary.org/obo/OBI_0000869)), total RNA ([EFO:0004964](http://www.ebi.ac.uk/efo/EFO_0004964))

###Protocols
- EXTRACTION_PROTOCOL The protocol used to isolate the extract material.
- RNA_PREPARATION_3RNA_ADAPTER_LIGATION_PROTOCOL – The protocol for 3’ adapter ligation used in preparation.
- RNA_PREPARATION_5RNA_ADAPTER_LIGATION_PROTOCOL - The protocol for 5’ adapter ligation used in preparation.
- LIBRARY_GENERATION_PCR_PRODUCT_ISOLATION_PROTOCOL The protocol for isolating PCR products used for library generation.
- PREPARATION_REVERSE_TRANSCRIPTION_PROTOCOL The protocol for reverse transcription used in preparation.
- LIBRARY_GENERATION_PROTOCOL The protocol used to generate the library.

###Attributes
- EXTRACTION_PROTOCOL_FRAGMENTATION The fragmentation method used in the extraction protocol.
- RNA_PREPARATION_FRAGMENT_SIZE_RANGE The RNA fragment size range of the preparation.
- RNA_PREPARATION_5RNA_ADAPTER_SEQUENCE The sequence of the 5’ RNA adapter used in preparation.
- RNA_PREPARATION_3RNA_ADAPTER_SEQUENCE The sequence of the 3’ RNA adapter used in preparation.
- RNA_PREPARATION_REVERSE_TRANSCRIPTION_PRIMER_SEQUENCE The sequence of the primer for reverse transcription used in preparation.
- RNA_PREPARATION_5DEPHOSPHORYLATION The protocol for 5’ dephosphorylation used in preparation.
- RNA_PREPARATION_5PHOSPHORYLATION The protocol for 5’ phosphorylation used in preparation.
- LIBRARY_GENERATION_PCR_TEMPLATE_CONC The PCR template concentration for library generation.
- LIBRARY_GENERATION_PCR_POLYMERASE_TYPE The PCR polymerase used for library generation
- LIBRARY_GENERATION_PCR_THERMOCYCLING_PROGRAM The thermocycling program used for library generation.
- LIBRARY_GENERATION_PCR_NUMBER_CYCLES The number of PCR cycles used for library generation.
- LIBRARY_GENERATION_PCR_F_PRIMER_SEQUENCE The sequence of the PCR forward primer used for library generation.
- LIBRARY_GENERATION_PCR_R_PRIMER_SEQUENCE The sequence of the PCR reverse primer used for library generation.
- LIBRARY_GENERATION_PCR_PRIMER_CONC The concentration of the PCR primers used for library generation.
- TEMPLATE_TYPE The type of template (mRNA or cDNA). 
- AMPLIFIED Is the sample amplified? (true or false).
- PREPARATION_INITIAL_MRNA_QNTY The initial mRNA quantity used in preparation.
- PREPARATION_PCR_NUMBER_CYCLES The number of PCR cycles used to amplify
- LIBRARY_GENERATION_FRAGMENTATION The fragmentation method used in the library protocol.
- LIBRARY_GENERATION_FRAGMENT_SIZE_RANGE The fragment size range of the preparation.
- LIBRARY_GENERATION_3ADAPTER_SEQUENCE The sequence of the 3' adapter used for library generation.
- LIBRARY_GENERATION_5ADAPTER_SEQUENCE The sequence of the 5' adapter used for library generation.
- READ_STRAND Where a strand specific protocol is used, specify which mate pair maps to the transcribed strand. (NA otherwise).
