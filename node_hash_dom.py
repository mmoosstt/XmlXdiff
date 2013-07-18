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
    M_min     = set()

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
        self.M_min     = set()

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

    def computemindist(self, x, y):
        c1 = x.childNodes
        c2 = y.childNodes

        # generate partial bipartite matching between childNodes
        bestMatching = None
        minDist      = -1
        for (unmapedX, mapped, unmappedY) in self.getPartialBipartMatch (c1, c2):
            dist = 0
            for childx in unmapedX:
                dist = dist + self.disttable[(childx, None)]

            for childy in unmapedY:
                dist = dist + self.disttable[(None, childy)]

            for (childx, childY) in mapped:
                dist = dist + self.disttable[(childx, childy)]

            if minDist < 0 or minDist > dist:
                minDist = dist

        self.disttable[(x, y)] = minDist

    def computedist (self, x, y):
        '''
        Computes distance between two nodes of two diffenent XML docs.
        Uses 'computemindist', 'costInsert', 'costDelete'
        '''
        # leaf node
        if self.isleafnode(x) and self.isleafnode(y)
            if self.signature(x) == self.signature(y):
                if x.value == y.value:  # values same. dist zero
                    self.disttable[(x, y)] = 0
                else:
                    self.disttable[(x, y)] = 1
        if self.isleafnode(x) and y == None:
            self.disttable[(x, y)] = 1

        if x == None and self.isleafnode(y):
            self.disttable[(x, y)] = 1

        # none leaf node
        if not self.isleafnode(x) and y == None:
            self.disttable[(x, y)] = self.costDelete(x)

        elif x == None and not self.isleafnode(y):
            self.disttable[(x, y)] = self.costInsert(x)

        elif not isleafnode(x) and not isleafnode(y):
            if self.signature(x) != self.signature(y):
                self.disttable[(x, y)] = self.costDelete(x) + self.costInsert(y)

            else:
                self.computemindist(x, y)

    def addChildtoMmin (self, root1, root2):
        self.M_min.add ((root1, root2))

        for x in root1.childNodes:
            for y in root2.childNodes:
                if (x, y) in self.disttable.keys():
                    if self.disttable[(x, y)] == 0:
                        self.M_min.add ((x, y))
                self.addChildtoMmin(x, y)

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
                    self.computedist (x, y)
            n1 = self.parents (n1)
            n2 = self.parents (n2)

        # for k1, k2 in self.disttable.keys():
        #     print self.signature(k1), self.signature(k2)
        #     print self.disttable[(k1, k2)]

        if self.signature(self.root1) != self.signature(self.root2):
            return
        else:
            #self.M_min.add ((self.root1, self.root2))
            self.addChildtoMmin(self.root1, self.root2)

    @classmethod
    def isleafnode (self, node):
        if node == None:
            return False

        if node.hasChildNodes:
            return False
        else:
            return True

    def notPresentInFst (self, node):
        for (x, y) in self.M_min:
            if x == node:
                return False
        return True

    def notPresentInSnd (self, node):
        for (x, y) in self.M_min:
            if y == node:
                return False
        return True

    def generatescript(self, root1, root2):
        if (root1, root2) not in self.M_min:
            print "Delete ", root1.nodeName, "Inset ", root2.nodeName
        else:
            if (root1, root2) in self.disttable.keys():
                if self.disttable[(root1, root2)] == 0:
                    print '1'

            for x in root1.childNodes:
                for y in root2.childNodes:
                    if self.isleafnode(x) and self.isleafnode(y):
                        if (x, y) in self.disttable.keys():
                            if self.disttable[(x, y)] == 0:
                                print '1'
                        else:
                            print "update ", x.nodeValue, " to ", y.nodeValue
                    else: #x, y are not leaf nodes
                        self.generatescript(x, y)

                    if self.notPresentInSnd (y):
                        print "insert ", y.nodeName
                if self.notPresentInFst (x):
                    print "delete ", x.nodeName

    def xdiff(self):
        # check and filtering
        if self.checkroothash():
            print "XML are same"
        else:
            # for x in self.root1.childNodes:
            #     for y in self.root2.childNodes:
            #         if self.dict1[x] == self.dict2[y]:
            #             self.root1.removeChild(x)
            #             self.root2.removeChild(y)
            pass

            # matching
            self.mincostmatching (self.root1, self.root2)

            # generate editscript
            self.generatescript (self.root1, self.root2)

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
    xd.readxml('tests/a.xml', 'tests/b.xml')
    #xd.mincostmatching(xd.root1, xd.root2);
    xd.xdiff()

    #_test_signature()
