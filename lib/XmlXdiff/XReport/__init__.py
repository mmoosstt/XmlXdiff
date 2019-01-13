# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: create diff report
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import lxml.etree
import copy

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


class ElementMarker(object):
    size = (2.5, 2.5)
    fill = rgb(200, 0, 0)
    unit = 10

    def __init__(self):
        self.svg_mark = Rect(size=self.__class__.size,
                             fill=self.__class__.fill)

    @classmethod
    def name(cls):
        return cls.__name__.replace("Element", "")

    def markSvgElement(self, svg_element):

        self.svg_mark['x'] = float(svg_element['x'])
        self.svg_mark['y'] = float(svg_element['y'])

        self.svg_mark['y'] = (float(self.svg_mark['y']) -
                              0.3 * self.__class__.unit)
        self.svg_mark['x'] = (float(self.svg_mark['x']) +
                              0.6 * self.__class__.unit)

        self.moveLeft()

        return self.svg_mark

    def moveLeft(self):
        self.svg_mark['x'] = float(
            self.svg_mark['x']) - 1.2 * self.__class__.unit


class DrawLegend(object):

    def __init__(self):

        self.dwg = None
        self.x = 0
        self.y = 0
        self.y_max = 0
        self.x_max = 0
        self.unit = 10
        self.font_size = 10
        self.font_family = "Lucida Console"

        XRender.Render.setFontFamily(self.font_family)
        XRender.Render.setFontSize(self.font_size)

        self.dwg = svgwrite.Drawing()

        self.moveRight()
        self.moveRight()

        for _class in XTypes.LOOP_XTYPES():
            _text, _width, _height = self.addLine(_class.name())
            _mark = _class()

            _rect = Rect()
            _rect['x'] = _text['x']
            _rect['y'] = float(_text['y']) - _height
            _rect['height'] = _height
            _rect['width'] = _width
            _rect['fill'] = _mark.fill
            _rect['opacity'] = 0.3

            self.dwg.add(_text)
            self.dwg.add(_rect)

    def addLine(self, text):
        _x, _y = XRender.Render.getTextSize(text)

        self.y = self.y + _y  # (0.6 * self.unit)
        self.x_max = max(self.x_max, _x + self.x)
        self.y_max = max(self.y_max, self.y)

        _text = Text(text, fill=rgb(0, 0, 0),
                     insert=(self.x, self.y), font_size=self.font_size, font_family=self.font_family)

        return _text, _x, _y

    def moveLeft(self):
        self.x = self.x - 1.2 * self.unit

    def moveRight(self):
        self.x = self.x + 1.2 * self.unit
        self.x_max = max(self.x_max, self.x)


