# Zotero2DocOncePublish

Want to know how to use this repository? Go straight [here](#how-to-use-this-repository).

Recently I decided to give a try working with [DocOnce](http://hplgit.github.io/doconce/doc/pub/manual/manual.html) program in order to write my own documents.
One of the first problems I hit was working with bibliography. Well, the authors of DocOnce honestly admits in their manual that this, in fact, might be troublesome and advise to use a script to automate the work of transforming your .bib file to the form that will be accepted by DocOnce program. This is my try.

I have a large bibliography run by Zotero, however in DocOnce you cannot use standard LaTeX .bib files (that can be easily exported from Zotero). You need to transform them into the format that is compatible with DocOnce, which is Publish.
This transformation process can be a daunting and troublesome task, so here I gathered some hints and scripts that can be used to ease the pain a bit.

## Typical workflow with DocOnce's Publish format
According to [DocOnce Quick Reference](https://hplgit.github.io/doconce/doc/pub/quickref/quickref.html#___sec16) a publication database is in a Publish format. More information on using bibliography can be found in [DocOnce Manual](http://hplgit.github.io/doconce/doc/pub/manual/html/manual.html#bibliography-references).

The link provided in both documents leads to [non existing repository](https://bitbucket.org/logg/publish).
I decided not to hassle its owner and rely on pip's version of the package.

Theoretically, if everything goes smooth the workflow should be as follows:

1. Export Zotero bibliograpy to .bib file (BibTeX format! not BibLaTeX!) (Zotero -> File -> Export Library... -> Format: BibTeX).

2. Install `publish` package from pip.

		pip3 install publish-doconce
		pip3 install future  # needed for seemless work of Publish
   
3. run: 

		publish import library.bib
  
   and do everything publish will need to process the file during its import.

There are few catches that can make this simple process really painful.

1. Firstly, you need to remember to export bibliography in Zotero to **BibTeX format**, not BibLaTeX, Better BibTeX, Better BibLaTeX etc. Other formats store date information in the field 'date', while `publish` looks for 'year' field.

2. `publish` assumes that the value of each .bib entry field is embraced with curly braces `{...}`. I couldn't make Zotero to export entries in such format. In my case each field value was embraced with quotation marks `"..."`. At this point, we already know that we need to some kind of automation of the work. This is a job for a script (`zobib2pubib.py`).

3. The previous point is not really a problem. The worst things come when importing .bib file with `publish`. There are a lot of entry types or entry fields that `publish` cannot handle properly and refuses to add to its database. For example, `month` field of .bib entry of `book` type is unmanageable for `publish`. There are a lot of other problematic cases. During my work I simply added these cases, one by one, so they can be resolved automatically by the python script. In most cases it simply came down to removing problematic fields of an entry (I wanted to have the work done as fast as I could and I didn't bother about the less significant .bib entry fields).

The last point forced me to look for some .bib file parser in order to ease the whole process. This way I stumbled upon [`pybtex` package](https://pybtex.org) and use it in `zobib2pubib.py` script. Unfortunately, all these additional burden did not free me from the necessity of the manual approving of many, many entries, but at least it made importing possible at all.


## How to use this repository

Improved, automated workflow for converting standard BibTeX bibliography to DocOnce compatible format comes down to:

1. Export Zotero bibliograpy to ZoteroLibrary.bib file (BibTeX format! not BibLaTeX!) (Zotero -> File -> Export Library... -> Format: BibTeX) -- this step probably can also be automated by some python package, however I didn't have time to do a proper research.

2. run
   
	   git clone https://github.com/przemarbor/zobib2pubib.git
	   cd zobib2pubib
	   python3 -m venv venv
	   source venv/bin/activate
	   pip3 install -r requirements.txt # installing pybtex and publish-doconce
	   # now, we assume that ZoteroLibrary.bib with your bibliography is inside the directory
	   python3 zobib2pubib.py
	   # now, depending on the size of the ZoteroLibrary.bib file, 
	   # one may need to spend _a_lot_of_time_ on typing.
	   
	   # zobib3pubib.py script produces 2 files: 
	   #   - papers.pub (with the bibliography entries) and 
	   #   - venues.list (list of publishers). 
	   # Copy both of them to the proper place in doconce document structure. 
   


