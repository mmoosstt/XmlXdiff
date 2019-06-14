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


class DrawDiffxNodes(compact.DrawDiffxNodes):
    '''
    Create diff without text.
    '''

    def __init__(self):
        super(DrawDiffxNodes, self).__init__()

    def _lines_callback(self, text):
        return [('', 40, 10)]


class DrawDiffxNodesCompared(compact.DrawDiffxNodesCompared):
    '''
    Create diff without text.
    '''

    def __init__(self):
        super(DrawDiffxNodesCompared, self).__init__()
        self.report1 = DrawDiffxNodes()
        self.report2 = DrawDiffxNodes()
