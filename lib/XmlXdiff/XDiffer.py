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

        self.findUnchangedElements(self.xelements1, self.xelements2)
        self.findMovedElements(self.xelements1, self.xelements2)

        for _xelements1, _xelements2 in XTypes.LOOP_UNCHANGED_SEGMENTS(self.xelements1,
                                                                       self.xelements2):

            _child_cnts = {}
            _ = [_child_cnts.update({_e.child_cnt: None})
                 for _e in _xelements1]
            _ = [_child_cnts.update({_e.child_cnt: None})
                 for _e in _xelements2]

            for _child_cnt in reversed(sorted(_child_cnts.keys())):
                self.findTagNameAttributeNameValueConsitency(
                    _child_cnt, _xelements1, _xelements2)

                self.findAttributeValueElementValueConsitency(
                    _child_cnt, _xelements1, _xelements2)

                self.findTagNameAttributeNameConsitency(
                    _child_cnt,  _xelements1, _xelements2)

                self.findTagNameConsitency(
                    _child_cnt,  _xelements1, _xelements2)

        #.findUnchangedElements(1)
        # self.findChangedElements(1)

        # self.findTagNameAttributeNameValueConsitency(1)
        # self.findAttributeValueElementValueConsitency(1)
        # self.findTagNameAttributeNameConsitency(1)
        # self.findTagNameConsitency(1)

        # self.verifyChangedElements(self.xelements1)
        # self.verifyChangedElements(self.xelements2)

        # for _e in XTypes.LOOP(
        #        self.xelements1, XTypes.ElementUnknown):
        #    _e.setType(XTypes.ElementDeleted)

        # for _e in XTypes.LOOP(
        #        self.xelements2, XTypes.ElementUnknown):
        #    _e.setType(XTypes.ElementAdded)

    def verifyChangedElements(self, xelements):

        # find all changed elements
        _changed_elements = []
        for _xelement in XTypes.LOOP(xelements, XTypes.ElementChanged):
            _changed_elements.append(
                (len(_xelement.xpath), _xelement.xpath, xelements.index(_xelement)))

        # get most nested changed element first
        for _, _path, _index in reversed(sorted(_changed_elements)):

            _verified = False
            for _xelement in xelements[_index + 1:]:

                if _xelement.xpath.find(_path) == 0:

                    if isinstance(_xelement.type, XTypes.ElementChanged):
                        _verified = False
                        break

                    else:
                        _verified = True

                else:
                    break

            if _verified:
                xelements[_index].setType(XTypes.ElementVerified)

    def setChildrenAndElementType(self, xelement1, xelement2, xtype):

        _xelements1 = XTypes.LOOP_CHILD_ELEMENTS(self.xelements1, xelement1)
        _xelements2 = XTypes.LOOP_CHILD_ELEMENTS(self.xelements2, xelement2)

        for _xelement1 in _xelements1:
            _xelement2 = next(_xelements2)
            _xelement1.setType(xtype)
            _xelement2.setType(xtype)
            _xelement1.addXelement(_xelement2)
            _xelement2.addXelement(_xelement1)

    def setElementType(self, xelement1, xelement2, xtype):

        xelement1.setType(xtype)
        xelement2.setType(xtype)
        xelement1.addXelement(xelement2)
        xelement2.addXelement(xelement1)

    def findTagNameConsitency(self, child_cnt, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP_CHILD_CNT(
                xelements1,  child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP_CHILD_CNT(
                xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashTagNameConsitency)

        for _xelement2 in XTypes.LOOP_CHILD_CNT(xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_CHILD_CNT(xelements1, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):

                    self.setChildrenAndElementType(_xelement1,
                                                   _xelement2,
                                                   XTypes.ElementTagConsitency)

                    break

    def findAttributeValueElementValueConsitency(self, child_cnt, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP_CHILD_CNT(
                xelements1,  child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP_CHILD_CNT(
                xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        for _xelement2 in XTypes.LOOP_CHILD_CNT(xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_CHILD_CNT(xelements1, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):

                    self.setChildrenAndElementType(_xelement1,
                                                   _xelement2,
                                                   XTypes.ElementTextAttributeValueConsitency)

                    break

    def findTagNameAttributeNameValueConsitency(self, child_cnt, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP_CHILD_CNT(
                xelements1,  child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP_CHILD_CNT(
                xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency)

        for _xelement2 in XTypes.LOOP_CHILD_CNT(
                xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_CHILD_CNT(
                    xelements1, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):

                    self.setChildrenAndElementType(_xelement1,
                                                   _xelement2,
                                                   XTypes.ElementTagAttributeNameValueConsitency)

                    break

    def findTagNameAttributeNameConsitency(self, child_cnt, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP_CHILD_CNT(
                xelements1,  child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP_CHILD_CNT(
                xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        for _xelement2 in XTypes.LOOP_CHILD_CNT(xelements2, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_CHILD_CNT(xelements1, child_cnt, XTypes.ElementChanged, XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):

                    self.setChildrenAndElementType(_xelement1,
                                                   _xelement2,
                                                   XTypes.ElementTagAttributeNameConsitency)

                    break

    def findMovedElementsChildCnt(self, child_cnt, xelements1, xelements2):

        def _getHash(callback):

            _elements1 = XTypes.LOOP_CHILD_CNT(xelements1,
                                               child_cnt,
                                               XTypes.ElementChanged,
                                               XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP_CHILD_CNT(xelements2,
                                               child_cnt,
                                               XTypes.ElementChanged,
                                               XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashAll)

        for _xelement2 in XTypes.LOOP_CHILD_CNT(xelements2,
                                                child_cnt,
                                                XTypes.ElementChanged,
                                                XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_CHILD_CNT(xelements1,
                                                    child_cnt,
                                                    XTypes.ElementChanged,
                                                    XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    if not(_xelement1.xpath == _xelement2.xpath):

                        self.setChildrenAndElementType(_xelement1,
                                                       _xelement2,
                                                       XTypes.ElementMoved)
                        break

    def findMovedElements(self, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP(xelements1,
                                     XTypes.ElementChanged,
                                     XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP(xelements2,
                                     XTypes.ElementChanged,
                                     XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashAll)

        for _xelement2 in XTypes.LOOP(xelements2,
                                      XTypes.ElementChanged,
                                      XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP(xelements1,
                                          XTypes.ElementChanged,
                                          XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    if not(_xelement1.xpath == _xelement2.xpath):

                        self.setChildrenAndElementType(_xelement1,
                                                       _xelement2,
                                                       XTypes.ElementMoved)
                        break

    def findUnchangedElements(self, xelements1, xelements2):

        def _getHash(callback):
            _elements1 = XTypes.LOOP(xelements1,
                                     XTypes.ElementChanged,
                                     XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements1, callback)

            _elements2 = XTypes.LOOP(xelements2,
                                     XTypes.ElementChanged,
                                     XTypes.ElementUnknown)

            XHash.XDiffHasher.getHashes(_elements2, callback)

        _getHash(XHash.XDiffHasher.callbackHashAll)

        for _xelement2 in XTypes.LOOP(xelements2,
                                      XTypes.ElementChanged,
                                      XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP(xelements1,
                                          XTypes.ElementChanged,
                                          XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    if(_xelement1.xpath == _xelement2.xpath):

                        self.setChildrenAndElementType(_xelement1,
                                                       _xelement2,
                                                       XTypes.ElementUnchanged)

                        break
