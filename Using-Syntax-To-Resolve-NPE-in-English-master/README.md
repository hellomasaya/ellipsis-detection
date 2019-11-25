# Using-Syntax-To-Resolve-NPE-in-English
## What is Nominal Ellipsis?

Nominal Ellipsis or Noun Phrase Ellipsis (NPE, henceforth) is a type of ellipsis in linguists wherein the sub-parts of a nominal projection are elided, with the remaining projection pronounced in the overt syntax.

## What does this system do?
It is a syntax-based system for automatic detection and resolution of Noun Phrase Ellipsis (NPE) in English.

## Installation

##### Dependencies
- Install Spacy
- Install pickle
- Install xlwt

## Development
1. Run `ipython -i npe_system.py`

## Usage
2. The main functions are find_licensors and find_antecedent. 
3. Value to the function find_licensors is any English sentence with or without npe.
3. Ouput will be a list of licensors of the npe and potential antecedent candidates if present.

## Copyright
This system was presented at RANLP 2019 in Varna, Bulgaria and is published in the conference proceedings.
