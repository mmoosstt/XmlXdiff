"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: data types used within XmlXdiff
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

from inspect import isclass
from svgwrite import rgb


class DiffxElement:
    '''
    General type extending an xml node to an xelement node.

    This node contains further information about counterparts,
    hash and compare state.

    '''

    child_cnt_median = 0

    def __init__(self):
        self.hash = None
        self.xpath = None
        self.type = None
        self.node = None
        self.child_cnt = None
        self.svg_node = None
        self.xelements_compared = None

    def set_child_cnt(self, inp):
        '''
        interface setter for child_cnt

        :param inp: int
        '''

        self.child_cnt = inp

    def add_svg_node(self, inp):
        '''
        interface setter for svg_node
        :param inp:
        '''
        self.svg_node = inp

    def add_xelement(self, xelement):
        '''
        interface setter for xelment_compared

        :param xelement: XTypes.DiffxElement
        '''
        self.xelements_compared = xelement

    def get_xelement(self):
        '''
        interface getter for xelment_compared
        '''
        return self.xelements_compared

    def set_node(self, inp):
        '''
        interface setter for node

        :param inp: lxml.etree.element
        '''
        self.node = inp

    def set_type(self, inp):
        '''
        interface setter for type

        :param inp: XTypes.DiffxElement
        '''

        if isclass(inp):
            self.type = inp()
        else:
            self.type = inp

    def set_xpath(self, inp):
        '''
        interface setter for xpath
        custom xpath, different compatible to lxml.xpath but different syntax used.

        :param inp: str - xpath syntax
        '''
        self.xpath = inp

    def set_hash(self, inp):
        '''
        interface setter for hash
        current calculated hash.

        :param inp: ? - hash value
        '''

        self.hash = inp


class DiffxNode:
    '''
    Type for DiffxElement description.
    provides standard interfaces for XmlXdiff.
    '''

    opacity = 0.3

    @classmethod
    def name(cls):
        '''
        Should be used as standard Interface for class name.
        '''
        return cls.__name__.replace("Element", "")


class DiffxNodeUnknown(DiffxNode):
    '''
    SVG interface for Unknown DiffxElements
    '''
    fill = rgb(0xd0, 0xd0, 0xd0)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeUnchanged(DiffxNode):
    '''
    SVG interface for Unchanged DiffxElements
    '''

    fill = rgb(0x7e, 0x62, 0xa1)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeChanged(DiffxNode):
    '''
    SVG interface for Changed DiffxElements
    '''

    fill = rgb(0xfc, 0xd1, 0x2a)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeDeleted(DiffxNode):
    '''
    SVG interface for Deleted DiffxElements
    '''

    fill = rgb(0xff, 0x00, 0xff)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeAdded(DiffxNode):
    '''
    SVG interface for added diffx node
    '''

    fill = rgb(0x0f, 0xff, 0x00)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeMoved(DiffxNode):
    '''
    SVG interface for moved diffx node
    '''

    fill = rgb(0x1e, 0x2d, 0xd2)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxParentNodeMoved(DiffxNode):
    '''
    SVG interface for parent diffx node moved
    '''

    fill = rgb(0x55, 0x99, 0xff)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeTagConsi(DiffxNode):
    '''
    SVG interface for diffx node with tag consistency
    '''

    fill = rgb(0x00, 0xa0, 0x70)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeTagAttriNameConsi(DiffxNode):
    '''
    SVG interface for diffx node with tag, attribute and name consistency
    '''

    fill = rgb(0x00, 0xd0, 0xe0)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeTagAttriNameValueConsi(DiffxNode):
    '''
    SVG interface for diffx node with tag, attri, name and value consistency
    '''

    fill = rgb(0x00, 0xa0, 0xf0)

    def __init__(self):
        DiffxNode.__init__(self)


class DiffxNodeTextAttriValueConsi(DiffxNode):
    '''
    SVG interface for diffx node with text, attributes and value consistency
    '''

    fill = rgb(0x00, 0x70, 0xa0)

    def __init__(self):
        DiffxNode.__init__(self)


def gen_child_nodes(elements, element):
    '''
    Generator for all child elements of element that are part of elements

    :param elements: [DiffxElement, ... ]
    :param element: DiffxElement
    '''
    for _element in elements[elements.index(element):]:
        if _element.xpath.find(element.xpath) == 0:
            yield _element


def arr_child_nodes(elements, element):
    '''
    Returns an array of child elements of element that are part of elements
    Use CHILD_ARRAY over gen_child_nodes if it is consumed more times afterwards.

    :param elements: [DiffxElement, ..]
    :param element: DiffxElement
    '''

    _start_index = elements.index(element)
    for _element in elements[_start_index:]:
        if _element.xpath.find(element.xpath) == 0:
            _stop_elment = _element
        elif _element.xpath.find(element.xpath) != 0:
            break

    _stop_index = elements.index(_stop_elment)

    return elements[_start_index + 1:_stop_index + 1]


def gen_child_count(elements, child_cnt, *element_types):
    '''
    Generator for elements of a certain type and a specific number of children

    :param elements: [DiffxElement, DiffxElement, .. ]
    :param child_cnt: int - number of children
    '''

    for _element in elements:

        if _element.child_cnt == child_cnt:
            if isinstance(_element.type, element_types):
                yield _element


def gen_diffx_nodes(elements, *element_types):
    """
    Generator for elements of a certain type.


    :param elements: [DiffxElement, DiffxElement, ...]
    """

    _append = []
    for _element in elements:
        if isinstance(_element.type, element_types):
            _append.append((len(elements) - _element.child_cnt,
                            _element.xpath, _element))

    for _, _, _element in sorted(_append):
        if isinstance(_element.type, element_types):
            yield _element


def gen_available_diffx_node_types():
    '''
    Generator for all available XTypes
    '''
    for _xtype in DiffxNode.__subclasses__():
        yield _xtype
