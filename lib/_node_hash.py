import xml.etree.ElementTree as ElementTree
import hashlib

def computehash (elem, hashdict):
    """
    This routine inserts into 'hashdict', hash value of
    each element of the subtree rooted at 'elem'.
    Attributes have not been taken care yet.
    """

    # [1]. Create a hash object
    sha = hashlib.sha1()

    # [2]. Look for attributes

    # [3]. Check if 'elem' is the leaf object.
    #      If yes, the create hash using the text object
    if len(elem) == 0:
        sha.update (elem.text.strip())
        hashdict[elem] = sha.hexdigest()
    else:
        childhash = []
        for child in elem:
            childhash.append(computehash(child, hashdict))

        for iter in sorted(childhash):
            sha.update (iter)

        hashdict[elem] = sha.hexdigest()

    return hashdict[elem]


def readxml():
    dict1 = {}
    tree1 = ElementTree.parse ('tests/a.xml')
    root1 = tree1.getroot()
    computehash (root1, dict1)

    dict2 = {}
    tree2 = ElementTree.parse ('tests/d.xml')
    root2 = tree2.getroot()
    computehash (root2, dict2)

    if dict1[root1] == dict2[root2]:
        print "XMLs are same"
    else:
        print "XMLs are different"

if __name__ == '__main__':
    readxml()
