"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: inteface for diffx
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

import os


def get_path():
    return __path__[0]


class main:
    from diffx.svg.coloured_text import DrawDiffxNodesCompared
    diffx = None

    @classmethod
    def compare_xml(cls, first_xml_content, second_xml_content):
        cls.diffx = cls.DrawDiffxNodesCompared()
        cls.diffx.set_first_xml_content(first_xml_content)
        cls.diffx.set_second_xml_content(second_xml_content)
        cls.diffx.draw()

    @classmethod
    def save(cls, filepath, pretty=False):
        if not cls.diffx.dwg is None:
            cls.diffx.dwg.saveas(filepath, pretty=pretty)

    @classmethod
    def get_string(cls):
        if not cls.diffx.dwg is None:
            return cls.diffx.dwg.tostring()

    @classmethod
    def get_etree(cls):
        if not cls.diffx.dwg is None:
            return cls.diffx.dwg.get_xml()
