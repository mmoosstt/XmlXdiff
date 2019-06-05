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

from xml_xdiff import get_path
from xml_xdiff import differ
from xml_xdiff.report import render_text
from xml_xdiff.xpath import XDiffXmlPath
from xml_xdiff import base


class TextBoxCompare:

    def __init__(self):
        self.max_line_width = render_text.Render.max_textbox_len
        self.pos_x = 0
        self.pos_y = 0
        self.act_line_width = 0
        self.font_family = None
        self.font_size = None
        self.width, self.height_line = render_text.Render.get_text_size("")
        self.height = self.height_line
        self.width_max = 0
        self.svg_text = Text(text="")

    def build_svg_line(self, line_fragment, fill):
        _lines = render_text.Render.split_text_to_lines(line_fragment, self.act_line_width)
        _line, _w, _h = _lines[0]

        if self.svg_text is None:
            self.svg_text = Text(text="")

        if len(_lines) == 1 and self.act_line_width < self.max_line_width:
            self.svg_text.add(TSpan(text=_line, fill=fill))
            self.act_line_width += _w
            self.width_max = max(self.act_line_width, self.width_max)

        elif len(_lines) == 1 and self.act_line_width >= self.max_line_width:
            self.svg_text.add(TSpan(text=_line, fill=fill))
            self.svg_text["x"] = 0
            self.svg_text["y"] = self.height
            self.svg.add(self.svg_text)
            self.height += _h
            self.act_line_width = 0
            self.svg_text = None

        elif len(_lines) > 1:

            for _line, _w, _h in _lines:

                if self.svg_text is None:
                    self.svg_text = Text(text="")

                if _line == "%NewLine%":
                    self.svg_text["x"] = 0
                    self.svg_text["y"] = self.height
                    self.svg.add(self.svg_text)
                    self.height += _h
                    self.act_line_width = 0
                    self.svg_text = None

                elif self.act_line_width < self.max_line_width:
                    self.svg_text.add(TSpan(text=_line, fill=fill))
                    self.act_line_width += _w
                    self.width_max = max(self.act_line_width, self.width_max)

                else:

                    self.svg_text["x"] = 0
                    self.svg_text["y"] = self.height
                    self.svg.add(self.svg_text)
                    self.height += _h
                    self.act_line_width = _w
                    self.width_max = max(self.act_line_width, self.width_max)
                    self.svg_text = None

    def compare(self, text_block1, text_block2):

        self.svg = SVG(insert=(self.pos_x, self.pos_y),
                       font_family=self.font_family,
                       font_size=self.font_size)

        _len_textblock1 = len(text_block1)
        _len_textblock2 = len(text_block2)

        if text_block1 == text_block2:
            _fill = rgb(0x00, 0x0, 0x0)
            self.build_svg_line(text_block2, _fill)

        elif _len_textblock1 > 0 and _len_textblock2 > 0:
            _matcher = SequenceMatcher(None, text_block1, text_block2)

            for tag, _s1, _e1, _s2, _e2 in _matcher.get_opcodes():

                if tag == "replace":
                    _text = text_block2[_s2:_e2]
                    _fill = rgb(0x00, 0x80, 0xff)
                    self.build_svg_line(_text, _fill)

                elif tag == "delete":
                    pass

                elif tag == "insert":
                    _text = text_block2[_s2:_e2]
                    _fill = rgb(0x00, 0x80, 0xff)
                    self.build_svg_line(_text, _fill)

                elif tag == "equal":
                    _text = text_block1[_s1:_e1]
                    _fill = rgb(0x0, 0x0, 0x0)
                    self.build_svg_line(_text, _fill)

        elif _len_textblock1 == 0 and _len_textblock2 > 0:
            _fill = rgb(0x00, 0x0, 0x0)
            self.build_svg_line(text_block2, _fill)

        elif _len_textblock1 > 0 and _len_textblock2 == 0:
            _fill = rgb(0x00, 0x0, 0x0)
            self.build_svg_line(text_block1, _fill)

        else:
            _fill = rgb(0x00, 0x0, 0x0)
            self.build_svg_line("", _fill)

        if self.svg_text is not None:
            self.svg_text["x"] = 0
            self.svg_text["y"] = self.height
            self.svg.add(self.svg_text)

            self.height += self.height_line * 0.3
            self.svg_text = None

        self.svg['height'] = self.height
        self.svg['width'] = self.width_max

        return self.svg, self.width_max, self.height


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

        render_text.Render.set_font_family(self.font_family)
        render_text.Render.set_font_size(self.font_size)

        self.dwg = svgwrite.Drawing()
        self._move_right()

        _svg = SVG(insert=(self.pos_x, self.pos_y))

        for _class in base.generator_available_xtypes():
            _svg.add(self.add_line(_class))

        _svg["width"] = self.pos_x_max
        _svg["height"] = self.pos_y_max
        self.dwg["width"] = self.pos_x_max
        self.dwg["height"] = self.pos_y_max

        self.dwg.add(_svg)

    def add_line(self, instance_xtype):
        '''
        Draw svg line representing XElement.

        :param instance_xtype: XTypes.XElement
        '''

        _text = instance_xtype.name()
        _w, _h = render_text.Render.get_text_size(_text)

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

    def _move_left(self):
        '''
        Positioning within svg.
        '''

        self.pos_x = self.pos_x - 1.2 * self.unit

    def _move_right(self):
        '''
        Positioning within svg
        '''

        self.pos_x = self.pos_x + 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def save_svg(self, filepath=None):
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

        render_text.Render.set_font_family(self.font_family)
        render_text.Render.set_font_size(self.font_size)
        self.pos_y = render_text.Render.font_metrics.height() * 2

    def get_element_text(self, element):
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

    def load_from_xelements(self, xelements, callback):
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
                    self._move_right()

            elif _steps < 0:

                for _x in range(abs(_steps)):
                    self._move_left()

            _xelement.add_svg_node(callback(_xelement))

    def _lines_callback(self, text):
        '''
        For debugging purpose.

        :param text: str - line
        '''

        return render_text.Render.split_text_to_lines(text)

    def add_text_box(self, xelement):
        '''
        Simple text box with fixed width.

        :param xelement: XTypes.XElement
        '''
        _text = self.get_element_text(xelement.node)
        _lines = self._lines_callback(_text)

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

    def add_text_block_compare(self, text_block1, text_block2):
        '''
        Create difference of to text lines.

        :param line1: str
        :param line2: str
        '''

        _tc = TextBoxCompare()
        _tc.pos_x = self.pos_x
        _tc.pos_y = self.pos_y
        _tc.font_family = render_text.Render.font_family
        _tc.font_size = render_text.Render.font_size

        svg, width_max, height = _tc.compare(text_block1, text_block2)

        return svg, width_max, height

    def _move_left(self):
        self.pos_x = self.pos_x - 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def _move_right(self):
        self.pos_x = self.pos_x + 1.2 * self.unit
        self.pos_x_max = max(self.pos_x_max, self.pos_x)

    def _move_top(self):
        self.fill = self.fill_blue
        self.pos_y = 0.3 * self.unit
        self.pos_x = self.pos_x_max  # + (5.5 * self.unit)

    def save_svg(self, xelements):
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
        self.differ = differ.XDiffExecutor()
        self.report1 = DrawXml()
        self.report2 = DrawXml()

    def draw(self):
        '''
        Starts diff creation.
        '''

        self.differ.set_left_path(self.path1)
        self.differ.set_right_path(self.path2)
        self.differ.execute()

        self.filepath = "{path}\\xdiff_{filename1}_{filename2}.svg".format(path=self.differ.path1.path,
                                                                           filename1=self.differ.path1.filename,
                                                                           filename2=self.differ.path2.filename)

        self.report1._move_right()
        self.report1.load_from_xelements(self.differ.xelements1,
                                         self.report1.add_text_box)
        self.report1.save_svg(self.differ.xelements1)

        self.report2._move_right()
        self.report2.load_from_xelements(self.differ.xelements2,
                                         self.report2.add_text_box)
        self.report2.save_svg(self.differ.xelements2)

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

        self._draw_move_pattern(base.ElementMoved)
        self._draw_move_pattern(base.ElementMovedParent)
        self._draw_move_pattern(base.ElementUnchanged)
        self._draw_move_pattern(base.ElementTagAttributeNameConsitency)
        self._draw_move_pattern(base.ElementTextAttributeValueConsitency)
        self._draw_move_pattern(base.ElementTagConsitency)
        self._draw_move_pattern(base.ElementTagAttributeNameValueConsitency)

        self._draw_changed_pattern(base.ElementChanged,
                                   self.differ.xelements2,
                                   self.report1.pos_x_max * 1.2)

        self._draw_changed_pattern(base.ElementAdded,
                                   self.differ.xelements2,
                                   self.report1.pos_x_max * 1.2)

        self._draw_changed_pattern(base.ElementDeleted,
                                   self.differ.xelements1)

    def save_svg(self, filepath=None):
        '''
        Save svg to filepath

        :param filepath: str
        '''

        if filepath is not None:
            self.dwg.filename = filepath
            self.filepath = filepath

        self.dwg.save()

    def _draw_move_pattern(self, xtype):

        for _e in base.generator_xtypes(self.differ.xelements1, xtype):
            _start_svg1 = _e.svg_node

            if _e.get_xelement():
                _stop_svg2 = _e.get_xelement().svg_node

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

    def _draw_changed_pattern(self, xtype, xelements, x_offset=0):

        for _e in base.generator_xtypes(xelements, xtype):
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