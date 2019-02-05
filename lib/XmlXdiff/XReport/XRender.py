"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: get size of text within svg
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
 
"""

import sys
import copy
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgGenerator
from PySide2.QtGui import QFontMetricsF, QFont


class Render:
    '''
    Interface for getting the svg rendered size of an svg text element
    '''

    app = QApplication(sys.argv)

    font = None
    font_size = None
    font_family = None
    font_generator = None
    font_metrics = None
    max_textbox_len = 700  # px

    @classmethod
    def _initFontInterface(cls):
        '''
        static init interface, font family and font size have to be
        set first. This function does not have to be called.
        '''
        if (cls.font_size is not None and cls.font_family is not None):
            cls.font = QFont(cls.font_family, cls.font_size)
            cls.font_metrics = QFontMetricsF(cls.font, QSvgGenerator())

    @classmethod
    def setFontFamily(cls, inp):
        '''
        set font family
        :param inp: str - "arial"
        '''
        cls.font_family = inp
        cls._initFontInterface()

    @classmethod
    def setFontSize(cls, inp):
        '''
        set font size

        :param inp: int - size in px (pixels)
        '''

        cls.font_size = inp
        cls._initFontInterface()

    @classmethod
    def getTextSize(cls, text):
        """
            calculates the height and width of the input text string.

            return: (width, height)

        :param text: str - input text
        """
        return (cls.font_metrics.width(text), cls.font_metrics.height())

    @classmethod
    def splitTextToLines(cls, text):
        """
            Split Into Max TextBoxSize

            return = [(text1:str, width1:int, height1:int), (text1, width2, height2), (..)]
        """

        def getTextSegment(text):
            '''
            find the first wigth space from the right side
            '''

            _len_text = len(text)

            def getValidIndex(inp_str):
                _index = text.rfind(inp_str)

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

            index = getValidIndex("\n")
            if not index:

                index = getValidIndex("\t")
                if not index:

                    index = getValidIndex(" ")
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
                    _width2, _height2 = cls.getTextSize(_line_x)

                _text.append((_line_x, _width2, _height2))
                text = text[len(_line_x):]
            else:
                _text.append((text, _width, _height))

        return _text
