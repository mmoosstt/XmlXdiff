import sys
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


test_svg = """
 <svg>
  <rect x="0" y="0" width="{width}" height="{height}" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
  <text font-family="{font_family}" font-size="{font_size}" x="0" y="{y}" width="{width}" height="{height}" >{text}</text>
</svg> 
"""


if __name__ == '__main__':

    Render.setFontFamily('AvantGarde')
    Render.setFontSize(30)
    print(Render.getTextSize("hallo halli hallo halli"))
