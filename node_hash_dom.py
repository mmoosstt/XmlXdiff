import xml.dom.minidom as minidom
import hashlib

class Xmldiff:

    dict1 = {}
    dict2 = {}
    doc1  = 0
    doc2  = 0
    root1 = 0
    root2 = 0

    @classmethod
    def signature (self, elem):
        if elem.nodeType == minidom.Node.DOCUMENT_NODE:
            return ''
        elif elem.nodeType == minidom.Node.ATTRIBUTE_NODE:
            return self.signature (elem.ownerElement) + '/' + elem.nodeName + '/#attr'
        elif elem.nodeType != minidom.Node.TEXT_NODE:
            return self.signature(elem.parentNode) + '/' + elem.nodeName
        else:
            return self.signature(elem.parentNode) + '/' + elem.nodeName

    @classmethod
    def valid_node (self, node):
        if node.nodeName == '#text':
            if node.nodeValue.strip() == '':
                return False
        return True


    def __init__ (self):
        self.dict1 = {}
        self.dict2 = {}
        self.doc1  = 0
        self.doc2  = 0
        self.root1 = 0
        self.root2 = 0

    def computehash (self, elem, hashdict):
        # [1]. Create a hash object
        sha = hashlib.sha1()

        # [2]. Look for attributes

        # [3]. Look for child nodes
        if not elem.hasChildNodes():
            elem.normalize()
            value = elem.nodeValue

            sha.update (value.strip())
            hashdict[elem] = sha.hexdigest()

        else:
            childhash = []
            for child in elem.childNodes:
                childhash.append (self.computehash (child, hashdict))

                for iter in sorted (childhash):
                    sha.update (iter)

            hashdict[elem] = sha.hexdigest()

        return hashdict[elem]


    def readxml(self, xml1, xml2):
        self.doc1 = minidom.parse (xml1)
        self.root1 = self.doc1.documentElement
        self.computehash (self.root1, self.dict1)

        self.doc2 = minidom.parse (xml2)
        self.root2 = self.doc2.documentElement
        self.computehash (self.root2, self.dict2)

        if self.dict1[self.root1] == self.dict2[self.root2]:
            print "XMLs are same"
        else:
            print "XMLs are different"


    def checkroothash(self):
        if self.dict1[self.root1] == self.dict2[self.root2]:
            return True
        else:
            return False

    def computedist (x, y):
        if not valid_node(x) and not valid_node(y):
            return 0
        if not valid_node(x) and valid_node(y):
            return 1
        if valid_node(x) and not valid_node(y):
            return 1
        
        assert x.nodeType == y.nodeType

        if x.nodeType == minidom.Node.ATTRIBUTE_NODE:
            if x.value == y.value:  # values same. dist zero
                return 0
            else:
                return 1

        if x.nodeType == minidom.Node.TEXT_NODE:
            if x.nodeValue == y.nodeValue:
                return 0
            else:
                return 1

    def mincostmatching (self):
        n1 = set()
        for leaf1 in self.iterleafnodes (self.doc1):
            n1.append (leaf1)

        n2 = set()
        for leaf2 in self.iterleafnodes (self.doc2):
            n2.append (leaf2)

        while len(n1) != 0 or len(n2) != 0:
            for x in n1:
                for y in n2:
                    if self.signature(x) == self.signature(y):
                        computedist (x, y)
                        pass

            n1 = self.parents (n1)
            n2 = self.parents (n2)




def _test_signature():
    doc1 = minidom.parse('tests/a.xml')
    root1 = doc1.documentElement

    def inner_test(elem):
        # [1]. print self
        print Xmldiff.signature (elem)

        # [2]. print attributes
        if elem.nodeType != minidom.Node.TEXT_NODE and elem.hasAttributes:
            attrmap = elem.attributes
            for v in attrmap._attrs.values():
                print Xmldiff.signature(v)

        # [3]. print children
        if elem.hasChildNodes():
            for child in elem.childNodes:
                if Xmldiff.valid_node (child):
                    inner_test (child)

    inner_test (root1)

if __name__ == '__main__':
    #    xd = Xmldiff();
    #xd.readxml('tests/a.xml', 'tests/d.xml')
    _test_signature()
