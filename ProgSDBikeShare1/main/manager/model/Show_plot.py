import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import geopandas

sys.path.append("..")
from main.manager.manager import *
import random


class App(QMainWindow):

    def __init__(self, i=0):
        super().__init__()
        self.des = i
        self.left = 10
        self.top = 10
        self.title = 'Plot'
        self.width = 1200
        self.height = 1200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, i=self.des, width=7, height=7)
        m.move(0, 0)

        self.back = QPushButton('Return to Main', self)
        self.back.setToolTip('This s an example button')
        self.back.move(1000, 0)
        self.back.resize(140, 100)

        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100, i=0):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.des = i
        self.ma = mananger()
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        if self.des == 1:
            self.start_popularity()
        elif self.des == 2:
            self.end_popularity()
        elif self.des == 3:
            self.top_user()
        elif self.des == 4:
            self.spent_most()
        elif self.des == 5:
            self.monthly_report()
        elif self.des == 6:
            self.yearly_report()
        elif self.des == 7:
            self.operator_efficiency()

    def start_popularity(self):
        x = self.ma.starting_population()
        ax = self.figure.add_subplot(111)
        ax.barh(x['Name'], x['Number'])
        ax.tick_params(labelsize=5)
        ax.grid(True)
        self.draw()

    def geo_start(self):
        ax = self.figure.add_subplot(111)
        scatter = self.ma.start_scatter()
        ax.scatter(scatter['LAT'], scatter['LON'], (50 * scatter['Number'] / np.mean(scatter['Number'])),
                   c='red', alpha=0.5, zorder=10)
        self.draw()

    def end_popularity(self):
        tmp = self.ma.ending_population()
        ax = self.figure.add_subplot(111)
        ax.bar(tmp['Name'], tmp['Number'])
        ax.tick_params(labelsize=5, rotation=-15)
        ax.grid(True)
        self.draw()

    def top_user(self):
        tmp = self.ma.top_user()
        ax = self.figure.add_subplot(111)
        ax.bar(tmp['Name'], tmp['Number'])
        ax.tick_params(labelsize=5)
        ax.grid(True)
        self.draw()

    def spent_most(self):
        tmp = self.ma.spent_most()
        ax = self.figure.add_subplot(111)
        ax.bar(tmp['Name'], tmp['Money'])
        ax.tick_params(labelsize=5)
        ax.grid(True)
        self.draw()

    def monthly_report(self):
        tmp = self.ma.monthly_report()
        ax = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)
        ax.plot(tmp['Date'], tmp['Number'], marker='o', mfc='black', linewidth=4)
        ax2.plot(tmp['Date'], tmp['money'], 'orange', marker='o', mfc='black', linewidth=4)
        ax.tick_params(labelsize=5)
        ax2.tick_params(labelsize=5)
        tmp = self.ma.monthly_report_2()
        ax3 = self.figure.add_subplot(111)
        ax3.plot(tmp['Date'], tmp['Number'], 'red', marker='o', mfc='black')
        ax3.tick_params(labelsize=5)
        ax3.legend(['Rent frequency', 'Profit', 'Report'], loc=1)

        self.draw()

    def yearly_report(self):
        tmp = self.ma.yearly_report()
        ax = self.figure.add_subplot(111)
        ax.plot(tmp['Date'], tmp['Number'], marker='o', mfc='black', linewidth=4)
        self.draw()

    def operator_efficiency(self):
        tmp = self.ma.yearly_report()
        ax = self.figure.add_subplot(111)
        ax.pie(tmp['Number'], labels=tmp['OP_NAME'], autopct='%1.1f%%')
        ax.axis('equal')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
