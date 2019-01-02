# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: calculate difference between source and target file (inspired from xdiff algorithm)
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

from XmlXdiff import XTypes, XPath, XHash, getPath
import lxml.etree
import os


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

        self.findTagNameAttributeNameConsitency()

        self.findAttributeValueElementValueConsitency()

        self.findTagNameConsitency()

        self.verifyElements(self.xelements1)
        self.verifyElements(self.xelements2)

        for _e in XTypes.LOOP(
                self.xelements1, XTypes.ElementUnknown):
            _e.setType(XTypes.ElementDeleted)

        for _e in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):
            _e.setType(XTypes.ElementAdded)

    def verifyElements(self, elements=None):

        _xpaths = [[elements[0], None]]

        for _element in elements[1:]:

            if isinstance(_element.type, XTypes.ElementChanged):

                if _element.xpath.find(_xpaths[-1:][0][0].xpath) == -1:
                    _0, _1 = _xpaths.pop()
                    if _1 is None:
                        _xpaths[-1:][0][1] = False
                    else:
                        _xpaths[-1:][0][1] = _1
                        _0.setType(XTypes.ElementVerified)

                    if _xpaths[-1:][0][1]:
                        _xpaths[-1:][0][0].setType(XTypes.ElementVerified)

                _xpaths.append([_element, None])

            else:

                if _element.xpath.find(_xpaths[-1:][0][0].xpath) == -1:
                    _0, _1 = _xpaths.pop()
                    if _1 is None:
                        _xpaths[-1:][0][1] = False
                    else:
                        _xpaths[-1:][0][1] = _1
                        _0.setType(XTypes.ElementVerified)

                    if _xpaths[-1:][0][1]:
                        _xpaths[-1:][0][0].setType(XTypes.ElementVerified)

                else:
                    if _xpaths[-1:][0][1] is None:
                        _xpaths[-1:][0][1] = True

    def findTagNameConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashTagNameConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashTagNameConsitency)

        for _xelement1 in XTypes.LOOP(
                self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown):
            for _xelement2 in XTypes.LOOP(
                    self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTagConsitency)
                    _xelement2.setType(
                        XTypes.ElementTagConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)
                    break

    def findAttributeValueElementValueConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashAttributeValueElementValueConsitency)

        for _xelement1 in XTypes.LOOP(
                self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown):
            for _xelement2 in XTypes.LOOP(
                    self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTextAttributeValueConsitency)
                    _xelement2.setType(
                        XTypes.ElementTextAttributeValueConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)
                    break

    def findTagNameAttributeNameConsitency(self):

        _elements1 = XTypes.LOOP(
            self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements1, XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        _elements2 = XTypes.LOOP(
            self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown)
        XHash.XDiffHasher.getHashes(
            _elements2, XHash.XDiffHasher.callbackHashTagNameAttributeNameConsitency)

        for _xelement1 in XTypes.LOOP(
                self.xelements1, XTypes.ElementChanged, XTypes.ElementUnknown):
            for _xelement2 in XTypes.LOOP(
                    self.xelements2, XTypes.ElementChanged, XTypes.ElementUnknown):
                if (_xelement1.hash == _xelement2.hash):
                    _xelement1.setType(
                        XTypes.ElementTagAttributeNameConsitency)
                    _xelement2.setType(
                        XTypes.ElementTagAttributeNameConsitency)

                    _xelement1.addXelement(_xelement2)
                    _xelement2.addXelement(_xelement1)
                    break

    def findUnchangedMovedElements(self):

        def subElements(element, elements):

            for _element in elements[elements.index(element):]:
                if _element.xpath.find(element.xpath) == 0:
                    yield _element

        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP(
                    self.xelements1, XTypes.ElementUnknown):

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

                        break

    def findChangedElements(self):
        for _xelement2 in XTypes.LOOP(
                self.xelements2, XTypes.ElementUnknown):

            for _xelement1 in XTypes.LOOP(
                    self.xelements1, XTypes.ElementUnknown):

                if (_xelement1.xpath == _xelement2.xpath):

                    _xelement1.setType(XTypes.ElementChanged)
                    _xelement2.setType(XTypes.ElementChanged)
                    break


if __name__ == '__main__':
    path1 = '{}\\tests\\test1\\a.xml'.format(getPath())

    y = XDiffPath(path1)
    _x = XDiffExecutor()
    _x.run()

    for _x in _x.xelements1:
        print(_x.xpath, _x.type)
