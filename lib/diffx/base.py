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


class DiffxNode:
    '''
    General type extending an xml node to an dx_node node.

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
        self.dx_nodes_compared = None

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

    def add_dx_node(self, dx_node):
        '''
        interface setter for xelment_compared

        :param dx_node: XTypes.DiffxNode
        '''
        self.dx_nodes_compared = dx_node

    def get_dx_nodes(self):
        '''
        interface getter for xelment_compared
        '''
        return self.dx_nodes_compared

    def set_lxml_node(self, inp):
        '''
        interface setter for node

        :param inp: lxml.etree.dx_node
        '''
        self.node = inp

    def set_dx_type(self, inp):
        '''
        interface setter for type

        :param inp: XTypes.DiffxNode
        '''

        if isclass(inp):
            self.type = inp()
        else:
            self.type = inp

    def set_dx_path(self, inp):
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


class DiffxNodeType:
    '''
    Type for DiffxNode description.
    provides standard interfaces for XmlXdiff.
    '''

    opacity = 0.3

    @classmethod
    def name(cls):
        '''
        Should be used as standard Interface for class name.
        '''
        return cls.__name__.replace("Element", "")


class DiffxNodeUnknown(DiffxNodeType):
    '''
    SVG interface for Unknown DiffxElements
    '''
    fill = rgb(0xd0, 0xd0, 0xd0)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeUnchanged(DiffxNodeType):
    '''
    SVG interface for Unchanged DiffxElements
    '''

    fill = rgb(0x7e, 0x62, 0xa1)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeChanged(DiffxNodeType):
    '''
    SVG interface for Changed DiffxElements
    '''

    fill = rgb(0xfc, 0xd1, 0x2a)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeDeleted(DiffxNodeType):
    '''
    SVG interface for Deleted DiffxElements
    '''

    fill = rgb(0xff, 0x00, 0xff)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeAdded(DiffxNodeType):
    '''
    SVG interface for added diffx node
    '''

    fill = rgb(0x0f, 0xff, 0x00)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeMoved(DiffxNodeType):
    '''
    SVG interface for moved diffx node
    '''

    fill = rgb(0x1e, 0x2d, 0xd2)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxParentNodeMoved(DiffxNodeType):
    '''
    SVG interface for parent diffx node moved
    '''

    fill = rgb(0x55, 0x99, 0xff)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeTagConsi(DiffxNodeType):
    '''
    SVG interface for diffx node with tag consistency
    '''

    fill = rgb(0x00, 0xa0, 0x70)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeTagAttriNameConsi(DiffxNodeType):
    '''
    SVG interface for diffx node with tag, attribute and name consistency
    '''

    fill = rgb(0x00, 0xd0, 0xe0)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeTagAttriNameValueConsi(DiffxNodeType):
    '''
    SVG interface for diffx node with tag, attri, name and value consistency
    '''

    fill = rgb(0x00, 0xa0, 0xf0)

    def __init__(self):
        DiffxNodeType.__init__(self)


class DiffxNodeTextAttriValueConsi(DiffxNodeType):
    '''
    SVG interface for diffx node with text, attributes and value consistency
    '''

    fill = rgb(0x00, 0x70, 0xa0)

    def __init__(self):
        DiffxNodeType.__init__(self)


def gen_child_nodes(dx_nodes, dx_node):
    '''
    Generator for all child dx_nodes of dx_node that are part of dx_nodes

    :param dx_nodes: [DiffxNode, ... ]
    :param dx_node: DiffxNode
    '''
    for _dx_node in dx_nodes[dx_nodes.index(dx_node):]:
        if _dx_node.xpath.find(dx_node.xpath) == 0:
            yield _dx_node


def arr_child_nodes(dx_nodes, dx_node):
    '''
    Returns an array of child dx_nodes of dx_node that are part of dx_nodes
    Use CHILD_ARRAY over gen_child_nodes if it is consumed more times afterwards.

    :param dx_nodes: [DiffxNode, ..]
    :param dx_node: DiffxNode
    '''

    _start_index = dx_nodes.index(dx_node)
    for _dx_node in dx_nodes[_start_index:]:
        if _dx_node.xpath.find(dx_node.xpath) == 0:
            _stop_elment = _dx_node
        elif _dx_node.xpath.find(dx_node.xpath) != 0:
            break

    _stop_index = dx_nodes.index(_stop_elment)

    return dx_nodes[_start_index + 1:_stop_index + 1]


def gen_child_count(dx_nodes, child_cnt, *dx_node_types):
    '''
    Generator for dx_nodes of a certain type and a specific number of children

    :param dx_nodes: [DiffxNode, DiffxNode, .. ]
    :param child_cnt: int - number of children
    '''

    for _dx_node in dx_nodes:

        if _dx_node.child_cnt == child_cnt:
            if isinstance(_dx_node.type, dx_node_types):
                yield _dx_node


def gen_dx_nodes(dx_nodes, *dx_types):
    """
    Generator for dx_nodes of a certain type.


    :param dx_nodes: [DiffxNode, DiffxNode, ...]
    """

    _append = []
    for _dx_node in dx_nodes:
        if isinstance(_dx_node.type, dx_types):
            _append.append((len(dx_nodes) - _dx_node.child_cnt,
                            _dx_node.xpath, _dx_node))

    for _, _, _dx_node in sorted(_append):
        if isinstance(_dx_node.type, dx_types):
            yield _dx_node


def gen_available_dx_node_types():
    '''
    Generator for all available XTypes
    '''
    for _xtype in DiffxNodeType.__subclasses__():
        yield _xtype
