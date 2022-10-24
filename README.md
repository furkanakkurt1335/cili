# Collaborative Interlingual Index

The Collaborative Interlingual Index (CILI) maintains the data for a
single interlingual index of concepts for wordnets. This respository
contains all the data that is available in CILI as well as mappings to
other resources.

## Development and Maintenance

CILI is maintained by the [Open Multilingual Wordnet][OMW]. Please see
its [CILI page][CILI] for more information about the project,
including how to propose new concepts.

[OMW]: https://lr.soh.ntu.edu.sg/omw/
[CILI]: https://lr.soh.ntu.edu.sg/omw/ili

## Repository Contents

The following files are in this repository:

* `ili.ttl`: The main interlingual index file, containing a definition and a 
    source for each identifier. This file is in the Turtle RDF format.
* `ili-map.ttl`, `ili-map-wn30.ttl`: These two files contain the mapping from
    Princeton WordNet 3.0 to the ILI in Turtle. These files are identical
* `ili-map-pwn30.tab`: The mapping from Princeton WordNet 3.0 to the ILI as
    tab-separated values.
* `ili-map-pwn31.tab`, `ili-map-wn31.ttl`: The mappings from Princeton WordNet 3.1
    to the ILI
* `ili-map-odwn13.ttl`: The mapping from Open Dutch WordNet 1.3 to the ILI.
* `older-wn-mappings`: Automatically constructed mappings from previous versions
    of WordNet to the ILI

## Building scripts

There are two scripts to create the HTML and the TSV versions of the data. They both require Python 3.6+. The requirements can be installed with

    pip install -r requirements.txt

The TSV script can be run as follows:

    python3 make-tsv.py > cili.tsv
    
For the HTML the following will update the site

    git checkout gh-pages
    rm -fr docs
    python make-html.py docs
    git commit -am "A useful commit message"
    git push

