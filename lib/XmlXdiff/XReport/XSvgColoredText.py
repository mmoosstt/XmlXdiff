"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""
from svgwrite.container import SVG
from XmlXdiff.XReport import XSvgCompact
from XmlXdiff.XReport.XSvgCompact import DrawLegend


class DrawXml(XSvgCompact.DrawXml):
    '''
    Draw svg signle xml
    '''

    def __init__(self):
        XSvgCompact.DrawXml.__init__(self)

    def addTextBox(self, xelement):
        '''
        Text box with fixed width and content text diff.

        :param xelement: XTypes.XElement
        '''

        _node_text1 = self.getElementText(xelement.node)

        if xelement.getXelement() is None:
            _node_text2 = ""
        else:
            _node_text2 = self.getElementText(xelement.getXelement().node)

        _svg, _width, _height = self.addTextBlockCompare(_node_text1, _node_text2)
        self.pos_y = self.pos_y + float(_height)
        self.pos_y_max = max(self.pos_y_max, self.pos_y)
        self.pos_x_max = max(self.pos_x_max, self.pos_x + float(_width))

        return _svg


class DrawXmlDiff(XSvgCompact.DrawXmlDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        XSvgCompact.DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXml()
        self.report2 = DrawXml()
