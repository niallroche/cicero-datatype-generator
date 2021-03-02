# cicero-datatype-generator
The Project is a starting point for examining hpw to automatically generate Cicero Data Models and appropriate data types from Cicerto templates. 

This can be achieve by a combination of approaches such as:
* Hueristics for matching variable names against a set of string patterns for commonly used patterns that resemble common strings found in data/times/currency/durations.
* Natural Language Processing (NLP) in particular, Language models capable of Named Entity Extraction (NER).
* Using Weak Labelling as defined in https://www.snorkel.org/ using a combination of:
* Weak Labeling Functions (LFs) capable of using a combination of:
  * pattern matching using string/regular expressions for common used patterns of variable names
  * lookup of data in a list of existing data models from sources such as the Accord Project library at https://templates.accordproject.org/
  
## Usage 
extractDataTypes.py pathToInputCiceroFile.md --outputfile optionalPathToOuputConcertoFile.cto