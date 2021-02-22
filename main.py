import sys
import os
import glob

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ftemplate import load_teplate, TEMPLATES_DIR, EXT
from ftemplate import Template, SimpleTextField, BlockTextField, ImageField, SelectField


class TemplateManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #create window
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Template Manager')
        self.setWindowIcon(QIcon('ico.png'))

        #templates list
        template_files = glob.glob(TEMPLATES_DIR + "*" + EXT)
        templates = []

        for path in template_files:
            temp = load_teplate(path)
            templates.append(temp)

        #widgets
        label = QLabel("Saved templates")

        templates_list = QVBoxLayout()

        for t in templates:
            btn = QPushButton(t.name)
            templates_list.addWidget(btn)

        templates_list.setAlignment(Qt.AlignTop)

        control_btns = QHBoxLayout()

        create_btn = QPushButton("Create new template")
        create_btn.clicked.connect(self.on_create_new_template_click)

        control_btns .addWidget(create_btn)

        root = QVBoxLayout(self)
        root.addWidget(label)
        root.addLayout(templates_list)
        root.addLayout(control_btns)

        root.setAlignment(Qt.AlignTop)

        self.show()

    def on_create_new_template_click(self):
        print("create")



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #create window
        self.setGeometry(300, 300, 640, 420)
        self.setWindowTitle('.✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.[Form Editor].✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.')
        self.setWindowIcon(QIcon('ico.png'))

        #templates list
        template_files = glob.glob(TEMPLATES_DIR + "*" + EXT)
        templates = []

        for path in template_files:
            temp = load_teplate(path)
            templates.append(temp)

        label = QLabel(self)
        label.setText("Saved templates")

        templates_list = QVBoxLayout(self)

        for t in templates:
            btn = QPushButton(t.name)
            templates_list.addWidget(btn)



        templates_list.setAlignment(Qt.AlignTop)

        self.show()

def dialog():
    mbox = QMessageBox()

    mbox.setText("-_-_-_-_-_-_")
    mbox.setDetailedText(":v")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    mbox.exec_()

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle(".✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.[Form Editor].✫*ﾟ･ﾟ｡.★.*｡･ﾟ✫*.")
    w.resize(300,300)

    label = QLabel("text text text")
    #label.move(100,130)
    label.show()

    line = QLineEdit()
    line.show()

    btn = QPushButton('?')
    btn.show()
    btn.clicked.connect(dialog)

    vb = QVBoxLayout(w)

    vb.addWidget(label)
    vb.addWidget(line)
    vb.addWidget(btn)

    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TemplateManager()
    sys.exit(app.exec_())
