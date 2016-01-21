#FAANG sample metadata spec

This document describes the specification for all sample metadata. You can find an overview of our metadata and archival plans in [the overview document](faang_metadata_overview.md). The [experiment](faang_experiment_metadata.md) and [analysis](faang_analysis_metadata.md) documents are also in this [git repo](https://github.com/FAANG/faang-metadata).

In the sample context, we consider donor animals, tissue samples, primary cells or other biological material to be samples. All Samples must be registered in BioSamples (at EMBL-EBI). This resource is a peer of  BioSample (at NCBI), and they exchange data regularly. FAANG samples should be registered in BioSamples prior to data submission. This document describes the attributes which must be associated with any BioSamples submission.

##Metadata requirements

Requirements are laid out like this:  

* `attribute name` (*data type*) a brief description

##Data types for sample attributes

[BioSamples](http://www.ebi.ac.uk/biosamples) takes sample records with a set of attributes. Each attribute has a name and a value. It can also have 'Units', or a 'Term Source' and a 'Term Source ID'. The Term Source and ID allow us to refer to entries in other databases or ontologies. This is fully described on the [BioSamples help pages](http://www.ebi.ac.uk/biosamples/help/st_scd.html). The following section describe the expectations for each data type within FAANG.

###date

Dates should be reported in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format,  YYYY-MM-DD. To ensure clarity, the format should be reported as the 'units'.

###NCBI taxon ID

A species name and identifier from the [NCBI Taxonomy database](http://www.ncbi.nlm.nih.gov/taxonomy). For example, a [human](http://www.ncbi.nlm.nih.gov/taxonomy/9606) would be described with a value of 'Homo sapiens', a term source of  'NCBI Taxonomy' and a term source ID of 9606.

###number

A number, with units specified. BioSamples recommends that units are given without abbreviations .For example, a birth weight could have a value of 1.3 and the units specified as 'kilograms'.

###protocol

A URL link to a protocol document on the FAANG FTP site. Please contact the [FAANG data coordination centre](mailto:faang-dcc@ebi.ac.uk) to have your protocol documents added to the FTP site.

###text

Text, using US English spellings.

###URL

A URL,  such as 'http://faang.org/'. Depending on the context, http, ftp, mailto links may be appropriate. Examples:

 * ftp, ftp://ftp.faang.ebi.ac.uk/ftp/README
 * http,  http://faang.org/
 * mailto, mailto:bob@example.org 
 

###ontology term

A reference to an ontology term. The attribute value should be the term label. The term source should be the ontology used, and the term source ID should be an ID from that ontology. For example, cerebral cortex could be  described with a term source of 'UBERON', a term source ID of 'UBERON:0000956' and a value of 'cerebral cortex'.

###location

A location should be reported as using three attributes:

 * `location` (*text*) name of the location
 * `location latitude` (*number*) latitude in decimal degrees. Units should be reported as 'decimal degrees'
 * `location longitude`(*number*) longitude in decimal degrees. Units should be reported as 'decimal degrees'

###Common 

These attributes should be present on every sample record.

Required:

  * Sample Name / ID
  * `material` (*ontology term*) the type of material being described. This will be used to decide what metadata are required and must be one of the expected terms:
   * [organism](http://purl.obolibrary.org/obo/OBI_0100026)
   * [tissue specimen](http://purl.obolibrary.org/obo/OBI_0001479)
   * [cell specimen](http://purl.obolibrary.org/obo/OBI_0001468)
   * [cell culture](http://purl.obolibrary.org/obo/OBI_0001876)
   * [pool of specimens](http://purl.obolibrary.org/obo/OBI_0302716)

Optional:

 * `description` (*text*) a brief description of the sample
 * `availability` (*URL*) either a link to a web page giving information on sample availability (who to contact and if the sample is available), or a e-mail address to contact about availability. E-mail addresses should be prefixed with 'mailto:', e.g. 'mailto:samples@example.ac.uk'. In either case, long term support of the web page or e-mail address is necessary. Group e-mail addressees are preferable to indiviudal.

###Animal

An animal sampled for FAANG. The following attributes are in addition to the  attributes listed in the 'Common' section above. The `material` should be reported as [organism](http://purl.obolibrary.org/obo/OBI_0100026).

Required:

 * `species` (*NCBI taxon ID*)
 * `sex`  (*ontology term*) animal sex, described using any child term of [PATO_0000047](http://purl.obolibrary.org/obo/PATO_0000047)
 * `birth date` (*date*) birth date, in the format YYYY-MM-DD
 * `breed` (*ontology term*) animal breed, described using a term from the [Livestock Breed Ontology](http://purl.obolibrary.org/obo/LBO_0000000)
 
Optional:

 * birth location (*location*)
   * `birth location` (*text*) name of the birth location
   * `birth location latitude` (*number*) latitude of the birth location in decimal degrees. Units should be specified as 'decimal degrees'
   * `birth location longitude` (*number*) longitude of the birth location in decimal degrees. Units should be specified as 'decimal degrees'
 * `birth weight` (*number*) weight, in kilograms or grams. Units must be specified
 * `placental weight` (*number*) weight, in kilograms or grams. Units must be specified.
 * `pregnancy length` (*number*) length of time, in days, weeks or months 
 * `delivery timing` (*text*) 
 * `delivery ease` (*text*)
 * `physiological conditions`(*ontology term*) use as many terms as necessary from [ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en))
 * `environmental conditions`(*ontology term*) as many terms as necessary from [EOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en))
 * `phenotype` (*ontology term*) as many terms as required from the [VT](http://purl.bioontology.org/ontology/VT), [ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en) or [MP](http://purl.bioontology.org/ontology/MP)) ontologies
 * `pedigree` (*URL*) a link to pedigree information for the animal

Links to other records (required if related animals are part of FAANG, e.g. quads)

 * Sire (child of)
 * Dam (child of)
 * Siblings

###Specimen

A piece of tissue taken from an animal. The following attributes are in addition to the attributes listed in the 'Common' section above. The `material` should be reported as [tissue specimen](http://purl.obolibrary.org/obo/OBI_0001479).

Required:

 * `specimen collection date`(*date*) date at which the  specimen was collected
 * `animal age at collection` (*number*) animal age at the point of collection, in years, months, weeks or days. Units must be specified. An estimmate is acceptable where the age is not precisely known.
 * `developmental stage` (*ontology term*) a child term of [life cycle stage](http://purl.obolibrary.org/obo/UBERON_0000105)
 * Animal Disease / health status at point of collection
 * `tissue` ([UBERON](http://uberon.github.io/) term preferred)
 * `specimen collection protocol` (*protocol*) a link to the protocol followed when taking the specimen 
 * `fasted status` - (*text*) One of the following values, for which the criteria _must_ be specified in the protocol:
   * fed
   * fasted
   * unkown 

Optional:

 * `physiological_conditions`(*ontology term*) as many terms as necessary from
[ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en)
 * `number_of_pieces` (*number*) Units must be specified as 'count'
 * `specimen volume` (*number*) Units must be specified as either 'square centimeters', 'liters' or 'milliliters'
 * `specimen size`(*number*) Units must be specified as either 'meters', 'centimeters' or 'millimeters'
 * `specimen weight` (*number*) Units must be specified as either 'grams', 'kilograms'
 * `specimen picture url` (*URL*) Link to a picture of the specimen
 * `gestational age at sample collection` (*number*)  If the animal was pregnant when the specimen was taken, state how long had it been pregnant for. Units must be specified as 'days' or 'weeks'.

Links to other records:

 * Animal (derived from) (required)

###Purified cells

Cells purified from a specimen. The following attributes are in addition to the  attributes listed in the 'Common' section above. The `material` should be reported as [cell specimen](http://purl.obolibrary.org/obo/OBI_0001468). 

Required:

 * `markers` (*text*) markers used to isolate and identify the cell type
 * `cell type` (*ontology term*) a term from the  [CL ontology](http://www.ontobee.org/browser/index.php?o=CL)
 * `purification protocol` (*protocol*) protocol describing how the cells were purified

Links to other records:

 * Specimen (derived from) (required)

###Cell culture

Cells cultured from a specimen or purified cells. The following attributes are in addition to the  attributes listed in the 'Common' section above.

Required:

 * `culture type`(*ontology term*) a child term of [BTO_0000214](http://purl.obolibrary.org/obo/BTO_0000214))
 * `cell type` (*ontology term*) a term from the [CL ontology](http://www.ontobee.org/browser/index.php?o=CL) 
 * `cell culture protocol` (*protocol*) protocol describing how the cells were purified
 * `culture conditions` (*text*) brief description of culture conditions (e.g. 'on feeder cells', 'E8 media')
 * `number of passages` (*number*)  number of times the cell line has been re-plated and allowed to grow back to confluency or to some maximum density if using suspension cultures

Links to other records - require one of the possibilities below:

 * Specimen (derived from) 
 * Purified cell (derived from)

###Pooled samples

Where samples are pooled, a new sample record should be created, containing 

 * `pooling protocol` (*protocol*)

Links to other records
 * pooled samples (derived from)
 

##Sample naming

We propose a sample naming scheme comprising the following elements:

 * short species code
 * lab or institute short name
 * alpha numeric sample ID from LIMS

The purpose is to ensure that samples are uniquely and clearly identified, with reasonably short names.



##Submission

BioSample have a template for animal submissions:

https://submit.ncbi.nlm.nih.gov/biosample/template/?package=Model.organism.animal.1.0&action=definition

##Notes

As mentioned in the [overview](faang_metadata_overview.md) document, Sample submission is an open question. Data Exchange between between the EBI and NCBI sample databases isn't entirely ironed out and if FAANG partners are to share samples this will need to be resolved before the best scenario for sample registration can be used.

The current plan also has some redundancy contained within it. We need to work out how much redundancy can be removed. 



