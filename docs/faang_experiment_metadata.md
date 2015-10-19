#FAANG experiment metadata spec

This document describes the specification for all experiment metadata. You can find an overview of our metadata and archival plans in [the overview document](faang_metadata_overview.md). The [sample](faang_sample_metadata.md) and [analysis](faang_analysis_metadata.md) documents are also in this [git repo](https://github.com/FAANG/faang-metadata).

Experiments are expected to fall into two categories 

sequencing experiments, archived in an SRA database (hosted at NCBI, EMBL-EBI and DDBJ). Some of this submissions will be brokered by ArrayExpress.
array experiments, archived in ArrayExpress or GEO. 

##Experiment attributes

These following elements must always be present in any experiment metadata

* Assay Type
	* What class of experiment is being performed? e.g. RNA-Seq or expression array. This is stored as a library strategy attribute in the SRA database model. Terms used should have an equivalent in EFO (child term of [EFO:0002773](http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=EFO&termId=EFO%3A0002773&termName=assay%20by%20instrument)), but may be constrained by the SRA controlled vocabulary.
* Experiment target
	* What is the experiment trying to find? e.g. Methylated DNA, polyA RNA, total RNA. This should be stored in the experiment attributes for SRA archives using their controlled vocabulary.
* Sample
	* This should be a reference to the BioSample ID for the specimen, purified cell, cultured cell or cell line the experiment was conducted on.
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
<dl>
<dt>extraction protocol</dt>
<dd>The protocol used to isolate the extract material</dd>
<dt>bisulfite conversion protocol</dt>
<dd></dd>
<dt>PCR product isolation protocol</dt>
<dd>The protocol for isolating PCR products used for library generation.</dd>
</dl>

###Attributes
<dl>
<dt>bisulfite conversion percent</dt>
<dd>the bisulfite conversion percent</dd>
</dl>

##ChIP-seq
Assay type: ChIP-seq ([EFO:0002692](http://www.ebi.ac.uk/efo/EFO_0002692))

Experiment target: variable. Consider child terms of ([SO:0001700](http://www.sequenceontology.org/browser/current_svn/term/SO:0001700)) for histone modifications

###Protocols
<dl>
<dt>extraction protocol</dt>
<dd>the protocol used to isolate the extract material.</dd>
<dt>ChIP protocol</dt>
<dd>the chip protocol used.</dd>
</dl>

###Attributes
<dl>
<dt>ChIP antibody </dt>
<dd>the specific antibody used in the ChIP protocol</dd>
<dt>ChIP antibody provider</dt>
<dd>the name of the company, laboratory or person that provided the antibody</dd>
<dt>ChIP antibody catalog</dt>
<dd>the catalog from which the antibody was purchased</dd>
<dt>ChIP antibody lot</dt>
<dd>the lot identifier of the antibody</dd>
<dt>library generation fragment size range</dt>
<dd>the fragment size range of the preparation.</dd>
</dl>


##RNA-seq
Assay type: RNA-seq of coding RNA ([EFO:0003738](http://www.ebi.ac.uk/efo/EFO_0003738))

Experiment target: RNA e.g. polyA RNA ([OBI:0000869](http://purl.obolibrary.org/obo/OBI_0000869)), total RNA ([EFO:0004964](http://www.ebi.ac.uk/efo/EFO_0004964))

###Protocols
<dl>
<dt>extraction_protocol</dt>
<dd>the protocol used to isolate the extract material.</dd>
<dt>RNA preparation 3' adapter ligation protocol</dt>
<dd>the protocol for 3’ adapter ligation used in preparation.</dd>
<dt>RNA preparation 5' adapter ligation protocol</dt>
<dd>the protocol for 5’ adapter ligation used in preparation.</dd>
<dt>library generation pcr product isolation_protocol</dt>
<dd>the protocol for isolating pcr products used for library generation.</dd>
<dt>preparation reverse transcription protocol</dt>
<dd>the protocol for reverse transcription used in preparation.</dd>
<dt>library generation protocol</dt>
<dd>the protocol used to generate the library.</dd>
</dl>

###Attributes
<dl>
<dt>read strand</dt>
<dd>where a strand specific protocol is used, specify which mate pair maps to the transcribed strand. (NA otherwise).</dd>
</dl>
