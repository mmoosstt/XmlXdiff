import PySide2.QtWidgets
import pyqtgraph


class TraidingWidget(PySide2.QtWidgets.QWidget):

    color_cnt = 1

    def __init__(self, parent=None):
        PySide2.QtWidgets.QWidget.__init__(self, parent)

        self.plotWidgets = {}
        self.plotWidgets["plot1"] = {}
        self.plotWidgets["plot1"]["widget"] = pyqtgraph.PlotWidget(
            self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.plotWidgets["plot1"]["curves"] = {}
        self.plotWidgets["plot1"]["curves"]["value_mean"] = {}
        self.plotWidgets["plot1"]["curves"]["value_mean"]["widget"] = self.plotWidgets["plot1"]["widget"].plot()
        self.plotWidgets["plot1"]["curves"]["value_mean"]["x"] = self.GroundControl.logger.ring_trades_time
        self.plotWidgets["plot1"]["curves"]["value_mean"]["y"] = self.GroundControl.logger.ring_value_mean_quantity


if __name__ == "__main__":

    app = PySide2.QtWidgets.QApplication([])
    MainWidget = TraidingWidget()
    MainWidget.resize(800, 800)
    MainWidget.show()
    app.exec_()