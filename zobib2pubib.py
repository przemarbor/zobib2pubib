## pip3 install pybtex
## pip3 install publish 

import os
from publish.importing import import_file
from pybtex.database import parse_file
from pybtex.database import BibliographyData
from pybtex.database import Person

bib_data = parse_file('ZoteroLibrary.bib')

# auxiliary variable for storing output bibliography
output_bib_data = BibliographyData()

# auxiliary variable - it will be added to the .bib entry if 
# there is no author for the entry
dummyPerson = Person('')

###  remove all other items than article and book from the bibliography
### newBib = [entry for entry in bib_data.entries.values() if entry.type != 'incollection']
###  - this is done per entry in the loop below


for entry in bib_data.entries.values():
        
    # remove unnecessary or troublesome fields from the entry        
    if 'month' in list(entry.fields.keys()):                
        entry.fields.pop('month')

    if 'abstract' in list(entry.fields.keys()):                
        entry.fields.pop('abstract')

    if 'keywords' in list(entry.fields.keys()):                
        entry.fields.pop('keywords')
        
    if 'file' in list(entry.fields.keys()):                
        entry.fields.pop('file')

    if 'note' in list(entry.fields.keys()):
        entry.fields.pop('note')

    # If entry has no 'year' field - add it because publish moans about it...
    if not 'year' in list(entry.fields.keys()):
        entry.fields['year'] = ''        
            
    # If entry has no authors - add a dummy one
    if len(list(entry.persons)) == 0:
        entry.add_person(dummyPerson,'author')
        

    # add entry fields for special types of documents
    # (Publish requires for some types of documents to have 
    # various field explicitly )
    
    if entry.type == 'article':
        if not 'journal' in list(entry.fields.keys()):
            entry.fields['journal'] = ''

    if entry.type == 'book':
        if not 'publisher' in list(entry.fields.keys()):
            entry.fields['publisher'] = ''

    if entry.type == 'techreport':
        if not 'institution' in list(entry.fields.keys()):
            entry.fields['institution'] = ''

    if entry.type == 'inproceedings':
        if not 'booktitle' in list(entry.fields.keys()):
            entry.fields['booktitle'] = ''

    if entry.type == 'phdthesis':
        if not 'school' in list(entry.fields.keys()):
            entry.fields['school'] = ''

    if entry.type == 'unpublished':
        if not 'note' in list(entry.fields.keys()):
            entry.fields['note'] = ''


    # Publish cannot handle 'incollection' type of document so 
    # just remove them from output bibliograpy
    if entry.type != 'incollection':
        output_bib_data.add_entry( entry.key, entry )

           
output_bib_data.to_file('preprocessedTEMP.bib')    


# Embrace all field values in bib file from "..." to {...}
fileIn = open('preprocessedTEMP.bib', 'r')
fileOut = open('processed.bib', 'w')

Lines = fileIn.readlines()

for line in Lines:
        
    # find the first occurance of " in this line
    first = line.find("\"" )
    
    if first != -1: # if there exist " in this line ...
        # look for the closing quotation mark
        last = line.rfind("\"" )    
        
        # and make appropriate changes
        line = line[:first] + '{' + line[first+1:]
        line = line[:last] + '}' + line[last+1:]
        
        
    fileOut.writelines(line)
      
        
fileOut.close()
fileIn.close()

# importing BibTeX file into Publish bibliography
import_file('processed.bib')

os.remove('preprocessedTEMP.bib')
os.remove('processed.bib')
