# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QRegion
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text = "Test function"

        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Drawing text')

        # 无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 背景完全透明，控件受setWindowOpacity控制
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 透明度
        self.setWindowOpacity(0.6)

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def resizeEvent(self, event):
        side = max(self.width(), self.height())
        maskedRegion = QRegion(self.width() / 2 - side / 2, self.height() / 2 - side / 2, side, side, QRegion.Ellipse)
        self.setMask(maskedRegion)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.a
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

    print('hello')
