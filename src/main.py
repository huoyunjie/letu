# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QPushButton, QToolTip, QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QRegion, QIcon, QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF

import pdf2txt
import words_parser
import words_manager

WORK_MODE_IDLE = 'idle'
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

new_str = 'new'
easy_str = 'easy'
familiar_str = 'familiar'
difficult_str = 'difficult'
error_str = 'error'


class Example(QWidget):
    pdf_page_num = 0
    def __init__(self):
        super().__init__()
        self.words_path = '../words'
        self.work_mode = WORK_MODE_IDLE

        self.words_manager_inst = words_manager.WordsManager('../words')

        self.new_dict = dict()
        # # old words
        # self.error_dict = dict()
        # self.easy_dict = dict()
        # self.familiar_dict = dict()
        # self.difficult_dict = dict()

        self.words_lists = dict()
        self.words_lists[new_str] = []
        # new words
        self.words_lists[error_str] = []
        self.words_lists[easy_str] = []
        self.words_lists[familiar_str] = []
        self.words_lists[difficult_str] = []

        # self.words_dicts = dict()
        # self.words_dicts[error_str] = dict()
        # self.words_dicts[easy_str] = dict()
        # self.words_dicts[familiar_str] = dict()
        # self.words_dicts[difficult_str] = dict()

        print(self.words_lists[new_str])

        self.init_ui()

        self.new_index = 0

        self.words_move_history = []

        self.finished = True

        # TODO: Load self.words_lists[new_str]
        self.load_temp_data()

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

        btn = QPushButton('Setting', self)
        btn.clicked.connect(self.setting_btn)
        btn.setToolTip('Setting this software')
        btn.resize(btn.sizeHint())
        btn.move(300, 0)

        btn = QPushButton('About', self)
        btn.clicked.connect(self.about_btn)
        btn.setToolTip('About this software')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(400, 0)

        self.label = QLabel(self)
        self.label.setText('pdf page number: ')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.pdf_page_number_edit = QLineEdit(self)
        self.pdf_page_number_edit.setText('0')
        self.label.move(30, 60)
        self.pdf_page_number_edit.move(160, 60)


        # Add LineEditor
        self.label = QLabel(self)
        self.label.setText('new')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits = dict()
        self.words_edits[new_str] = QLineEdit(self)
        # self.new_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.new_words_edit.setReadOnly(True)
        self.words_edits[new_str].move(216, 300)
        self.label.move(216 + 60, 300 - 20)
        # self.new_words_edit.textChanged[str].connect(self.new_line_edit_changed)

        self.label = QLabel(self)
        self.label.setText('error')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[error_str] = QLineEdit(self)
        # self.error_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.error_words_edit.setReadOnly(True)
        self.words_edits[error_str].move(216, 300-100)
        self.label.move(216 + 60, 280-100)
        # self.error_words_edit.textChanged[str].connect(self.error_line_edit_changed)

        self.label = QLabel(self)
        self.label.setText('easy')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[easy_str] = QLineEdit(self)
        # self.easy_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.easy_words_edit.setReadOnly(True)
        self.words_edits[easy_str].move(216, 300+100)
        self.label.move(216 + 60, 280+100)
        # self.easy_words_edit.textChanged[str].connect(self.easy_line_edit_changed)

        self.label = QLabel(self)
        self.label.setText('familiar')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[familiar_str] = QLineEdit(self)
        # self.familiar_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.familiar_words_edit.setReadOnly(True)
        self.words_edits[familiar_str].move(10, 300)
        self.label.move(10+60, 300-20)
        # self.familiar_words_edit.textChanged[str].connect(self.familiar_line_edit_changed)


        self.label = QLabel(self)
        self.label.setText('difficult')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[difficult_str] = QLineEdit(self)
        # self.difficult_words_edit.setFocusPolicy(Qt.ClickFocus)
        # self.difficult_words_edit.setReadOnly(True)
        self.words_edits[difficult_str].move(420, 300)
        self.label.move(420+60, 300-20)
        # self.difficult_words_edit.textChanged[str].connect(self.difficult_line_edit_changed)

        self.work_mode_classify()

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
        self.pdf_page_number_edit.setFocusPolicy(Qt.NoFocus)
        self.pdf_page_number_edit.setReadOnly(True)

        self.words_edits[new_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[new_str].setReadOnly(True)
        self.words_edits[error_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[error_str].setReadOnly(True)
        self.words_edits[easy_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[easy_str].setReadOnly(True)
        self.words_edits[familiar_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[familiar_str].setReadOnly(True)
        self.words_edits[difficult_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[difficult_str].setReadOnly(True)

    def work_mode_edit(self):
        self.pdf_page_number_edit.setFocusPolicy(Qt.ClickFocus)
        self.pdf_page_number_edit.setReadOnly(False)

        self.words_edits[new_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[new_str].setReadOnly(False)
        self.words_edits[error_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[error_str].setReadOnly(True)
        self.words_edits[easy_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[easy_str].setReadOnly(True)
        self.words_edits[familiar_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[familiar_str].setReadOnly(True)
        self.words_edits[difficult_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[difficult_str].setReadOnly(True)

    def work_mode_switch(self):
        if self.work_mode == WORK_MODE_CLASSIFY:
            self.work_mode_edit()
            self.work_mode = WORK_MODE_EDIT
        elif self.work_mode == WORK_MODE_EDIT:
            self.work_mode_classify()
            self.work_mode = WORK_MODE_CLASSIFY
        elif self.work_mode == WORK_MODE_IDLE:
            self.work_mode_edit()
            self.work_mode = WORK_MODE_EDIT
        else:
            print('[WARNING] work_mode is invalid: ', self.work_mode)

        print('work_mode_switch: ', self.work_mode)

    def keyPressEvent(self, event):
        # 这里event.key（）显示的是按键的编码
        print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        if event.key() == Qt.Key_Tab:
            print('Key：Tab')
            self.work_mode_switch()

        if self.work_mode == WORK_MODE_CLASSIFY:
            if event.key() == Qt.Key_W:
                print('Key：Up')
                self.word_move_to(error_str)
            if event.key() == Qt.Key_S:
                print('Key：Down')
                self.word_move_to(easy_str)
            if event.key() == Qt.Key_A:
                print('Key：Left')
                self.word_move_to(familiar_str)
            if event.key() == Qt.Key_D:
                print('Key：Right')
                self.word_move_to(difficult_str)
            if event.key() == Qt.Key_Backspace:
                print('Key：Backspace')
                self.word_move_back(self.words_move_history[-1])

        # if (event.key() == Qt.Key_Enter):
        #     print('测试：Space')

        # 当需要组合键时，要很多种方式，这里举例为“shift+单个按键”，也可以采用shortcut、或者pressSequence的方法。
        # if (event.key() == Qt.Key_P):
        #     if QApplication.keyboardModifiers() == Qt.ShiftModifier:
        #         print("shift + p")
        #     else:
        #         print("p")

    def word_move_to(self, name):
        if self.new_index == len(self.words_lists[new_str]):
            self.finished = True
            print('...END...')
        else:
            word = self.words_edits[new_str].text()
            self.words_list_push_end(name, word)
            self.words_edits[name].setText(word)
            self.new_index += 1
            if self.new_index == len(self.words_lists[new_str]):
                self.finished = True
                self.words_edits[new_str].setText('...END...')
            else:
                self.words_edits[new_str].setText(self.words_lists[new_str][self.new_index])

            self.words_move_history.append(name)

    def word_move_back(self, name):
        if self.new_index <= 0:
            print('[word_move_back] new_index <= 0')
        else:
            # print(self.words_lists[name])
            print('[word_move_back] name: ', name)
            # print(self.words_list_pop_end(name))
            # print(self.words_list_pop_end(name))
            # print(self.words_list_pop_end(name))
            word = self.words_list_pop_end(name)
            print('[word_move_back] pop: ', word)
            self.words_edits[name].setText(self.words_lists[name][-1])
            print('[word_move_back] set: ', self.words_lists[name][-1])
            self.new_index -= 1
            self.words_edits[new_str].setText(self.words_lists[new_str][self.new_index])
            self.words_move_history.pop()

            print('[word_move_back] new_index: ', self.new_index)

    def open_btn(self):
        print('Open button click')
        page_num_str = self.pdf_page_number_edit.text()
        self.pdf_page_num = int(page_num_str)
        print('pdf page number: ', self.pdf_page_num)

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

            self.new_dict = self.words_manager_inst.get_words_dict(new_str)

            self.new_index = 0
            self.words_lists[new_str] = list(self.new_dict.keys())
            self.words_edits[new_str].setText(self.words_lists[new_str][self.new_index])

            self.work_mode_classify()
            self.work_mode = WORK_MODE_CLASSIFY

            self.finished = False
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
            if self.pdf_page_num == 0:
                pdf2txt_cmd = ['-o', file_txt_name, file_name]
            else:
                pdf2txt_cmd = ['-m', self.pdf_page_num, '-o', file_txt_name, file_name]
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

    # def words_list_pop_head(self, name):
    #     word = self.words_lists[name].pop(0)
    #     return word

    def words_list_pop_end(self, name):
        word = self.words_lists[name].pop(-1)
        return word

    # def words_list_push_head(self, name, word):
    #     self.words_lists[name].insert(0, word)

    def words_list_push_end(self, name, word):
        self.words_lists[name].append(word)

    def words_list2str(self, words_list):
        words_str = ''
        for word in words_list:
            if word in self.words_lists[new_str]:
                words_str += word + '\n'
        return words_str

    def export_words_file(self, dir_name, name_str):
        file_path = dir_name + '/export_' + name_str + '.txt'
        with open(file_path, 'w') as file_handler:
            words_str = self.words_list2str(self.words_lists[name_str])
            file_handler.write(words_str)

    def export_words_files(self, dir_name):
        print('[export_words_file] dir name: ', dir_name)
        self.export_words_file(dir_name, error_str)
        self.export_words_file(dir_name, easy_str)
        self.export_words_file(dir_name, familiar_str)
        self.export_words_file(dir_name, difficult_str)

    def get_words_dict(self, name_str):
        # new_dict = self.words_manager_inst.get_words_dict(new_str)
        words_dict = dict()
        for word in self.words_lists[name_str]:
            if word in self.new_dict:
                words_dict[word] = self.new_dict[word]
            else:
                print('[WARNING] Can not find word(%s) in new dict' % word)

        return words_dict

    def save_words_into_file(self, dir_name, name_str):
        file_path = dir_name + '/words_' + name_str + '.txt'
        print('[save_words_into_files] file path: ', file_path)

        if name_str == new_str:
            self.words_lists[new_str] = self.words_lists[new_str][self.new_index:]
            all_dict = self.get_words_dict(new_str)
            print(all_dict)
        else:
            old_dict = self.words_manager_inst.get_words_dict(name_str)
            now_dict = self.get_words_dict(name_str)
            print('old_dict: ', old_dict)

            all_dict = self.words_manager_inst.words_dict_add([old_dict, now_dict])
            print('old_dict: ', old_dict)
            print('now_dict: ', now_dict)
            print('all_dict: ', all_dict)

        order_dict = self.words_manager_inst.words_dict_sort(all_dict)
        self.words_manager_inst.write_dict_to_words_file(name_str, order_dict)

    def save_words_into_files(self, dir_name):
        print('[save_words_into_files] dir name: ', dir_name)
        self.save_words_into_file(dir_name, new_str)
        self.save_words_into_file(dir_name, error_str)
        self.save_words_into_file(dir_name, easy_str)
        self.save_words_into_file(dir_name, familiar_str)
        self.save_words_into_file(dir_name, difficult_str)

    def export_btn(self):
        print('Export button click')
        # Save words into dicts
        # words_list2str(self.words_list)

        dir_name = QFileDialog.getExistingDirectory(self,
                                                    'Select export words path',
                                                    '')
        # print(dir_name)

        if dir_name is not '':
            print('Select export words path: ', dir_name)

            # Export files
            self.export_words_files(dir_name)

            # Save files into words
            self.save_words_into_files(self.words_path)
        else:
            print('Select words_path cancel')

    def save_temp_words(self, name_str):
        file_path = '../temp' + '/temp_' + name_str + '.txt'
        print(file_path)

        words_dict = self.get_words_dict(name_str)
        print(words_dict)

        order_dict = self.words_manager_inst.words_dict_sort(words_dict)
        self.words_manager_inst.write_dict_to_temp_file(file_path, order_dict)

    def save_temp_index(self):
        file_path = '../temp' + '/temp_index.txt'
        print(file_path)
        with open(file_path, 'w') as file_handler:
            file_handler.write(str(self.new_index))

    def save_temp_data(self):
        file_path = '../temp' + '/temp_data.txt'
        print(file_path)
        with open(file_path, 'w') as file_handler:
            file_handler.write(str(self.finished))

    def save_work_space(self):
        self.save_temp_words(new_str)
        self.save_temp_words(error_str)
        self.save_temp_words(easy_str)
        self.save_temp_words(familiar_str)
        self.save_temp_words(difficult_str)
        self.save_temp_index()

    def setting_btn(self):
        print('Setting button click')

        # dir_name = QFileDialog.getExistingDirectory(self,
        #                                             'Select words path',
        #                                             '')
        # # print(dir_name)
        #
        # if dir_name is not '':
        #     print('Select words_path: ', dir_name)
        #     self.words_path = dir_name
        # else:
        #     print('Select words_path cancel')

    def load_temp_words_to_list(self, name_str):
        file_path = '../temp' + '/temp_' + name_str + '.txt'
        print(file_path)

        words_dict = self.words_manager_inst.parse_words_dict(file_path)
        print(words_dict)

        self.words_lists[name_str] = list(words_dict.keys())
        print(self.words_lists[name_str])

    def load_temp_new_words_to_dict(self):
        file_path = '../temp' + '/temp_new.txt'
        print(file_path)

        self.new_dict = self.words_manager_inst.parse_words_dict(file_path)

    def load_temp_index(self):
        file_path = '../temp' + '/temp_index.txt'
        print(file_path)

        with open(file_path, 'r') as file_handler:
            new_index_str = file_handler.readline()
            self.new_index = int(new_index_str)

        print(self.new_index)

    def load_temp_data(self):
        file_path = '../temp' + '/temp_data.txt'
        print(file_path)

        with open(file_path, 'r') as file_handler:
            data_str = file_handler.readline()
            if data_str == 'True':
                self.finished = True
            elif data_str == 'False':
                self.finished = False
            else:
                self.finished = True
                print('[ERROR] data_str(%s) is invalid'%data_str)

        print(self.finished)

        if self.finished is False:
            self.load_temp_words()

    def load_temp_words(self):
        print('load_temp_words')
        # Test load
        self.load_temp_words_to_list(new_str)
        self.load_temp_words_to_list(error_str)
        self.load_temp_words_to_list(easy_str)
        self.load_temp_words_to_list(familiar_str)
        self.load_temp_words_to_list(difficult_str)

        self.load_temp_new_words_to_dict()
        self.load_temp_index()

        self.words_edits[new_str].setText(self.words_lists[new_str][self.new_index])

        self.work_mode_classify()
        self.work_mode = WORK_MODE_CLASSIFY

        self.finished = False

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

    def closeEvent(self, event):
        if self.finished is False:
            self.save_work_space()
            print('Save work space!')
        else:
            print('Work is done!')

        self.save_temp_data()
        print('Close...')

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