class DrawXml(object):

    def __init__(self):
        self.dwg = None
        self.x = 0
        self.y = 0
        self.x_max = 0
        self.y_max = 0
        self.unit = 10
        self.svg_elements = {}
        self.xml = "xml1"
        self.fill_red = rgb(200, 0, 0)
        self.fill_blue = rgb(0, 0, 200)
        self.fill = self.fill_red
        self.blue = 0
        self.font_size = 10
        self.font_family = "Lucida Console"

        XRender.Render.setFontFamily(self.font_family)
        XRender.Render.setFontSize(self.font_size)
        self.y = XRender.Render.font_metrics.height() * 2

    def getElementText(self, element):

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

    def loadFromXElements(self, xelements):

        self.dwg = svgwrite.Drawing(filename="test.svg")

        _root = xelements[0]
        _node_level_z = 0
        for _xelement in xelements:
            _node_text = self.getElementText(_xelement.node)

            _node_level = XDiffXmlPath.getXpathDistance(
                _root.xpath, _xelement.xpath)

            _steps = _node_level - _node_level_z

            _node_level_z = _node_level

            if _steps > 0:

                for _x in range(abs(_steps)):
                    self.moveRight()

            elif _steps < 0:

                for _x in range(abs(_steps)):
                    self.moveLeft()

            _xelement.addSvgNode(self.addTextBox(_node_text))

    def addTextBox2(self, element):
        _g = Group()

        if isinstance(element, lxml.etree._Comment):
            _tag = "COMMENT"
        else:
            _tag = element.tag[element.tag.find("}") + 1:]
        _attribs = " "

        _w, _h = XRender.Render.getTextSize(_tag)
        _t = Text(_tag)

        _tag = TSpan(_tag)
        _tag['x'] = 0
        _tag['y'] = 0
        _tag['id'] = 'tag'

        for _attrib_name in sorted(element.attrib.keys()):
            _w1, _h1 = XRender.Render.getTextSize(_attrib_name)

            _attrib_value = element.attrib[_attrib_name]
            _w2, _h2 = XRender.Render.getTextSize(_attrib_name)

            _attribs = _attribs + " {name}='{value}' ".format(
                name=_attrib_name, value=None)

        _attribs = _attribs[:-1]

        XRender.Render.splitTextToLines(element.text)

        return "{tag}{attribs}: {text}".format(attribs=_attribs, tag=_tag, text=element.text)

    def linesCallback(self, text):
        return XRender.Render.splitTextToLines(text)

    def addTextBox(self, text):
        _lines = self.linesCallback(text)

        _y = copy.deepcopy(self.y)

        _svg = SVG(insert=(self.x, self.y))
        _t = Text('', insert=(0, 0), font_size=self.font_size,
                  font_family=self.font_family)

        _h = 0
        _w = 0
        for _line, _width, _height in _lines:
            _h = _h + float(_height)
            _w = max(_w, float(_width))

            _text = TSpan(_line, fill="black", insert=(0, _h))
            _t.add(_text)

        self.y = self.y + _h
        self.y_max = max(self.y_max, self.y)
        self.x_max = max(self.x_max, _w + self.x)

        _svg['height'] = _h
        _svg['width'] = _w
        _svg.viewbox(0, 0, _w, _h)

        _svg.add(_t)

        return _svg

    def moveLeft(self):
        self.x = self.x - 1.2 * self.unit
        self.x_max = max(self.x_max, self.x)

    def moveRight(self):
        self.x = self.x + 1.2 * self.unit
        self.x_max = max(self.x_max, self.x)

    def moveTop(self):
        self.fill = self.fill_blue
        self.y = 0.3 * self.unit
        self.x = self.x_max  # + (5.5 * self.unit)

    def saveSvg(self, xelements):
        for _xelement in xelements:
            self.dwg.add(_xelement.svg_node)

        self.dwg.save()

    def markAs(self, svg_node, mark):

        _r = Rect(insert=(0, 0),
                  width=svg_node['width'],
                  height=svg_node['height'],
                  fill=mark.fill,
                  opacity=0.2)

        svg_node.add(_r)


