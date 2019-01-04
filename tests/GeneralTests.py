# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: basic tests XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import time
import unittest
import inspect
from XmlXdiff import getPath, XDiffer
from XmlXdiff.XReport import DrawXmlDiff
from XmlXdiff.XPath import XDiffXmlPath


class UnSorted(unittest.TestCase):

    def calcDistance(self):
        _res = XDiffXmlPath.getXpathDistance("a/b/c/d/1/2/3", "a/b/c/d/1/3")
        self.assertEqual(_res, 3)


class Usability(unittest.TestCase):

    def simpleExample(self):

        from XmlXdiff.XReport import DrawXmlDiff

        _xml1 = """<root><deleted>with content</deleted><unchanged/><changed name="test1" /></root>"""
        _xml2 = """<root><unchanged/><changed name="test2" /><added/></root>"""

        with open("test1.xml", "w") as f:
            f.write(_xml1)

        with open("test2.xml", "w") as f:
            f.write(_xml2)

        x = DrawXmlDiff("test1.xml", "test2.xml")
        x.saveSvg('xdiff.svg')


class CompareAll(unittest.TestCase):

    @staticmethod
    def execute_old(folder_name):
        _i = XDiffer.XDiffExecutor()
        _i.setPath1("{}\\..\\..\\tests\\{}\\a.xml".format(
            getPath(), folder_name))
        _i.setPath2("{}\\..\\..\\tests\\{}\\b.xml".format(
            getPath(), folder_name))
        _i.run()

    @classmethod
    def execute(cls, folder_name):
        _t = time.time()
        _path1 = "{}\\..\\..\\tests\\{}\\a.xml".format(getPath(), folder_name)
        _path2 = "{}\\..\\..\\tests\\{}\\b.xml".format(getPath(), folder_name)
        cls.differ = DrawXmlDiff(_path1, _path2)
        cls.differ.save()
        print("{name}: delta_t={time:.4f}s xml_elements={cnt}".format(name=folder_name,
                                                                      time=time.time() - _t,
                                                                      cnt=len(cls.differ.differ.xelements2) + len(cls.differ.differ.xelements1)))

    def test1(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test2(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test3(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test4(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test5(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test6(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test7(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test8(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test9(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
