# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: calculate hashes over etree
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import lxml.etree
import hashlib


class XDiffHasher(object):

    @classmethod
    def callbackHashAll(cls, element, hashpipe):

        _element_childes = element.getchildren()

        for child in _element_childes:
            hashpipe.update(cls.callbackHashAll(child, hashpipe))

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
    def callbackHashAttributeValueElementValueConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(
                cls.callbackHashAttributeValueElementValueConsitency(child, hashpipe))

        # attributes and text are only taken into account for leaf nodes
        if _element_childes:
            hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        else:
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
    def callbackHashTagNameAttributeNameConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(
                cls.callbackHashTagNameAttributeNameConsitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))
        # attributes and text are only taken into account for leaf nodes
        if not _element_childes:
            if hasattr(element, 'attrib'):
                for _name in sorted(element.attrib.keys()):
                    hashpipe.update(bytes(_name + '#att', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def callbackHashTagNameConsitency(cls, element, hashpipe):

        _element_childes = element.getchildren()
        for child in _element_childes:
            hashpipe.update(cls.callbackHashTagNameConsitency(child, hashpipe))

        hashpipe.update(bytes(str(element.tag) + '#tag', 'utf-8'))

        return bytes(hashpipe.hexdigest(), 'utf-8')

    @classmethod
    def getHashesElementBased(cls, xml, element, hashes, pathes):

        _hash = hashlib.sha1()
        _hash.update(lxml.etree.tostring(element))
        _path = xml.getpath(element)
        pathes[_path] = [_hash.hexdigest(), 'ElementUnchanged']
        hashes[_hash.hexdigest()] = _path

        for _child in element.getchildren():
            cls.getHashesElementBased(xml, _child, hashes, pathes)

    @classmethod
    def getHashes(cls, xelements, callbackHashAlgorithm):

        for _xelement in xelements:

            _hash_algo = hashlib.sha1()
            callbackHashAlgorithm(_xelement.node, _hash_algo)
            _hash = _hash_algo.hexdigest()

            _xelement.setHash(_hash)
