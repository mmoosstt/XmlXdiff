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
from diffx import base, xpath, hash, get_path


class DiffxPath:
    '''
    Interface for file names
    '''

    def __init__(self, filepath):
        _x = os.path.abspath(filepath).replace("\\", "/")

        self.path = _x[:_x.rfind("/")].replace("/", "\\")
        self.filename = _x[_x.rfind("/") + 1:_x.rfind('.')]
        self.fileending = _x[_x.rfind('.') + 1:]
        self.filepath = _x.replace("/", "\\")


class DiffxExecutor:
    '''
    This is the heart and entry point of XmlXdiff. The orchestration of looping, hashing and
    comparing.
    '''

    def __init__(self):
        self.path1 = DiffxPath(
            '{}\\..\\..\\tests\\test1\\a.xml'.format(get_path()))
        self.path2 = DiffxPath(
            '{}\\..\\..\\tests\\test1\\b.xml'.format(get_path()))

        # initialised when execute is executed
        self.gravity = 0
        self.path1 = None
        self.path2 = None
        self.xml1 = None
        self.xml2 = None
        self.root1 = None
        self.root2 = None
        self.diffx_nodes_one = None
        self.diffx_nodes_two = None

    def set_gravity(self, inp):
        '''
        Interface setter for gravity - unused till now.
        replaced by parent indentification

        :param inp: int
        '''

        self.gravity = inp

    def get_gravity(self):
        '''
        Interface getter for gravity.
        '''
        return copy.deepcopy(self.gravity)

    def set_left_path(self, path):
        '''
        Interface setter for path1 - normal the left/elder side

        :param path: str - path not checked for validity till now
        '''
        self.path1 = DiffxPath(path)

    def set_right_path(self, path):
        '''
        Interface setter for path2 - normal the right/latest side

        :param path: str - path not checked for validity till now
        '''
        self.path2 = DiffxPath(path)

    def execute(self):
        '''
        Entry point for differ.
        '''

        self.xml1 = lxml.etree.parse(self.path1.filepath)
        self.xml2 = lxml.etree.parse(self.path2.filepath)

        self.root1 = self.xml1.getroot()
        self.root2 = self.xml2.getroot()

        _xpath = xpath.DiffxPath()

        self.diffx_nodes_one = _xpath.get_diffx_nodes(self.root1, "", 1)
        self.diffx_nodes_two = _xpath.get_diffx_nodes(self.root2, "", 1)

        _child_cnts = {}
        _ = [_child_cnts.update({_e.child_cnt: None})
             for _e in self.diffx_nodes_one]
        _ = [_child_cnts.update({_e.child_cnt: None})
             for _e in self.diffx_nodes_two]

        for _child_cnt in reversed(sorted(_child_cnts.keys())):

            self.find_unchanged_diffx_nodes_with_children(_child_cnt,
                                                   self.diffx_nodes_one,
                                                   self.diffx_nodes_two)

            self.find_moved_diffx_nodes_with_children(_child_cnt,
                                               self.diffx_nodes_one,
                                               self.diffx_nodes_two)

            self.find_moved_parent_diffx_nodes(_child_cnt,
                                         self.diffx_nodes_one,
                                         self.diffx_nodes_two)

    def _calculate_hashes(self,
                         xelements,
                         callback,
                         child_cnt=None,
                         children=True,
                         xtypes=(base.DiffxNodeChanged, base.DiffxNodeUnknown)):

        pass

    def _gen_diffx_nodes(self,
                            xelements,
                            hash_algorithm=hash.DiffxHasher.callback_hash_all,
                            child_cnt=None,
                            children=True,
                            xtypes=(base.DiffxNodeChanged, base.DiffxNodeUnknown)):

        if child_cnt is None:
            _diffx_nodes_gen = base.gen_diffx_nodes(xelements,
                                                  *xtypes)

        else:
            _diffx_nodes_gen = base.gen_child_count(xelements,
                                                      child_cnt,
                                                      *xtypes)

        hash.DiffxHasher.get_hashes(_diffx_nodes_gen, hash_algorithm, children)

        if child_cnt is None:
            _generator = base.gen_diffx_nodes(xelements, *xtypes)

        else:
            _generator = base.gen_child_count(
                xelements, child_cnt, *xtypes)

        return _generator

    def set_xdiff_type_child_nodes(self, xelement1, xelement2, xtype):
        '''
        Set element type of child elements

        :param xelement1: [DiffxElement, DiffxElement, ..]
        :param xelement2: [DiffxElement, DiffxElement, ..]
        :param xtype: XType
        '''

        _diffx_nodes_one = base.gen_child_nodes(self.diffx_nodes_one,
                                                  xelement1)

        _diffx_nodes_two = base.gen_child_nodes(self.diffx_nodes_two,
                                                  xelement2)

        for _diffx_node_one in _diffx_nodes_one:
            _diffx_node_two = next(_diffx_nodes_two)

            if (isinstance(_diffx_node_one.type, base.DiffxNodeUnknown) and
                    isinstance(_diffx_node_two.type, base.DiffxNodeUnknown)):

                _diffx_node_one.set_type(xtype)
                _diffx_node_two.set_type(xtype)
                _diffx_node_one.add_xelement(_diffx_node_two)
                _diffx_node_two.add_xelement(_diffx_node_one)

    def find_moved_parent_diffx_nodes(self, child_cnt, diffx_nodes_one, diffx_nodes_two):
        '''
        Entry point of pseudo recursive execution

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)
        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_nodes_two,
                                                         hash_algorithm=hash.DiffxHasher.callback_hash_all,
                                                         children=False,
                                                         child_cnt=child_cnt,
                                                         xtypes=_xtypes)

        for _diffx_node_two in _diffx_nodes_two_gen:
            _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_nodes_one,
                                                             hash_algorithm=hash.DiffxHasher.callback_hash_all,
                                                             children=False,
                                                             xtypes=_xtypes)

            for _diffx_node_one in _diffx_nodes_two_gen:
                if _diffx_node_one.hash == _diffx_node_two.hash:

                    _diffx_node_one.set_type(base.DiffxParentNodeMoved)
                    _diffx_node_two.set_type(base.DiffxParentNodeMoved)
                    _diffx_node_one.add_xelement(_diffx_node_two)
                    _diffx_node_two.add_xelement(_diffx_node_one)

                    _diffx_nodes_one = base.arr_child_nodes(diffx_nodes_one,
                                                          _diffx_node_one)

                    _diffx_nodes_two = base.arr_child_nodes(diffx_nodes_two,
                                                          _diffx_node_two)

                    _child_cnts = {}
                    _ = [_child_cnts.update({_e.child_cnt: None})
                         for _e in _diffx_nodes_one]
                    _ = [_child_cnts.update({_e.child_cnt: None})
                         for _e in _diffx_nodes_two]

                    for _child_cnt in reversed(sorted(_child_cnts.keys())):

                        self.find_unchanged_diffx_nodes_with_children(_child_cnt,
                                                               _diffx_nodes_one,
                                                               _diffx_nodes_two)

                        self.find_moved_diffx_nodes_with_children(_child_cnt,
                                                           _diffx_nodes_one,
                                                           _diffx_nodes_two)

                        # recursive entry point
                        self.find_moved_parent_diffx_nodes(_child_cnt,
                                                     _diffx_nodes_one,
                                                     _diffx_nodes_two)

                        self.find_tag_name_attribute_name_value_consitency_with_children(_child_cnt,
                                                                                 _diffx_nodes_one,
                                                                                 _diffx_nodes_two)

                        self.find_attribute_value_element_value_consitency_with_children(_child_cnt,
                                                                                  _diffx_nodes_one,
                                                                                  _diffx_nodes_two)

                        self.find_tag_name_attribute_name_consitency_with_children(_child_cnt,
                                                                            _diffx_nodes_one,
                                                                            _diffx_nodes_two)

                        self.find_tag_name_consitency_with_children(_child_cnt,
                                                               _diffx_nodes_one,
                                                               _diffx_nodes_two)

                    for _e in _diffx_nodes_one:
                        if isinstance(_e.type, base.DiffxNodeUnknown):
                            _e.set_type(base.DiffxNodeDeleted)

                    for _e in _diffx_nodes_two:
                        if isinstance(_e.type, base.DiffxNodeUnknown):
                            _e.set_type(base.DiffxNodeAdded)

                    break

    def find_tag_name_consitency_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_consitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_consitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)
            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:

                    self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                    _diffx_node_two,
                                                    base.DiffxNodeTagConsi)

                    break

    def find_attribute_value_element_value_consitency_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         hash_algorithm=hash.DiffxHasher.callback_hash_attribute_value_element_value_consitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             hash_algorithm=hash.DiffxHasher.callback_hash_attribute_value_element_value_consitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:

                    self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                    _diffx_node_two,
                                                    base.DiffxNodeTextAttriValueConsi)

                    break

    def find_tag_name_attribute_name_value_consitency_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_attribute_name_value_consitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_attribute_name_value_consitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:

                    self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                    _diffx_node_two,
                                                    base.DiffxNodeTagAttriNameValueConsi)

                    break

    def find_tag_name_attribute_name_consitency_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_attribute_name_consitency,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             hash_algorithm=hash.DiffxHasher.callback_hash_tag_name_attribute_name_consitency,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:

                    self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                    _diffx_node_two,
                                                    base.DiffxNodeTagAttriNameConsi)

                    break

    def find_moved_diffx_nodes_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:
                    if not _diffx_node_one.xpath == _diffx_node_two.xpath:

                        self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                        _diffx_node_two,
                                                        base.DiffxNodeMoved)
                        break

    def find_unchanged_diffx_nodes_with_children(self, child_cnt, diffx_node_one, diffx_node_two):
        '''
        TBD

        :param child_cnt: int - only elements with a certain number of children are investigated
        :param diffx_nodes_one: [DiffxElement, DiffxElement, ...]
        :param diffx_nodes_two: [DiffxElement, DiffxElement, ...]
        '''

        _xtypes = (base.DiffxNodeChanged, base.DiffxNodeUnknown)

        _diffx_nodes_two_gen = self._gen_diffx_nodes(xelements=diffx_node_two,
                                                         xtypes=_xtypes,
                                                         child_cnt=child_cnt)

        for _diffx_node_two in _diffx_nodes_two_gen:

            _diffx_nodes_one_gen = self._gen_diffx_nodes(xelements=diffx_node_one,
                                                             xtypes=_xtypes,
                                                             child_cnt=child_cnt)

            for _diffx_node_one in _diffx_nodes_one_gen:

                if _diffx_node_one.hash == _diffx_node_two.hash:
                    if _diffx_node_one.xpath == _diffx_node_two.xpath:

                        self.set_xdiff_type_child_nodes(_diffx_node_one,
                                                        _diffx_node_two,
                                                        base.DiffxNodeUnchanged)

                        break
