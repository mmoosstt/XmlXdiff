import lxml.etree
import svgwrite
import copy

from svgwrite import cm, mm, rgb
from svgwrite.data.full11 import elements

from svgwrite.container import Group, SVG
from svgwrite.shapes import Rect, Polyline
from svgwrite.text import Text, TSpan, TextArea
from importlib.resources import path
from XmlXdiff import getPath
from inspect import isclass
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


class ElementMoved(ElementMarker):
    fill = rgb(0x1e, 0x2d, 0xd2)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnchanged(ElementMarker):
    fill = rgb(0x7e, 0x62, 0xa1)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementChanged(ElementMarker):
    fill = rgb(0xaa, 0xa6, 0x7f)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementDeleted(ElementMarker):
    fill = rgb(0xff, 0x00, 0xff)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementAdded(ElementMarker):
    fill = rgb(0x91, 0xdf, 0x4e)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementVerified(ElementMarker):
    fill = rgb(0xcd, 0x5d, 0x47)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagConsitency(ElementMarker):
    fill = rgb(0x55, 0x8d, 0x30)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTextAttributeValueConsitency(ElementMarker):
    fill = rgb(0x66, 0xb2, 0x7e)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnknown(ElementMarker):
    fill = rgb(0x5c, 0xa3, 0x43)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagAttributeNameConsitency(ElementMarker):
    fill = rgb(150, 50, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementNameConsitency(ElementMarker):
    fill = rgb(0xec, 0x91, 0xf8)

    def __init__(self):
        super(self.__class__, self).__init__()


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

        self.filepath = "{path}\\..\\..\\doc\\legend.svg".format(
            path=getPath())

        self.dwg = svgwrite.Drawing(self.filepath)

        self.moveRight()
        self.moveRight()

        for _class in ElementMarker.__subclasses__():
            _text = self.addLine(_class.name())
            _mark = _class()
            _mark = _mark.markSvgElement(_text)

            self.dwg.add(_text)
            self.dwg.add(_mark)

        self.dwg.save()

    def addLine(self, text):
        _x, _y = XRender.Render.getTextSize(text)

        self.y = self.y + _y  # (0.6 * self.unit)
        self.x_max = max(self.x_max, _x + self.x)
        self.y_max = max(self.y_max, self.y)

        _text = Text(text, fill=rgb(0, 0, 0),
                     insert=(self.x, self.y), font_size=self.font_size, font_family=self.font_family)

        return _text

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
            _tag = element.tag[element.tag.find("}") + 1:]
        _attribs = " "
        for _akey in sorted(element.attrib.keys()):
            _attribs = " {name}='{value}' ".format(
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

    def addTextBox(self, text):
        _lines = XRender.Render.splitTextToLines(text)

        _y = copy.deepcopy(self.y)

        _svg = SVG(insert=(self.x, self.y))
        _t = Text('', insert=(0, 0), font_size=self.font_size,
                  font_family=self.font_family)

        _h = 0
        _w = 0
        for _line, _width, _height in _lines:
            _h = _h + float(_height)
            _w = max(_w, float(_width))

            _text = TSpan(_line, fill=rgb(0, 0, 255), insert=(0, _h))
            _t.add(_text)

        self.y = self.y + _h
        self.y_max = max(self.y_max, self.y)
        self.x_max = max(self.x_max, _w + self.x)

        _svg['height'] = _h
        _svg['width'] = _w
        _svg.viewbox(0, 0, _w, _h)

        _svg.add(_t)

        return _svg

    def addTextBoxLine(self, text, width, height):

        if self.blue > 250:
            self.blue = 0

        _text = TSpan(text, fill=rgb(0, 0, self.blue), insert=(self.x, self.y))

        self.y = self.y + height
        self.y_max = max(self.y_max, self.y)
        self.x_max = max(self.x_max, width + self.x)

        self.blue = self.blue + 25

        return _text

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

        self.differ = XDiffer.XDiffExecutor()
        self.differ.setPath1(path1)
        self.differ.setPath2(path2)
        self.differ.run()

        self.filepath = "{path}\\xdiff_{filename1}_{filename2}.svg".format(path=self.differ.path1.path,
                                                                           filename1=self.differ.path1.filename,
                                                                           filename2=self.differ.path2.filename)

        self.report1 = DrawXml()
        self.report1.moveRight()
        self.report1.loadFromXElements(self.differ.xelements1)
        self.report1.saveSvg(self.differ.xelements1)

        self.report2 = DrawXml()
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
        self.drawMovePattern(XTypes.ElementUnchanged)
        self.drawMovePattern(XTypes.ElementTagAttributeNameConsitency)

        self.drawChangedPattern(XTypes.ElementAdded, self.differ.xelements2)
        self.drawChangedPattern(XTypes.ElementDeleted, self.differ.xelements1)
        self.drawChangedPattern(XTypes.ElementVerified, self.differ.xelements2)
        self.drawChangedPattern(XTypes.ElementVerified, self.differ.xelements1)

    def save(self):
        print(self.filepath)
        self.dwg.save()
        pass

    def drawMovePattern(self, xtype):

        _color = globals()[xtype.__name__].fill

        for _e in XTypes.LOOP(self.differ.xelements1, xtype):
            _start_svg1 = _e.svg_node

            if _e.xelements:
                _stop_svg2 = _e.xelements[0].svg_node

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
                                 stroke_width="1",
                                 stroke=_color,
                                 fill=_color,
                                 opacity=0.1)

                self.dwg.add(_line)

    def drawChangedPattern(self, xtype, xelements):

        _color = globals()[xtype.__name__].fill

        for _e in XTypes.LOOP(xelements, xtype):
            _start_svg1 = _e.svg_node

            _x1 = float(_start_svg1['x'])
            _y1 = float(_start_svg1['y'])

            _p01 = (_x1, _y1)
            _p02 = (_x1 + _start_svg1['width'], _y1)
            _p03 = (_x1 + _start_svg1['width'],
                    _y1 + _start_svg1['height'])
            _p04 = (_x1,
                    _y1 + _start_svg1['height'])

            _line = Polyline(points=[_p01, _p02, _p03, _p04, _p01],
                             stroke_width="1",
                             stroke=_color,
                             fill=_color,
                             opacity=0.1)

            self.dwg.add(_line)


if __name__ == "__main__":

    import cProfile

    def run():
        _path1 = r'{path}\tests\test1\a.xml'.format(path=getPath())
        _path2 = r'{path}\tests\test1\b.xml'.format(path=getPath())

        x = DrawXmlDiff(_path1, _path2)
        x.save()

    cProfile.run('run()')
