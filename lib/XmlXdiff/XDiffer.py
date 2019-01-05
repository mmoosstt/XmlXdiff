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

        XHash.XDiffHasher.getHashes(
            self.xelements1, XHash.XDiffHasher.callbackHashAll)
        XHash.XDiffHasher.getHashes(
            self.xelements2, XHash.XDiffHasher.callbackHashAll)

        self.findUnchangedMovedElements()

        self.findChangedElements()

        self.findTagNameAttributeNameValueConsitency()

        self.findAttributeValueElementValueConsitency()

        self.findTagNameAttributeNameConsitency()

        self.findTagNameConsitency()

        self.verifyChangedElements(self.xelements1)

        self.verifyChangedElements(self.xelements2)

        for _e in XTypes.LOOP(
                self.xelements1, XTypes.ElementUnknown):
            _e.setType(XTypes.ElementDeleted)

        for _e in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):
            _e.setType(XTypes.ElementAdded)

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

    def findTagNameConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashTagNameConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashTagNameConsitency)

        _gravity_index = self.getGravity()

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):

            _gravity_index1 = self.gravityIndexPredesesor(
                _xelement2, self.xelements2, self.xelements1)

            if _gravity_index1 is not None:
                _gravity_index = _gravity_index1

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTagConsitency)
                    _xelement2.setType(
                        XTypes.ElementTagConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)

                    _gravity_index = self.xelements1.index(_xelement1)
                    break

        self.setGravity(_gravity_index)

    def findAttributeValueElementValueConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        _gravity_index = self.getGravity()

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):

            _gravity_index1 = self.gravityIndexPredesesor(
                _xelement2, self.xelements2, self.xelements1)

            if _gravity_index1 is not None:
                _gravity_index = _gravity_index1

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTextAttributeValueConsitency)
                    _xelement2.setType(
                        XTypes.ElementTextAttributeValueConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)

                    _gravity_index = self.xelements1.index(_xelement1)

                    break

        self.setGravity(_gravity_index)

    def findTagNameAttributeNameValueConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1,  XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashTagNameAttributeNameValueConsitency)

        _gravity_index = self.getGravity()

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):

            _gravity_index1 = self.gravityIndexPredesesor(
                _xelement2, self.xelements2, self.xelements1)

            if _gravity_index1 is not None:
                _gravity_index = _gravity_index1

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementChanged, XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTagAttributeNameValueConsitency)
                    _xelement2.setType(
                        XTypes.ElementTagAttributeNameValueConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)

                    _gravity_index = self.xelements1.index(_xelement1)

                    break

        self.setGravity(_gravity_index)

    def findTagNameAttributeNameConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1,  XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        _gravity_index = self.getGravity()

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):

            _gravity_index1 = self.gravityIndexPredesesor(
                _xelement2, self.xelements2, self.xelements1)

            if _gravity_index1 is not None:
                _gravity_index = _gravity_index1

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementChanged, XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTagAttributeNameConsitency)
                    _xelement2.setType(
                        XTypes.ElementTagAttributeNameConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)

                    _gravity_index = self.xelements1.index(_xelement1)

                    break

        self.setGravity(_gravity_index)

    def gravityIndexPredesesor(self, xelement_a, xelements_a, xelement_b):

        # iterate over all elements before xelement_a (reversed)
        for _xelement in reversed(xelements_a[:xelements_a.index(xelement_a)]):

            # check if _xelement is from the same tree branch (xpath)
            _distance = XPath.XDiffXmlPath.getXpathDistance(
                _xelement.xpath, xelement_a.xpath)
            if _distance < 3:

                # check if predecessor has been linked
                if _xelement.xelements:
                    _xelement_b = _xelement.xelements[0]
                    return xelement_b.index(_xelement_b)

            else:
                return None

        return None

    def findUnchangedMovedElements(self):

        def subElements(element, elements):

            for _element in elements[elements.index(element):]:
                if _element.xpath.find(element.xpath) == 0:
                    yield _element

        _gravity_index = self.getGravity()

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):

            _gravity_index1 = self.gravityIndexPredesesor(
                _xelement2, self.xelements2, self.xelements1)

            if _gravity_index1 is not None:
                _gravity_index = _gravity_index1

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementUnknown):

                if (_xelement1.hash == _xelement2.hash):
                    if(_xelement1.xpath == _xelement2.xpath):

                        _gen1 = subElements(_xelement1, self.xelements1)
                        _gen2 = subElements(_xelement2, self.xelements2)

                        for _xelement11 in _gen1:
                            _xelement22 = next(_gen2)
                            _xelement11.setType(XTypes.ElementUnchanged)
                            _xelement22.setType(XTypes.ElementUnchanged)
                            _xelement11.addXelement(_xelement22)
                            _xelement22.addXelement(_xelement11)

                        _gravity_index = self.xelements1.index(_xelement1)

                        break

                    else:

                        _gen1 = subElements(_xelement1, self.xelements1)
                        _gen2 = subElements(_xelement2, self.xelements2)

                        for _xelement11 in _gen1:
                            _xelement22 = next(_gen2)
                            _xelement11.setType(XTypes.ElementMoved)
                            _xelement22.setType(XTypes.ElementMoved)
                            _xelement11.addXelement(_xelement22)
                            _xelement22.addXelement(_xelement11)

                        _gravity_index = self.xelements1.index(_xelement1)
                        break

        self.setGravity(_gravity_index)

    def findChangedElements(self):
        _gravity_index = 0

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP_GRAVITY(
                    self.xelements1, _gravity_index, XTypes.ElementUnknown):

                if (_xelement1.xpath == _xelement2.xpath):

                    _xelement1.setType(XTypes.ElementChanged)
                    _xelement2.setType(XTypes.ElementChanged)
                    _gravity_index = self.xelements1.index(_xelement1)
                    break