class DrawXmlDiff(object):

    def __init__(self, path1, path2):

        self.path1 = path1
        self.path2 = path2
        self.differ = XDiffer.XDiffExecutor()
        self.report1 = DrawXml()
        self.report2 = DrawXml()

    def draw(self):

        self.differ.setPath1(self.path1)
        self.differ.setPath2(self.path2)
        self.differ.run()

        self.filepath = "{path}\\xdiff_{filename1}_{filename2}.svg".format(path=self.differ.path1.path,
                                                                           filename1=self.differ.path1.filename,
                                                                           filename2=self.differ.path2.filename)

        self.report1.moveRight()
        self.report1.loadFromXElements(self.differ.xelements1)
        self.report1.saveSvg(self.differ.xelements1)

        self.report2.moveRight()
        self.report2.loadFromXElements(self.differ.xelements2)
        self.report2.saveSvg(self.differ.xelements2)

        self.legend = DrawLegend()

        self.report1.dwg['x'] = 0
        self.report1.dwg['y'] = 0

        self.report2.dwg['x'] = self.report1.x_max * 1.2
        self.report2.dwg['y'] = 0

        self.legend.dwg['x'] = self.report2.x_max * 1.2 + self.report1.x_max
        self.legend.dwg['y'] = 0

        _height = max(self.report2.y_max,
                      self.report1.y_max,
                      self.legend.y_max)

        _width = (self.report1.x_max +
                  self.report2.x_max +
                  self.legend.x_max)

        self.dwg = svgwrite.Drawing(filename=self.filepath)
        self.dwg['height'] = _height
        self.dwg['width'] = _width
        self.dwg.viewbox(0, 0, _width, _height)

        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        self.dwg.add(self.legend.dwg)

        self.drawMovePattern(XTypes.ElementMoved)
        self.drawMovePattern(XTypes.ElementTagRed)
        self.drawMovePattern(XTypes.ElementUnchanged)
        self.drawMovePattern(XTypes.ElementTagAttributeNameConsitency)
        self.drawMovePattern(XTypes.ElementTextAttributeValueConsitency)
        self.drawMovePattern(XTypes.ElementTagConsitency)
        self.drawMovePattern(XTypes.ElementTagAttributeNameValueConsitency)

        self.drawChangedPattern(XTypes.ElementChanged,
                                self.differ.xelements2,
                                self.report1.x_max * 1.2)

        self.drawChangedPattern(XTypes.ElementAdded,
                                self.differ.xelements2,
                                self.report1.x_max * 1.2)
        self.drawChangedPattern(XTypes.ElementDeleted,
                                self.differ.xelements1)
        self.drawChangedPattern(XTypes.ElementVerified,
                                self.differ.xelements2,
                                self.report1.x_max * 1.2)
        self.drawChangedPattern(XTypes.ElementVerified,
                                self.differ.xelements1)

    def save(self):
        self.dwg.save()
        pass

    def saveSvg(self, filepath=None):

        if filepath is not None:
            self.dwg.filename = filepath
            self.filepath = filepath

        self.dwg.save()

    def drawMovePattern(self, xtype):

        for _e in XTypes.LOOP(self.differ.xelements1, xtype):
            _start_svg1 = _e.svg_node

            if _e.getXelement(xtype):
                _stop_svg2 = _e.getXelement(xtype).svg_node

                _x1 = float(_start_svg1['x'])
                _y1 = float(_start_svg1['y'])

                _x2 = float(self.report2.dwg['x'])
                _y2 = float(self.report2.dwg['y'])

                _x3 = float(_stop_svg2['x'])
                _y3 = float(_stop_svg2['y'])

                _h1 = float(_start_svg1['height'])
                _h2 = float(_stop_svg2['height'])

                _p01 = (_x1, _y1)
                _p02 = (self.report1.x_max, _y1)
                _p03 = (float(self.report2.dwg['x']), _y3)
                _p04 = (_x3 + _x2 + float(_stop_svg2['width']), _y3)
                _p05 = (_x3 + _x2 + float(_stop_svg2['width']), _y3 + _h2)
                _p06 = (float(self.report2.dwg['x']), _y3 + _h2)
                _p07 = (self.report1.x_max, _y1 + _h1)
                _p08 = (_x1, _y1 + _h1)

                _line = Polyline(points=[_p01, _p02, _p03, _p04, _p05, _p06, _p07, _p08, _p01],
                                 stroke_width="0.5",
                                 stroke=xtype.fill,
                                 fill=xtype.fill,
                                 opacity=xtype.opacity)

                self.dwg.add(_line)

    def drawChangedPattern(self, xtype, xelements, x_offset=0):

        for _e in XTypes.LOOP(xelements, xtype):
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

    def __init__(self):
        DrawXml.__init__(self)

    def linesCallback(self, text):
        return [('', 40, 10)]


class DrawXmlDiffBoxesOnly(DrawXmlDiff):

    def __init__(self, path1, path2):
        DrawXmlDiff.__init__(self, path1, path2)
        self.report1 = DrawXmlBoxesOnly()
        self.report2 = DrawXmlBoxesOnly()
