# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: calculate difference between source and target file (inspired from xdiff algorithm)
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

from XmlXdiff import XTypes, XPath, XHash, getPath
import lxml.etree
import os
import copy


class XDiffPath(object):

    def __init__(self, filepath):
        _x = os.path.abspath(filepath).replace("\\", "/")

        self.path = _x[:_x.rfind("/")].replace("/", "\\")
        self.filename = _x[_x.rfind("/") + 1:_x.rfind('.')]
        self.fileending = _x[_x.rfind('.') + 1:]
        self.filepath = _x.replace("/", "\\")


class XDiffExecutor(object):

    def __init__(self):
        self.path1 = XDiffPath('{}\\tests\\test1\\a.xml'.format(getPath()))
        self.path2 = XDiffPath('{}\\tests\\test1\\b.xml'.format(getPath()))
        self.setGravity(0)

    def setGravity(self, inp):
        self.gravity = inp

    def getGravity(self):
        return copy.deepcopy(self.gravity)

    def setPath1(self, path):
        self.path1 = XDiffPath(path)

    def setPath2(self, path):
        self.path2 = XDiffPath(path)

    def run(self):
        self.xml1 = lxml.etree.parse(self.path1.filepath)
        self.xml2 = lxml.etree.parse(self.path2.filepath)

        self.root1 = self.xml1.getroot()
        self.root2 = self.xml2.getroot()

        _xpath = XPath.XDiffXmlPath()

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

            self.findMovedElementsWithoutChildren(_child_cnt,
                                                  self.xelements1,
                                                  self.xelements2)

    def _calculateHashes(self, xelements, callback, child_cnt=None, children=True, xtypes=(XTypes.ElementChanged, XTypes.ElementUnknown)):

        if child_cnt is None:
            _xelements_gen = XTypes.LOOP(xelements,
                                         *xtypes)

        else:
            _xelements_gen = XTypes.LOOP_CHILD_CNT(xelements,
                                                   child_cnt,
                                                   *xtypes)

        XHash.XDiffHasher.getHashes(_xelements_gen, callback, children)

    def _generatorXElements(self, xelements, hash_algorithm=XHash.XDiffHasher.callbackHashAllNoChilds, child_cnt=None, children=True, xtypes=(XTypes.ElementChanged, XTypes.ElementUnknown)):

        self._calculateHashes(xelements, hash_algorithm,
                              child_cnt, children, xtypes)

        if child_cnt is None:
            _generator = XTypes.LOOP(xelements, *xtypes)

        else:
            _generator = XTypes.LOOP_CHILD_CNT(xelements, child_cnt, *xtypes)

        return _generator

    def setElementTypeWithChildren(self, xelement1, xelement2, xtype):

        _xelements1 = XTypes.LOOP_CHILD_ELEMENTS(self.xelements1,
                                                 xelement1)

        _xelements2 = XTypes.LOOP_CHILD_ELEMENTS(self.xelements2,
                                                 xelement2)

        for _xelement1 in _xelements1:
            _xelement2 = next(_xelements2)

            if (isinstance(_xelement1.type, XTypes.ElementUnknown) and
                    isinstance(_xelement2.type, XTypes.ElementUnknown)):

                _xelement1.setType(xtype)
                _xelement2.setType(xtype)
                _xelement1.addXelement(_xelement2)
                _xelement2.addXelement(_xelement1)

    def setElementType(self, xelement1, xelement2, xtype):

        xelement1.setType(xtype)
        xelement2.setType(xtype)
        xelement1.addXelement(xelement2)
        xelement2.addXelement(xelement1)

    def findMovedElementsWithoutChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)
        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=XHash.XDiffHasher.callbackHashAll,
                                                         children=False,
                                                         child_cnt=child_cnt,
                                                         xtypes=_xtypes)

        for _xelement2 in _xelements2_generator:
            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=XHash.XDiffHasher.callbackHashAll,
                                                             children=False,
                                                             xtypes=_xtypes)

            for _xelement1 in _xelements1_generator:
                if (_xelement1.hash == _xelement2.hash):

                    self.setElementType(_xelement1,
                                        _xelement2,
                                        XTypes.ElementTagRed)

                    _xelements1 = XTypes.CHILDS_ARRAY(xelements1,
                                                      _xelement1)

                    _xelements2 = XTypes.CHILDS_ARRAY(xelements2,
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

                        self.findMovedElementsWithoutChildren(_child_cnt,
                                                              _xelements1,
                                                              _xelements2)

                        self.findTagNameConsitencyWithChildren(_child_cnt,
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

                    for _e in _xelements1:
                        if isinstance(_e.type, XTypes.ElementUnknown):
                            _e.setType(XTypes.ElementDeleted)

                    for _e in _xelements2:
                        if isinstance(_e.type, XTypes.ElementUnknown):
                            _e.setType(XTypes.ElementAdded)

                    break

    def findTagNameConsitencyWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=XHash.XDiffHasher.callbackHashTagNameConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=XHash.XDiffHasher.callbackHashTagNameConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)
            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    XTypes.ElementTagConsitency)

                    break

    def findAttributeValueElementValueConsitencyWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    XTypes.ElementTextAttributeValueConsitency)

                    break

    def findTagNameAttributeNameValueConsitencyWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=XHash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=XHash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    XTypes.ElementTagAttributeNameValueConsitency)

                    break

    def findTagNameAttributeNameConsitencyWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         hash_algorithm=XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             hash_algorithm=XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):

                    self.setElementTypeWithChildren(_xelement1,
                                                    _xelement2,
                                                    XTypes.ElementTagAttributeNameConsitency)

                    break

    def findMovedElementsWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):
                    if not(_xelement1.xpath == _xelement2.xpath):

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        XTypes.ElementMoved)
                        break

    def findUnchangedElementsWithChildren(self, child_cnt, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):
                    if(_xelement1.xpath == _xelement2.xpath):

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        XTypes.ElementUnchanged)

                        break

    def findMovedElements(self, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):
                    if not(_xelement1.xpath == _xelement2.xpath):

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        XTypes.ElementMoved)
                        break

    def findUnchangedElements(self, xelements1, xelements2):

        _xtypes = (XTypes.ElementChanged, XTypes.ElementUnknown)

        _xelements2_generator = self._generatorXElements(xelements=xelements2,
                                                         xtypes=_xtypes)

        for _xelement2 in _xelements2_generator:

            _xelements1_generator = self._generatorXElements(xelements=xelements1,
                                                             xtypes=_xtypes)

            for _xelement1 in _xelements1_generator:

                if (_xelement1.hash == _xelement2.hash):
                    if(_xelement1.xpath == _xelement2.xpath):

                        self.setElementTypeWithChildren(_xelement1,
                                                        _xelement2,
                                                        XTypes.ElementUnchanged)

                        break
