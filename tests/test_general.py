# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: basic tests XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import time
import os
import unittest
import inspect

from diffx import get_path, main
from diffx.xpath import DiffxPath

import lxml.etree

XSLT = '''
<xsl:stylesheet version="1.0" xmlns:diff="http://namespaces.shoobx.com/diff" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="@diff:insert-formatting">
        <xsl:attribute name="class">
            <xsl:value-of select="'insert-formatting'"/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="diff:delete">
        <del><xsl:apply-templates /></del>
    </xsl:template>
    
    <xsl:template match="diff:insert">
        <ins><xsl:apply-templates /></ins>
    </xsl:template>
    
    <xsl:template match="@*| node()">
        <xsl:copy>
        <xsl:apply-templates select="@*| node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
'''


XSLT_TEMPLATE = lxml.etree.fromstring(XSLT)


class UnSorted(unittest.TestCase):

    def calcDistance(self):
        _res = DiffxPath.get_xpath_distance("a/b/c/d/1/2/3", "a/b/c/d/1/3")
        self.assertEqual(_res, 3)


class ReportModule(unittest.TestCase):

    def testLegend(self):
        _l = DrawLegend()
        _l.save_svg('{}\\..\\..\\tests\\simple\\legend.svg'.format(get_path()))

    def testXSvgCompact(self):
        from diffx.svg.compact import DrawDiffxNodesCompared
        self._simpleModule(DrawDiffxNodesCompared)

    def testXSvgColoredText(self):
        from diffx.svg.coloured_text import DrawDiffxNodesCompared
        self._simpleModule(DrawDiffxNodesCompared)

    def testXSvgColorOnly(self):
        from diffx.svg.coloured_without_text import DrawDiffxNodesCompared
        self._simpleModule(DrawDiffxNodesCompared)

    def _simpleModule(self, modul_under_test):

        _xml1 = """<ngs_sample id="40332">
  <workflow value="salmonella" version="101_provisional" />
  <results>
  <gastro_prelim_st reason="not novel" success="false">
      <type st="1364" />
      <type st="9999" />
  </gastro_prelim_st>
 </results>
</ngs_sample>"""

        _xml2 = """<ngs_sample id="40332">
  <workflow value="salmonella" version="101_provisional" />
  <results>
  <gastro_prelim_st reason="not novel" success="false">
      <type st="1364" />
   </gastro_prelim_st>
 </results>
</ngs_sample>"""

        _path1 = '{}\\..\\..\\tests\\simple\\xml1.xml'.format(get_path())
        _path2 = '{}\\..\\..\\tests\\simple\\xml2.xml'.format(get_path())
        _out = '{}\\..\\..\\tests\\simple\\{}.svg'.format(get_path(),
                                                          modul_under_test.__module__)

        _path1 = os.path.abspath(_path1)
        _path2 = os.path.abspath(_path2)
        _out = os.path.abspath(_out)

        with open(_path1, "w") as f:
            f.write(_xml1)

        with open(_path2, "w") as f:
            f.write(_xml2)

        x = modul_under_test(_path1, _path2)
        x.draw()
        x.save_svg(_out)


class CompareAllJsons(unittest.TestCase):

    @classmethod
    def execute(cls, folder_name):
        _t = time.time()
        _path1 = "{}\\..\\..\\tests\\{}\\a.json".format(get_path(), folder_name)
        _path2 = "{}\\..\\..\\tests\\{}\\b.json".format(get_path(), folder_name)
        _path_svg = "{}\\..\\..\\tests\\{}\\xdiff_a_b.svg".format(get_path(), folder_name)

        main.compare_json(_path1, _path2)
        main.save(_path_svg, pretty=False)

        print("{name}: delta_t={time:.4f}s xml_elements={cnt}".format(name=folder_name,
                                                                      time=time.time() - _t,
                                                                      cnt=len(main.diffx.differ.second_dx_nodes) + len(main.diffx.differ.first_dx_nodes)))

    def test15(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)


class CompareAllXmls(unittest.TestCase):

    @classmethod
    def execute(cls, folder_name):
        _t = time.time()
        _path1 = "{}\\..\\..\\tests\\{}\\a.xml".format(get_path(), folder_name)
        _path2 = "{}\\..\\..\\tests\\{}\\b.xml".format(get_path(), folder_name)
        _path_svg = "{}\\..\\..\\tests\\{}\\xdiff_a_b.svg".format(get_path(), folder_name)

        main.compare_xml(_path1, _path2)
        main.save(_path_svg, pretty=False)

        print("{name}: delta_t={time:.4f}s xml_elements={cnt}".format(name=folder_name,
                                                                      time=time.time() - _t,
                                                                      cnt=len(main.diffx.differ.second_dx_nodes) + len(main.diffx.differ.first_dx_nodes)))

    def test13(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

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

    def test12(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test14(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
