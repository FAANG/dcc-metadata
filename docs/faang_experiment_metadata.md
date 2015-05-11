FAANG analysis metadata spec

Raw data produced by each experiment will be analysed, producing results. E.g. 
ChIP-seq experiment will generate reads.
Reads will are aligned to the genome.
Normalized signal plots and QC metrics will be produced from the alignments. 
ChIP & input/IgG alignments be used for peak calling. 

Steps 2-4 produce analysis results. For each of these analysis results we should record which data, reference data and protocol were used to produce them. 

Metadata

Input data

A list of files used at input and experiment IDs.

Reference data - e.g. genome assembly, gene set, etc

Analysis protocol - precise description of the analysis protocol, including the following information:

URLs and versions for all software used (including in-house scripts)
Full command line used to run the analysis
Link to any VM or containers used, if applicable

The analysis must be entirely reproducible based on the protocol document. 

QC attributes produced by the analysis. These will vary based on the experiment type, but for sequencing work should always include mapping statistics as a bare minimum.
File naming

Each file should be uniquely identifiable with a human readable name, giving sufficient information to understand what it contains. We expect analysis to be repeated at intervals, as reference data and protocols are updated, so a data freeze data is included.

Short names based on the following, separated with a dot (‘.’):

species / assembly version
sample name
sample description (tissue or cell type)
assay type
experiment target
experiment ID
analysis protocol name
results type (e.g. genotypes vs. sites for 1000genomes vcf files)
data freeze date
file format

