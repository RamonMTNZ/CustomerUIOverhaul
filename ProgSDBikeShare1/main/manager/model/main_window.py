import sys
from PyQt5.QtWidgets import *

sys.path.append("..")
from main.manager.model import Welcome_page
from main.manager.model import decision_page
from main.manager.model import Show_plot


class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.main_login()

    def main_login(self):
        self.welcome = Welcome_page.Welcome_page()
        self.welcome.setParent(self)
        self.welcome.move(390, 120)
        self.welcome.login.clicked.connect(self.welcome_fun)

    def welcome_fun(self):
        self.welcome.setVisible(False)
        self.show_page()

    def show_page(self):
        self.body = decision_page.decision_page()
        self.body.setParent(self)
        self.body.setVisible(True)
        self.body.start_station_popularity.clicked.connect(self.start_plot)
        self.body.end_station_popularity.clicked.connect(self.end_plot)
        self.body.top_user.clicked.connect(self.top_user)
        self.body.spent_most.clicked.connect(self.spent_most)
        self.body.monthly_report.clicked.connect(self.monthly_report)
        self.body.yearly_report.clicked.connect(self.yearly_report)
        self.body.operator_efficiency.clicked.connect(self.operator_efficiency)

    def back_page(self):
        self.plot_body.setVisible(False)
        self.show_page()

    def start_plot(self):
        self.plot_body = Show_plot.App(1)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def end_plot(self):
        self.plot_body = Show_plot.App(2)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def top_user(self):
        self.plot_body = Show_plot.App(3)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def spent_most(self):
        self.plot_body = Show_plot.App(4)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def monthly_report(self):
        self.plot_body = Show_plot.App(5)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def yearly_report(self):
        self.plot_body = Show_plot.App(6)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)

    def operator_efficiency(self):
        self.plot_body = Show_plot.App(6)
        self.plot_body.setParent(self)
        self.body.setVisible(False)
        self.plot_body.setVisible(True)
        self.plot_body.back.clicked.connect(self.back_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
