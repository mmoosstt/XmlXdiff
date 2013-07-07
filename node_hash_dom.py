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
    def signature (self, elem, docroot):
        if elem == docroot:
            return ''
        else:
            parent = elem.parentNode
            return self.signature(parent, docroot) + '/' + elem.nodeName

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

        # [3].
        if not elem.hasChildNodes():
            elem.normalize()
            value = elem.nodeValue

            sha.update (value.strip())
            hashdict[elem] = sha.hexdigest()

        else:
            childhash = []
            for child in elem.childNodes:
                childhash.append (computehash (child, hashdict))

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

    def mincostmatching (self):
        n1 = set()
        for leaf1 in iterleafnodes (doc1):
            n1.append (leaf1)

        n2 = set()
        for leaf2 in iterleafnodes (doc2):
            n2.append (leaf2)

        while len(n1) != 0 or len(n2) != 0:
            for x in n1:
                for y in n2:
                    if signature(x) == signature(y):
                        # computedist (x, y)

            n1 = parents (n1)
            n2 = parents (n2)



    
def _test_signature():
    doc1 = minidom.parse('tests/a.xml')
    root1 = doc1.documentElement

    def inner_test(elem):
        print Xmldiff.signature (elem, doc1)

        if elem.hasChildNodes:
            for child in elem.childNodes:
                if Xmldiff.valid_node (child):
                    inner_test (child)
        else:
            print 'elem has no child'

    inner_test (root1)

if __name__ == '__main__':
    xd = Xmldiff();

    xd.readxml('tests/a.xml', 'tests/d.xml')
