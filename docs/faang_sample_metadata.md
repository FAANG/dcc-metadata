#FAANG sample metadata spec

This document describes the specification for all sample metadata. You can find an overview of our metadata and archival plans in [the overview document](faang_metadata_overview.md). The [experiment](faang_experiment_metadata.md) and [analysis](faang_analysis_metadata.md) documents are also in this [git repo](https://github.com/FAANG/faang-metadata).

In the sample context, we consider donor animals, tissue samples, primary cells or other biological material to be samples. All Samples must be registered in BioSamples (at EMBL-EBI). This resource is a peer of  BioSample (at NCBI), and they exchange data regularly. FAANG samples should be registered in BioSamples prior to data submission. This document describes the attributes which must be associated with any BioSamples submission.

##Metadata requirements

Requirements are laid out like this:  

* `attribute_name` (*data type*) a brief description

To avoid duplication, each *data type* is explained at the end of the document. 

###Common 

These attributes should be present on every type of sample record

Required:

  * Sample Name / ID
  * `material` (*ontology term*) the type of material being described. This will be used to decide what metadata are required and must be one of the expected terms:
   * [organism](http://purl.obolibrary.org/obo/OBI_0100026)
   * [tissue specimen](http://purl.obolibrary.org/obo/OBI_0001479)
   * [cell specimen](http://purl.obolibrary.org/obo/OBI_0001468)
   * [cell culture](http://purl.obolibrary.org/obo/OBI_0001876)
   * [pool of specimens](http://purl.obolibrary.org/obo/OBI_0302716)

Optional:

 * `description` (*text*) a brief description of the sample.
 * `availability` (*uri*) either a link to a web page giving information on sample availability (who to contact and if the sample is available), or a e-mail address to contact about availability. E-mail addresses should be prefixed with 'mailto:', e.g. 'mailto:samples@example.ac.uk'. In either case, long term support of the web page or e-mail address is necessary. Group e-mail addressees are preferable to indiviudal.

###Animal

An animal sampled for FAANG. The following attributes are in addition to the common attributes listed above. The `material` should be reported as [organism](http://purl.obolibrary.org/obo/OBI_0100026).

Required:

 * `species` (*NCBI taxon ID*)
 * `sex`  (*ontology term*) animal sex, described using any child term of [PATO_0000047](http://bioportal.bioontology.org/ontologies/EFO/?p=classes&conceptid=http%3A%2F%2Fpurl.org%2Fobo%2Fowl%2FPATO%23PATO_0000047&jump_to_nav=true))
 * `birth_date` (*date*) 
 * `breed` (*ontology term*) animal breed, described using a term from the [Livestock Breed Ontology](http://purl.obolibrary.org/obo/LBO_0000000)
 
Optional:

 * `birth location` (*location*)
 * `physiological_conditions`(*ontology term*) use as many terms as necessary from [ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en))
 * `environmental_conditions`(*ontology term*) as many terms as necessary from [EOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en))
 * `phenotype` (*ontology term*) as many terms as required from the [VT](http://purl.bioontology.org/ontology/VT), [ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en) or [MP](http://purl.bioontology.org/ontology/MP)) ontologies
 * Birth weight
 * Placental weight
 * Pregnancy length
 * Delivery timing
 * Delivery Ease
 
 * Pedigree (link to pedigree DB entry - do we have any examples of this?)
 * Phenotype data - not clear what to expect here, assume similar data to IMPC. Can we use BioStudies or BioSamples for this?

Links to other records (required if related animals are part of FAANG, e.g. quads)

 * Sire (child of)
 * Dam (child of)
 * Siblings

###Specimen

A piece of tissue taken from an animal. The following attributes are in addition to the common attributes listed above. The `material` should be reported as [tissue specimen](http://purl.obolibrary.org/obo/OBI_0001479).

Required:
 * Date at which specimen collection occurred
 * Animal age at point of specimen collection
 * Animal Disease / health status at point of collection
 * Tissue ([UBERON](http://uberon.github.io/) term preferred)
 * Method of collection (protocol)
 * Fasted status - either 'fed', 'fasted' or 'unknown'. Criteria *must* be specified in the protocol.

Optional:
 * Physiological conditions (as many terms as required from [ATOL](http://www.atol-ontology.com/index.php/en/les-ontologies-en/visualisation-en))
 * Number of pieces
 * Volume
 * Size
 * Weight
 * Organ/tissue picture (URL or include image directly in submission?)

Links to other records
 * Animal (derived from) (required)

###Purified cell

Cells purified from a specimen. The following attributes are in addition to the common attributes listed above...

Required:
 * Markers
 * Cell type ([CL](http://www.ontobee.org/browser/index.php?o=CL) term preferred)
 * Protocol

Links to other records
 * Specimen (derived from) (required)

###Cell culture

Cells cultured from a specimen or purified cells. The following attributes are in addition to the common attributes listed above...

Required:
 * Culture type (child term of [BTO_0000214](http://purl.obolibrary.org/obo/BTO_0000214))
 * Cell type  ([CL](http://www.ontobee.org/browser/index.php?o=CL) term preferred)
 * Protocol
 * Culture conditions (e.g. 'on feeder cells', 'E8 media')
 * Number of passages

Links to other records - require one of the possibilities below:
 * Specimen (derived from) 
 * Purified cell (derived from)

###Data types
 * Text
 * Ontology link (text for term + Ontology + ID within that ontology)
 * Age (specify units in submission)
 * Date (specify format in submission)
 * Location (longitude / latitude in decimal degrees + region name text)
 * Sex (ontology link, any child term of [EFO_0000695](http://www.ebi.ac.uk/efo/EFO_0000695))
 * Protocol (URL of protocol document)

###Sample naming

We propose a sample naming scheme comprising the following elements:

 * short species code
 * lab or institute short name
 * alpha numeric sample ID from LIMS

The purpose is to ensure that samples are uniquely and clearly identified, with reasonably short names.

###Pooled samples

Where samples are pooled, a new sample record should be created, containing 

 * Protocol

Links to other records
 * Other samples (derived from)

###Submission

BioSample have a template for animal submissions:

https://submit.ncbi.nlm.nih.gov/biosample/template/?package=Model.organism.animal.1.0&action=definition

###Notes

As mentioned in the [overview](faang_metadata_overview.md) document, Sample submission is an open question. Data Exchange between between the EBI and NCBI sample databases isn't entirely ironed out and if FAANG partners are to share samples this will need to be resolved before the best scenario for sample registration can be used.

The current plan also has some redundancy contained within it. We need to work out how much redundancy can be removed. 



