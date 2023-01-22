import sys, math, random
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *



from ui_main import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Hunger Manager 2023')
        self.show()
        barChildren = self.ui.frame_5.findChildren(QProgressBar)
        labelChildren = self.ui.frame_4.findChildren(QLabel)
        self.anims = []

        for x in range(len(barChildren)):
            child = barChildren[x]
            anim = QPropertyAnimation(child, b'value')
            
            anim.setDuration(5000)

            if child.objectName() == 'fBar':
                child.setFormat("Sanity")
                anim.setKeyValueAt(0, 85)
                anim.setKeyValueAt(0.5, 15)
                anim.setKeyValueAt(1, 85)

            elif child.objectName() == 'pBar':
                child.setFormat("Efficiency")
                anim.setKeyValueAt(0, 15)
                anim.setKeyValueAt(0.5, 85)
                anim.setKeyValueAt(1, 15)

            anim.setLoopCount(-1)
            anim.setEasingCurve(QtCore.QEasingCurve.InOutSine)
            anim.start()
            self.anims.append(anim)    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())