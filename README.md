# BabyBERT

## Background

This repository contains research code that compares syntactic abilities of BERT trained on 
a small cognitively plausible corpus of child-directed speech (5M words from American-English CHILDES) 
to that trained on a large (standard) adult-generated text.

The code is for research purpose only. 
The goal of this research project is to understand language acquisition from the point of view of distributional learning models.

## History

- 2020 (Spring): The BabyBERT project grew out of the BabySRL project led by Cynthia Fisher, Dan Roth, Michael Connor and Yael Gertner, 
whose published work is available [here](https://www.aclweb.org/anthology/W08-2111/). 
Having found little benefit for joint SRL and MLM training of a custom (smaller in size) version of BERT,
 a new line of research into BERT's success on syntactic task was begun. 
 
## Probing for syntactic knowledge

Probing data can be found [here](https://github.com/phueb/Babeval). 


## BabyBERT vs. BERT
 
Due to the limited size of child-directed speech data, 
a much smaller BERT than the standard BERT models is trained here, which is called BabyBERT.
It has fewer hidden units and layers, and preliminary observations show that the reduced size is sufficient for reaching near-optimal pre-training performance on the CHILDES corpus.
Contrary to the original BERT implementation, no next-sentence prediction objective is used during training, 
as was done in the original implementation. This reduces training time, code complexity and [learning two separate semantic spaces](https://scholarworks.umass.edu/cgi/viewcontent.cgi?article=1117&context=scil).


## Using the code

### Pre-training from scratch

Call the function `babybert.job.main()`

### Probing pre-trained models

Run the script `scripts/probe_pretrained_models`

## Compatibility

Tested on Ubuntu 16.04, Python 3.7, transformers=3.02, and torch==1.2.0