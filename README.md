# DokuwikiToConfluence
This is a tool to export pages from a local Dokuwiki into a useable format for Atlassian Confluence.

## Usage
    python DokuwikiToConfluence.py <IdOfLocalWikiPage>
    python DokuwikiToConfluence.py splunk
    python DokuwikiToConfluence.py splunk > result.file
    
## Description
This tool uses the export functionality of [Dokuwiki](https://www.dokuwiki.org/). It takes the HTML output of it and does the following:
* remove all CSS classes
* remove all IDs
* replace pre tags with Confluence CDATA tags and macros
* print output to command line (which you could pipe into a file if you want)
