# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QPushButton, QToolTip, QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor, QRegion, QIcon, QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF

import pdf2txt
import txt2words
import words_manager
import words

from global_cfg import *
from utils import *

WORK_MODE_CLASSIFY  = 'classify'
WORK_MODE_EDIT      = 'edit'

new_str = 'new'
easy_str = 'easy'
familiar_str = 'familiar'
difficult_str = 'difficult'
error_str = 'error'

class Example(QWidget):
    pdf_page_num = 0
    def __init__(self):
        super().__init__()
        # self.words_manager_inst = words_manager.WordsManager('../words')

        self.new_dict = dict()

        self.words_lists = dict()
        self.words_lists[new_str] = []
        # new words
        self.words_lists[error_str] = []
        self.words_lists[easy_str] = []
        self.words_lists[familiar_str] = []
        self.words_lists[difficult_str] = []

        print(self.words_lists[new_str])

        self.init_ui()

        self.words_inst = words.Struct()
        self.words_input_inst = words.Struct()
        self.words = {}
        self.words_input = {}
        self.load_words()

        self.word_move_history_init()

        self.finished = True

        self.load_workspace()

    def init_ui(self):
        # Open button
        btn = QPushButton('Open', self)
        btn.clicked.connect(self.open_btn)
        btn.setToolTip('Open a .pdf file')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(TOOLBAR_L_OPEN_POS, TOOLBAR_H_POS)

        # Export button
        btn = QPushButton('Export', self)
        btn.clicked.connect(self.export_btn)
        btn.setToolTip('Export words file')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(TOOLBAR_L_EXPORT_POS, TOOLBAR_H_POS)

        # Setting button
        btn = QPushButton('Setting', self)
        btn.clicked.connect(self.setting_btn)
        btn.setToolTip('Setting this software')
        btn.resize(btn.sizeHint())
        btn.move(TOOLBAR_L_SETTING_POS, TOOLBAR_H_POS)

        # About button
        btn = QPushButton('About', self)
        btn.clicked.connect(self.about_btn)
        btn.setToolTip('About this software')
        btn.setFocusPolicy(Qt.NoFocus)
        btn.resize(btn.sizeHint())
        btn.move(TOOLBAR_L_ABOUT_POS, TOOLBAR_H_POS)

        # Setting page range
        self.label = QLabel(self)
        self.label.setText('pdf page number: ')
        self.label.setFocusPolicy(Qt.NoFocus)

        self.pdf_page_number_edit = QLineEdit(self)
        self.pdf_page_number_edit.setText('0')
        self.label.move(PAGE_RANGE_L_LABEL_POS, PAGE_RANGE_H_POS)
        self.pdf_page_number_edit.move(PAGE_RANGE_L_EDIT_POS, PAGE_RANGE_H_POS)

        # Add LineEditor
        # NEW
        self.label = QLabel(self)
        self.label.setText(NEW_GROUP_NAME)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits = dict()
        self.words_edits[new_str] = QLineEdit(self)
        self.words_edits[new_str].move(216, 300)
        self.label.move(216 + 60, 300 - 20)

        # ERROR
        self.label = QLabel(self)
        self.label.setText(ERROR_GROUP_NAME)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[error_str] = QLineEdit(self)
        self.words_edits[error_str].move(216, 300-100)
        self.label.move(216 + 60, 280-100)

        # EASY
        self.label = QLabel(self)
        self.label.setText(EASY_GROUP_NAME)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[easy_str] = QLineEdit(self)
        self.words_edits[easy_str].move(216, 300+100)
        self.label.move(216 + 60, 280+100)

        # FAMILIAR
        self.label = QLabel(self)
        self.label.setText(FAMILIAR_GROUP_NAME)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[familiar_str] = QLineEdit(self)
        self.words_edits[familiar_str].move(10, 300)
        self.label.move(10+60, 300-20)

        # DIFFICULT
        self.label = QLabel(self)
        self.label.setText(DIFFICULT_GROUP_NAME)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.words_edits[difficult_str] = QLineEdit(self)
        self.words_edits[difficult_str].move(420, 300)
        self.label.move(420+60, 300-20)

        self.work_mode_classify()

        # Window
        self.resize(MAIN_WINDOW_L_LEN, MAIN_WINDOW_H_LEN)
        self.center()
        self.setWindowTitle('ELFU')
        self.setWindowIcon(QIcon('../ico/title.ico'))

        self.show()

    def center(self):
        # Make main window display in the center of the display screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def display_word(self, name, word):
         self.words_edits[name].setText(word)
    
    def get_display_word(self, name):
        return self.words_edits[name].text()

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

        self.work_mode = WORK_MODE_CLASSIFY

    def work_mode_edit(self):
        self.pdf_page_number_edit.setFocusPolicy(Qt.ClickFocus)
        self.pdf_page_number_edit.setReadOnly(False)

        self.words_edits[new_str].setFocusPolicy(Qt.ClickFocus)
        self.words_edits[new_str].setReadOnly(False)
        self.words_edits[error_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[error_str].setReadOnly(True)
        self.words_edits[easy_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[easy_str].setReadOnly(True)
        self.words_edits[familiar_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[familiar_str].setReadOnly(True)
        self.words_edits[difficult_str].setFocusPolicy(Qt.NoFocus)
        self.words_edits[difficult_str].setReadOnly(True)

        self.work_mode = WORK_MODE_EDIT

    def work_mode_switch(self):
        if self.work_mode == WORK_MODE_CLASSIFY:
            self.work_mode_edit()
        elif self.work_mode == WORK_MODE_EDIT:
            self.work_mode_classify()
        else:
            print('[WARNING] work_mode is invalid: ', self.work_mode)

        print('work_mode_switch: ', self.work_mode)

    def keyPressEvent(self, event):
        print("Enter：" + str(event.key()))
        if event.key() == Qt.Key_Tab:
            print('Key：Tab')
            self.work_mode_switch()

        if self.work_mode == WORK_MODE_CLASSIFY:
            if event.key() == Qt.Key_W:
                print('Key：Up')
                self.word_move_to(ERROR_GROUP_NAME)
            if event.key() == Qt.Key_S:
                print('Key：Down')
                self.word_move_to(EASY_GROUP_NAME)
            if event.key() == Qt.Key_A:
                print('Key：Left')
                self.word_move_to(FAMILIAR_GROUP_NAME)
            if event.key() == Qt.Key_D:
                print('Key：Right')
                self.word_move_to(DIFFICULT_GROUP_NAME)
            if event.key() == Qt.Key_Backspace:
                print('Key：Backspace')
                self.word_move_back()

    def word_move_to(self, name):
        if len(self.words_input[NEW_GROUP_NAME].get_list()):
            item = self.words_input[NEW_GROUP_NAME].pop_head()
            item['word'] = self.get_display_word(NEW_GROUP_NAME)
            self.words_input[name].push_end(item)

            self.display_word(name, item['word'])

            if len(self.words_input[NEW_GROUP_NAME].get_list()):
                item = self.words_input[NEW_GROUP_NAME].get_item_head()
                self.display_word(NEW_GROUP_NAME, item['word'])
            else:
                print('...END...')

            self.word_move_history_push(name) 
        else:
            print('...END...')

    def word_move_back(self):
        name = self.word_move_history_pop()
        if name is None:
            print('Can not find any move operation!!!')
        else:
            print('[word_move_back] name: ', name)
            if len(self.words_input[name].get_list()):
                item = self.words_input[name].pop_end()
                self.words_input[NEW_GROUP_NAME].push_head(item)

                self.display_word(NEW_GROUP_NAME, item['word'])
                if len(self.words_input[name].get_list()):
                    item = self.words_input[name].get_item_end()
                    self.display_word(name, item['word'])
                else:
                    self.display_word(name, '')
    
    def word_move_history_init(self):
        self.words_move_history = []

    def word_move_history_pop(self):
        if len(self.words_move_history):
            name = self.words_move_history.pop()
        else:
            name = None

        return name 
        
    def word_move_history_push(self, name):
        self.words_move_history.append(name)

    def load_words(self):
        self.words_inst.load(WORDS_DIR + WORDS_FILE)
        self.words[NEW_GROUP_NAME]          = self.words_inst.get_group(NEW_GROUP_NAME)
        self.words[EASY_GROUP_NAME]         = self.words_inst.get_group(EASY_GROUP_NAME)
        self.words[FAMILIAR_GROUP_NAME]     = self.words_inst.get_group(FAMILIAR_GROUP_NAME)
        self.words[DIFFICULT_GROUP_NAME]    = self.words_inst.get_group(DIFFICULT_GROUP_NAME)
        self.words[ERROR_GROUP_NAME]        = self.words_inst.get_group(ERROR_GROUP_NAME)
    
    def load_words_input(self):
        self.words_input_inst.load(TEMP_DIR + WORDS_INPUT_FILE)
        self.words_input[NEW_GROUP_NAME]        = self.words_input_inst.get_group(NEW_GROUP_NAME)
        self.words_input[EASY_GROUP_NAME]       = self.words_input_inst.get_group(EASY_GROUP_NAME)
        self.words_input[FAMILIAR_GROUP_NAME]   = self.words_input_inst.get_group(FAMILIAR_GROUP_NAME)
        self.words_input[DIFFICULT_GROUP_NAME]  = self.words_input_inst.get_group(DIFFICULT_GROUP_NAME)
        self.words_input[ERROR_GROUP_NAME]      = self.words_input_inst.get_group(ERROR_GROUP_NAME)

        # print(words_inst_group_easy.get_words_list())
        # print(words_input_inst_group_new.get_words_list())

    def save_worksapce(self):
        self.words_input_inst.add_group(self.words_input[NEW_GROUP_NAME])
        self.words_input_inst.add_group(self.words_input[EASY_GROUP_NAME])
        self.words_input_inst.add_group(self.words_input[FAMILIAR_GROUP_NAME])
        self.words_input_inst.add_group(self.words_input[DIFFICULT_GROUP_NAME])
        self.words_input_inst.add_group(self.words_input[ERROR_GROUP_NAME])
        self.words_input_inst.save(TEMP_DIR + WORDS_INPUT_FILE)

    def load_workspace(self):
        self.load_words_input()

        if len(self.words_input[NEW_GROUP_NAME].get_list()):
            print("[load_workspace] start from work space")
            self.start_classify()
        else:
            print("[load_workspace] work space is clean")

    def start_classify(self):
        item = self.words_input[NEW_GROUP_NAME].get_item_head()
        self.display_word(NEW_GROUP_NAME, item['word'])

        self.work_mode_classify()

        self.finished = False


    def open_btn(self):
        print('Open button click...')
        page_num_str = self.pdf_page_number_edit.text()
        self.pdf_page_num = int(page_num_str)
        print('pdf page number: ', self.pdf_page_num)

        file_name_list, file_type = QFileDialog.getOpenFileNames(self,
                                                             'Select files',
                                                             '',
                                                             'pdf Files (*.pdf);;mkv Files (*.mkv)')

        print('Select files: ', file_name_list)
        print('File type is:', file_type)

        if file_type == 'pdf Files (*.pdf)':
            print("Select pdf file")
            if len(file_name_list) is not 0:
                print('Process pdf file...')
                file_txt_list = self.pdf2txt(file_name_list)
                file_words_name = self.txt2words(file_txt_list)

                self.load_words_input()
                self.filter_input_words()
                self.start_classify()
            else:
                print('Can not select any pdf files')
        elif file_type == 'mkv Files (*.mkv)':
            print("Select mkv file: TODO")
        else:
            print('Can not select any files')

    def pdf2txt(self, file_name_list):
        print('[pdf2txt] Start...')
        file_txt_name_list = []

        for file_name in file_name_list:
            print('[pdf2txt] pdf2txt: ', file_name)
            name = parse_file_name(file_name, type = False)

            file_txt_name = TEMP_DIR + name + '.txt'
            # TODO: use page range replaces page number
            if self.pdf_page_num == 0:
                pdf2txt_cmd = ['-o', file_txt_name, file_name]
            else:
                pdf2txt_cmd = ['-m', self.pdf_page_num, '-o', file_txt_name, file_name]
            pdf2txt.process(pdf2txt_cmd)
            file_txt_name_list.append(file_txt_name)
        
        print('[pdf2txt] End...')

        return file_txt_name_list

    def txt2words(self, file_name_list):
        print('[txt2words] txt2words: ', file_name_list)
        file_words_name = TEMP_DIR + WORDS_INPUT_FILE
        txt2words.process(file_name_list, file_words_name)

        print('[txt2words] End...')

        return file_words_name

    def filter_input_words(self):
        words_input_inst_group_new = self.words_input[NEW_GROUP_NAME] - self.words[EASY_GROUP_NAME] - self.words[FAMILIAR_GROUP_NAME] - self.words[DIFFICULT_GROUP_NAME] - self.words[ERROR_GROUP_NAME]
        # print(words_input_inst_group_new.get_words_list())
        self.words_input_inst.add_group(words_input_inst_group_new)

    def export_btn(self):
        print('Export button click')

        file_name, file_type = QFileDialog.getSaveFileName( self,
                                                            'Export files',
                                                            '',
                                                            'json Files (*.json)')

        print('Export file name: ', file_name, file_type)

        if file_name is not '':
            print('Export words...')

            # Export words_input
            # Must call save_worksapce firstly, then save inst to file name
            self.save_worksapce()
            self.words_input_inst.save(file_name)


            # Save words_input into words
            # new group of words means the words can not be classified.
            # so you can load words and judge whether need to classify words continuely
            self.words_inst.add_group(self.words[NEW_GROUP_NAME] + self.words_input[NEW_GROUP_NAME])
            self.words_inst.add_group(self.words[EASY_GROUP_NAME] + self.words_input[EASY_GROUP_NAME])
            self.words_inst.add_group(self.words[FAMILIAR_GROUP_NAME] + self.words_input[FAMILIAR_GROUP_NAME])
            self.words_inst.add_group(self.words[DIFFICULT_GROUP_NAME] + self.words_input[DIFFICULT_GROUP_NAME])
            self.words_inst.add_group(self.words[ERROR_GROUP_NAME] + self.words_input[ERROR_GROUP_NAME])
            self.words_inst.save(WORDS_DIR + 'words_xxx.json')    # FIXME: WORDS_DIR + WORDS_FILE

            self.finished = True
        else:
            print('Export words is cancelled')

    def setting_btn(self):
        print('TODO: Setting button click')
    
    def about_btn(self):
        print('TODO: About button click')

    def closeEvent(self, event):
        if self.finished is False:
            # TODO: pop Dialog to check
            # self.save_worksapce()
            print('Save work space!')
        else:
            print('Work is done!')

        print('Close...')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # self.drawText(event, qp)
        # self.draw_lines(qp)
        qp.end()

def app_func():
    app = QApplication(sys.argv)
    # app.desktop()
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

    print('hello')


import json
# import txt2words
import os

TEST_DIR = '../tmp/'

def test_func():
    # words_manager_inst = words_manager.WordsManager('../words')
    # words_manager_inst.test()
    # words_manager_inst.generate_new_words('../words/words.txt')

    file_pdf_name = TEST_DIR + 'input.pdf'
    file_txt_name = TEST_DIR + 'input.txt'
    file_json_name = TEST_DIR + 'input.json'

    print('test pdf2txt...')
    # pdf2txt_cmd = ['-o', file_txt_name, file_pdf_name]                # Default translate all pages
    # # pdf2txt_cmd = ['-p', '4,5', '-o', file_txt_name, file_pdf_name]   # Select some pages   
    # pdf2txt.process(pdf2txt_cmd)

    print('test txt2words...')

    # txt2words.process([file_txt_name], file_json_name)

    print('test utils...')
    # dir_path, file_name, file_type = parse_file_path(file_json_name)
    # print(dir_path)
    # print(file_name)
    # print(file_type)

    tmp_v = parse_dir_path('../input.json')
    print(tmp_v)

    print('test struct operate...')
    struct_inst1 = words.Struct()
    struct_inst1.load('../tmp/input1.json')
    new_group1 = struct_inst1.get_group(NEW_GROUP_NAME)
    # print(new_group1.get_list())

    struct_inst2 = words.Struct()
    struct_inst2.load('../tmp/input2.json')
    new_group2 = struct_inst2.get_group(NEW_GROUP_NAME)
    # print(new_group2.get_list())

    print('test group operate...')
    # tmp_group = words.Group(NEW_GROUP_STR)

    # tmp_group = new_group1 - new_group2
    tmp_group = new_group1 + new_group2

    print(new_group1.get_words_list())
    print(new_group2.get_words_list())
    print(tmp_group.get_words_list())
    print(tmp_group.get_list())

    # print(new_group2.get_item('speech'))

    # sort_list = [1,2,3,4]
    # sort_list.sort()



    
if __name__ == '__main__':
    print('Start...')

    # test_func()

    app_func()

    print('End...')
