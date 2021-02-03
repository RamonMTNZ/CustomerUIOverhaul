import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Welcome_page(QWidget):
    def __init__(self):
        super().__init__()
        self.Layout = QGridLayout()

        # Set the title
        self.title = QLabel(self)
        self.title.setText("Welcome Manager Page")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedSize(480, 60)

        # set account

        account_title = QLabel()
        account_title.setText("Account")

        self.account = QLineEdit()
        self.account.setFixedSize(300, 30)
        self.account.setPlaceholderText("Account")
        self.account.setTextMargins(5, 5, 5, 5)

        # set account

        password_title = QLabel()
        password_title.setText("Password")

        self.password = QLineEdit()
        self.password.setFixedSize(300, 30)
        self.password.setPlaceholderText("Password")
        self.password.setTextMargins(5, 5, 5, 5)

        # Login button
        self.login = QPushButton()
        self.login.setText("Login")
        self.login.setFixedSize(80, 30)

        # Set a layout for widget
        self.box_layout = QVBoxLayout()
        self.box_layout.addWidget(account_title)
        self.box_layout.addWidget(self.account)
        self.box_layout.addWidget(password_title)
        self.box_layout.addWidget(self.password)
        self.box_layout.addWidget(self.login)

        # Set a display in the box
        self.box = QWidget()
        self.box.setObjectName("box")
        self.box.setContentsMargins(30, 30, 30, 30)
        self.box.setFixedSize(500, 300)
        self.box.setLayout(self.box_layout)

        # Add Widget in self body
        self.Layout.addWidget(self.title, 0, 0)
        self.Layout.addWidget(self.box, 1, 0)
        self.setLayout(self.Layout)
        self.setFixedSize(700, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Welcome_page()
    ex.show()
    sys.exit(app.exec_())
