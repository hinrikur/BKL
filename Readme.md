# UNDER CONSTRUCTION

### Extracting word frequency data from ELAN transcriptions

This repository is part of the research project: _“Í beinan karllegg: Skráning talmáls þriggja ættliða”_ (_‘Patrilineal Descent: Transcribing Spoken Language of Three Generations’_),
funded by The University of Iceland Research Fund.

This repo contains:

* Scripts for processing [ELAN Annotation Format](https://tla.mpi.nl/tools/tla-tools/elan/) transcription files (`.eaf`) into output `.tsv` files. The [Pympi module](https://github.com/dopefishh/pympi) is used for extracting the transcription annotations.
* Scripts for preparing the extracted annotations for POS-tagging and lemmatization.
* Scripts for calculating word frequency from PoS tagged and lemmatized output files.

Tools used in PoS tagging and lemmatization steps but are not found in this repository:
* PoS tagger: [ABLtagger by Steinþór Steingrímsson et al.](https://github.com/steinst/ABLTagger)
* Lemmatizer: [Nefnir by Jón Friðrik Daðason](https://github.com/jonfd/nefnir)
