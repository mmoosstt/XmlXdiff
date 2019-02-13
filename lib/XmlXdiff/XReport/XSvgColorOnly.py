"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

from XmlXdiff.XReport import XSvgCompact
from XmlXdiff.XReport.XSvgCompact import DrawLegend


class DrawXml(XSvgCompact.DrawXml):
    '''
    Create diff without text.
    '''

    def __init__(self):
        XSvgCompact.DrawXml.__init__(self)

    def _linesCallback(self, text):
        return [('', 40, 10)]


class DrawXmlDiff(XSvgCompact.DrawXmlDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        XSvgCompact.DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXml()
        self.report2 = DrawXml()
