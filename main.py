import sys
import os
import glob

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ftemplate import load_teplate, TEMPLATES_DIR, EXT
from ftemplate import Template, SimpleTextField, BlockTextField, ImageField, SelectField

from vars import UI_MAIN_WINDOW, UI_TEMPLATES_MANAGER, IC_APP_ICON

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(UI_MAIN_WINDOW, self)

        self.setWindowIcon(QtGui.QIcon(IC_APP_ICON))
        self.setWindowTitle(".✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.[Form Editor].✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.")

        #self.templateName.setText("NYA")

        #self.actionExit_Main.clicked.connect(self.on_action_exit)
        self.actionExit_Main.triggered.connect(self.close)

        self.show()

    def closeEvent(self, event):
        print(event)
        result = QMessageBox.question(self,
                    "Confirm Exit",
                    "Are you sure you want to exit ?",
                    QMessageBox.Yes| QMessageBox.No)

        event.ignore()
        print(result)
        if result == QMessageBox.Yes:
            event.accept()


    def show_exit_dialog(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
