import lxml.etree


def getTag(element, pos):

    if isinstance(element, lxml.etree._Comment):
        return "comment()[{pos}]".format(pos=pos)

    else:
        return "*[name()='{name}'][{pos}]".format(name=element.tag, pos=pos)


def walk(element, parent_path, pos, visited=[]):

    _lxml_path = xml.getpath(element)
    _path = "{parent}/{tag}".format(parent=parent_path,
                                    tag=getTag(element, pos))

    print(_path)

    if not xml.xpath(_path):
        raise ""

    _pos_dict = {}
    for _child in element.getchildren():

        if _child.tag in _pos_dict.keys():
            _pos_dict[_child.tag] += 1

        else:
            _pos_dict[_child.tag] = 1

        walk(_child, _path, _pos_dict[_child.tag], visited)


xml = lxml.etree.parse(
    r'C:\Users\morit\git\XmlXdiff\lib\XmlXdiff\tests\test9\a.xml')

archive = {}
walk(xml.getroot(), "", 1)

print(len(archive.keys()))
