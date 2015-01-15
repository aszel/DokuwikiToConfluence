import sys
import urllib2
from bs4 import BeautifulSoup, Comment

dokuwikipageid = "start"
attributes = ["id", "class"]

def getExportFromWiki():
    dokuwikipageid = sys.argv[-1]
    url = "http://wiki.local/doku.php?id=" + dokuwikipageid + "&do=export_xhtmlbody"
    print "getExport " + dokuwikipageid
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup

# Read whole file to string from command line
def readFromFile():
    filename = sys.argv[-1]
    with open (filename, "r") as myfile:
        inputData = myfile.read()
        soup = BeautifulSoup(inputData)
        return soup

# Remove all HTML comments
def removeAllComments(soup):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup

def removeAttributes(soup, attributes):
    for tag in soup.findAll(True):
        #tag.attrs['id'] = None
        #tag.attrs['class'] = None
        del tag["id"]
        del tag["class"]
    return soup


# Add CDATA tags
# open with <![CDATA[
# close with ]]>
def addCdataTags(soup):
    openCdata = "<![CDATA["
    closeCdata = "\n]]>"
    findStart = "<ac:plain-text-body>"
    findEnd = "</ac:plain-text-body>"
    string = str(soup)
    replaceStart = findStart + openCdata
    replaceEnd = closeCdata + findEnd
    string = string.replace(findStart, replaceStart)
    string = string.replace(findEnd, replaceEnd)
    soup = BeautifulSoup(string)
    return soup


#   find
#<pre class="code">
#</pre>
#   replace with
#<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[
#]]></ac:plain-text-body></ac:structured-macro>
def replacePreTagsWithConfluenceMacroTags(soup):

    for pre in soup.findAll("pre", { "class" : "code" }):
        tag1 = soup.new_tag("ac:structured-macro")
        tag1["ac:name"] = "code"
        tag2 = soup.new_tag("ac:plain-text-body")
        tag2.string = pre.string
        tag1.append(tag2)
        pre.replace_with(tag1)

    return soup

# Adds block to top of Confluence page
def addContentAndHistoryBlock(soup):
    historyBlock = """
<ac:structured-macro ac:name="section">
<ac:rich-text-body>
<ac:structured-macro ac:name="column">
<ac:rich-text-body>
<h1>Inhaltsverzeichnis</h1>
<ac:structured-macro ac:name="toc">
<ac:parameter ac:name="location">top</ac:parameter>
<ac:parameter ac:name="exclude">Inhaltsverzeichnis|Ueberblick</ac:parameter>
<ac:parameter ac:name="type">list</ac:parameter>
</ac:structured-macro>
</ac:rich-text-body>
</ac:structured-macro>
<ac:structured-macro ac:name="column">
<ac:rich-text-body>
<h1>Ueberblick</h1>
<table>
<tbody>
<tr>
<th>
<p>Klassifizierung:</p>
</th>
<td>
<p>intern</p>
</td>
</tr>
<tr>
<th>
<p>Verteiler:</p>
</th>
<td>
<p>The unbelievable Machine Company GmbH</p>
</td>
</tr>
</tbody>
</table>
<p>
<strong>Versionshistorie:</strong>
</p>
<p>
<ac:structured-macro ac:name="version-history">
<ac:parameter ac:name="first">6</ac:parameter>
</ac:structured-macro>
</p>
</ac:rich-text-body>
</ac:structured-macro>
</ac:rich-text-body>
</ac:structured-macro>"""

    string = str(soup)
    result = historyBlock + string
    soup = BeautifulSoup(result)
    return soup

#soup = readFromFile()
soup = getExportFromWiki()
soup = removeAllComments(soup)
soup = replacePreTagsWithConfluenceMacroTags(soup)
soup = removeAttributes(soup, attributes)
soup = addCdataTags(soup)
soup = addContentAndHistoryBlock(soup)
print soup

