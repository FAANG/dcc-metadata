#FAANG experiment metadata spec

Experiments are expected to fall into two categories 

sequencing experiments, archived in an SRA database (hosted at NCBI, EMBL-EBI and DDBJ). Some of this submissions will be brokered by ArrayExpress.
array experiments, archived in ArrayExpress or GEO. 

##Experiment attributes

These following elements must always be present in any experiment metadata

* Assay Type
	* What class of experiment is being performed? e.g. RNA-Seq or expression array. This is stored as a library strategy attribute in the SRA database model. Terms used should have an equivalent in EFO (child term of EFO:0002773).
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

