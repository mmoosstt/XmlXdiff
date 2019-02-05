"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

import copy
from difflib import SequenceMatcher
import lxml.etree

import svgwrite
from svgwrite import cm, mm, rgb
from svgwrite.container import Group, SVG
from svgwrite.shapes import Rect, Polyline
from svgwrite.text import Text, TSpan, TextArea

from XmlXdiff import getPath
from XmlXdiff import XDiffer
from XmlXdiff.XReport import XRender
from XmlXdiff.XPath import XDiffXmlPath
from XmlXdiff import XTypes


class DrawLegend:
    '''
    Draw svg legend.
    '''

    def __init__(self):

        self.dwg = None
        self.pos_x = 0
        self.pos_y = 0
        self.pos_y_max = 0
        self.pos_x_max = 0
        self.unit = 10
        self.font_size = 10
        self.font_family = "Lucida Console"
        self.filepath = None

        XRender.Render.setFontFamily(self.font_family)
        XRender.Render.setFontSize(self.font_size)

        self.dwg = svgwrite.Drawing()
        self._moveRight()

        _svg = SVG(insert=(self.pos_x, self.pos_y))

        for _class in XTypes.generatorAvailableXTypes():
            _svg.add(self.addLine(_class))

        _svg["width"] = self.pos_x_max
        _svg["height"] = self.pos_y_max
        self.dwg["width"] = self.pos_x_max
        self.dwg["height"] = self.pos_y_max

        self.dwg.add(_svg)

    def addLine(self, instance_xtype):
        '''
        Draw svg line representing XElement.

        :param instance_xtype: XTypes.XElement
        '''

        _text = instance_xtype.name()
        _w, _h = XRender.Render.getTextSize(_text)

        _h += _h * 0.25

        _svg = SVG(insert=(self.pos_x, self.pos_y),
                   width=_w,
                   height=_h)

        _text_svg = Text(_text)
        _text_svg['x'] = 0
        _text_svg['y'] = _h - _h * 0.25
        _text_svg['font-size'] = self.font_size
        _text_svg['font-family'] = self.font_family
        _text_svg['opacity'] = 1.0
        _text_svg['fill'] = rgb(0, 0, 0)

        _rect_svg = Rect()
        _rect_svg['x'] = 0
        _rect_svg['y'] = 0
        _rect_svg['fill'] = instance_xtype.fill
        _rect_svg['opacity'] = instance_xtype.opacity
        _rect_svg['height'] = _h
        _rect_svg['width'] = _w

        _svg.add(_text_svg)
        _svg.add(_rect_svg)

        _svg.viewbox(0, 0, _w, _h)

        self.pos_y = self.pos_y + _h
        self.pos_x_max = max(self.pos_x_max, _w + self.pos_x)
        self.pos_y_max = max(self.pos_y_max, self.pos_y)

        return _svg

    def _moveLeft(self):
        '''
        Positioning within svg.
        '''

        self.pos_x = self.pos_x - 1.2 * self.unit

    def _moveRight(self):
        '''
        Positioning within svg
        '''

        self.pos_x = self.pos_x + 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def saveSvg(self, filepath=None):
        '''
        save svg.

        :param filepath: str - filepath
        '''

        if filepath is not None:
            self.dwg.filename = filepath
            self.filepath = filepath

        self.dwg.save()


