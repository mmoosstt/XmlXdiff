import lxmldiff
import lxml.etree
import hashlib


class xDiff(object):

    @classmethod
    def callbackHashAll(cls, element, hashpipe):
      
        hashpipe.update(bytes(str(element.tag)  + "#tag", 'utf-8'))
        
        if hasattr(element, "attrib"):
            for _name in sorted(element.attrib.keys()):
                _attrib_value = element.attrib[_name]
                hashpipe.update(bytes(_name + _attrib_value + "#att", 'utf-8'))
                
        if element.text is not None:
            hashpipe.update(bytes(element.text.strip() + "#txt",'utf-8'))
        
        if element.tail is not None:
            hashpipe.update(bytes(element.tail.strip() + "#txt", 'utf-8'))
                
        for child in element.getchildren():
            hashpipe.update(cls.callbackHashAll(child, hashpipe))
            
            
        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashValueConsitency(cls, element, hashpipe):
             
        if hasattr(element, "attrib"):
            for _name in sorted(element.attrib.keys()):
                _attrib_value = element.attrib[_name]
                hashpipe.update(bytes(_attrib_value + "#att", 'utf-8'))
                
        if element.text is not None:
            hashpipe.update(bytes(element.text.strip() + "#txt",'utf-8'))
        
        if element.tail is not None:
            hashpipe.update(bytes(element.tail.strip() + "#txt", 'utf-8'))
                
        for child in element.getchildren():
            hashpipe.update(cls.callbackHashAll(child, hashpipe))
            
            
        return bytes(hashpipe.hexdigest(), 'utf-8')
    
    @classmethod
    def callbackHashGrammerConsitency(cls, element, hashpipe):
        # check path consentiently  and attribute consentiently
        
        hashpipe.update(bytes(str(element.tag) + "#tag", 'utf-8'))
        
        if hasattr(element, "attrib"):
            for _name in sorted(element.attrib.keys()):
                hashpipe.update(bytes(_name + "#tag", 'utf-8'))
                
                
        for child in element.getchildren():
            hashpipe.update(cls.callbackHashGrammerConsitency(child, hashpipe))
            
            
        return bytes(hashpipe.hexdigest(), 'utf-8')
        

    @classmethod
    def getHashesElementBased(cls, xml, element, hashes, pathes):
        
        _hash = hashlib.sha1()
        _hash.update(lxml.etree.tostring(element))
        _path = xml.getpath(element)
        pathes[_path] = _hash
        hashes[_hash.hexdigest()] = _path
        
        for _child in element.getchildren():
            cls.getHashesElementBased(xml, _child, hashes, pathes)
        


    @classmethod           
    def getHashesElementBasedCustomised(cls, xml, element, hashes, pathes, callbackHashCalculation):
        
        _hash = hashlib.sha1()
        callbackHashCalculation(element, _hash)
        _path = xml.getpath(element)
        
        pathes[_path] = _hash.hexdigest()
        
        if _hash.hexdigest() not in hashes.keys():
            hashes[_hash.hexdigest()] = [_path]
        else:
            hashes[_hash.hexdigest()].append(_path)
        
        
        for _child in element.getchildren():
            cls.getHashesElementBasedCustomised(xml, _child, hashes, pathes, callbackHashCalculation)
            
