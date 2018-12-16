import lxml.etree
import svgwrite
from svgwrite import cm, mm, rgb
from svgwrite.data.full11 import elements

from svgwrite.container import Group
from svgwrite.shapes import Rect
from svgwrite.text import Text, TSpan, TextArea
from importlib.resources import path
from XmlXdiff import getPath
from inspect import isclass


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
    fill = rgb(200, 0, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnchanged(ElementMarker):
    fill = rgb(0, 200, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementChanged(ElementMarker):
    fill = rgb(0, 0, 200)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementDeleted(ElementMarker):
    fill = rgb(100, 100, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementAdded(ElementMarker):
    fill = rgb(100, 0, 100)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementVerified(ElementMarker):
    fill = rgb(0, 100, 100)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagConsitency(ElementMarker):
    fill = rgb(150, 0, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTextAttributeValueConsitency(ElementMarker):
    fill = rgb(0, 150, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnknown(ElementMarker):
    fill = rgb(0, 0, 150)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagAttributeNameConsitency(ElementMarker):
    fill = rgb(150, 50, 0)

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementNameConsitency(ElementMarker):
    fill = rgb(150, 0, 50)

    def __init__(self):
        super(self.__class__, self).__init__()


class DrawLegend(object):

    def __init__(self):

        self.dwg = None
        self.x = 0
        self.y = 0
        self.x_max = 0
        self.unit = 10

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
        self.y = self.y + (0.6 * self.unit)

        _text = Text(text, fill=rgb(0, 0, 0),
                     insert=(self.x, self.y), font_size="25%")

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
        self.unit = 10
        self.svg_elements = {}
        self.xml = "xml1"
        self.fill_red = rgb(200, 0, 0)
        self.fill_blue = rgb(0, 0, 200)
        self.fill = self.fill_red
        self.blue = 0

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

    def walkElementTree(self, element):

        _xml_path = self.xml.getpath(element)
        self.svg_elements[_xml_path] = self.addLine(
            self.getElementText(element))
        self.moveRight()
        for _child in element.getchildren():
            self.walkElementTree(_child)

        self.moveLeft()

    def loadFromFile(self, _filepath):
        self.xml = lxml.etree.parse(_filepath)
        self.root = self.xml.getroot()
        _filepath = _filepath.replace("\\", "/")
        self.filename = _filepath[_filepath.rfind(
            "/") + 1:_filepath.rfind('.')]
        self.filepath = _filepath[:_filepath.rfind("/")].replace("/", "\\")
        self.file_path_svg = "{}.svg".format(_filepath[:_filepath.rfind('.')])
        self.dwg = svgwrite.Drawing(filename=self.file_path_svg)
        self.walkElementTree(self.root)

    def addLine(self, path):
        self.y = self.y + (0.6 * self.unit)

        self.blue = self.blue + 25

        if self.blue > 250:
            self.blue = 0

        _text = Text(path, fill=rgb(0, 0, self.blue),
                     insert=(self.x, self.y), font_size="25%")

        return _text

    def moveLeft(self):
        self.x = self.x - 1.2 * self.unit

    def moveRight(self):
        self.x = self.x + 1.2 * self.unit
        self.x_max = max(self.x_max, self.x)

    def moveTop(self):
        self.fill = self.fill_blue
        self.y = 0.3 * self.unit
        self.x = self.x_max + (5.5 * self.unit)

    def saveSvg(self):
        for _key in self.svg_elements.keys():
            self.dwg.add(self.svg_elements[_key])

        self.dwg.save()

    def markAs(self, path, mark):

        if issubclass(mark, ElementMarker):
            _mark = mark()

        _svg_element = self.svg_elements[path]
        _svg_mark = _mark.markSvgElement(_svg_element)

        self.dwg.add(_svg_mark)


class DrawXmlDiff(object):

    def __init__(self, path1, path2):

        self.report1 = DrawXml()
        self.report1.moveRight()
        self.report1.loadFromFile(path1)
        self.report1.saveSvg()

        self.report2 = DrawXml()
        self.report2.moveRight()
        self.report2.loadFromFile(path2)
        self.report2.saveSvg()

        self.legend = DrawLegend()

        self.filepath = "{path}\\..\\..\\doc\\example_diff_{filename1}_{filename2}.svg".format(path=getPath(),
                                                                                               filename1=self.report1.filename,
                                                                                               filename2=self.report2.filename)

        self.report2.dwg['x'] = self.report1.x_max * 2.0
        self.report2.dwg['y'] = 0

        self.legend.dwg['x'] = self.report2.x_max * 4.0
        self.legend.dwg['y'] = 0

        self.dwg = svgwrite.Drawing(filename=self.filepath)
        self.dwg['height'] = 250 * 3
        self.dwg['width'] = 350 * 3
        self.dwg.viewbox(0, 0, 350, 250)

        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        self.dwg.add(self.legend.dwg)

    def save(self):
        self.dwg.save()


if __name__ == "__main__":
    import XmlXdiff.XDiffer

    _diff = XmlXdiff.XDiffer.XDiffExecutor()
    _diff.path1 = r'{path}\tests\test1\a.xml'.format(path=getPath())
    _diff.path2 = r'{path}\tests\test1\b.xml'.format(path=getPath())
    _diff.run()

    x = DrawXmlDiff(_diff.path1, _diff.path2)

    def mark(pathes, report):
        for _path1 in pathes.keys():
            _, _action1 = pathes[_path1]
            print(_action1)

            _marker_class = globals()[_action1]

            report.markAs(_path1, _marker_class)

    mark(_diff.pathes1, x.report1)
    mark(_diff.pathes2, x.report2)

    x.save()

    DrawLegend()