class DrawXml:
    '''
    Draw svg signle xml
    '''

    def __init__(self):
        self.dwg = None
        self.pos_x = 0
        self.pos_y = 0
        self.pos_x_max = 0
        self.pos_y_max = 0
        self.unit = 10
        self.svg_elements = {}
        self.fill_red = rgb(200, 0, 0)
        self.fill_blue = rgb(0, 0, 200)
        self.fill = self.fill_red
        self.blue = 0
        self.font_size = 10
        self.font_family = "Lucida Console"

        XRender.Render.setFontFamily(self.font_family)
        XRender.Render.setFontSize(self.font_size)
        self.pos_y = XRender.Render.font_metrics.height() * 2

    def getElementText(self, element):
        '''
        returning string representing lxml.etree.node.
        handing comments, namespace and attributes.

        :param element: lxml.etree.node
        '''

        if isinstance(element, lxml.etree._Comment):
            _tag = "!comment"
        else:
            _tag = element.tag

            if _tag[0] == "{":
                for _ns in element.nsmap.keys():
                    _ns_long = element.nsmap[_ns]
                    _ns_long = "{{{}}}".format(_ns_long)

                    if _ns is None:
                        _ns = ""
                    else:
                        _ns = "{}:".format(_ns)

                    if _tag.find(_ns_long) > -1:
                        _tag = _tag.replace(_ns_long, _ns)
                        break

        _attribs = " "
        for _akey in sorted(element.attrib.keys()):
            _attribs = _attribs + " {name}='{value}' ".format(
                name=_akey, value=element.attrib[_akey])

        _attribs = _attribs[:-1]

        return "{tag}{attribs}: {text}".format(attribs=_attribs, tag=_tag, text=element.text)

    def loadFromXElements(self, xelements, callback):
        '''
        XElements to svg representation.

        :param xelements: [XElement, ...]
        :param callback: method defining svg representation of xelement
        '''

        self.dwg = svgwrite.Drawing(filename="test.svg")

        _root = xelements[0]
        _node_level_z = 0
        for _xelement in xelements:

            _node_level = XDiffXmlPath.getXpathDistance(
                _root.xpath, _xelement.xpath)

            _steps = _node_level - _node_level_z

            _node_level_z = _node_level

            if _steps > 0:

                for _x in range(abs(_steps)):
                    self._moveRight()

            elif _steps < 0:

                for _x in range(abs(_steps)):
                    self._moveLeft()

            _xelement.addSvgNode(callback(_xelement))

    def _linesCallback(self, text):
        '''
        For debugging purpose.

        :param text: str - line
        '''

        return XRender.Render.splitTextToLines(text)

    def addTextBox(self, xelement):
        '''
        Simple text box with fixed width.

        :param xelement: XTypes.XElement
        '''
        _text = self.getElementText(xelement.node)
        _lines = self._linesCallback(_text)

        _y = copy.deepcopy(self.pos_y)

        _svg = SVG(insert=(self.pos_x, self.pos_y))
        _t = Text('', insert=(0, 0), font_size=self.font_size,
                  font_family=self.font_family)

        _h = 0
        _w = 0
        for _line, _width, _height in _lines:
            _h = _h + float(_height)
            _w = max(_w, float(_width))

            _text = TSpan(_line, fill="black", insert=(0, _h))
            _t.add(_text)

        self.pos_y = self.pos_y + _h
        self.pos_y_max = max(self.pos_y_max, self.pos_y)
        self.pos_x_max = max(self.pos_x_max, _w + self.pos_x)

        _svg['height'] = _h
        _svg['width'] = _w
        _svg.viewbox(0, 0, _w, _h)

        _svg.add(_t)

        return _svg

    def addTextBoxLineCompare(self, xelement):
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

    def lineCompare(self, line1, line2):
        '''
        Create difference of to text lines.

        :param line1: str
        :param line2: str
        '''

        text = Text(text="")

        _matcher = SequenceMatcher(None, line1, line2)

        _text = ''
        for tag, _s1, _e1, _s2, _e2 in _matcher.get_opcodes():

            if tag == "replace":
                text.add(
                    TSpan(text=line2[_s2:_e2], fill=rgb(0x00, 0x80, 0xff)))
                # text.add(TSpan(text=line1[_s1:_e1],
                #               text_decoration="line-through"))
                _text += line2[_s2:_e2]
                #_text += line1[_s1:_e1]

            elif tag == "delete":
                # text.add(TSpan(text=line1[_s1:_e1],
                #              text_decoration="line-through"))
                #_text += line1[_s1:_e1]
                pass

            elif tag == "insert":
                text.add(
                    TSpan(text=line2[_s2:_e2], fill=rgb(0x00, 0x80, 0xff)))
                _text += line2[_s2:_e2]

            elif tag == "equal":
                text.add(TSpan(text=line1[_s1:_e1]))
                _text += line1[_s1:_e1]

        _width, _height = XRender.Render.getTextSize(_text)

        text['y'] = _height
        text['x'] = 0

        return text, _width, _height

    def _moveLeft(self):
        self.pos_x = self.pos_x - 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def _moveRight(self):
        self.pos_x = self.pos_x + 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def _moveTop(self):
        self.fill = self.fill_blue
        self.pos_y = 0.3 * self.unit
        self.pos_x = self.pos_x_max  # + (5.5 * self.unit)

    def saveSvg(self, xelements):
        """
        Save svg to file.
        """

        for _xelement in xelements:
            self.dwg.add(_xelement.svg_node)

        self.dwg.save()


