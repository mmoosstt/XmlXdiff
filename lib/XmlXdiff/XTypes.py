from inspect import isclass


class XElement(object):

    def __init__(self):
        self.hash = None
        self.xpath = None
        self.type = None
        self.node = None
        self.svg_node = None
        self.xelements = []

    def addSvgNode(self, inp):
        self.svg_node = inp

    def addXelement(self, xelement):
        self.xelements.append(xelement)

    def setNode(self, inp):
        self.node = inp

    def setType(self, inp):
        if isclass(inp):
            self.type = inp()
        else:
            self.type = inp

    def setXpath(self, inp):
        self.xpath = inp

    def setHash(self, inp):
        self.hash = inp


class XType(object):
    pass


class ElementCopied(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUntouched(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementMoved(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnchanged(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementChanged(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementDeleted(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementAdded(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementVerified(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagConsitency(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTextAttributeValueConsitency(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementUnknown(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementTagAttributeNameConsitency(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


class ElementNameConsitency(XType):

    def __init__(self):
        super(self.__class__, self).__init__()


def LOOP(elements, *element_types):

    for _element in elements:
        if isinstance(_element.type, element_types):
            yield _element
