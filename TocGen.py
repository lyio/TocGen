# parsing index.html to generate eclipse toc.xml
import TocFile
import lxml.html

# command line parameters:
# filepath to index.html
# filepath to target xml file
# filepath to the cover html file

def main(args):
    # having a look at the command line parameters
    if len(args) != 3:
        print("1. filepath to index.htm \n2. filepath to target xml \n3. filepath to cover html file")
        return
    
    print("opening source html")
    f = open(args[0])
    html = f.read()
    tree = lxml.html.fromstring(html)
    # iterating over html
    for e in tree.iter():
        # getting document title    
        if (e.tag == "p") and ("class" in e.attrib):
            if e.attrib["class"] == "navtitle":
                print ("Document title: " + e.text)
                title = e.text
                # creating XML file
                tocXml = TocFile.TocFile(args[1], title, args[2])
        
        # stopping at links and getting the doc link and topic name
        
        if (e.tag == "a"):
            link = "html/" + e.attrib["href"]
            print ("Link found: " + link)
        if e.tag == "span" and "id" in e.attrib:
                idString = e.attrib["id"]
                topicName = e.text
                print ("Topic info: " + topicName + " :: " + idString)
                
                # with link, topicName and idString identified, write topic
                tocXml.writeTopic(topicName, link, idString)
            
            
            
            
    tocXml.closeFile()
    f.close()

def findNameID(sSpanString):
    ''' (string) -> (string, string)
    takes the inner Node of a link tag and
    extracts the information in the inner span tag.
    Returns a tuple of the caption id and the name of the topic
    
    >>> print(findNameID("<span id="s1" class="heading1">1 Einfuhrung - Was ist LabImage 1D</span>"))
    ("s1", "1 Einfuhrung - Was ist LabImage 1D")
    '''
    spantree = lxml.html.fromstring(sSpanString)
    for e in spantree.iter():
        if e.tag == "span":
            dbnjk = 5
    return
    

if __name__ == "__main__":
    # DEBUG
    main(("test.html", "toc.xml", "test.link"))
    #import sys
    #main(sys.argv[1:])
