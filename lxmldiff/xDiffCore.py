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
    def getHashesElementBased(cls, xml, element, hashes):
        
        _hash = hashlib.sha1()
        _hash.update(lxml.etree.tostring(element))
        _path = xml.getpath(element)
        #pathes[_path] = _hash
        hashes[_hash.hexdigest()] = _path
        
        for _child in element.getchildren():
            cls.getHashesElementBased(xml, _child, hashes)
        


    @classmethod           
    def getHashesElementBasedCustomised(cls, xml, element, hashes, callbackHashCalculation):
        
        _hash = hashlib.sha1()
        callbackHashCalculation(element, _hash)
        _path = xml.getpath(element)
        
        #pathes[_path] = _hash.hexdigest()
        
        if _hash.hexdigest() not in hashes.keys():
            hashes[_hash.hexdigest()] = [_path]
        else:
            hashes[_hash.hexdigest()].append(_path)
        
        
        for _child in element.getchildren():
            cls.getHashesElementBasedCustomised(xml, _child, hashes, callbackHashCalculation)
            
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
        
        xDiff.getHashesElementBasedCustomised(self.xml1, self.root1,  self.hashes1, xDiff.callbackHashAll)
        xDiff.getHashesElementBasedCustomised(self.xml2, self.root2,  self.hashes2, xDiff.callbackHashAll)
        
        
        self.dev1()
        

    def dev1(self):
        for _hash1 in self.hashes1.keys():
            _pathes1 = self.hashes1[_hash1]
            
            if _hash1 in self.hashes2.keys():
                _pathes2 = self.hashes2[_hash1]          
                
                # remove equals
                for _path1 in _pathes1:
                    if _path1 in _pathes2:
                        _pathes2.remove(_path1)
                        _pathes1.remove(_path1)
                        
                        print('unchanged', _path1)
                        
                # moved couple
                for _path1 in _pathes1:
                    if _pathes2:
                        _moved_path2 = _pathes2[0]
                        _moved_path1 = _path1
                        
                        _pathes1.remove(_moved_path1)
                        _pathes2.remove(_moved_path2)
                        
                        print("moved {} -> {}".format(_moved_path1, _moved_path2))
                        
                # unmoved pathes
                for _path1 in _pathes1:
                    print("deleted dublicate {}".format(_path1))
                    
                # added pathes
                for _path2 in _pathes2:
                    print("copied {}".format(_path2))
                        
                        
            else:
                print("changed {}".format(_pathes1))
                   
                   
                   
                _element = self.root1.xpath(_pathes1[0])[0]
                _hashes1 = {}
                _hashes2 = {}
                xDiff.getHashesElementBasedCustomised(self.xml1, _element,  _hashes1, xDiff.callbackHashValueConsitency)
                xDiff.getHashesElementBasedCustomised(self.xml2, self.root2,  _hashes2, xDiff.callbackHashValueConsitency)
                print(_hashes1, _hashes2)
 
                _hashes1 = {}
                _hashes2 = {}
                xDiff.getHashesElementBasedCustomised(self.xml1, _element,  _hashes1, xDiff.callbackHashGrammerConsitency)
                xDiff.getHashesElementBasedCustomised(self.xml2, self.root2,  _hashes2, xDiff.callbackHashGrammerConsitency)
                print(_hashes1, _hashes2)
                        
            
            if 0:
            
                for _path1 in _pathes1:
                    if _hash1 in self.hashes2.keys():
                        _pathes2 = self.hashes2[_hash1]
                        
                        for _path2 in _pathes2:
                            if _path1 == _path2:
                                print('element unchanged, path unchanged', _path1, _path2)
                            else:
                                print('element unchanged, path   changed', _path1, _path2)
                    else:
                        print('element   changed,                    ', _path1)
           





if __name__ == "__main__":
    _x = xDiffExecutor()
    