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

from difflib import SequenceMatcher


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

        _svg = SVG(insert=(self.x, self.y))

        for _class in XTypes.LOOP_XTYPES():
            _svg.add(self.addLine(_class))

        _svg["width"] = self.x_max
        _svg["height"] = self.y_max
        self.dwg["width"] = self.x_max
        self.dwg["height"] = self.y_max

        self.dwg.add(_svg)

    def addLine(self, class_):

        _text = class_.name()
        _w, _h = XRender.Render.getTextSize(_text)

        _h += _h * 0.25

        _svg = SVG(insert=(self.x, self.y),
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
        _rect_svg['fill'] = class_.fill
        _rect_svg['opacity'] = class_.opacity
        _rect_svg['height'] = _h
        _rect_svg['width'] = _w

        _svg.add(_text_svg)
        _svg.add(_rect_svg)

        _svg.viewbox(0, 0, _w, _h)

        self.y = self.y + _h
        self.x_max = max(self.x_max, _w + self.x)
        self.y_max = max(self.y_max, self.y)

        return _svg

    def moveLeft(self):
        self.x = self.x - 1.2 * self.unit

    def moveRight(self):
        self.x = self.x + 1.2 * self.unit
        self.x_max = max(self.x_max, self.x)

    def saveSvg(self, filepath=None):

        if filepath is not None:
            self.dwg.filename = filepath
            self.filepath = filepath

        self.dwg.save()


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

    def loadFromXElements(self, xelements, callback):

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
                    self.moveRight()

            elif _steps < 0:

                for _x in range(abs(_steps)):
                    self.moveLeft()

            _xelement.addSvgNode(callback(_xelement))

    def linesCallback(self, text):
        return XRender.Render.splitTextToLines(text)

    def addTextBox(self, xelement):
        _text = self.getElementText(xelement.node)
        _lines = self.linesCallback(_text)

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

    def addTextBox2(self, xelement):
        _node_text = self.getElementText(xelement.node)
        _lines1 = self.linesCallback(_node_text)

        if xelement.getXelement() is None:
            _lines2 = []
        else:
            _node_text2 = self.getElementText(xelement.getXelement().node)
            _lines2 = self.linesCallback(_node_text2)

        _l = max(len(_lines1), len(_lines2))

        _lines1 = _lines1 + [(' ', 0, 0)] * (_l - len(_lines1))
        _lines2 = _lines2 + [(' ', 0, 0)] * (_l - len(_lines2))

        _svg = SVG(insert=(self.x, self.y),
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

        self.y = self.y + float(_h)
        self.y_max = max(self.y_max, self.y)
        self.x_max = max(self.x_max, self.x + float(_w))

        return _svg

    def lineCompare(self, line1, line2):

        text = Text(text="")

        s = SequenceMatcher(None, line1, line2)

        _text = ''
        for tag, i1, i2, j1, j2 in s.get_opcodes():

            if tag == "replace":
                text.add(TSpan(text=line2[j1:j2], fill=rgb(0x00, 0x80, 0xff)))
                # text.add(TSpan(text=line1[i1:i2],
                #               text_decoration="line-through"))
                _text += line2[j1:j2]
                #_text += line1[i1:i2]

            elif tag == "delete":
                # text.add(TSpan(text=line1[i1:i2],
                #              text_decoration="line-through"))
                #_text += line1[i1:i2]
                pass

            elif tag == "insert":
                text.add(
                    TSpan(text=line2[j1:j2], fill=rgb(0x00, 0x80, 0xff)))
                _text += line2[j1:j2]

            elif tag == "equal":
                text.add(TSpan(text=line1[i1:i2]))
                _text += line1[i1:i2]

        w, h = XRender.Render.getTextSize(_text)

        text['y'] = h
        text['x'] = 0

        return text, w, h

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
        self.report1.loadFromXElements(
            self.differ.xelements1, self.report1.addTextBox2)
        self.report1.saveSvg(self.differ.xelements1)

        self.report2.moveRight()
        self.report2.loadFromXElements(
            self.differ.xelements2, self.report2.addTextBox2)
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

        _width = (self.report1.x_max * 1.2 +
                  self.report2.x_max * 1.2 +
                  self.legend.x_max)

        self.dwg = svgwrite.Drawing(filename=self.filepath)
        self.dwg['height'] = _height
        self.dwg['width'] = _width
        self.dwg.viewbox(0, 0, _width, _height)

        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        self.dwg.add(self.legend.dwg)

        self.drawMovePattern(XTypes.ElementMoved)
        self.drawMovePattern(XTypes.ElementMovedParent)
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
