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

        _node_text = self.getElementText(xelement.node)
        _lines1 = self._linesCallback(_node_text)

        if xelement.getXelement() is None:
            _lines2 = []
        else:
            _node_text2 = self.getElementText(xelement.getXelement().node)
            _lines2 = self._linesCallback(_node_text2)

        _l = max(len(_lines1), len(_lines2))

        _lines1 = _lines1 + [(' ', 0, 0)] * (_l - len(_lines1))
        _lines2 = _lines2 + [(' ', 0, 0)] * (_l - len(_lines2))

        _svg = SVG(insert=(self.pos_x, self.pos_y),
                   font_family=self.font_family,
                   font_size=self.font_size)

        _w = 0
        _h = 0

        while _lines1 and _lines2:
            _line1, _, _ = _lines1[0]
            _lines1 = _lines1[1:]
            _line2, _, _ = _lines2[0]
            _lines2 = _lines2[1:]

            _text, _w1, _h1 = self.lineCompare(_line2, _line1)

            _h1_offset = _h1 * 0.25

            _w = max(_w, _w1)
            _h = _h + _h1

            _text['x'] = 0
            _text['y'] = _h

            _h = _h + _h1_offset

            _svg.add(_text)

        _svg['height'] = _h
        _svg['width'] = _w
        #_factor = 0.25
        #_svg.viewbox(0, 0, _w + _w * _factor, _h + _h * _factor)

        self.pos_y = self.pos_y + float(_h)
        self.pos_y_max = max(self.pos_y_max, self.pos_y)
        self.pos_x_max = max(self.pos_x_max, self.pos_x + float(_w))

        return _svg


class DrawXmlDiff(XSvgCompact.DrawXmlDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        XSvgCompact.DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXml()
        self.report2 = DrawXml()
