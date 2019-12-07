# Newspaper Article Analysis

This code loads articles from a particular newspaper for data analysis.

This was written for `Python 3.8`.

## Download Articles

To download the articles, run the `download-pages.py` script.

It will download them from, by default, the `url-list.txt` file.

This will load them all, by default, into the `downloads` directory.

## Extract Articles From Raw Data

The previous script will have loaded articles as raw `html` files.

To extract the actual articles from that, run the `parse-pages.py` script.

This will extract all the data and put it, by default, into the `all-articles-with-metadata.yaml` 
and `all-articles.md` files.

## Perform Data Analysis

The previous script will have extracted the articles from the raw downloaded files.

To then analyze these articles, run the `analyze-pages.py` script.

This will retrieve the data from, by default, the `all-articles-with-metadata.yaml` file.

This can search the articles for a string of text, fetch statistics such as the total number of articles
and paragraphs, give a count of how many articles were produced each year, and how many articles
each author contributed. See the `--help` information for details on usage.