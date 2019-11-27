# Newspaper Article Analysis

This code loads articles from a particular newspaper for data analysis.

This was written for `Python 3.8`.

## Download Articles

To download the articles, run the `download-pages.py` script.

It will download them from, by default, the `url-list.txt` file.

This will load them all, by default, into the `downloads` directory.

## Extract Articles From Raw Data

The previous script will have loaded articles as raw `html` files.

To extract the actual articles from that, runn the `parse-pages.py` script.

This will extract all the data and put it, by default, into the `all-articles-with-metadata.yaml` 
and `all-articles.md` files.

## Perform Data Analysis

TBD.
