import xml.dom.minidom as minidom
import hashlib

class Xmldiff:

    dict1     = {}
    dict2     = {}
    doc1      = 0
    doc2      = 0
    root1     = 0
    root2     = 0
    disttable = {}

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

    @classmethod
    def iterleafnodes (self, elem):
        '''
        Returns all the leaf level nodes of a subtree rooted at 'elem'
        That includes all the text nodes and all the attributes.
        It filter outs all the elements which are not valid node.
        '''
        leafnodes = []

        if elem.nodeType != minidom.Node.TEXT_NODE and elem.hasAttributes:
            attrmap = elem.attributes
            for v in attrmap._attrs.values():
                leafnodes.append (v)

        if elem.hasChildNodes():
            for child in elem.childNodes:
                if Xmldiff.valid_node (child):
                    leafnodes.extend (self.iterleafnodes (child))
        else:
            leafnodes.append (elem)

        return leafnodes

    @classmethod
    def parents (self, nodes):
        '''
        for each element in the set of 'nodes', return the set
        of their parents.
        '''
        p = set()

        for node in nodes:
            if node.nodeType == minidom.Node.DOCUMENT_NODE:
                pass
            elif node.nodeType == minidom.Node.ATTRIBUTE_NODE:
                p.add (node.ownerElement)
            else:
                p.add (node.parentNode)
        return p


    def __init__ (self):
        self.dict1     = {}
        self.dict2     = {}
        self.doc1      = 0
        self.doc2      = 0
        self.root1     = 0
        self.root2     = 0
        self.disttable = {}

    def computehash (self, elem, hashdict):
        # [1]. Create a hash object
        sha = hashlib.sha1()

        # [2]. Look for attributes
        if elem.nodeType != minidom.Node.TEXT_NODE and elem.hasAttributes:
            attrmap = elem.attributes
            for v in attrmap._attrs.values():
                sha.update (v.nodeName)
                sha.update (v.value)

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

                for it in sorted (childhash):
                    sha.update (it)
            hashdict[elem] = sha.hexdigest()

        return hashdict[elem]


    def readxml(self, xml1, xml2):
        self.doc1  = minidom.parse (xml1)
        self.root1 = self.doc1.documentElement
        self.computehash (self.root1, self.dict1)

        self.doc2  = minidom.parse (xml2)
        self.root2 = self.doc2.documentElement
        self.computehash (self.root2, self.dict2)


    def checkroothash(self):
        if self.dict1[self.root1] == self.dict2[self.root2]:
            return True
        else:
            return False

    def computedist (self, x, y):
        if x == y == None:
            return 0
        elif x == None:
            return 1
        elif y == None:
            return 1

        # leaf node
        if x.nodeType == minidom.Node.ATTRIBUTE_NODE:
            if x.value == y.value:  # values same. dist zero
                return 0
            else:
                return 1

        # leaf node
        elif x.nodeType == minidom.Node.TEXT_NODE:
            if x.nodeValue == y.nodeValue:
                return 0
            else:
                return 1

        # none leaf node
        else:
            pass

    def mincostmatching (self, root1, root2):
        '''
        compute the minimum edit distance (cost) between two nodes
        in two different xml files.
        '''
        n1 = set()
        for leaf1 in self.iterleafnodes (root1):
            n1.add (leaf1)

        n2 = set()
        for leaf2 in self.iterleafnodes (root2):
            n2.add (leaf2)

        while len(n1) != 0 or len(n2) != 0:
            for x in n1:
                for y in n2:
                    if self.signature(x) == self.signature(y):
                        self.disttable[(x, y)] = self.computedist (x, y)
                    else:
                        self.disttable[(x, y)] = self.computedist (x, None) + self.computedist (None, y)

            n1 = self.parents (n1)
            n2 = self.parents (n2)

        # for k1, k2 in self.disttable.keys():
        #     print self.signature(k1), self.signature(k2)
        #     print self.disttable[(k1, k2)]
        M_min = {}

        if self.signature(self.root1) != self.signature(self.root2):
            return

        else:
            pass


    def xdiff(self):

        # check and filtering
        if self.checkroothash():
            print "XML are same"
        else:
            for x in self.root1.childNodes:
                for y in self.root2.childNodes:
                    if self.dict1[x] == self.dict2[y]:
                        self.root1.removeChild(x)
                        self.root2.removeChild(y)

            # matching
            self.mincostmatching (self.root1, self.root2)

            # generate editscript

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
    xd = Xmldiff();
    xd.readxml('tests/a.xml', 'tests/d.xml')
    xd.mincostmatching(xd.root1, xd.root2);

    #_test_signature()
