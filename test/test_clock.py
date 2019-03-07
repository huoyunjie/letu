# -*- coding: utf-8 -*-

# Reference: https://blog.csdn.net/powerdoom/article/details/50868196
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class ShapedClock(QWidget):
    def __init__(self):
        super(ShapedClock, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.quitAction = QAction('Exit', self)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.triggered.connect(qApp.quit)
        self.quitAction2 = QAction('Exit2', self)
        self.quitAction2.setShortcut('Ctrl+Q')
        self.quitAction2.triggered.connect(qApp.quit)
        self.addAction(self.quitAction)
        self.addAction(self.quitAction2)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setToolTip('Drag the clock with the left mouse button.\n '
                        'Use the right mouse button to open a context menu.')
        self.setWindowTitle('Shaped Analog Clock')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def paintEvent(self, QPaintEvent):
        hourHand = [
            QPoint(7, 8),
            QPoint(-7, 8),
            QPoint(0, -40)
        ]
        minuteHand = [
            QPoint(7, 8),
            QPoint(-7, 8),
            QPoint(0, -70)
        ]

        hourColor = QColor(127, 0, 127)
        minuteColor = QColor(0, 127, 127, 191)

        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(hourColor)
        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60))
        painter.drawConvexPolygon(QPolygon(hourHand))
        painter.restore()

        painter.setPen(hourColor)
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(minuteColor)
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60))
        painter.drawConvexPolygon(QPolygon(minuteHand))
        painter.restore()

        painter.setPen(minuteColor)
        for i in range(60):
            if i % 5 != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        painter.end()

    def resizeEvent(self, event):
        side = max(self.width(), self.height())
        maskedRegion = QRegion(self.width() / 2 - side / 2, self.height() / 2 - side / 2, side, side, QRegion.Ellipse)
        self.setMask(maskedRegion)

    def sizeHint(self):
        return QSize(100, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = ShapedClock()
    clock.show()
    app.exec_()