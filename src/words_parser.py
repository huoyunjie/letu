import os
import sys
import re

WORDS_MODE = 1
WORDS_NUM_MODE = 3

# Experiment
# man-uscript
def words_preprocess(words):

    words_list = []
    for word in words:
        word = word.lower()
        words_list.append(word)

    return words_list


def words_counter(file_names_list):
    word_num_dict = {}

    # print(file_names_list)

    for file_name in file_names_list:
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

    # Do not need close file???

    return word_num_dict


def words_file_generater(file_name, word_num_dict):
    words_file = open(file_name, 'w')

    # Optimize: use string to store
    for word, num in word_num_dict:
        # words_file.write(word+'\n')
        words_file.write(word.ljust(50) + str(num) +'\n')

    words_file.close()


def process(in_file_names_list, out_file_name):
    word_num_dict = words_counter(in_file_names_list)
    words_file_generater(out_file_name, word_num_dict)
