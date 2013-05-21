# class to create the toc.xml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

#class for the xml file
class TocFile:
    
    def __init__(self, sFilePath, sHelpFile, sTopicLink):
        ''' creates the object and opens the xml file'''
        self.sFilePath = sFilePath
        self.rootNode = Element("toc")
        self.rootNode.set('label', sHelpFile)
        self.rootNode.set('topic', "html/" + sTopicLink)
        
        #rootNode is parent topic for first topic
        #and all topics on the first level
        self.nodeTree = {1: self.rootNode}
        

        
    def writeTopic(self, sTopicName, sTopicFile, sIdString):
        '''(string, string, string) -> NoneType
    Take the name of the topic, the link to the topic file and the id as string
    and creates the xml node accordingly. Places it in the tree as well
    '''
        nCurrentNode = Element("topic")
        nCurrentNode.set('label', sTopicName)
        nCurrentNode.set('href', sTopicFile)
        parentNode = self.evaluateID(sIdString, nCurrentNode)
        
        parentNode.append(nCurrentNode)
        
        

    def evaluateID(self, sIdString, nCurrentNode):
        ''' (string, xml node) -> xml node
    Evaluate the id string of the node to find out where to place the node
    in the tree. Returns the parent node.
    '''
        idNumber = self.transform(sIdString)
        # highest node, place right under rootNode
        # add current node for future child nodes
        if idNumber == 1:
            self.nodeTree.clear()
            self.nodeTree[1] = nCurrentNode
            return self.rootNode

        # if there is no node for this id,
        #create it and return parent node
        if not idNumber in self.nodeTree:
            self.nodeTree[idNumber] = nCurrentNode
            return self.nodeTree[idNumber - 1]
        
        # otherwise return node one level up
        return self.nodeTree[idNumber-1]
        
    def transform(self, sIdString):
        '''(self, string) -> int
    Strips unnecessary characters from the idString and returns the
    length of the remaining string.
    >>> tocFile = TocFile("test", "test", "test")
    >>> tocFile.transform("s1")
    1
    >>> tocFile.transform("s1.1")
    2
    >>> tocFile.transform("s2.2.3")
    3
    '''
        sId = ''
        for c in sIdString:
            if (c != "s") and (c != "."):
                sId += c

        return len(sId)

    def closeFile(self):
        f = open(self.sFilePath, 'w')
        elem = self.prettify(self.rootNode)
        f.write(elem)
        f.close()
    

    def prettify(self, elem):
        '''
    Return a pretty-printed XML string
        '''
        roughString = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(roughString)
        return reparsed.toprettyxml(indent = "  ")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    
