"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: calculate hashes over etree
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

import hashlib


class DiffxHasher():
    """
    Collection of hash calculation of xml element tree structures.
    hash algorithm differ in the selection of relevant data.

    <tag attribute_name[x]="attribute_value[x]" ... >
        pre_text
            <children[x] ... >
        post_text
    </tag>

    x = 0 ... n

    """

    @classmethod
    def callback_hash_all(cls, element, hashpipe, children=True):
        '''
        calculate hash over tag, attribute_names, attribute_values, pre- and post-text

        :param element: etree.element
        :param hashpipe: hash algorithm interface
        :param children: bool - if false children of element ignored for hash calculation
        '''

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(cls.callback_hash_all(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                _attrib_value = element.attrib[_name]
                hashpipe.update(
                    bytes(_name + _attrib_value + '#att', 'utf-8'))

        if element.text is not None:
            hashpipe.update(bytes(element.text.strip() + '#txt', 'utf-8'))

        if element.tail is not None:
            hashpipe.update(bytes(element.tail.strip() + '#txt', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callback_hash_attribute_value_element_value_consitency(cls, element, hashpipe, children=True):
        '''
        calculate hash over attribute_values, pre- and post-text

        :param element: etree.element
        :param hashpipe: hash algorithm interface
        :param children: bool - if false children of element ignored for hash calculation
        '''

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callback_hash_attribute_value_element_value_consitency(child, hashpipe))

        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                _attrib_value = element.attrib[_name]
                hashpipe.update(bytes(_attrib_value + '#att', 'utf-8'))

        if element.text is not None:
            hashpipe.update(bytes(element.text.strip() + '#txt', 'utf-8'))

        if element.tail is not None:
            hashpipe.update(bytes(element.tail.strip() + '#txt', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callback_hash_tag_name_attribute_name_value_consitency(cls, element, hashpipe, children=True):
        '''
        calculate hash over tag, attribute_names, attribute_values

        :param element: etree.element
        :param hashpipe: hash algorithm interface
        :param children: bool - if false children of element ignored for hash calculation
        '''

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callback_hash_tag_name_attribute_name_value_consitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                _value = element.attrib[_name]
                hashpipe.update(bytes(_name + _value + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callback_hash_tag_name_attribute_name_consitency(cls, element, hashpipe, children=True):
        '''
        calculate hash over tag, attribute_names

        :param element: etree.element
        :param hashpipe: hash algorithm interface
        :param children: bool - if false children of element ignored for hash calculation
        '''

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callback_hash_tag_name_attribute_name_consitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                hashpipe.update(bytes(_name + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callback_hash_tag_name_consitency(cls, element, hashpipe, children=True):
        '''
        calculate hash over tag

        :param element: etree.element
        :param hashpipe: hash algorithm interface
        :param children: bool - if false children of element ignored for hash calculation
        '''

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callback_hash_tag_name_consitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def get_hashes(cls, dx_nodes, callback_hash_algorithm, children=True):
        '''

        calculate hashes for dx_nodes

        :param dx_nodes: [XmlXdiff.XTypes.DiffxElement, ...]
        :param callback_hash_algorithm: callback of this class for selection of hash algorithm
        :param children: bool - if true children are included
        '''

        for _dx_node in dx_nodes:

            _hash_algo = hashlib.sha1()
            callback_hash_algorithm(_dx_node.node, _hash_algo, children)
            _hash = _hash_algo.hexdigest()
            _dx_node.set_hash(_hash)
