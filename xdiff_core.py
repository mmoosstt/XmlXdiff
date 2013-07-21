import xml.dom.minidom as minidom
import hashlib
import itertools

class Xmldiff:

    dict1     = {}
    dict2     = {}
    doc1      = 0
    doc2      = 0
    root1     = 0
    root2     = 0
    disttable = {}
    M_min     = {}

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

    @classmethod
    def powerset(self, s):
        x = len(s)
        for i in range (1 << x):
            yield [s[j] for j in range(x) if (i & (1 << j))]

    @classmethod
    def isleafnode (self, node):
        if node == None:
            return False

        if node.hasChildNodes():
            return False
        else:
            return True

    @classmethod
    def totalNodes (self, node):
        total = 0
        if node != None:
            total = 1
            if node.hasChildNodes():
                for child in [i for i in node.childNodes if self.valid_node(i)]:
                    total = total + self.totalNodes (child)
        return total

    @classmethod
    def costInsert (self, node):
        return self.totalNodes (node)

    @classmethod
    def costDelete (self, node):
        return self.totalNodes (node)

    def __init__ (self):
        self.dict1     = {}
        self.dict2     = {}
        self.doc1      = 0
        self.doc2      = 0
        self.root1     = 0
        self.root2     = 0
        self.disttable = {}
        self.M_min     = {}

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
            for child in [i for i in elem.childNodes if self.valid_node(i)]:
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

    def getPartialBipartMatch (self, a, b):
        aset = set(a)
        bset = set(b)

        for asub in self.powerset(a):
            for bsub in self.powerset(b):
                if len(asub) == len(bsub):
                    asubset = set(asub)
                    bsubset = set(bsub)

                    adiff = aset - asubset
                    bdiff = bset - bsubset

                    for p in itertools.permutations(asub):
                        yield (adiff, zip(p, bsub), bdiff)

    def computemindist(self, x, y):
        c1 = [i for i in x.childNodes if self.valid_node(i)]
        c2 = [i for i in y.childNodes if self.valid_node(i)]

        # generate partial bipartite matching between childNodes
        bestMapped = None
        minDist    = -1
        for (unmappedX, mapped, unmappedY) in self.getPartialBipartMatch (c1, c2):
            dist = 0
            for childx in unmappedX:
                dist = dist + self.costDelete(childx) #self.disttable[(childx, None)]

            for childy in unmappedY:
                dist = dist + self.costInsert(childy) #self.disttable[(None, childy)]

            for (childx, childY) in mapped:
                dist = dist + self.disttable[(childx, childy)]

            if minDist < 0 or minDist > dist:
                minDist    = dist
                bestMapped = mapped

        # set the distance computed.
        #print "Setting mindist for", x, y, minDist
        self.disttable[(x, y)] = minDist

        # set the min cost matching
        self.M_min[(x, y)] = set([(x, y)])
        for (childx, childy) in bestMapped:
            if (childx, childy) in self.M_min.keys():
                # mset = self.M_min[(x, y)]
                # mset.add(self.M_min[(childx, childy)])
                for (mat1, mat2) in self.M_min[(childx, childy)]:
                    self.M_min[(x, y)].add((mat1, mat2))

    def computedist (self, x, y):
        '''
        Computes distance between two nodes of two diffenent XML docs.
        Uses 'computemindist', 'costInsert', 'costDelete'
        '''
        # leaf node
        if self.isleafnode(x) and self.isleafnode(y):
            if self.signature(x) == self.signature(y):
                if x.nodeValue == y.nodeValue:  # values same. dist zero
                    #print "Setting mindist for ", x, y, 0
                    self.disttable[(x, y)] = 0
                else:
                    #print "Setting mindist for ", x, y, 1
                    self.disttable[(x, y)] = 1
                self.M_min[(x, y)]     = set([(x, y)])

        if self.isleafnode(x) and y == None:
            #print "Setting mindist for ", x, y, 1
            self.disttable[(x, y)] = 1

        if x == None and self.isleafnode(y):
            #print "Setting midist for ", x, y, 1
            self.disttable[(x, y)] = 1

        # none leaf node
        if not self.isleafnode(x) and y == None:
            #print "Setting mindist for ", x, y, self.costDelete(x)
            self.disttable[(x, y)] = self.costDelete(x)

        elif x == None and not self.isleafnode(y):
            #print "Setting mindist for ", x, y, self.costInsert(y)
            self.disttable[(x, y)] = self.costInsert(y)

        elif not self.isleafnode(x) and not self.isleafnode(y):
            if self.signature(x) != self.signature(y):
                #print "Setting mindist for ", x, y, self.costDelete(x) + self.costInsert(y)
                self.disttable[(x, y)] = self.costDelete(x) + self.costInsert(y)

            else:
                self.computemindist(x, y)

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

    def notPresentInFst (self, mminset, node):
        for (x, y) in mminset:
            if x == node:
                return False
        return True

    def notPresentInSnd (self, mminset,  node):
        for (x, y) in mminset:
            if y == node:
                return False
        return True

    def generatescript(self, root1, root2):
        if (root1, root2) not in self.M_min[(root1, root2)]:
            print "Delete ", root1.nodeName, "Inset ", root2.nodeName
        else:
            if (root1, root2) in self.disttable.keys():
                if self.disttable[(root1, root2)] == 0:
                    print ''

            for x in [i for i in root1.childNodes if self.valid_node(i)]:
                for y in [i for i in root2.childNodes if self.valid_node(i)]:
                    if (x, y) in self.M_min[(root1, root2)]:
                        if self.isleafnode(x) and self.isleafnode(y):
                            if (x, y) in self.disttable.keys():
                                if self.disttable[(x, y)] == 0:
                                    print ''
                                else:
                                    print "update ", x.nodeValue, " to ", y.nodeValue
                        else: #x, y are not leaf nodes
                            self.generatescript(x, y)

                    if self.notPresentInSnd (self.M_min[(root1, root2)], y):
                        print "insert ", y.toxml()
                if self.notPresentInFst (self.M_min[(root1, root2)], x):
                    print "delete ", x.toxml()

    def xdiff(self):
        # check and filtering
        if self.checkroothash():
            print "XML are same"
        else:
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
    xd.xdiff()

    #_test_signature()
