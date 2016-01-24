#FAANG experiment metadata spec

This document describes the specification for all experiment metadata. You can find an overview of our metadata and archival plans in [the overview document](faang_metadata_overview.md). The [sample](faang_sample_metadata.md) and [analysis](faang_analysis_metadata.md) documents are also in this [git repo](https://github.com/FAANG/faang-metadata).

Experiments are expected to fall into two categories:

 1. sequencing experiments, archived in an SRA database (hosted at (EMBL-EBI)[https://www.ebi.ac.uk/ena], [NCBI](http://www.ncbi.nlm.nih.gov/sra/) and [DDBJ](http://trace.ddbj.nig.ac.jp/dra/index_e.html)). Some of these submissions may be brokered by specialist services such as [ArrayExpress](https://www.ebi.ac.uk/arrayexpress/) and [GEO](http://www.ncbi.nlm.nih.gov/geo/)
 2. array experiments, archived in [ArrayExpress](https://www.ebi.ac.uk/arrayexpress/) or [GEO](http://www.ncbi.nlm.nih.gov/geo/).


##Experiment metadata requirements

Requirements are laid out like this:  

 * `attribute name` (*data type*) a brief description

The data types will be described later in this document. The metadata group will seek guidance from the assay group on what needs to be recorded here for each assay type.

Each assay type will require metadata in addition to the core set of common attributes. The initial set proposed is based upon the [IHEC metadata standards](http://ihec-epigenomes.org/research/reference-epigenome-standards/)


###Common

These following elements must always be present in any experiment metadata

 * Each experiment should reference one `sample`. The metadata for that sample should comply with the FAANG metadata specification.
	* This should be a reference to the BioSample ID for the specimen, purified cell, cultured cell or cell line the experiment was conducted on.
 * `assay type` (*ontology term*) The class of experiment performed. e.g. RNA-Seq or expression array. This should be a child term of [EFO:0002773](http://www.ebi.ac.uk/efo/EFO_0002773)
 * `experiment target` (*ontology term*) What is the experiment trying to find?
  * ChIP-seq for histone modifications should use a child term of [histone modification](http://purl.obolibrary.org/obo/SO_0001700)
	* ChIP-seq input should use the term [input DNA](http://www.ebi.ac.uk/efo/EFO_0005031)
	* RNA-seq should use a child term of [RNA](http://purl.obolibrary.org/obo/CHEBI_33697)
	* ATAC-seq and DNase-seq should use the term [open_chromatin_region](http://purl.obolibrary.org/obo/SO_0001747)
	* Methylation assays should use the term [DNA methylation](http://purl.obolibrary.org/obo/GO_0006306)
 * `sample storage` (*text*) This should document how the sample was stored, from one of these values:
		*  frozen, liquid nitrogen
		*  frozen, -70 freezer
		*  frozen, vapor phase
		*  RNAlater, frozen
		*  paraffin block
		*  cut slide
		*  fresh
* `sample storage processing` (*text*) This should document how the sample was prepared for storage, from one of these values:
		* cryopreservation in liquid nitrogen (dead tissue)
		* cryopreservation in dry ice (dead tissue)
		* cryopreservation of live cells in liquid nitrogen
		* cryopreservation, other
		* formalin fixed, unbuffered
		* formalin fixed, buffered
		* formalin fixed and paraffin embedded
		* fresh
* `sampling to preparation interval` (*number*) This should list how long between the sample being taken and used in the experiment. Units should be specified, and be either 'minutes','hours','days','weeks' or 'years'.
* `experimental protocol` (*protocol*) a description of the experiment protocol.


###Whole-genome bisulfite sequencing
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
<dt>RNA purity - 260:280 ratio</dt>
<dd>Sample purity assesed with fluoresence ratio at 260 and 280nm, informative for protein contamination</dd>
<dt>RNA purity - 260:230 ratio</dt>
<dd>Sample purity assesed with fluoresence ratio at 260 and 230nm, informative for contamination by phenolate ion, thiocyanates, and other organic compounds</dd>
<dt>RNA integrity number</dt>
<dd>See <a href="http://www.biomedcentral.com/1471-2199/7/3">Schroeder <i>et al</i>, 2006</a></dd>
</dl>
