
# name string
new_str = 'new'
easy_str = 'easy'
familiar_str = 'familiar'
difficult_str = 'difficult'
error_str = 'error'

# file_str_list = [new_str, easy_str, familiar_str, difficult_str, error_str]


class WordsManager:
    words_dicts = dict()
    words_dicts[new_str] = dict()
    words_dicts[easy_str] = dict()
    words_dicts[familiar_str] = dict()
    words_dicts[difficult_str] = dict()
    words_dicts[error_str] = dict()

    def __init__(self, words_path):
        self.words_path = words_path

        print('test WordsManager')
        self.parse_words_dicts()
        print(self.words_dicts)

    @staticmethod
    def check_files():
        print('check_files')

    def get_file_name(self, name_str):
        file_path =  self.words_path + '/words_' + name_str + '.txt'
        return file_path

    @staticmethod
    def parse_words_dict(file_name):
        words_dict = dict()
        with open(file_name, 'r+') as file_handler:
            words_lines = file_handler.readlines()
            # print(words_lines)
            for word_line in words_lines:
                word_line = word_line.strip('\n')
                # # print word.split(' ')
                # word = word.rstrip()
                pos_left_space = word_line.find(' ')
                pos_right_space = word_line.rfind(' ')
                # print(pos_left_space, pos_right_space)

                if pos_left_space == -1:
                    word_str = word_line[:]
                else:
                    word_str = word_line[:pos_left_space]

                if pos_right_space == -1:
                    word_num = 0
                else:
                    word_num_str = word_line[pos_right_space+1:]
                    if word_num_str.isdecimal() is True:
                        word_num = int(word_num_str)
                    else:
                        word_num = 0

                words_dict[word_str] = word_num

        return words_dict

    def parse_words_dicts(self):
        for words_str, words_dict in self.words_dicts.items():
            print(words_str, ':', words_dict)
            file_name = self.get_file_name(words_str)
            print(file_name)
            self.words_dicts[words_str] = self.parse_words_dict(file_name)

        return self.words_dicts

    def words_dict_add(self, words_dict_list):
        print('words_dict_add: Start...')
        if type(words_dict_list) is not list:
            print('words_dict_list is not a list type: ', type(words_dict_list))
            return None

        dict_num = len(words_dict_list)
        if dict_num == 0:
            print('words_dict_list length is 0')
            return None
        elif dict_num == 1:
            return words_dict_list[0]
        else:
            sum = words_dict_list[0]
            for i in range(1, dict_num):
                for key, value in words_dict_list[i].items():
                    num = sum.get(key)
                    if num is None:
                        sum[key] = value
                    else:
                        sum[key] = num + value

        return sum

    # Operation: res = v0 - v1 - v2 - v3...
    # Modify num in v1, v2, v3...
    def words_dict_subtraction(self, words_dict_list):
        print('words_dict_subtraction: Start...')
        if type(words_dict_list) is not list:
            print('words_dict_list is not a list type: ', type(words_dict_list))
            return None

        dict_num = len(words_dict_list)
        if dict_num == 0:
            print('words_dict_list length is 0')
            return None
        elif dict_num == 1:
            return words_dict_list[0]
        else:
            res = words_dict_list[0]
            for i in range(1, dict_num):
                for key, value in words_dict_list[i].items():
                    num = res.get(key)
                    if num is not None:
                        words_dict_list[i][key] = num + value
                        res.pop(key)
        return res

    def words_dict2str(self, words_dict):
        words_str = ''
        for word, num in words_dict.items():
            # words_str += word + '\n'
            words_str += word.ljust(50) + str(num) + '\n'
        return words_str

    def write_dict_to_file(self, words_name_str, words_dict):
        file_name = self.get_file_name(words_name_str)
        print('write_dict_to_file: ', file_name)
        print(words_dict)
        with open(file_name, 'r+') as file_handler:
            words_str = self.words_dict2str(words_dict)
            # print 'words_str: ', words_str
            file_handler.seek(0)
            file_handler.truncate()
            # print 'words_file: ', words_file.readlines()
            file_handler.write(words_str)

    def generate_new_words(self, file_name):
        # Clear up new dict
        self.words_dicts[new_str].clear()

        # Get words dict
        words_dict = self.parse_words_dict(file_name)

        # Operate subtraction
        subtraction_list = [words_dict]
        exist_list = list(self.words_dicts.values())
        # print(subtraction_list)
        # print(list(exist_list))
        subtraction_list = subtraction_list + exist_list
        self.words_dicts[new_str] = self.words_dict_subtraction(subtraction_list)

        print(self.words_dicts[new_str])

        # Write file
        self.write_dict_to_file(new_str, self.words_dicts[new_str])

    def get_words_dict(self, name_str):
        return self.words_dicts[name_str]

    def test(self):
        print('Test...')
        # easy_words_list = self.get_words_list(easy_file)

        # print(self.words_dicts[difficult_str])
        # print(self.words_dicts[error_str])
        # print(self.words_dict_subtraction([self.words_dicts[difficult_str], self.words_dicts[error_str]]))
        # print(self.words_dicts[difficult_str])
        # print(self.words_dicts[error_str])
        # print(self.words_dict_add([self.words_dicts[difficult_str], self.words_dicts[error_str]]))

        # self.generate_new_words()
