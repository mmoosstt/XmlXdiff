import xml.dom.minidom as minidom
import hashlib

def computehash (elem, hashdict):
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


def typeofelem (elem, docroot):
    if elem == docroot:
        return ''
    else:
        parent = elem.parentNode
        return typeofelem(parent, docroot) + '/' + elem.nodeName

def readxml():
    dict1 = {}
    doc1 = minidom.parse ('tests/a.xml')
    root1 = doc1.documentElement
    computehash (root1, dict1)

    dict2 = {}
    doc2 = minidom.parse ('tests/c.xml')
    root2 = doc2.documentElement
    computehash (root2, dict2)

    if dict1[root1] == dict2[root2]:
        print "XMLs are same"
    else:
        print "XMLs are different"

def valid_node (node):
    if node.nodeName == '#text':
        if node.nodeValue.strip() == '':
            return False
    return True

def _test_typeofelem():
    doc1 = minidom.parse('tests/a.xml')
    root1 = doc1.documentElement

    def inner_test(elem):
        print typeofelem (elem, doc1)

        if elem.hasChildNodes:
            for child in elem.childNodes:
                if valid_node (child):
                    inner_test (child)
        else:
            print 'elem has no child'

    inner_test (root1)

if __name__ == '__main__':
    _test_typeofelem()
