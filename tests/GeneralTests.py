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
from xmldiff import main, formatting

from XmlXdiff import getPath, XDiffer
from XmlXdiff.XReport.XSvgColoredText import DrawXmlDiff, DrawLegend
from XmlXdiff.XPath import XDiffXmlPath

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


class HTMLFormatter(formatting.XMLFormatter):
    def render(self, result):
        transform = lxml.etree.XSLT(XSLT_TEMPLATE)
        result = transform(result)
        return super(HTMLFormatter, self).render(result)


class UnSorted(unittest.TestCase):

    def calcDistance(self):
        _res = XDiffXmlPath.getXpathDistance("a/b/c/d/1/2/3", "a/b/c/d/1/3")
        self.assertEqual(_res, 3)


class ReportModule(unittest.TestCase):

    def testLegend(self):
        _l = DrawLegend()
        _l.saveSvg('{}\\..\\..\\tests\\simple\\legend.svg'.format(getPath()))

    def testXSvgCompact(self):
        from XmlXdiff.XReport.XSvgCompact import DrawXmlDiff
        self._simpleModule(DrawXmlDiff)

    def testXSvgColoredText(self):
        from XmlXdiff.XReport.XSvgColoredText import DrawXmlDiff
        self._simpleModule(DrawXmlDiff)

    def testXSvgColorOnly(self):
        from XmlXdiff.XReport.XSvgColorOnly import DrawXmlDiff
        self._simpleModule(DrawXmlDiff)

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

        _path1 = '{}\\..\\..\\tests\\simple\\xml1.xml'.format(getPath())
        _path2 = '{}\\..\\..\\tests\\simple\\xml2.xml'.format(getPath())
        _out = '{}\\..\\..\\tests\\simple\\{}.svg'.format(getPath(),
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
        cls.differ.draw()
        cls.differ.saveSvg()
        print("{name}: delta_t={time:.4f}s xml_elements={cnt}".format(name=folder_name,
                                                                      time=time.time() - _t,
                                                                      cnt=len(cls.differ.differ.xelements2) + len(cls.differ.differ.xelements1)))

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
