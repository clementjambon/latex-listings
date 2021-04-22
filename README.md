# latex-listings
*Clément JAMBON*

This small program allows you to include all your source code in a provided LaTeX file. The listings are included with respect to their hierarchy in the selected folder. The package used for code highlighting is *minted* and thus needs to be included in your template file.

To include your listings, please add the following line in your target *.tex* file at the desired location :
```latex
% {insert_listing}
```
For more information, please refer to the example template file *ex_template.tex*.

Then, run
```bash
python ./insert_listing.py RELATIVE_PATH DEST_PATH TEMPLATE_PATH
```
and you should find the resulting *.tex* file in *DEST_PATH*

For now, the supported languages are:
- .tex
- .cpp
- .txt

By default, the hierarchy is translated to LaTeX hierachy (section, subsection, subsubsection). This can be changed by setting *ADD_HIERARCHY* to *False* in *latex-listings.py*.