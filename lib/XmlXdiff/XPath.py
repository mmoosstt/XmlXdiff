# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: build more suitable xpathes
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import lxml.etree
from XmlXdiff import XTypes


class XPathException(Exception):
    pass


class XDiffXmlPath(object):

    xml = None

    @classmethod
    def setXmlValidation(cls, xml_root):
        cls.xml = xml_root

    @classmethod
    def getXelements(cls, element, parent_path="", pos=0):
        cls.xelements = []
        cls.walk(element, parent_path, pos)
        return cls.xelements

    @classmethod
    def getXpathDistance(cls, path1, path2):

        _arr1 = path1.split("/")
        _arr2 = path2.split("/")

        while True:

            if _arr1 == [] or _arr2 == []:
                return len(_arr1) + len(_arr2)

            if _arr1[0] == _arr2[0]:
                _arr1 = _arr1[1:]
                _arr2 = _arr2[1:]

            else:
                return len(_arr1) + len(_arr2)

    @classmethod
    def getTag(cls, element, pos):

        if isinstance(element, lxml.etree._Comment):
            return "comment()[{pos}]".format(pos=pos)

        else:

            _tag = element.tag
            if _tag.find("{") > -1:
                for _ns in element.nsmap.keys():

                    _nslong = "{{{nslong}}}".format(
                        nslong=element.nsmap[_ns])
                    if _ns is None:
                        _nsshort = ""
                    else:
                        _nsshort = "{nsshort}:".format(nsshort=_ns)

                    _tag = _tag.replace(_nslong, _nsshort)

                    if _tag.find("{") < 0:
                        break

            return "*[name()='{tag}'][{pos}]".format(tag=_tag, pos=pos)

    @classmethod
    def walk(cls, element, parent_path, pos, child_cnt=0):

        _path = "{parent}/{tag}".format(parent=parent_path,
                                        tag=cls.getTag(element, pos))

        _xelement = XTypes.XElement()
        _xelement.setType(XTypes.ElementUnknown)
        _xelement.setNode(element)
        _xelement.setXpath(_path)

        cls.xelements.append(_xelement)

        if cls.xml is not None:
            if not cls.xml.xpath(_path):
                raise XPathException("{} does not exist in xml".format(_path))

        _pos_dict = {}
        for _child in element.getchildren():

            if _child.tag in _pos_dict.keys():
                _pos_dict[_child.tag] += 1

            else:
                _pos_dict[_child.tag] = 1

            child_cnt += cls.walk(
                _child, _path, _pos_dict[_child.tag], 0)

        _xelement.setChildCnt(child_cnt)
        child_cnt = child_cnt + 1

        return child_cnt
