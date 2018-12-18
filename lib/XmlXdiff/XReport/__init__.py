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
from XmlXdiff import XDiffer


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
        self.y_max = 0
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

    def walkElementTree(self, element, path="", path_dict={"": 0}, visited=[]):

        if not(path in visited):
            visited.append(path)

            # path building syntax has to be in line with XDiffer
            if isinstance(element, lxml.etree._Comment):
                _tag = "comment()"
            else:
                if element.tag.find("{") > -1:
                    for _ns in element.nsmap.keys():

                        _nslong = "{{{nslong}}}".format(
                            nslong=element.nsmap[_ns])
                        if _ns is None:
                            _nsshort = ""
                        else:
                            _nsshort = "{nsshort}:".format(nsshort=_ns)

                        _tag = element.tag.replace(_nslong, _nsshort)

                        if _tag.find("{") < 0:
                            break
                else:
                    _tag = element.tag

            _path_key = "{path}/{tag}".format(path=path, tag=_tag)

            if _path_key in path_dict.keys():
                path_dict[_path_key] = path_dict[_path_key] + 1
            else:
                path_dict[_path_key] = 1

            if isinstance(element, lxml.etree._Comment):
                _path = "{path}/{tag}[{cnt}]".format(path=path,
                                                     tag=_tag, cnt=path_dict[_path_key])

            else:
                _path = "{path}/*[name()='{tag}'][{cnt}]".format(path=path,
                                                                 tag=_tag,
                                                                 cnt=path_dict[_path_key])

            self.svg_elements[_path] = self.addLine(
                self.getElementText(element))

            self.moveRight()

            for _child in element.getchildren():
                self.walkElementTree(_child, _path, path_dict)

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
        self._d = {}
        self._a = []
        self.walkElementTree(self.root, "", self._d, self._a)

    def addLine(self, path):
        self.y = self.y + (0.6 * self.unit)
        self.y_max = max(self.y_max, self.y)

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

        _path = path1
        _path = _path.replace("\\", "/")
        _path = _path[:_path.rfind("/")].replace("/", "\\")

        self.differ = XDiffer.XDiffExecutor()
        self.differ.path1 = path1
        self.differ.path2 = path2
        self.differ.run()

        self.report1 = DrawXml()
        self.report1.moveRight()
        self.report1.loadFromFile(self.differ.path1)
        self.report1.saveSvg()

        self.report2 = DrawXml()
        self.report2.moveRight()
        self.report2.loadFromFile(self.differ.path2)
        self.report2.saveSvg()

        self.legend = DrawLegend()

        self.filepath = "{path}\\xdiff_{filename1}_{filename2}.svg".format(path=_path,
                                                                           filename1=self.report1.filename,
                                                                           filename2=self.report2.filename)

        self.report2.dwg['x'] = self.report1.x_max * 2.0
        self.report2.dwg['y'] = 0

        self.legend.dwg['x'] = self.report2.x_max * 4.0
        self.legend.dwg['y'] = 0

        self.dwg = svgwrite.Drawing(filename=self.filepath)
        self.dwg['height'] = max(self.report2.y_max, self.report1.y_max) * 3
        self.dwg['width'] = 350 * 3
        self.dwg.viewbox(0, 0, 350, 250)

        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        self.dwg.add(self.legend.dwg)

        self._mark(self.differ.pathes1, self.report1)
        self._mark(self.differ.pathes2, self.report2)

    def save(self):
        print(self.filepath)
        self.dwg.save()

    def _mark(self, pathes, report):
        for _path1 in pathes.keys():
            _, _action1 = pathes[_path1]
            print(_action1)

            _marker_class = globals()[_action1]

            report.markAs(_path1, _marker_class)


if __name__ == "__main__":

    _path1 = r'{path}\tests\test1\a.xml'.format(path=getPath())
    _path2 = r'{path}\tests\test1\b.xml'.format(path=getPath())

    x = DrawXmlDiff(_path1, _path2)
    x.save()
