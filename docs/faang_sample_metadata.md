FAANG sample metadata spec

In this context, we consider donor animals, tissue samples, primary cells or other biological material to be samples. All Samples must be registered in BioSamples (at EMBL-EBI). This resource is a peer of  BioSample (at NCBI), and they exchange data regularly. FAANG samples should be registered in BioSamples prior to data submission. This document describes the attributes which must be associated with any BioSamples submission.

Metadata requirements

Common 

These attributes should be present on every type of sample record

Sample Name / ID
Description (optional)
Biomaterial provider
Animal

Required:
Species - NCBI taxon ID.
Sex (any child term of EFO_0000695)
Birth date
Birth location
Strain / Breed (ontology or link to DB?)
Pedigree (point to pedigree DB - examples?) 
Optional:
Phenotype terms - as many terms as required from MP or similar ontology?
Phenotype data - not clear what to expect here, assume similar data to IMPC. Can we use BioStudies or BioSamples for this?

Links to other records (required if related animals are part of FAANG, e.g. quads)
Sire
Dam
Siblings

Specimen

A piece of tissue taken from an animal.

Required:
Date at which specimen collection occurred
Animal age at point of specimen collection
Animal Disease / health status at point of collection
Tissue (UBERON term)
Method of collection (protocol)

Links to other records
Animal (derived from) (required)


Purified cell

Cells purified from a specimen.

Required:
Markers
Cell type (CL term)
Protocol

Links to other records
Specimen (derived from) (required)

Cell culture

Cells cultured from a specimen or purified cells

Required:
Cell type  (CL term)
Protocol
Culture conditions

Links to other records - require one of the possibilities below:
Specimen (derived from) 
Purified cell (derived from)

Data types
Text
Ontology link (text for term + Ontology + ID within that ontology)
Age (specify units in submission)
Date (specify format in submission)
Location (longitude / latitude in decimal degrees + region name text)
Sex (One of male/female/unknown)
Protocol (URL of protocol document)




Sample naming

We propose a sample naming scheme comprising the following elements:

short species code
lab or institute short name
alpha numeric sample ID from LIMS

The purpose is to ensure that samples are uniquely and clearly identified, with reasonably short names.

Pooled samples

Where samples are pooled, a new sample record should be created, containing 

Protocol

Links to other records
Other samples (derived from)

Notes


BioSample have a template for animal submissions:

https://submit.ncbi.nlm.nih.gov/biosample/template/?package=Model.organism.animal.1.0&action=definition

This shares the same problems as the IHEC standards - redundant provision of information across records. We need to know if we can use our model with BioSample@NCBI, or just with BioSamples@EMBL-EBI. 

