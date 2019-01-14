# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: data types used within XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD


from inspect import isclass
from svgwrite import rgb


class XElement(object):

    child_cnt_median = 0

    def __init__(self):
        self.hash = None
        self.xpath = None
        self.type = None
        self.node = None
        self.child_cnt = None
        self.svg_node = None
        self.xelements_compared = {}

    def setChildCnt(self, inp):
        self.child_cnt = inp

    def addSvgNode(self, inp):
        self.svg_node = inp

    def addXelement(self, xelement):

        _key = xelement.type.__class__.__name__

        if _key in self.xelements_compared.keys():
            self.xelements_compared[_key].append(xelement)
        else:
            self.xelements_compared[_key] = [xelement]

    def getXelement(self, xtype):
        if isclass(xtype):
            _key = xtype.__name__
        else:
            _key = xtype.__class__.__name__

        if _key in self.xelements_compared.keys():
            return self.xelements_compared[_key][0]

    def setNode(self, inp):
        self.node = inp

    def setType(self, inp):
        if isclass(inp):
            self.type = inp()
        else:
            self.type = inp

    def setXpath(self, inp):
        self.xpath = inp

    def setHash(self, inp):
        self.hash = inp


class XType(object):

    opacity = 0.3

    @classmethod
    def name(cls):
        return cls.__name__.replace("Element", "")


class ElementUnknown(XType):
    fill = rgb(0xd0, 0xd0, 0xd0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnchanged(XType):
    fill = rgb(0x7e, 0x62, 0xa1)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementChanged(XType):
    fill = rgb(0xff, 0x00, 0x80)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementDeleted(XType):
    fill = rgb(0xff, 0x00, 0xff)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementAdded(XType):
    fill = rgb(0x0f, 0xff, 0x00)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementVerified(XType):
    fill = rgb(0xff, 0xff, 0x00)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementMoved(XType):
    fill = rgb(0x1e, 0x2d, 0xd2)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagConsitency(XType):
    fill = rgb(0x00, 0xa0, 0x70)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTextAttributeValueConsitency(XType):
    fill = rgb(0x00, 0x70, 0xa0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagAttributeNameConsitency(XType):
    fill = rgb(0x00, 0xd0, 0xe0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagAttributeNameValueConsitency(XType):
    fill = rgb(0x00, 0xa0, 0xf0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagRed(XType):
    fill = rgb(0xff, 0, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


def LOOP_UNCHANGED_SEGMENTS(xelementsa, xelementsb):

    _start_indexb = xelementsb.index(xelementsb[0])
    _start_indexa = xelementsa.index(xelementsa[0])

    while True:

        _stop_elementb = None
        for _e in xelementsb[_start_indexb:]:
            if isinstance(_e.type, ElementUnchanged):
                _stop_elementb = _e
                break

        if _stop_elementb is not None:
            _stop_indexb = xelementsb.index(_stop_elementb)
            _stop_indexa = xelementsa.index(
                _stop_elementb.getXelement(ElementUnchanged))
        else:
            _stop_indexb = len(xelementsb)
            _stop_indexa = len(xelementsa)

        _yield_b = xelementsb[_start_indexb:_stop_indexb + 1]
        _yield_a = xelementsa[_start_indexa:_stop_indexa + 1]

        yield _yield_a, _yield_b

        for _e in xelementsb[_stop_indexb:]:

            if isinstance(_e.type, ElementUnchanged):
                _stop_elementb = _e

            else:
                break

        if _stop_elementb is None:
            break

        _start_indexb = xelementsb.index(_stop_elementb) + 1
        _start_indexa = xelementsa.index(
            _stop_elementb.getXelement(ElementUnchanged)) + 1


def LOOP_GRAVITY(xelementsa, xelementsb, xelementb):

    _g = None
    for _g in reversed(xelementsb[:xelementsb.index(xelementb)]):
        if _g.xelement_compared != None:
            break

    _index = 0
    if _g is not None:
        if _g.xelement_compared is not None:
            _index = xelementsa.index(_g.xelement_compared)

    for _element in xelementsa[_index:]:
        yield _element

    for _element in xelementsa[_index:]:
        yield _element


def LOOP_CHILD_ELEMENTS(elements, element):
    for _element in elements[elements.index(element):]:
        if _element.xpath.find(element.xpath) == 0:
            yield _element


def CHILDS_ARRAY(elements, element):

    _start_index = elements.index(element)
    for _element in elements[_start_index:]:
        if _element.xpath.find(element.xpath) == 0:
            _stop_elment = _element
        elif _element.xpath.find(element.xpath) != 0:
            break

    _stop_index = elements.index(_stop_elment)

    return elements[_start_index + 1:_stop_index + 1]


def LOOP_CHILD_CNT(elements, child_cnt, *element_types):

    for _element in elements:

        if (_element.child_cnt == child_cnt):
            if isinstance(_element.type, element_types):
                yield _element


def LOOP(elements, *element_types):

    # try to match shortest paths first - identification of biggest blocks
    # /root
    # /node1
    # /node1/node2
    # ...

    _append = []
    for _element in elements:
        if isinstance(_element.type, element_types):
            _append.append((len(elements) - _element.child_cnt,
                            _element.xpath, _element))

    for _, _, _element in sorted(_append):
        if isinstance(_element.type, element_types):
            yield _element


def LOOP_XTYPES():
    for _xtype in XType.__subclasses__():
        yield _xtype