class DrawXmlDiff:
    '''
    Creation diff output.
    '''

    def __init__(self, path1, path2):
        self.dwg = None
        self.legend = None
        self.filepath = None
        self.differ = None
        self.path1 = path1
        self.path2 = path2
        self.differ = XDiffer.XDiffExecutor()
        self.report1 = DrawXml()
        self.report2 = DrawXml()

    def draw(self):
        '''
        Starts diff creation.
        '''

        self.differ.setLeftPath(self.path1)
        self.differ.setRightPath(self.path2)
        self.differ.execute()

        self.filepath = "{path}\\xdiff_{filename1}_{filename2}.svg".format(path=self.differ.path1.path,
                                                                           filename1=self.differ.path1.filename,
                                                                           filename2=self.differ.path2.filename)

        self.report1._moveRight()
        self.report1.loadFromXElements(self.differ.xelements1,
                                       self.report1.addTextBoxLineCompare)
        self.report1.saveSvg(self.differ.xelements1)

        self.report2._moveRight()
        self.report2.loadFromXElements(self.differ.xelements2,
                                       self.report2.addTextBoxLineCompare)
        self.report2.saveSvg(self.differ.xelements2)

        self.legend = DrawLegend()

        self.report1.dwg['x'] = 0
        self.report1.dwg['y'] = 0

        self.report2.dwg['x'] = self.report1.pos_x_max * 1.2
        self.report2.dwg['y'] = 0

        self.legend.dwg['x'] = self.report2.pos_x_max * \
            1.2 + self.report1.pos_x_max
        self.legend.dwg['y'] = 0

        _height = max(self.report2.pos_y_max,
                      self.report1.pos_y_max,
                      self.legend.pos_y_max)

        _width = (self.report1.pos_x_max * 1.2 +
                  self.report2.pos_x_max * 1.2 +
                  self.legend.pos_x_max)

        self.dwg = svgwrite.Drawing(filename=self.filepath)
        self.dwg['height'] = _height
        self.dwg['width'] = _width
        self.dwg.viewbox(0, 0, _width, _height)

        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        self.dwg.add(self.legend.dwg)

        self._drawMovePattern(XTypes.ElementMoved)
        self._drawMovePattern(XTypes.ElementMovedParent)
        self._drawMovePattern(XTypes.ElementUnchanged)
        self._drawMovePattern(XTypes.ElementTagAttributeNameConsitency)
        self._drawMovePattern(XTypes.ElementTextAttributeValueConsitency)
        self._drawMovePattern(XTypes.ElementTagConsitency)
        self._drawMovePattern(XTypes.ElementTagAttributeNameValueConsitency)

        self._drawChangedPattern(XTypes.ElementChanged,
                                 self.differ.xelements2,
                                 self.report1.pos_x_max * 1.2)

        self._drawChangedPattern(XTypes.ElementAdded,
                                 self.differ.xelements2,
                                 self.report1.pos_x_max * 1.2)

        self._drawChangedPattern(XTypes.ElementDeleted,
                                 self.differ.xelements1)

    def saveSvg(self, filepath=None):
        '''
        Save svg to filepath

        :param filepath: str
        '''

        if filepath is not None:
            self.dwg.filename = filepath
            self.filepath = filepath

        self.dwg.save()

    def _drawMovePattern(self, xtype):

        for _e in XTypes.generatorXTypes(self.differ.xelements1, xtype):
            _start_svg1 = _e.svg_node

            if _e.getXelement():
                _stop_svg2 = _e.getXelement().svg_node

                _x1 = float(_start_svg1['x'])
                _y1 = float(_start_svg1['y'])

                _x2 = float(self.report2.dwg['x'])
                _y2 = float(self.report2.dwg['y'])

                _x3 = float(_stop_svg2['x'])
                _y3 = float(_stop_svg2['y'])

                _h1 = float(_start_svg1['height'])
                _h2 = float(_stop_svg2['height'])

                _p01 = (_x1, _y1)
                _p02 = (self.report1.pos_x_max, _y1)
                _p03 = (float(self.report2.dwg['x']), _y3)
                _p04 = (_x3 + _x2 + float(_stop_svg2['width']), _y3)
                _p05 = (_x3 + _x2 + float(_stop_svg2['width']), _y3 + _h2)
                _p06 = (float(self.report2.dwg['x']), _y3 + _h2)
                _p07 = (self.report1.pos_x_max, _y1 + _h1)
                _p08 = (_x1, _y1 + _h1)

                _line = Polyline(points=[_p01, _p02, _p03, _p04, _p05, _p06, _p07, _p08, _p01],
                                 stroke_width="0.5",
                                 stroke=xtype.fill,
                                 fill=xtype.fill,
                                 opacity=xtype.opacity)

                self.dwg.add(_line)

    def _drawChangedPattern(self, xtype, xelements, x_offset=0):

        for _e in XTypes.generatorXTypes(xelements, xtype):
            _start_svg1 = _e.svg_node

            _x1 = float(_start_svg1['x']) + x_offset
            _y1 = float(_start_svg1['y'])

            _p01 = (_x1, _y1)
            _p02 = (_x1 + _start_svg1['width'], _y1)
            _p03 = (_x1 + _start_svg1['width'],
                    _y1 + _start_svg1['height'])
            _p04 = (_x1,
                    _y1 + _start_svg1['height'])

            _line = Polyline(points=[_p01, _p02, _p03, _p04, _p01],
                             stroke_width="1",
                             stroke=xtype.fill,
                             fill=xtype.fill,
                             opacity=xtype.opacity)

            self.dwg.add(_line)

# trial overload boxes only report


class DrawXmlBoxesOnly(DrawXml):
    '''
    Create diff without text.
    '''

    def __init__(self):
        DrawXml.__init__(self)

    def _linesCallback(self, text):
        return [('', 40, 10)]


class DrawXmlDiffBoxesOnly(DrawXmlDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXmlBoxesOnly()
        self.report2 = DrawXmlBoxesOnly()
