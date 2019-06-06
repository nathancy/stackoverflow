from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QApplication
from PyQt5.QtCore import QTimer 
import time
import sys

class Ui_LoginUi(object):
    def setupUi(self, Ui_LoginUi):
        Ui_LoginUi.setObjectName("LoginUi")
        Ui_LoginUi.resize(293, 105)
        self.layout = QVBoxLayout(Ui_LoginUi)
        self.le_test = QLineEdit(Ui_LoginUi)
        self.layout.addWidget(self.le_test)

class LoginDialog(QDialog, Ui_LoginUi):

    def __init__(self):
        super(LoginDialog, self).__init__()
        self.setupUi(self)

        self.invalid_color = 'background-color: #c91d2e'
        self.valid_color = 'background-color: #FFF'
        self.le_test.textChanged.connect(self.redFlashHandler)

    def redFlashHandler(self):
        if self.le_test.text() == 'test':
            self.le_test.setStyleSheet(self.invalid_color)

            # After 2000 ms, reset field color
            QTimer.singleShot(2000, self.resetFieldColor)

    def resetFieldColor(self):
        self.le_test.setStyleSheet(self.valid_color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())
