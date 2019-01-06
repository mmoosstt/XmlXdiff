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

        _path1 = '{}\\..\\..\\tests\\simple\\xml1.xml'.format(getPath())
        _path2 = '{}\\..\\..\\tests\\simple\\xml2.xml'.format(getPath())
        _out = '{}\\..\\..\\tests\\simple\\xdiff.svg'.format(getPath())

        with open(_path1, "w") as f:
            f.write(_xml1)

        with open(_path2, "w") as f:
            f.write(_xml2)

        x = DrawXmlDiff(_path1, _path2)
        x.saveSvg(_out)


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

    def test11(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
