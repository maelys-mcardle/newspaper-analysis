# Newspaper Article Analysis

This code loads articles from a particular newspaper for data analysis.

This was put together for a research project into transphobia, and there was
simply too much data to go through by hand.

This was written for `Python 3.8`.

## Setting Up Scripts

Set-up the python requirements by invoking the following:

```
python -m pip install -r requirements.txt
```

## Running Scripts

The newspaper articles must be *downloaded* and then *extracted* before they can
be *analyzed*. There's a `config.yaml` file that sets up where files and 
directories will be created.

### Download Articles

The first stage is getting all the articles loaded onto the local system
in order to do the analysis. Otherwise you'd be fetching the articles over
and over.

To download the articles, run the `scripts/newspaper-download.py` script.
This will download them all as raw `html` files that can then be processed.

### Extract Articles From Raw Data

The previous script will have loaded articles as raw `html` files. The next
stage is taking all this raw data, and processing it in a way that extracts
all the important things like the article content, the authors, the date of
publication, etc.

To do this extraction, run the `scripts/newspaper-extract.py` script.

### Perform Data Analysis

The previous script will have extracted all the relevant data from the
articles. Now you can do the data analysis. This will let you do such
things as search for specific text, give a count of the authors, etc.

To do this analysis, run the `scripts/newspaper-analyze.py` script.

This script can do much more. See the `--help` information for 
details on usage. See also the `config.yaml` configuration file,
as it can also affect things like the output format for this script.