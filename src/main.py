# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QPushButton, QToolTip, QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QRegion, QIcon, QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF

import pdf2txt
import words_parser
import words_manager

WORK_MODE_CLASSIFY = 'classify'
WORK_MODE_EDIT = 'edit'


def parse_file_dir_name_without_type(file):
    if type(file) is str:
        # print_trace('str')
        pos_dot = file.rfind('.')
        pos_sprit = file.rfind('/')
        dir_path = file[:pos_sprit]
        name = file[pos_sprit+1:pos_dot]
        return dir_path, name
    else:
        print('file is not a string')
        return None, None

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.words_path = '../words'
        self.work_mode = WORK_MODE_CLASSIFY

        self.words_manager_inst = words_manager.WordsManager('../words')

        self.new_dict = self.words_manager_inst.get_words_dict('new')
        self.new_list = list(self.new_dict.keys())

        self.error_dict = self.words_manager_inst.get_words_dict('error')
        self.error_list = list(self.error_dict.keys())

        self.easy_dict = self.words_manager_inst.get_words_dict('easy')
        self.easy_list = list(self.easy_dict.keys())

        self.familiar_dict = self.words_manager_inst.get_words_dict('familiar')
        self.familiar_list = list(self.familiar_dict.keys())

        self.difficult_dict = self.words_manager_inst.get_words_dict('difficult')
        self.difficult_list = list(self.difficult_dict.keys())

        print(self.new_list)

        self.init_ui()

        self.new_index = 0
        word = self.new_list[0]
        self.new_words_edit.setText(word)

    def init_ui(self):
        self.text = "Test function"

        # QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget')

        # Add PushButton
        btn = QPushButton('Open', self)
        btn.clicked.connect(self.open_btn)
        btn.setToolTip('Open a .pdf file')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(100, 0)

        btn = QPushButton('Export', self)
        btn.clicked.connect(self.export_btn)
        btn.setToolTip('Export words file')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(200, 0)

        # btn = QPushButton('Setting', self)
        # btn.clicked.connect(self.setting_btn)
        # btn.setToolTip('Setting this software')
        # btn.resize(btn.sizeHint())
        # btn.move(300, 0)

        btn = QPushButton('Dir', self)
        btn.clicked.connect(self.dir_btn)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setToolTip('Set dir path')
        btn.resize(btn.sizeHint())
        btn.move(300, 0)

        btn = QPushButton('About', self)
        btn.clicked.connect(self.about_btn)
        btn.setToolTip('About this software')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(400, 0)

        # Add LineEditor
        self.label = QLabel(self)
        self.label.setText('new')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.new_words_edit = QLineEdit(self)
        # self.new_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.new_words_edit.setReadOnly(True)
        self.new_words_edit.move(216, 300)
        self.label.move(216 + 60, 300 - 20)
        # self.new_words_edit.textChanged[str].connect(self.new_line_edit_changed)

        self.label = QLabel(self)
        self.label.setText('error')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.error_words_edit = QLineEdit(self)
        # self.error_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.error_words_edit.setReadOnly(True)
        self.error_words_edit.move(216, 300-150)
        self.label.move(216 + 60, 280-150)
        # self.error_words_edit.textChanged[str].connect(self.error_line_edit_changed)

        self.label = QLabel(self)
        self.label.setText('easy')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.easy_words_edit = QLineEdit(self)
        # self.easy_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.easy_words_edit.setReadOnly(True)
        self.easy_words_edit.move(216, 300+150)
        self.label.move(216 + 60, 280+150)
        # self.easy_words_edit.textChanged[str].connect(self.easy_line_edit_changed)


        self.label = QLabel(self)
        self.label.setText('familiar')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.familiar_words_edit = QLineEdit(self)
        # self.familiar_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.familiar_words_edit.setReadOnly(True)
        self.familiar_words_edit.move(10, 300)
        self.label.move(10+60, 300-20)
        # self.familiar_words_edit.textChanged[str].connect(self.familiar_line_edit_changed)


        self.label = QLabel(self)
        self.label.setText('difficult')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.difficult_words_edit = QLineEdit(self)
        # self.difficult_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.difficult_words_edit.setReadOnly(True)
        self.difficult_words_edit.move(420, 300)
        self.label.move(420+60, 300-20)
        # self.difficult_words_edit.textChanged[str].connect(self.difficult_line_edit_changed)

        self.work_mode_classify()

        # # Add LineEditor
        # self.label = QLabel(self)
        # self.label.setText('word')
        #
        # self.new_words_edit = QLineEdit(self)
        # self.new_words_edit.move(200, 300)
        # self.label.move(260, 280)
        # # self.new_words_edit.textChanged[str].connect(self.current_line_edit_changed)
        #
        #
        # self.label = QLabel(self)
        # self.label.setText('easy')
        #
        # line_edit = QLineEdit(self)
        # line_edit.move(200, 300+150)
        # self.label.move(260, 280+150)
        # line_edit.textChanged[str].connect(self.easy_line_edit_changed)
        #
        #
        # self.label = QLabel(self)
        # self.label.setText('familiar')
        #
        # line_edit = QLineEdit(self)
        # line_edit.move(200-150, 300-150)
        # self.label.move(260-150, 280-150)
        # line_edit.textChanged[str].connect(self.familiar_line_edit_changed)
        #
        #
        # self.label = QLabel(self)
        # self.label.setText('difficult')
        #
        # line_edit = QLineEdit(self)
        # line_edit.move(200+150, 300-150)
        # self.label.move(260+150, 280-150)
        # line_edit.textChanged[str].connect(self.difficult_line_edit_changed)


        # self.des
        self.resize(600, 600)
        self.center()
        self.setWindowTitle('ELFU')
        self.setWindowIcon(QIcon('../ico/title.ico'))

        # 无边框
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # 背景完全透明，控件受setWindowOpacity控制
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 透明度
        # self.setWindowOpacity(0.6)



        self.show()

    def center(self):   # 实现窗体在屏幕中央
        # screen = QDesktopWidget().screenGeometry()    # QDesktopWidget为一个类，调用screenGeometry函数获得屏幕的尺寸
        # size = self.geometry()  # 同上
        # self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)    # 调用move移动到指定位置

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 检测键盘回车按键，函数名字不要改，这是重写键盘事件

    def work_mode_classify(self):
        self.new_words_edit.setFocusPolicy(Qt.NoFocus)
        self.new_words_edit.setReadOnly(True)
        self.error_words_edit.setFocusPolicy(Qt.NoFocus)
        self.error_words_edit.setReadOnly(True)
        self.easy_words_edit.setFocusPolicy(Qt.NoFocus)
        self.easy_words_edit.setReadOnly(True)
        self.familiar_words_edit.setFocusPolicy(Qt.NoFocus)
        self.familiar_words_edit.setReadOnly(True)
        self.difficult_words_edit.setFocusPolicy(Qt.NoFocus)
        self.difficult_words_edit.setReadOnly(True)

    def work_mode_edit(self):
        self.new_words_edit.setFocusPolicy(Qt.ClickFocus)
        self.new_words_edit.setReadOnly(False)
        self.error_words_edit.setFocusPolicy(Qt.ClickFocus)
        self.error_words_edit.setReadOnly(True)
        self.easy_words_edit.setFocusPolicy(Qt.ClickFocus)
        self.easy_words_edit.setReadOnly(True)
        self.familiar_words_edit.setFocusPolicy(Qt.ClickFocus)
        self.familiar_words_edit.setReadOnly(True)
        self.difficult_words_edit.setFocusPolicy(Qt.ClickFocus)
        self.difficult_words_edit.setReadOnly(True)


    # self.work_mode = 'eidt', 'classifiy'
    def work_mode_switch(self):
        if self.work_mode == WORK_MODE_CLASSIFY:
            self.work_mode_edit()
            self.work_mode = WORK_MODE_EDIT
        else:
            self.work_mode_classify()
            self.work_mode = WORK_MODE_CLASSIFY

        print('work_mode_switch: ', self.work_mode)

    def keyPressEvent(self, event):
        # 这里event.key（）显示的是按键的编码
        print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        if (event.key() == Qt.Key_Tab):
            print('Key：Tab')
            self.work_mode_switch()
        if (event.key() == Qt.Key_W):
            print('Key：Up')
            word = self.new_words_pop()
            self.error_words_push(word)
        if (event.key() == Qt.Key_S):
            print('Key：Down')
            word = self.new_words_pop()
            self.easy_words_push(word)
        if (event.key() == Qt.Key_A):
            print('Key：Left')
            word = self.new_words_pop()
            self.familiar_words_push(word)
        if (event.key() == Qt.Key_D):
            print('Key：Right')
            word = self.new_words_pop()
            self.difficult_words_push(word)
        # if (event.key() == Qt.Key_Enter):
        #     print('测试：Space')
        # if (event.key() == Qt.Key_Backspace):
        #     print('测试：Space')
        # 当需要组合键时，要很多种方式，这里举例为“shift+单个按键”，也可以采用shortcut、或者pressSequence的方法。
        # if (event.key() == Qt.Key_P):
        #     if QApplication.keyboardModifiers() == Qt.ShiftModifier:
        #         print("shift + p")
        #     else:
        #         print("p")

    def open_btn(self):
        print('Open button click')
        file_names, file_type = QFileDialog.getOpenFileNames(self,
                                                             'Select files',
                                                             '',
                                                             'pdf Files (*.pdf);;mkv Files (*.mkv)')

        print(file_names)
        print(file_type)

        if len(file_names) is not 0:
            print('Process pdf file')
            words_file_name = self.pdf2words(file_names, file_type)
            self.filter_words_new(words_file_name)
            # self.test_display()
        else:
            print('Can not select pdf file')

    def pdf2words(self, file_names, file_type):
        print('[pdf2txt]: Start...')
        file_txt_name_list = []
        for file_name in file_names:
            print('[pdf2txt]: ', file_name)
            dir_path, name = parse_file_dir_name_without_type(file_name)
            # print(dir_path)
            # print(name)

            # pdf2txt
            file_txt_name = '../temp/' + name + '.txt'
            pdf2txt_cmd = ['-o', file_txt_name, file_name]
            pdf2txt.process(pdf2txt_cmd)
            file_txt_name_list.append(file_txt_name)

        # txt2words
        print(file_txt_name_list)
        words_file_name = self.words_path + '/words.txt'
        words_parser.process(file_txt_name_list, words_file_name)

        print('[pdf2txt]: End...')

        return words_file_name

    def filter_words_new(self, file_name):
        print('filter_words_new: ', file_name)
        self.words_manager_inst.generate_new_words(file_name)

    def new_words_pop(self):
        word = self.new_list[self.new_index]
        self.new_index += 1
        self.new_words_edit.setText(self.new_list[self.new_index])

        return word

    def error_words_push(self, word):
        self.error_words_edit.setText(word)
        # word = self.easy_list[self.easyindex]

    def easy_words_push(self, word):
        self.easy_words_edit.setText(word)
        # word = self.easy_list[self.easyindex]

    def familiar_words_push(self, word):
        self.familiar_words_edit.setText(word)
        # word = self.easy_list[self.easyindex]

    def difficult_words_push(self, word):
        self.difficult_words_edit.setText(word)
        # word = self.difficult_list[self.easyindex]

    def export_btn(self):
        print('Export button click')

    def dir_btn(self):
        print('Dir button click')
        dir_name = QFileDialog.getExistingDirectory(self,
                                                    'Select word path',
                                                    '')
        # print(dir_name)

        if dir_name is not '':
            print('Select words_path: ', dir_name)
            self.words_path = dir_name
        else:
            print('Select words_path cancel')


    def about_btn(self):
        print('About button click')

    def new_line_edit_changed(self, text):
        print('current_line_edit_changed: ', text)

    def error_line_edit_changed(self, text):
        print('error_line_edit_changed: ', text)

    def easy_line_edit_changed(self, text):
        print('easy_line_edit_changed: ', text)

    def familiar_line_edit_changed(self, text):
        print('familiar_line_edit_changed: ', text)

    def difficult_line_edit_changed(self, text):
        print('difficult_line_edit_changed: ', text)


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # self.drawText(event, qp)
        # self.draw_lines(qp)
        qp.end()

    def draw_lines(self, qp):

        pen = QPen(Qt.black, 2, Qt.SolidLine)

        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([2, 4, 2, 4])
        # pen.setJoinStyle(Qt.MiterJoin)  # 让箭头变尖
        qp.setPen(pen)

        # Move to init and wrap a function, just source and dest point
        self.source = QPointF(260-2, 280-2)
        self.dest = QPointF(260-90, 280-90)
        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() - 20)

        # draw line
        qp.drawLine(self.line)

        v = self.line.unitVector()
        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector() # 法向量
        n.setLength(n.length() * 0.5) # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector() # 两次法向量运算以后，就得到一个反向的法向量

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        qp.drawPolygon(p1, p2, p3)

        self.source = QPointF(260+40, 280-2)
        self.dest = QPointF(260+90+40, 280-90)
        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() - 20)

        # draw line
        qp.drawLine(self.line)

        v = self.line.unitVector()
        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector() # 法向量
        n.setLength(n.length() * 0.5) # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector() # 两次法向量运算以后，就得到一个反向的法向量

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        qp.drawPolygon(p1, p2, p3)

        # Reference:  https://blog.csdn.net/founderznd/article/details/51661523
        self.source = QPointF(260+20, 280+50)
        self.dest = QPointF(260+20, 280+130)
        self.line = QLineF(self.source, self.dest)
        self.line.setLength(self.line.length() - 20)

        # draw line
        qp.drawLine(self.line)

        # 首先利用QLineF().unitVector()函数得到它的单位向量，并将它移到原线的终点位置，注意这里的偏移量。
        v = self.line.unitVector()
        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        # 然后我们利用normalVector()函数得到他的法向量，然后再利用normalVector()得到法向量的反方向的向量。
        n = v.normalVector() # 法向量
        n.setLength(n.length() * 0.5) # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector() # 两次法向量运算以后，就得到一个反向的法向量

        # 然后我们取得 3 个向量的终点 为箭头的三个端点，并以这三点为顶点画出三角形
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        qp.drawPolygon(p1, p2, p3)

    # def drawText(self, event, qp):
    #     qp.setPen(QColor(168, 34, 3))
    #     qp.setFont(QFont('Decorative', 10))
    #     qp.drawText(event.rect(), Qt.AlignCenter, self.text)
    #
    # def resizeEvent(self, event):
    #     side = max(self.width(), self.height())
    #     maskedRegion = QRegion(self.width() / 2 - side / 2, self.height() / 2 - side / 2, side, side, QRegion.Ellipse)
    #     self.setMask(maskedRegion)
    #
    # def mousePressEvent(self, event):
    #
    #     if event.button() == Qt.LeftButton:
    #         self.m_flag = True
    #         self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
    #         event.accept()
    #         self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     if Qt.LeftButton and self.m_flag:
    #         self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
    #         QMouseEvent.accept()
    #
    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.m_flag = False
    #     self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.desktop()
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

    print('hello')


# if __name__ == '__main__':
#     print('Start...')
#     words_manager_inst = words_manager.WordsManager('../words')
#     words_manager_inst.test()
#     words_manager_inst.generate_new_words('../words/words.txt')
#     print('End...')