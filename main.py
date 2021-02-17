import sys
from PyQt5.QtWidgets import *

def dialog():
    mbox = QMessageBox()

    mbox.setText("-_-_-_-_-_-_")
    mbox.setDetailedText(":v")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    mbox.exec_()

if __name__ == "__main__":
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
