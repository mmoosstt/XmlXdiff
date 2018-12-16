import XmlXdiff
import lxml.etree
import hashlib


class XDiffHasher(object):

    @classmethod
    def callbackHashAll(cls, element, hashpipe):

        _element_childes = element.getchildren()

        
        for child in _element_childes:
            hashpipe.update(cls.callbackHashAll(child, hashpipe))        

        
        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        
        # attributes and text are only taken into account for leaf nodes
        if not _element_childes:
            if hasattr(element, 'attrib'):
                for _name in sorted(element.attrib.keys()):
                    _attrib_value = element.attrib[_name]
                    hashpipe.update(bytes(_name + _attrib_value + '#att', 'utf-8'))

            if element.text is not None:
                hashpipe.update(bytes(element.text.strip() + '#txt', 'utf-8'))

            if element.tail is not None:
                hashpipe.update(bytes(element.tail.strip() + '#txt', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashAttributeValueElementValueConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(cls.callbackHashAll(child, hashpipe))        

        # attributes and text are only taken into account for leaf nodes
        if _element_childes:
            hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        else:
            if hasattr(element, 'attrib'):
                for _name in sorted(element.attrib.keys()):
                    _attrib_value = element.attrib[_name]
                    hashpipe.update(bytes(_attrib_value + '#att', 'utf-8'))

            if element.text is not None:
                hashpipe.update(bytes(element.text.strip() + '#txt', 'utf-8'))

            if element.tail is not None:
                hashpipe.update(bytes(element.tail.strip() + '#txt', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashTagNameAttributeNameConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(cls.callbackHashAll(child, hashpipe))        

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        # attributes and text are only taken into account for leaf nodes
        if not _element_childes:
            if hasattr(element, 'attrib'):
                for _name in sorted(element.attrib.keys()):
                    hashpipe.update(bytes(_name + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')
    
    @classmethod
    def callbackHashTagNameConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(cls.callbackHashAll(child, hashpipe))        

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')
    
    @classmethod
    def getHashesElementBased(cls, xml, element, hashes, pathes):

        _hash = hashlib.sha1()
        _hash.update(lxml.etree.tostring(element))
        _path = xml.getpath(element)
        pathes[_path] = [_hash.hexdigest(), 'ElementUnchanged']
        hashes[_hash.hexdigest()] = _path

        for _child in element.getchildren():
            cls.getHashesElementBased(xml, _child, hashes, pathes)

    @classmethod
    def getHashesElementBasedCustomised(cls, xml, element, hashes, pathes, callbackHashCalculation):

        _hash = hashlib.sha1()
        callbackHashCalculation(element, _hash)
        _path = xml.getpath(element)

        pathes[_path] = [_hash.hexdigest(), 'ElementUnchanged']

        if _hash.hexdigest() not in hashes.keys():
            hashes[_hash.hexdigest()] = [_path]
        else:
            hashes[_hash.hexdigest()].append(_path)
        for _child in element.getchildren():
            cls.getHashesElementBasedCustomised(xml, _child, hashes, pathes, callbackHashCalculation)


class XDiffExecutor(object):

    def __init__(self):
        self.path1 = '{}\\tests\\test1\\a.xml'.format(XmlXdiff.getPath())
        self.path2 = '{}\\tests\\test1\\b.xml'.format(XmlXdiff.getPath())

    def run(self):
        self.xml1 = lxml.etree.parse(self.path1)
        self.xml2 = lxml.etree.parse(self.path2)

        self.root1 = self.xml1.getroot()
        self.root2 = self.xml2.getroot()

        self.hashes1 = {}
        self.hashes2 = {}

        self.pathes1 = {}
        self.pathes2 = {}

        XDiffHasher.getHashesElementBasedCustomised(self.xml1, self.root1,  self.hashes1, self.pathes1, XDiffHasher.callbackHashAll)
        
        XDiffHasher.getHashesElementBasedCustomised(self.xml2, self.root2,  self.hashes2, self.pathes2, XDiffHasher.callbackHashAll)

        self._return = []

        self.findChangedElements()

        self.findMovedElements()

        self.findTagNameAttributeNameConsitency()

        self.findAttributeValueElementValueConsitency()
        
        self.findTagNameConsitency()

        self.findAddedDeletedElements()
        

    def getChangedPathes(self, pathes):
        _changed_pathes = []
        for _path in pathes:
            _hash, _state = pathes[_path]

            if _state == 'ElementChanged':
                _changed_pathes.append((_path, _hash, _state))

        return sorted(_changed_pathes)

    def findAddedDeletedElements(self):

        def checkNoChange(path, pathes, root, xml):

            _hash, _state = pathes[path]

            for _child in root.xpath(path)[0].getchildren():
                _child_path = xml.getpath(_child)

                _hash, _state = pathes[_child_path]

                if _state == 'ElementChanged':
                    _state = checkNoChange(_child_path, pathes, root, xml)

                    if _state == 'ElementChanged':
                        return _state

            return _state

        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            if _path1 not in self.pathes2.keys():
                self.pathes1[_path1][1] = 'ElementDeleted'
                print('ElementDeleted', _path1)
                self._return.append(('ElementDeleted', _path1, None))

        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            if _path2 not in self.pathes1.keys():
                self.pathes2[_path2][1] = 'ElementAdded'
                print('ElementAdded', _path2)
                self._return.append(('ElementDeleted', None, _path2))
                
        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            _state1 = checkNoChange(_path1, self.pathes1, self.root1, self.xml1)
            if _state1 != 'ElementChanged':
                self.pathes1[_path1][1] = 'ElementVerified'
                print('ElementVerified', _path1)
                self._return.append(('ElementVerified', None, _path2))

        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            _state2 = checkNoChange(_path2, self.pathes2, self.root2, self.xml2)
            if _state2 != 'ElementChanged':
                self.pathes2[_path2][1] = 'ElementVerified'
                print('ElementVerified', _path2)
                self._return.append(('ElementVerified', None, _path2))

        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            print('ElementUnknown {}'.format(_path1))
            self._return.append(('ElementUnknown', _path1, None))

        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            print('ElementUnknown {}'.format(_path2))
            self._return.append(('ElementUnknown', None, _path2))

    def findTagNameConsitency(self):

        _hashes1 = {}
        _pathes1 = {}
        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            _element1 = self.root1.xpath(_path1)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml1,  _element1, _hashes1, _pathes1, XDiffHasher.callbackHashTagNameConsitency)

        _hashes2 = {}
        _pathes2 = {}
        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            _element2 = self.root2.xpath(_path2)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml2,   _element2, _hashes2, _pathes2, XDiffHasher.callbackHashTagNameConsitency)

        for _hash1 in _hashes1.keys():

            if _hash1 in _hashes2.keys():
                _pathes1 = sorted(_hashes1[_hash1])
                _pathes2 = sorted(_hashes2[_hash1])

                for _path1 in _pathes1:
                    if _pathes2:
                        _path2 = _pathes2[0]
                        _pathes2 = _pathes2[1:]

                        if (self.pathes1[_path1][1] == 'ElementChanged' and
                                self.pathes2[_path2][1] == 'ElementChanged'):

                            self.pathes1[_path1][1] = 'ElementNameConsitency'
                            self.pathes2[_path2][1] = 'ElementTagConsitency'

                            print('ElementTagConsitency {}, {}'.format(_path1, _path2))
                            self._return.append(('ElementTagConsitency', _path1, _path2))
                            
    def findAttributeValueElementValueConsitency(self):

        _hashes1 = {}
        _pathes1 = {}
        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            _element1 = self.root1.xpath(_path1)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml1,  _element1, _hashes1, _pathes1, XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        _hashes2 = {}
        _pathes2 = {}
        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            _element2 = self.root2.xpath(_path2)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml2,   _element2, _hashes2, _pathes2, XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        for _hash1 in _hashes1.keys():

            if _hash1 in _hashes2.keys():
                _pathes1 = sorted(_hashes1[_hash1])
                _pathes2 = sorted(_hashes2[_hash1])

                for _path1 in _pathes1:
                    if _pathes2:
                        _path2 = _pathes2[0]
                        _pathes2 = _pathes2[1:]

                        if (self.pathes1[_path1][1] == 'ElementChanged' and
                                self.pathes2[_path2][1] == 'ElementChanged'):

                            self.pathes1[_path1][1] = 'ElementTextAttributeValueConsitency'
                            self.pathes2[_path2][1] = 'ElementTextAttributeValueConsitency'

                            print('ElementTextAttributeValueConsitency {}, {}'.format(_path1, _path2))
                            self._return.append(('ElementTextAttributeValueConsitency', _path1, _path2))

    def findTagNameAttributeNameConsitency(self):

        _hashes1 = {}
        _pathes1 = {}
        for _path1, _, _ in self.getChangedPathes(self.pathes1):
            _element1 = self.root1.xpath(_path1)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml1,  _element1, _hashes1, _pathes1, XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        _hashes2 = {}
        _pathes2 = {}
        for _path2, _, _ in self.getChangedPathes(self.pathes2):
            _element2 = self.root2.xpath(_path2)[0]
            XDiffHasher.getHashesElementBasedCustomised(self.xml2,   _element2, _hashes2, _pathes2, XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        for _hash1 in _hashes1.keys():
            _pathes1 = iter(sorted(_hashes1[_hash1]))

            if _hash1 in _hashes2.keys():
                _pathes2 = sorted(_hashes2[_hash1])

                for _path1 in _pathes1:
                    if _pathes2:
                        _path2 = _pathes2[0]
                        _pathes2 = _pathes2[1:]

                        if (self.pathes1[_path1][1] == 'ElementChanged' and
                                self.pathes2[_path2][1] == 'ElementChanged'):

                            self.pathes1[_path1][1] = 'ElementTagAttributeNameConsitency'
                            self.pathes2[_path2][1] = 'ElementTagAttributeNameConsitency'

                            print('ElementTagAttributeNameConsitency {}, {}'.format(_path1, _path2))
                            self._return.append(('ElementTagAttributeNameConsitency', _path1, _path2))
                                
    def findMovedElements(self):

        _hashes1 = {}
        for _path1, _hash1, _state1 in self.getChangedPathes(self.pathes1):

            if _hash1 in _hashes1.keys():
                _hashes1[_hash1].append(_path1)
            else:
                _hashes1[_hash1] = [_path1]

        _hashes2 = {}
        for _path2, _hash2, _state2 in self.getChangedPathes(self.pathes2):

            if _hash2 in _hashes2.keys():
                _hashes2[_hash2].append(_path2)
            else:
                _hashes2[_hash2] = [_path2]

        for _hash1 in _hashes1.keys():

            if _hash1 in _hashes2.keys():
                _pathes1 = sorted(_hashes1[_hash1])
                _pathes2 = sorted(_hashes2[_hash1])

                for _path1 in _pathes1:

                    if _pathes2:
                        _path2 = _pathes2[0]
                        _pathes2 = _pathes2[1:]

                        print('ElementMoved {} -> {}'.format(_path1, _path2))
                        self._return.append(('ElementMoved', _path1, _path2))

                        self.pathes1[_path1][1] = 'ElementMoved'
                        self.pathes2[_path2][1] = 'ElementMoved'

    def findChangedElements(self):

        for _hash1 in self.hashes1.keys():
            _pathes1 = self.hashes1[_hash1]

            if _hash1 in self.hashes2.keys():
                _pathes2 = self.hashes2[_hash1]

                for _path1 in _pathes1:
                    if _path1 not in _pathes2:
                        self.pathes1[_path1][1] = 'ElementChanged'
            else:
                for _path1 in _pathes1:
                    self.pathes1[_path1][1] = 'ElementChanged'

        for _hash2 in self.hashes2.keys():
            _pathes2 = self.hashes2[_hash2]

            if _hash2 in self.hashes1.keys():
                _pathes1 = self.hashes1[_hash2]

                for _path2 in _pathes2:
                    if _path2 not in _pathes1:
                        self.pathes2[_path2][1] = 'ElementChanged'
            else:
                for _path2 in _pathes2:
                    self.pathes2[_path2][1] = 'ElementChanged'


if __name__ == '__main__':
    _x = XDiffExecutor()
    _x.run()
