import sys
import copy
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgGenerator
from PySide2.QtGui import QFontMetricsF, QFont


class Render(object):

    app = QApplication(sys.argv)

    font = None
    font_size = None
    font_family = None
    font_generator = None
    font_metrics = None
    max_textbox_len = 400

    @classmethod
    def _initFontInterface(cls):
        if (cls.font_size is not None and cls.font_family is not None):
            cls.font = QFont(cls.font_family, cls.font_size)
            cls.font_metrics = QFontMetricsF(cls.font, QSvgGenerator())

    @classmethod
    def setFontFamily(cls, inp):
        cls.font_family = inp
        cls._initFontInterface()

    @classmethod
    def setFontSize(cls, inp):
        cls.font_size = inp
        cls._initFontInterface()

    @classmethod
    def getTextSize(cls, text):

        return (cls.font_metrics.width(text), cls.font_metrics.height())

    @classmethod
    def splitTextToLines(cls, text):
        """
            Split Into Max TextBoxSize
        """

        def getTextSegment(text):
            '''
            find the first wigth space from the right side
            '''

            _len_text = len(text)

            def valid_index(c):
                _index = text.rfind(c)

                # not found
                if _index == -1:
                    return False

                # with zero the length will not be shortened
                if _index == 0:
                    return False

                _delta = _len_text - _index

                # the delta is to high for used text box size
                if _delta > cls.max_textbox_len:
                    return False

                return _index

            index = valid_index("\n")
            if not index:

                index = valid_index("\t")
                if not index:

                    index = valid_index(" ")
                    if not index:
                        index = abs(len(text) - 50)

            return text[:index]

        _width = cls.max_textbox_len + 10
        _text = []

        while _width > cls.max_textbox_len:

            _width, _height = cls.getTextSize(text)

            if _width > cls.max_textbox_len:

                _line_x = copy.deepcopy(text)
                _width2 = cls.max_textbox_len + 10
                while _width2 > cls.max_textbox_len:
                    _line_x = getTextSegment(_line_x)
                    _width2, _height = cls.getTextSize(_line_x)

                _text.append(_line_x)
                text = text[len(_line_x):]
            else:
                _text.append(text)

        return _text


if __name__ == '__main__':

    Render.setFontFamily('AvantGarde')
    Render.setFontSize(30)
    print(Render.splitTextToLines(
        "hallo1 halli2 hallo3 halli4 hallo5 halli6 hallo7 halli8 hallo9 halli0 hallo1 halli2 hallo3 halli4 hallo5 halli6 hallo7 halli8 hallo9 halli0 hallo halli hallo halli"))

    print(Render.splitTextToLines(
        "hallo1 halli2 hallo3 halli4 "))
