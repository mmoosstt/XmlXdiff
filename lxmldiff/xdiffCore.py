import lxmldiff
import lxml.etree
import hashlib
import xml.etree

xml.etree

_path1 = "{}\\tests\\test1\\a.xml".format(lxmldiff.getPath())
_path2 =  "{}\\tests\\test1\\b.xml".format(lxmldiff.getPath())

_xml1 = lxml.etree.parse(_path1)
_xml2 = lxml.etree.parse(_path2)

_root1 = _xml1.getroot()
_root2 = _xml2.getroot()


def customElementHash(element, hashpipe):
  
    hashpipe.update(bytes(str(element.tag), 'utf-8'))
    
    if hasattr(element, "attrib"):
        for _name in sorted(element.attrib.keys()):
            _attrib_value = element.attrib[_name]
            hashpipe.update(bytes(_name + _attrib_value, 'utf-8'))
            
    if element.text is not None:
        hashpipe.update(bytes(element.text.strip(),'utf-8'))
    
    if element.tail is not None:
        hashpipe.update(bytes(element.tail.strip(), 'utf-8'))
            
    for child in element.getchildren():
        hashpipe.update(customElementHash(child, hashpipe))
        
        
    return bytes(hashpipe.hexdigest(), 'utf-8')
        


def getChildren(xml, element, pathes, hashes):
    
    _hash = hashlib.sha1()
    _hash.update(lxml.etree.tostring(element))
    _path = xml.getpath(element)
    pathes[_path] = _hash
    hashes[_hash.hexdigest()] = _path
    
    for _child in element.getchildren():
        getChildren(xml, _child, pathes, hashes)
        

           
def getChildren2(xml, element, pathes, hashes):
    
    _hash = hashlib.sha1()
    customElementHash(element, _hash)
    _path = xml.getpath(element)
    pathes[_path] = _hash.hexdigest()
    hashes[_hash.hexdigest()] = _path
    
    
    for _child in element.getchildren():
        getChildren2(xml, _child, pathes, hashes)
              
_pathes1 = {}
_hashes1 = {}
_pipe = ()
getChildren2(_xml1, _root1,  _pathes1, _hashes1)

_pathes2 = {}
_hashes2 = {}
_pipe = ()
getChildren2(_xml2, _root2,  _pathes2, _hashes2)


def report(hashes1, hashes2):
    for _hash1 in hashes1.keys():
        _path1 = hashes1[_hash1]
        
        if _hash1 in hashes2.keys():
            _path2 = hashes2[_hash1]
            
            if _path1 == _path2:
                print('element unchanged, element unchanged', _path1, _path2)
            else:
                print('path      changed,   element unchanged', _path1, _path2)
        else:
            print('element   changed,                    ', _path1)
           
print('source -> target') 
report(_hashes1, _hashes2)

print('target -> source') 
report(_hashes2, _hashes1)




