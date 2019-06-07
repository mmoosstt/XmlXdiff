"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""
from svgwrite.container import SVG
from diffx.svg import compact
from diffx.svg.compact import DrawLegend


class DrawDiffx(compact.DrawDiffx):
    '''
    Draw svg signle xml
    '''

    def __init__(self):
        compact.DrawDiffx.__init__(self)

    def add_text_box(self, xelement):
        '''
        Text box with fixed width and content text diff.

        :param xelement: XTypes.DiffxElement
        '''

        _node_text1 = self.get_element_text(xelement.node)

        if xelement.get_xelement() is None:
            _node_text2 = ""
        else:
            _node_text2 = self.get_element_text(xelement.get_xelement().node)

        _svg, _width, _height = self.add_text_block_compare(_node_text1, _node_text2)
        self.pos_y = self.pos_y + float(_height)
        self.pos_y_max = max(self.pos_y_max, self.pos_y)
        self.pos_x_max = max(self.pos_x_max, self.pos_x + float(_width))

        return _svg


class DrawDiffxDiff(compact.DrawDiffxDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        compact.DrawDiffxDiff.__init__(self, path1, path2)
        self.report1 = DrawDiffx()
        self.report2 = DrawDiffx()
