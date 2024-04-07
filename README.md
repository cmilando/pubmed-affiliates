Authors: CWM and ChatGPT

A combined python and R script to find and clean co-authors and affiliations via PubMED only, in preparation for NSF and other grant submissions. Probably more cases could be added to `get_author_info()`.

First run `run.py`, changing the parameters in `get_all_IDs()`, then doing `> python3 run.py` in the terminal.

Then run `clean.R`, adjusting as necessary.

Helpful links:
* https://www.ncbi.nlm.nih.gov/books/NBK25501/
* https://github.com/emdb-empiar/pubmed-author-affiliations
* https://github.com/aolney/nsf-coa