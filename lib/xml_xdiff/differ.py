"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: calculate difference between source and target file (inspired from xdiff algorithm)
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD

"""

import os
import copy
import lxml.etree
from xml_xdiff import base, xpath, hash, get_path


class XDiffPath:
    '''
    Interface for file names
    '''

    def __init__(self, filepath):
        _x = os.path.abspath(filepath).replace("\\", "/")

        self.path = _x[:_x.rfind("/")].replace("/", "\\")
        self.filename = _x[_x.rfind("/") + 1:_x.rfind('.')]
        self.fileending = _x[_x.rfind('.') + 1:]
        self.filepath = _x.replace("/", "\\")


class XDiffExecutor:
    '''
    This is the heart and entry point of XmlXdiff. The orchestration of looping, hashing and
    comparing.
    '''

    def __init__(self):
        self.path1 = XDiffPath(
            '{}\\..\\..\\tests\\test1\\a.xml'.format(get_path()))
        self.path2 = XDiffPath(
            '{}\\..\\..\\tests\\test1\\b.xml'.format(get_path()))

        # initialised when execute is executed
        self.gravity = 0
        self.path1 = None
        self.path2 = None
        self.xml1 = None
        self.xml2 = None
        self.root1 = None
        self.root2 = None
        self.xelements1 = None
        self.xelements2 = None

    def setGravity(self, inp):
        '''
        Interface setter for gravity - unused till now.
        replaced by parent indentification

        :param inp: int
        '''

        self.gravity = inp

    def getGravity(self):
        '''
        Interface getter for gravity.
        '''
        return copy.deepcopy(self.gravity)

    def setLeftPath(self, path):
        '''
        Interface setter for path1 - normal the left/elder side

        :param path: str - path not checked for validity till now
        '''
        self.path1 = XDiffPath(path)

    def setRightPath(self, path):
        '''
        Interface setter for path2 - normal the right/latest side

        :param path: str - path not checked for validity till now
        '''
        self.path2 = XDiffPath(path)

    def execute(self):
        '''
        Entry point for differ.
        '''

        self.xml1 = lxml.etree.parse(self.path1.filepath)
        self.xml2 = lxml.etree.parse(self.path2.filepath)

        self.root1 = self.xml1.getroot()
        self.root2 = self.xml2.getroot()

        _xpath = xpath.XDiffXmlPath()

        self.xelements1 = _xpath.getXelements(self.root1, "", 1)
        self.xelements2 = _xpath.getXelements(self.root2, "", 1)

        _child_cnts = {}
        _ = [_child_cnts.update({_e.child_cnt: None})
             for _e in self.xelements1]
        _ = [_child_cnts.update({_e.child_cnt: None})
             for _e in self.xelements2]

        for _child_cnt in reversed(sorted(_child_cnts.keys())):

            self.findUnchangedElementsWithChildren(_child_cnt,
                                                   self.xelements1,
                                                   self.xelements2)

            self.findMovedElementsWithChildren(_child_cnt,
                                               self.xelements1,
                                               self.xelements2)

            self.findMovedParentElements(_child_cnt,
                                         self.xelements1,
                                         self.xelements2)

    def _calculateHashes(self,
                         xelements,
                         callback,
                         child_cnt=None,
                         children=True,
                         xtypes=(base.ElementChanged, base.ElementUnknown)):

        pass

    def _generatorXElements(self,
                            xelements,
                            hash_algorithm=hash.XDiffHasher.callbackHashAll,
                            child_cnt=None,
                            children=True,
                            xtypes=(base.ElementChanged, base.ElementUnknown)):

        if child_cnt is None:
            _xelements_gen = base.generator_xtypes(xelements,
                                                  *xtypes)

        else:
            _xelements_gen = base.generator_child_count(xelements,
                                                      child_cnt,
                                                      *xtypes)

        hash.XDiffHasher.getHashes(_xelements_gen, hash_algorithm, children)

        if child_cnt is None:
            _generator = base.generator_xtypes(xelements, *xtypes)

        else:
            _generator = base.generator_child_count(
                xelements, child_cnt, *xtypes)

        return _generator

    def setElementTypeWithChildren(self, xelement1, xelement2, xtype):
        '''
        Set element type of child elements

        :param xelement1: [XElement, XElement, ..]
        :param xelement2: [XElement, XElement, ..]
        :param xtype: XType
        '''

        _xelements1 = base.generator_child_elements(self.xelements1,
                                                  xelement1)

        _xelements2 = base.generator_child_elements(self.xelements2,
                                                  xelement2)

        for _xelement1 in _xelements1:
            _xelement2 = next(_xelements2)

            if (isinstance(_xelement1.type, base.ElementUnknown) and
                    isinstance(_xelement2.type, base.ElementUnknown)):

                _xelement1.set_type(xtype)
                _xelement2.set_type(xtype)
                _xelement1.add_xelement(_xelement2)
                _xelement2.add_xelement(_xelement1)

    def findMovedParentElements(self, child_cnt, xelements1, xelements2):
        '''
        Entry point of pseudo recursive execution

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)
        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=hash.XDiffHasher.callbackHashAll,
                                                         children=False,
                                                         child_cnt=child_cnt,
                                                         xtypes=_xtypes)

        for _xelement2 in _xelements2_generator:
            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=hash.XDiffHasher.callbackHashAll,
                                                             children=False,
                                                             xtypes=_xtypes)

            for _xelement1 in _xelements1_generator:
                if _xelement1.hash == _xelement2.hash:

                    _xelement1.set_type(base.ElementMovedParent)
                    _xelement2.set_type(base.ElementMovedParent)
                    _xelement1.add_xelement(_xelement2)
                    _xelement2.add_xelement(_xelement1)

                    _xelements1 = base.array_child_elements(xelements1,
                                                          _xelement1)

                    _xelements2 = base.array_child_elements(xelements2,
                                                          _xelement2)

                    _child_cnts = {}
                    _ = [_child_cnts.update({_e.child_cnt: None})
                         for _e in _xelements1]
                    _ = [_child_cnts.update({_e.child_cnt: None})
                         for _e in _xelements2]

                    for _child_cnt in reversed(sorted(_child_cnts.keys())):

                        self.findUnchangedElementsWithChildren(_child_cnt,
                                                               _xelements1,
                                                               _xelements2)

                        self.findMovedElementsWithChildren(_child_cnt,
                                                           _xelements1,
                                                           _xelements2)

                        # recursive entry point
                        self.findMovedParentElements(_child_cnt,
                                                     _xelements1,
                                                     _xelements2)

                        self.findTagNameAttributeNameValueConsitencyWithChildren(_child_cnt,
                                                                                 _xelements1,
                                                                                 _xelements2)

                        self.findAttributeValueElementValueConsitencyWithChildren(_child_cnt,
                                                                                  _xelements1,
                                                                                  _xelements2)

                        self.findTagNameAttributeNameConsitencyWithChildren(_child_cnt,
                                                                            _xelements1,
                                                                            _xelements2)

                        self.findTagNameConsitencyWithChildren(_child_cnt,
                                                               _xelements1,
                                                               _xelements2)

                    for _e in _xelements1:
                        if isinstance(_e.type, base.ElementUnknown):
                            _e.set_type(base.ElementDeleted)

                    for _e in _xelements2:
                        if isinstance(_e.type, base.ElementUnknown):
                            _e.set_type(base.ElementAdded)

                    break

    def findTagNameConsitencyWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=hash.XDiffHasher.callbackHashTagNameConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=hash.XDiffHasher.callbackHashTagNameConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)
            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    base.ElementTagConsitency)

                    break

    def findAttributeValueElementValueConsitencyWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=hash.XDiffHasher.callbackHashAttributeValueElementValueConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=hash.XDiffHasher.callbackHashAttributeValueElementValueConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    base.ElementTextAttributeValueConsitency)

                    break

    def findTagNameAttributeNameValueConsitencyWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=hash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=hash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    base.ElementTagAttributeNameValueConsitency)

                    break

    def findTagNameAttributeNameConsitencyWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=hash.XDiffHasher.callbackHashTagNameAttributeNameConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=hash.XDiffHasher.callbackHashTagNameAttributeNameConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    base.ElementTagAttributeNameConsitency)

                    break

    def findMovedElementsWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:
                    if not _xelement1.xpath == _xelement2.xpath:

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        base.ElementMoved)
                        break

    def findUnchangedElementsWithChildren(self, child_cnt, xelements1, xelements2):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param xelements1: [XElement, XElement, ...]
        :param xelements2: [XElement, XElement, ...]
        '''

        _xtypes = (base.ElementChanged, base.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if _xelement1.hash == _xelement2.hash:
                    if _xelement1.xpath == _xelement2.xpath:

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        base.ElementUnchanged)

                        break
