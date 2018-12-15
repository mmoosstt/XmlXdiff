import lxml.etree
import svgwrite
from svgwrite import cm, mm, rgb
from svgwrite.data.full11 import elements

from svgwrite.container import Group
from svgwrite.shapes import Rect
from svgwrite.text import Text, TSpan, TextArea
from importlib.resources import path
from lxmldiff import getPath


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
        self.fill_blue = rgb(0,0,200)
        self.fill = self.fill_red
        self.blue = 0
        
    def getElementText(self, element):
        
        if isinstance(element, lxml.etree._Comment):
            _tag = "!comment"
        else:
            _tag = element.tag[element.tag.find("}")+1:]
        _attribs = " "
        for _akey in sorted(element.attrib.keys()):
            _attribs = " {name}='{value}' ".format(name=_akey, value=element.attrib[_akey])
        
        _attribs = _attribs[:-1]
        
        return "{tag}{attribs}: {text}".format(attribs=_attribs,tag=_tag, text=element.text)
    
    def walkElementTree(self, element):
        
        _xml_path = self.xml.getpath(element)
        self.svg_elements[_xml_path] = self.addLine(self.getElementText(element))
        self.moveRight()
        for _child in element.getchildren():
            self.walkElementTree(_child)
            
        self.moveLeft()        

    def loadFromFile(self, _filepath):
        self.xml = lxml.etree.parse(_filepath)
        self.root = self.xml.getroot()
        _filepath = _filepath.replace("\\", "/")
        self.filename = _filepath[_filepath.rfind("/")+1:_filepath.rfind('.')]
        self.filepath = _filepath[:_filepath.rfind("/")].replace("/", "\\")
        self.file_path_svg = "{}.svg".format(_filepath[:_filepath.rfind('.')])
        self.dwg = svgwrite.Drawing(filename=self.file_path_svg)
        self.walkElementTree(self.root)

    def addLine(self, path):
        self.y = self.y + (0.6 * self.unit)
       
        self.blue = self.blue + 25
        
        if self.blue > 250:
            self.blue = 0
            
        _text = Text(path,fill=rgb(0,0,self.blue),insert=(self.x, self.y),font_size="25%")
        
        return _text
    

    def moveLeft(self):
        self.x = self.x-1.2*self.unit
      
    def moveLeftSvgElement(self, svg_element):
        _return = {}
        svg_element['x'] = float(svg_element['x']) - 1.2 * self.unit

    def moveRightSvgElement(self, svg_element):
        _return = {}
        svg_element['x'] = float(svg_element['x']) + 1.2 * self.unit       
        
    def copyPositionSvgElement(self, svg_element_src, svg_element_tar):    
        svg_element_tar['x'] = svg_element_src['x']
        svg_element_tar['y'] = svg_element_src['y']
        
    def moveRight(self):
        self.x = self.x+1.2*self.unit
        self.x_max = max(self.x_max, self.x)
        
    def moveTop(self):
        self.fill = self.fill_blue
        self.y = 0.3*self.unit
        self.x = self.x_max + (5.5*self.unit)
        
    def saveSvg(self):
        for _key in self.svg_elements.keys():
            self.dwg.add(self.svg_elements[_key])
        
        self.dwg.save()
        
    def markAsAdded(self, path):
        
        _svg_element = self.svg_elements[path]
        _svg_rect = Rect(size=(2.5, 2.5), fill=rgb(200,0,0))
        
        self.copyPositionSvgElement(_svg_element, _svg_rect)
        self.moveLeftSvgElement(_svg_rect)
        
        _svg_rect['y'] = (float(_svg_rect['y']) - 0.3 * self.unit)
        _svg_rect['x'] = (float(_svg_rect['x']) + 0.3 * self.unit)
        
        self.dwg.add(_svg_rect)

    def markAsDeleted(self, path):
        
        _svg_element = self.svg_elements[path]
        _svg_rect = Rect(size=(2.5, 2.5), fill=rgb(200,0,0))
        
        self.copyPositionSvgElement(_svg_element, _svg_rect)
        self.moveLeftSvgElement(_svg_rect)
        
        _svg_rect['y'] = (float(_svg_rect['y']) - 0.3 * self.unit)
        _svg_rect['x'] = (float(_svg_rect['x']) + 0.3 * self.unit)
        
        self.dwg.add(_svg_rect)
        
    def markAsMoved(self, path):
        _svg_element = self.svg_elements[path]
        _svg_rect = Rect(size=(2.5, 2.5), fill=rgb(0,200,0))
        
        self.copyPositionSvgElement(_svg_element, _svg_rect)
        self.moveLeftSvgElement(_svg_rect)
        
        _svg_rect['y'] = (float(_svg_rect['y']) - 0.3 * self.unit)
        _svg_rect['x'] = (float(_svg_rect['x']) + 0.3 * self.unit)
        
        self.dwg.add(_svg_rect)                  

    def markAsUndefined(self, path):
        _svg_element = self.svg_elements[path]
        _svg_rect = Rect(size=(2.5, 2.5), fill=rgb(230,230,0))
        
        self.copyPositionSvgElement(_svg_element, _svg_rect)
        self.moveLeftSvgElement(_svg_rect)
        
        _svg_rect['y'] = (float(_svg_rect['y']) - 0.3 * self.unit)
        _svg_rect['x'] = (float(_svg_rect['x']) + 0.3 * self.unit)
        
        self.dwg.add(_svg_rect)   
                 
class DrawXmlDiff(object):
    
    def __init__(self):
 
        self.report1 = DrawXml()
        self.report1.moveRight()
        self.report1.loadFromFile(r'C:\Users\morit\git\xml-diff\lxmldiff\tests\test1\a.xml')
        self.report1.saveSvg()
    
        self.report2 = DrawXml()
        self.report2.moveRight()
        self.report2.loadFromFile(r'C:\Users\morit\git\xml-diff\lxmldiff\tests\test1\b.xml')
        self.report2.saveSvg()
    
        self.filepath = "{path}\\doc\\example_diff_{filename1}_{filename2}.svg".format(path=getPath(), 
                                                                 filename1=self.report1.filename, 
                                                                 filename2=self.report2.filename)
        
        self.report2.dwg['x'] = self.report1.x_max *2.0
        self.report2.dwg['y'] = 0
        
        self.dwg = svgwrite.Drawing(filename =self.filepath)
        
        self.dwg.add(self.report1.dwg)
        self.dwg.add(self.report2.dwg)
        
        
    def save(self):
        self.dwg.save()
        
        
if __name__ == "__main__":
    import lxmldiff.xDiffCore
    
    _diff = lxmldiff.xDiffCore.xDiffExecutor()
    _diff.path1 = r'C:\Users\morit\git\xml-diff\lxmldiff\tests\test1\a.xml'
    _diff.path2 = r'C:\Users\morit\git\xml-diff\lxmldiff\tests\test1\b.xml'
    _diff.run()
    
    
    
    x = DrawXmlDiff()

    def mark(pathes, report):
        for _path1 in pathes.keys():
            _, _action1 = pathes[_path1]
            print(_action1)
            
            if _action1 == "ElementMoved":
                report.markAsMoved(_path1)
    
            elif _action1 == "ElementDeleted":
                report.markAsDeleted(_path1)
    
            elif _action1 == "ElementAdded":
                report.markAsAdded(_path1)
                
            elif _action1 == "ElementUnchanged":
                pass
            
            else:
                report.markAsUndefined(_path1)    

    mark(_diff.pathes1, x.report1)
    mark(_diff.pathes2, x.report2)
            
    x.save()
    