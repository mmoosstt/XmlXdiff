# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: basic tests XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import unittest
from diffx import main


class MainUseCases(unittest.TestCase):

    def test_compare_string(self):
        _xml1 = """<root><deleted>with content</deleted><unchanged/><changed name="test1" /></root>"""
        _xml2 = """<root><unchanged/><changed name="test2" /><added/></root>"""

        main.compare(_xml1, _xml2)
        main.save('./simple/diffx_string.svg')

    def test_compare_file(self):
        _xml1 = './simple/xml1.xml'
        _xml2 = './simple/xml2.xml'

        main.compare(_xml1, _xml2)
        main.save('./simple/diffx_file.svg')