class xDiffExecutor(object):
      
    def __init__(self):
        self.path1 = "{}\\tests\\test1\\a.xml".format(lxmldiff.getPath())
        self.path2 =  "{}\\tests\\test1\\b.xml".format(lxmldiff.getPath())

    def run(self):
        self.xml1 = lxml.etree.parse(self.path1)
        self.xml2 = lxml.etree.parse(self.path2)

        self.root1 = self.xml1.getroot()
        self.root2 = self.xml2.getroot()

        self.hashes1 = {}
        self.hashes2 = {}

        self.pathes1 = {}
        self.pathes2 = {}
                
        xDiff.getHashesElementBasedCustomised(self.xml1, self.root1,  self.hashes1, self.pathes1, xDiff.callbackHashAll)
        xDiff.getHashesElementBasedCustomised(self.xml2, self.root2,  self.hashes2, self.pathes2, xDiff.callbackHashAll)
        
        self.changed_pathes1 = []
        self.changed_pathes2 = []
        self.findChangedElements()
        
        self.moved_pathes = []
        self.findMovedElements()
        self.findChangedValues()
        self.findChangedGrammer()
        self.added_deleted_pathes = []
        self.findAddedDeletedElements()
        
        x = 1

    def findAddedDeletedElements(self):
        
        for _path1 in self.changed_pathes1:
            if _path1 not in self.pathes2.keys():
                self.added_deleted_pathes.append(_path1)
                self.changed_pathes1[self.changed_pathes1.index(_path1)] = None
                print("deleted", _path1)
                
        for _path2 in self.changed_pathes2:
            if _path2 not in self.pathes1.keys():
                self.added_deleted_pathes.append(_path2)
                self.changed_pathes2[self.changed_pathes2.index(_path2)] = None 
                print("added", _path2)                   

        for _path1 in self.changed_pathes1:
            if _path1 in self.changed_pathes2 and _path1 is not None:
                self.changed_pathes1[self.changed_pathes1.index(_path1)] = None
                self.changed_pathes2[self.changed_pathes2.index(_path1)] = None
                
                print("sub nodes changed", _path1)

        for _path2 in self.changed_pathes2:
            if _path2 in self.changed_pathes1 and _path2 is not None:
                self.changed_pathes1[self.changed_pathes1.index(_path2)] = None
                self.changed_pathes2[self.changed_pathes2.index(_path2)] = None
                
                print("sub nodes changed", _path1)

        self.changed_pathes1 = [x for x in self.changed_pathes1 if x is not None]
        self.changed_pathes2 = [x for x in self.changed_pathes2 if x is not None]
        
        for _path in self.changed_pathes1 + self.changed_pathes2:
            print("unknown {}".format(_path))
            
                            
    def findChangedGrammer(self):

        _hashes1 = {}
        _pathes1 = {}
        for _path1 in self.changed_pathes1:

            _element1 = self.root1.xpath(_path1).pop()
            xDiff.getHashesElementBasedCustomised(self.xml1,  _element1, _hashes1, _pathes1, xDiff.callbackHashValueConsitency)
            

        _hashes2 = {}
        _pathes2 = {}
        for _path2 in self.changed_pathes2:

            _element2 = self.root2.xpath(_path2).pop()
            xDiff.getHashesElementBasedCustomised(self.xml2,   _element2, _hashes2, _pathes2, xDiff.callbackHashValueConsitency)
                        
            _hash1 = self.pathes1[_path1]
            
            
        for _hash1 in _hashes1.keys():
            _pathes1 = _hashes1[_hash1]
            
            if _hash1 in _hashes2.keys():
                _pathes2 = _hashes2[_hash1]
                
                for _path1 in _pathes1:
                    if _pathes2:
                        _path2 = _pathes2.pop()
                        
                        if (_path1 in self.changed_pathes1 and
                            _path2 in self.changed_pathes2):
                        
                            self.changed_pathes1.remove(_path1)
                            self.changed_pathes2.remove(_path2)
                            
                            print(lxml.etree.tostring(self.root1.xpath(_path1).pop()))
                            print(lxml.etree.tostring(self.root2.xpath(_path2).pop()))
                            
                            print("grammer changed {}, {}".format(_path1, _path2))
                              
    def findChangedValues(self):

        _hashes1 = {}
        _pathes1 = {}
        for _path1 in self.changed_pathes1:

            _element1 = self.root1.xpath(_path1).pop()
            xDiff.getHashesElementBasedCustomised(self.xml1,  _element1, _hashes1, _pathes1, xDiff.callbackHashGrammerConsitency)
            

        _hashes2 = {}
        _pathes2 = {}
        for _path2 in self.changed_pathes2:

            _element2 = self.root2.xpath(_path2).pop()
            xDiff.getHashesElementBasedCustomised(self.xml2,   _element2, _hashes2, _pathes2, xDiff.callbackHashGrammerConsitency)
                        
            _hash1 = self.pathes1[_path1]
            
            
        for _hash1 in _hashes1.keys():
            _pathes1 = _hashes1[_hash1]
            
            if _hash1 in _hashes2.keys():
                _pathes2 = _hashes2[_hash1]
                
                for _path1 in _pathes1:
                    if _pathes2:
                        _path2 = _pathes2.pop()
                        
                        if (_path1 in self.changed_pathes1 and
                            _path2 in self.changed_pathes2):
                        
                            self.changed_pathes1.remove(_path1)
                            self.changed_pathes2.remove(_path2)
                            
                            print(lxml.etree.tostring(self.root1.xpath(_path1).pop()))
                            print(lxml.etree.tostring(self.root2.xpath(_path2).pop()))
                            
                            print("value changed {}, {}".format(_path1, _path2))
        
        
    def findMovedElements(self):
        
        _hashes1 = {}
        for _path1 in self.changed_pathes1:
            _hash1 = self.pathes1[_path1]
            
            if _hash1 in _hashes1.keys():
                _hashes1[_hash1].append(_path1)
            else:
                _hashes1[_hash1] = [_path1]
            
        _hashes2 = {}
        for _path2 in self.changed_pathes2:
            _hash2 = self.pathes2[_path2]
            
            if _hash2 in _hashes2.keys():
                _hashes2[_hash2].append(_path2)
            else:
                _hashes2[_hash2] = [_path2]
            
        for _path1 in sorted(self.changed_pathes1):
            
            _hash1 = self.pathes1[_path1]
            
            if _hash1 in _hashes2.keys():
                _pathes1 = _hashes1[_hash1]
                _pathes2 = _hashes2[_hash1]
                
                for _path1 in _pathes1:
                    
                    if _pathes2:
                        _path2 = _pathes2.pop()
                    
                        print("moved {} -> {}".format(_path1, _path2))
                        
                        self.moved_pathes.append(_path1)
                        self.moved_pathes.append(_path2)
                
                        self.changed_pathes1[self.changed_pathes1.index(_path1)] = None
                        self.changed_pathes2[self.changed_pathes2.index(_path2)] = None
                        
     
        self.changed_pathes1 = [x for x in self.changed_pathes1 if x is not None]
        self.changed_pathes2 = [x for x in self.changed_pathes2 if x is not None]
        
    def findChangedElements(self):
        
        for _hash1 in self.hashes1.keys():
            _pathes1 = self.hashes1[_hash1]

            if _hash1 in self.hashes2.keys():
                _pathes2 = self.hashes2[_hash1]
                
                for _path1 in _pathes1:
                    if _path1 not in _pathes2:
                        self.changed_pathes1.append(_path1)
            else:
                for _path1 in _pathes1:
                    self.changed_pathes1.append(_path1)
                        
        for _hash2 in self.hashes2.keys():
            _pathes2 = self.hashes2[_hash2]

            if _hash2 in self.hashes1.keys():
                _pathes1 = self.hashes1[_hash2]
                
                for _path2 in _pathes2:
                    if _path2 not in _pathes1:
                        self.changed_pathes2.append(_path2)
            else:
                for _path2 in _pathes2:
                    self.changed_pathes2.append(_path2)
    
    





if __name__ == "__main__":
    _x = xDiffExecutor()
    _x.run()
    