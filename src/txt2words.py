import os
import sys
import re

from global_cfg import *
import words


def words_counter(file_name_list):
    word_num_dict = {}

    # print(file_txt_list)

    for file_name in file_name_list:
        with open(file_name, encoding='UTF-8') as file_handler:
            file_str = file_handler.read()
            # print repr(file_str)
            file_str = file_str.replace('-\n', '')
            file_str = file_str.replace('-', ' ')
            # print file_str
            words = re.findall("[a-zA-Z]+'*-*[a-zA-z]", file_str)
            for word in words:
                word = word.lower()
                if word_num_dict.get(word) is not None:
                    # if word_num_dict.has_key(word) is True:
                    word_num_dict[word] = word_num_dict[word] + 1
                else:
                    word_num_dict[word] = 1

    word_num_dict = sorted(word_num_dict.items(), key=lambda e:e[1], reverse=True)

    return word_num_dict

def words_save_txt(file_name, word_num_dict):
    with open(file_name, 'w') as file_handler:
        for word, num in word_num_dict:
            file_handler.write(word.ljust(50) + str(num) +'\n')
    
def words_save_json(file_name, word_num_dict):
    new_group_list = []
    for word, num in word_num_dict:
        new_group_list.append(words.create_item(word, num))

    struct_inst = words.Struct()
    struct_inst.add_group_raw(NEW_GROUP_NAME, new_group_list)
    struct_inst.save(file_name)

def process(in_file_name_list, out_file_name):
    word_num_dict = words_counter(in_file_name_list)
    words_save_json(out_file_name, word_num_dict)
