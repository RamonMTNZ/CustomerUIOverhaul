import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from main.manager.model import Show_plot


class decision_page(QWidget):
    def __init__(self):
        super().__init__()

        self.title = QLabel(self)
        self.title.setText("Welcome Manager Page")
        self.title.setAlignment(Qt.AlignTop)
        self.title.setFixedSize(200, 60)

        self.setGeometry(0, 0, 1280, 720)

        # each button to each graph
        # Start_station_popularity
        self.start_station_popularity = QPushButton()
        self.start_station_popularity.setText("Start_station_popularity")
        self.start_station_popularity.setFixedSize(200, 100)

        # End_station_popularity
        self.end_station_popularity = QPushButton()
        self.end_station_popularity.setText("END_station_popularity")
        self.end_station_popularity.setFixedSize(200, 100)

        # Top_user
        self.top_user = QPushButton()
        self.top_user.setText("Top_user")
        self.top_user.setFixedSize(200, 100)

        # Spent_most
        self.spent_most = QPushButton()
        self.spent_most.setText("Spent_most")
        self.spent_most.setFixedSize(200, 100)

        # monthly_report
        self.monthly_report = QPushButton()
        self.monthly_report.setText("Monthly_report")
        self.monthly_report.setFixedSize(200, 100)

        # yearly_report
        self.yearly_report = QPushButton()
        self.yearly_report.setText("Yearly_report")
        self.yearly_report.setFixedSize(200, 100)

        # operator_efficiency
        self.operator_efficiency = QPushButton()
        self.operator_efficiency.setText("Operator_efficiency")
        self.operator_efficiency.setFixedSize(200, 100)

        layout = QGridLayout()
        layout.setSpacing(2)
        layout.addWidget(self.title, 0, 1, )
        layout.addWidget(self.start_station_popularity, 1, 0)
        layout.addWidget(self.end_station_popularity, 1, 1)
        layout.addWidget(self.top_user, 1, 2)
        layout.addWidget(self.spent_most, 2, 0)
        layout.addWidget(self.monthly_report, 2, 1)
        layout.addWidget(self.yearly_report, 2, 2)
        layout.addWidget(self.operator_efficiency, 3, 0)
        self.setWindowTitle('Chart decision')
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = decision_page()
    ex.show()
    sys.exit(app.exec_())
