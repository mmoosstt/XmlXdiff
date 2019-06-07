"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: create diff report
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

from diffx.svg import compact
from diffx.svg.compact import DrawLegend


class DrawDiffx(compact.DrawDiffx):
    '''
    Create diff without text.
    '''

    def __init__(self):
        super(DrawDiffx, self).__init__()

    def _lines_callback(self, text):
        return [('', 40, 10)]


class DrawDiffxDiff(compact.DrawDiffxDiff):
    '''
    Create diff without text.
    '''

    def __init__(self, path1, path2):
        super(DrawDiffxDiff, self).__init__(path1, path2)
        self.report1 = DrawDiffx()
        self.report2 = DrawDiffx()
