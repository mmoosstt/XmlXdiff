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
    signhash  = {}

    def signature (self, elem):
        if elem in self.signhash:
            return self.signhash[elem]
        else:
            retval = None
            if elem.nodeType == minidom.Node.DOCUMENT_NODE:
                retval = ''
            elif elem.nodeType == minidom.Node.ATTRIBUTE_NODE:
                retval = self.signature (elem.ownerElement) + '/' + elem.nodeName + '/#attr'
            else:
                retval =  self.signature(elem.parentNode) + '/' + elem.nodeName
        self.signhash[elem] = retval
        return retval

    @classmethod
    def valid_node (self, node):
        if node.nodeType == minidom.Node.COMMENT_NODE:
            return False

        if node.nodeName == '#text':
            if node.nodeValue.strip() == '':
                return False
        return True

    @classmethod
    def setParentToElem(self, a, p):
        a.parentNode = p

    @classmethod
    def child_nodes (self, node):
        if node.hasChildNodes():
            for child in node.childNodes:
                if self.valid_node (child):
                    self.setParentToElem (child, node)
                    yield child

        if node.nodeType != minidom.Node.TEXT_NODE and node.hasAttributes:
            attrmap = node.attributes
            if attrmap != None:
                for v in attrmap._attrs.values():
                    self.setParentToElem (v, node)
                    yield v

    @classmethod
    def iterleafnodes (self, elem):
        leafnodes = []
        haschild  = False

        for child in self.child_nodes (elem):
            haschild = True
            leafnodes.extend (self.iterleafnodes (child))

        if haschild == False:
            leafnodes.append (elem)

        return leafnodes


    @classmethod
    def parents (self, nodes):
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
    def isleafnode (self, node):
        retVal = True

        if node == None:
            retVal =  False
        else:
            for child in self.child_nodes (node):
                retVal = False;
                break

        return retVal

    @classmethod
    def totalNodes (self, node):
        total = 0
        if node != None:
            total = 1
            for child in self.child_nodes (node):
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
        self.signhash  = {}

    def computehash (self, elem, hashdict):
        # [0]. is valid node
        if not self.valid_node (elem):
            return

        # [1]. Create a hash object
        sha       = hashlib.sha1()
        isleaf    = True

        childhash = []
        for child in self.child_nodes (elem):
            isleaf = False
            childhash.append (self.computehash (child, hashdict))

        if isleaf == True:
            value = elem.nodeValue
            sha.update (value.strip())

        else:
            for it in sorted (childhash):
                sha.update (it)
            sha.update(elem.nodeName)

        hashdict[elem] = sha.hexdigest()
        
        #print 'hash of ', self.signature(elem), ' is ', hashdict[elem]

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


    def getPartialBipartMatch (self, x, y):
        bpm = graph.BipartiteMatcher (self, x, y)
        return bpm.findMatches()


    def computemindist(self, x, y):
        c1 = [i for i in self.child_nodes (x)]
        c2 = [i for i in self.child_nodes (y)]

        (unmappedX, mapped, unmappedY) = self.getPartialBipartMatch (c1, c2)
        dist = 0
        for childx in unmappedX:
            dist = dist + self.costDelete(childx)

        for childy in unmappedY:
            dist = dist + self.costInsert(childy)

        for (childx, childy) in mapped:
            if (childx, childy) in self.disttable:
                dist = dist + self.disttable[(childx, childy)]
            else:
                dist = dist + self.costDelete(childx) + self.costInsert(childy)

        # set the distance computed.
        self.updatedisttable(x, y, dist)

        # set the min cost matching
        self.M_min[(x, y)] = set([(x, y)])
        for (childx, childy) in mapped:
            if (childx, childy) in self.M_min:
                for (mat1, mat2) in self.M_min[(childx, childy)]:
                    self.M_min[(x, y)].add((mat1, mat2))


    def updatedisttable(self, x, y, dist):
        #print 'setting dist ', x.nodeName, y.nodeName, dist
        self.disttable[(x, y)] =  dist


    def computedist (self, x, y):
        #print 'computing distance (', x.nodeName, ',', x.nodeValue,')','(', y.nodeName, y.nodeValue, ')'
        if (x, y) in self.disttable:
            return None

        else:
            if self.signature(x) == self.signature(y):
                if self.isleafnode(x) and self.isleafnode(y):
                    if x.nodeValue == y.nodeValue:
                        self.updatedisttable(x, y, 0)
                    else:
                        self.updatedisttable(x, y, 1)
                    self.M_min[(x, y)] = set([(x, y)])

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
            #print 'n1 = ', [n.nodeName for n in n1]
            #print 'n2 = ', [n.nodeName for n in n2]
            for x in n1:
                for y in n2:
                    self.computedist (x, y)
            n1 = self.parents (n1)
            n2 = self.parents (n2)


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
        # print '---------------------------------'
        # for (k1, k2) in self.M_min:
        #     print '[', k1.nodeName, k2.nodeName, '] --> ', [(n1.nodeName, n2.nodeName) for (n1, n2) in self.M_min[(k1, k2)]]
        # print '---------------------------------'
 
        if  (root1, root2) not in self.M_min:
            print "Delete ", root1.nodeName, "Insert ", root2.nodeName
        elif (root1, root2) not in self.M_min[(root1, root2)]:
            print "Delete ", root1.nodeName, "Inset ", root2.nodeName
        else:
            if ((root1, root2) in self.disttable) and (self.disttable[(root1, root2)] == 0):
                pass
            else:
                for x in self.child_nodes (root1):
                    for y in self.child_nodes (root2):
                        if (x, y) in self.M_min[(root1, root2)]:
                            if self.isleafnode(x) and self.isleafnode(y):
                                if (x, y) in self.disttable:
                                    if self.disttable[(x, y)] == 0:
                                        pass
                                    else:
                                        print "update ", x.nodeValue, " to ", y.nodeValue
                            else: #x, y are not leaf nodes
                                self.generatescript(x, y)

                        if self.notPresentInSnd (self.M_min[(root1, root2)], y):
                            print "insert ", self.signature(y) #y.toxml()
                    if self.notPresentInFst (self.M_min[(root1, root2)], x):
                        print "delete ", self.signature(x) #x.toxml()

    def xdiff(self):
        # check and filtering
        if self.checkroothash():
            print "XML are same"
        else:
            # matching
            self.mincostmatching (self.root1, self.root2)

            # generate editscript
            self.generatescript (self.root1, self.root2)


def _test_signature(file):
    doc1 = minidom.parse(file)
    root1 = doc1.documentElement

    def inner_test(elem):
        # [1]. print self
        print Xmldiff.signature (elem)

        for child in Xmldiff.child_nodes (elem):
            inner_test (child)

    inner_test (root1)

import graph


if __name__ == '__main__':
    print "testing xdiff_core..."
    xd = Xmldiff();
    xd.readxml('tests/test3/a.xml', 'tests/test3/b.xml')
    xd.xdiff()
    
    # _test_signature('tests/test3/a.xml')
