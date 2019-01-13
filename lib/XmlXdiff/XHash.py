# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: calculate hashes over etree
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import hashlib


class XDiffHasher(object):

    @classmethod
    def callbackHashAll(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(cls.callbackHashAllNoChilds(child, hashpipe))

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
    def callbackHashAllNoChilds(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(cls.callbackHashAllNoChilds(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        # attributes and text are only taken into account for leaf nodes
        if not _element_childes:
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
    def callbackHashAttributeValueElementValueConsitency(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callbackHashAttributeValueElementValueConsitency(child, hashpipe))

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
    def callbackHashTagNameAttributeNameValueConsitency(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callbackHashTagNameAttributeNameValueConsitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                _value = element.attrib[_name]
                hashpipe.update(bytes(_name + _value + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashTagNameAttributeNameConsitency(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callbackHashTagNameAttributeNameConsitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        if hasattr(element, 'attrib'):
            for _name in sorted(element.attrib.keys()):
                hashpipe.update(bytes(_name + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashTagNameConsitency(cls, element, hashpipe, children=True):

        _element_childes = element.getchildren()
        if children:
            for child in _element_childes:
                hashpipe.update(
                    cls.callbackHashTagNameConsitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def getHashes(cls, xelements, callbackHashAlgorithm, children=True):

        for _xelement in xelements:

            _hash_algo = hashlib.sha1()
            callbackHashAlgorithm(_xelement.node, _hash_algo, children)
            _hash = _hash_algo.hexdigest()
            _xelement.setHash(_hash)
