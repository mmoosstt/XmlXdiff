import lxmldiff
import lxml.etree
import hashlib

_path1 = "{}\\tests\\test1\\a.xml".format(lxmldiff.getPath())
_path2 =  "{}\\tests\\test1\\b.xml".format(lxmldiff.getPath())

_xml1 = lxml.etree.parse(_path1)
_xml2 = lxml.etree.parse(_path2)

_root1 = _xml1.getroot()
_root2 = _xml2.getroot()

def getChildren(xml, element, pathes, hashes):
    
    _hash = hashlib.sha1()
    _hash.update(lxml.etree.tostring(element))
    _path = xml.getpath(element)
    pathes[_path] = _hash
    hashes[_hash.hexdigest()] = _path
    
    for _child in element.getchildren():
        getChildren(xml, _child, pathes, hashes)
        

def updatePipe(pipe, element):
    pipe += (element.tag,)
    if hasattr(element, "attrib"):
        for _name in sorted(element.attrib.keys()):
            _attrib_value = element.attrib[_name]
            pipe += (_name, _attrib_value,)
            
    if element.text is not None:
        pipe += (element.text.strip(), )
    
    if element.tail is not None:
        pipe += (element.tail.strip(), )
            
    return pipe
            
def getChildren2(xml, element, pipe, pathes, hashes):
    
    pipe = updatePipe(pipe, element)
       
    _hash = hashlib.sha1()
    _hash.update(str(pipe).encode('utf-8'))
    _path = xml.getpath(element)
    pathes[_path] = _hash
    hashes[_hash.hexdigest()] = _path
    
    for _child in element.getchildren():
        getChildren2(xml, _child, pipe,  pathes, hashes)
              
_pathes1 = {}
_hashes1 = {}
_pipe = ()
getChildren2(_xml1, _root1, _pipe, _pathes1, _hashes1)

_pathes2 = {}
_hashes2 = {}
_pipe = ()
getChildren2(_xml2, _root2, _pipe, _pathes2, _hashes2)


def report(hashes1, hashes2):
    for _hash1 in hashes1.keys():
        _path1 = hashes1[_hash1]
        
        if _hash1 in hashes2.keys():
            _path2 = hashes2[_hash1]
            
            if _path1 == _path2:
                print('eleeme unchanged, element unchanged', _path1, _path2)
            else:
                print('path changed,   element unchanged', _path1, _path2)
        else:
            print('element changed                 ', _path1)
           
print('source -> target') 
report(_hashes1, _hashes2)

print('target -> source') 
report(_hashes2, _hashes1)
