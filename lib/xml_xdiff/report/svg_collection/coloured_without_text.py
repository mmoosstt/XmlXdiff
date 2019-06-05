"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

from xml_xdiff.report.svg_collection import compact
from xml_xdiff.report.svg_collection.compact import DrawLegend


class DrawXml(compact):
    '''
    Create diff without text.
    '''

    def __init__(self):
        compact.DrawXml.__init__(self)

    def _lines_callback(self, text):
        return [('', 40, 10)]


class DrawXmlDiff(compact.DrawXmlDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        compact.DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXml()
        self.report2 = DrawXml()
