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
    _app = None
    font = None
    font_size = None
    font_family = None
    font_generator = None
    font_metrics = None
    max_textbox_len = 300  # px

    @classmethod
    def _init_font_interface(cls):
        '''
        static init interface, font family and font size have to be
        set first. This function does not have to be called.
        '''

        # should move to main
        # workaround
        if cls._app is None:
            try:
                cls._app = QApplication(sys.argv)
            except RuntimeError:
                cls._app = False

        if (cls.font_size is not None and cls.font_family is not None):
            cls.font = QFont(cls.font_family, cls.font_size)
            cls.font_metrics = QFontMetricsF(cls.font, QSvgGenerator())

    @classmethod
    def set_font_family(cls, inp):
        '''
        set font family
        :param inp: str - "arial"
        '''
        cls.font_family = inp
        cls._init_font_interface()

    @classmethod
    def set_font_size(cls, inp):
        '''
        set font size

        :param inp: int - size in px (pixels)
        '''

        cls.font_size = inp
        cls._init_font_interface()

    @classmethod
    def get_text_size(cls, text):
        """
            calculates the height and width of the input text string.

            return: (width, height)

        :param text: str - input text
        """
        return (cls.font_metrics.width(text), cls.font_metrics.height())

    @classmethod
    def split_text_to_lines(cls, text, offset=0):
        """
            Split Into Max TextBoxSize

            return = [(text1:str, width1:int, height1:int), (text1, width2, height2), (..)]
        """

        def _get_text_segment(text):
            '''
            find the first wigth space from the right side
            '''

            _len_text = len(text)

            def _get_valid_index(inp_str):
                _index = text.rfind(inp_str)

                # not found
                if _index == -1:
                    return False

                # with zero the length will not be shortened
                if _index == 0:
                    return False

                _delta = _len_text - _index

                # the delta is to high for used text box size
                if _delta > (cls.max_textbox_len - offset):
                    return False

                return _index

            index = _get_valid_index("\t")
            if not index:

                index = _get_valid_index(" ")
                if not index:
                    index = abs(len(text) - 50)

            return text[:index]

        _text = text.strip()
        _text = _text.replace('\n', '\n%NewLine%\n')
        _lines = _text.split('\n')
        _text_array = []
        _max_width = cls.max_textbox_len - offset
        _cnt = 0

        for _text in _lines:
            _text_width = (cls.max_textbox_len + 10)

            while _text_width > _max_width:
                _text_width, _text_height = cls.get_text_size(_text)

                # too long
                if _text_width > _max_width:

                    # create shorter string
                    _text_segment = copy.deepcopy(_text)
                    _text_segment_z = copy.deepcopy(_text)
                    _text_segment_width = cls.max_textbox_len + 10

                    while _text_segment_width > _max_width:
                        _text_segment = _get_text_segment(_text_segment)
                        _text_segment_width, _text_segment_height = cls.get_text_size(
                            _text_segment)

                        # exit if fragment does not change anymore
                        if _text_segment == _text_segment_z:
                            break

                        else:
                            _text_segment_z = _text_segment

                    _text_array.append((_text_segment, _text_segment_width, _text_segment_height))
                    _max_width = cls.max_textbox_len

                    # rest of string
                    _text = _text[len(_text_segment):]

                else:
                    _text_array.append((_text, _text_width, _text_height))
                    _max_width = cls.max_textbox_len

        return _text_array
