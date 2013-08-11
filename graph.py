import xml.dom.minidom as minidom
from xdiff_core import Xmldiff

from operator import itemgetter

class BipartiteMatcher:
    xd        = None
    x         = None
    y         = None
    unmappedX = None
    unmappedY = None
    mat       = None

    def __init__(self, xd, x, y):
        self.xd        = xd
        self.x         = x
        self.y         = y
        self.unmappedX = []
        self.unmappedY = []
        self.mat       = []

    def findMatches (self):
        self.createSignatureTables()
        return (self.unmappedX, self.mat, self.unmappedY)


    def createGroupsOfSameSign (self, alist, groups):
        for a in alist:
            if self.xd.signature(a) not in groups:
                groups[self.xd.signature(a)] = [a]
            else:
                groups[self.xd.signature(a)].append(a)

    def createSignatureTables(self):
        # create groups for x
        groupsofx = {}
        self.createGroupsOfSameSign(self.x, groupsofx)

        # create groups for y
        groupsofy = {}
        self.createGroupsOfSameSign(self.y, groupsofy)

        # create temporary copies
        xremaining = self.x[:]
        yremaining = self.y[:]

        for k in groupsofx.keys():
            if k in groupsofy.keys():
                (umx, mat, umy) = self.createPotentialMatchList (groupsofx[k][:],
                                                                 groupsofy[k][:])
                # remove from remaining list
                self.removeFromList (xremaining, groupsofx[k])
                self.removeFromList (yremaining, groupsofy[k])

                self.unmappedX.extend (umx)
                self.unmappedY.extend (umy)
                self.mat.extend       (mat)

        # found the unmapped compoments
        self.unmappedX.extend (xremaining)
        self.unmappedY.extend (yremaining)


    def removeFromList(self, remaining, groupsmapped):
        for k in groupsmapped:
            remaining.remove (k)

    def createPotentialMatchList (self, listx, listy):
        distlist = []

        for x in listx:
            for y in listy:
                if (x, y) not in self.xd.disttable.keys():
                    self.xd.computedist (x, y)
                    
                if (x, y) in self.xd.disttable.keys():
                    dist = self.xd.disttable[(x, y)]
                    distlist.append ((dist, x, y))
                else:
                    print "the following two do not have distance computed"
                    print x.toxml()
                    print '------------'
                    print y.toxml()

        matched = []

        # sort by distance
        #print distlist
        sortedlist = sorted(distlist, key=itemgetter(0))

        for item in sortedlist:
            if len(listx) != 0 and len(listy) != 0:
                matched.append((item[1], item[2]))
                listx.remove(item[1])
                listy.remove(item[2])

        unmatchedx = listx
        unmatchedy = listy

        return (unmatchedx, matched, unmatchedy)
