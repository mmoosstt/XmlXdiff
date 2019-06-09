"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: build more suitable xpathes
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""


import lxml.etree
from diffx import base


class DiffxException(Exception):
    '''
    Exception applicable for this module only
    '''


class DiffxPath():
    '''
    Implements a xpath conformed representation that is slightly different to lxml library

    lxml /*/*/tag_name[pos]
    Diffx /*[name()=tag_name1][10]/*[name()=tag_name2][10]/*[name()=tag_name3][10]
    '''

    xml = None

    @classmethod
    def get_dx_nodes(cls, node, parent_path="", pos=0):
        """
        Creates a list of XmlXdiff.XTypes.DiffxNode from lxml root element for instance.
        """

        cls.dx_nodes = []
        cls.walk(node, parent_path, pos)
        return cls.dx_nodes

    @classmethod
    def get_xpath_distance(cls, path1, path2):
        '''
        Calculate distance between paths.
        Can be used for cost calculation of moved nodes.
        Path seperator has to be /.

        :param path1: source xpath
        :param path2: destination xpath
        '''

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
    def get_tag(cls, element, pos):
        '''
        Creation of valid tag name for new xpath syntax by taking namespaces and
        comments into account.

        :param element: lxml tree element
        :param pos: position among parent children
        '''

        if isinstance(element, lxml.etree._Comment):
            return "comment()[{pos}]".format(pos=pos)

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
    def walk(cls, dx_node, parent_path, pos, child_cnt=0):
        '''
        Creation of new xpath style for selected lxml etree dx_node.

        :param dx_node: lxml etree dx_node
        :param parent_path: start point of xpath
        :param pos: start pos of dx_node
        :param child_cnt: number of investigated children
        '''

        _path = "{parent}/{tag}".format(parent=parent_path,
                                        tag=cls.get_tag(dx_node, pos))

        _dx_node = base.DiffxNode()
        _dx_node.set_dx_type(base.DiffxNodeUnknown)
        _dx_node.set_lxml_node(dx_node)
        _dx_node.set_dx_path(_path)

        cls.dx_nodes.append(_dx_node)

        if cls.xml is not None:
            if not cls.xml.xpath(_path):
                raise DiffxException("{} does not exist in xml".format(_path))

        _pos_dict = {}
        for _child in dx_node.getchildren():

            if _child.tag in _pos_dict.keys():
                _pos_dict[_child.tag] += 1

            else:
                _pos_dict[_child.tag] = 1

            child_cnt += cls.walk(
                _child, _path, _pos_dict[_child.tag], 0)

        _dx_node.set_child_cnt(child_cnt)
        child_cnt = child_cnt + 1

        return child_cnt
