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

    tocXml.closeFile()
    f.close()
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
