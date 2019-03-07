import json
from global_cfg import *

def create_item(word = '', number = 0, cn = '', phonetic_uk = '', phonetic_us = ''):
    word_item = {}
    word_item['word']           = word
    word_item['number']         = number
    word_item['cn']             = cn
    word_item['phonetic_uk']    = phonetic_uk
    word_item['phonetic_us']    = phonetic_us

    return word_item

# data_in = {NEW_GROUP_NAME: new_group_list, EASY_GROUP_NAME: easy_group_list}

##### Operate
class Group(object):

    def __init__(self, group_name, group_list = []):
        self._name = group_name
        self._list = group_list
    
    def get_name(self):
        return self._name

    def get_list(self):
        return self._list
    
    def get_words_list(self):
        words_list = []
        for item in self._list:
            words_list.append(item['word'])

        return words_list

    def get_item(self, word):
        for item in self._list:
            # print(item['word'])
            if item['word'] == word:
                return item

        return None

    def add_list(self, group_list):
        self._list = group_list

    # depend on number
    def sort(self):
        self._list.sort(key=lambda k: (k.get('number', 0)), reverse=True)

    def get_item_head(self):
        return self._list[0]

    def get_item_end(self):
        return self._list[-1]

    def pop_head(self):
        return self._list.pop(0)

    def pop_end(self):
        return self._list.pop(-1)

    def push_head(self, item):
        return self._list.insert(0, item)

    def push_end(self, item):
        return self._list.append(item)


    def __sub__(self, sub_group):
        res_list = []
        sub_words_list = sub_group.get_words_list()
        for item in self._list:
            if sub_words_list.count(item['word']) is 0:
                # Regardless of num
                res_list.append(item)
        
        return Group(self._name, res_list)

    def __add__(self, add_group):
        res_list = []
        _words_list = self.get_words_list()
        add_words_list = add_group.get_words_list()

        _words_set = set(_words_list)
        add_words_set = set(add_words_list)

        same_words_set = _words_set.intersection(add_words_set)
        _words_set.difference_update(same_words_set)
        add_words_set.difference_update(same_words_set)

        same_words_list = list(same_words_set)
        _words_only_list = list(_words_set)
        add_words_only_list = list(add_words_set)


        print(_words_set)
        print(add_words_set)
        print(same_words_list)

        for word in same_words_list:
            _item = self.get_item(word)
            add_item = add_group.get_item(word)
            _item['number'] = _item['number'] + _item['number']
            res_list.append(_item)

        for word in _words_only_list:
            _item = self.get_item(word)
            res_list.append(_item)

        for word in add_words_only_list:
            _item = add_group.get_item(word)
            res_list.append(_item)

        res_group = Group(self._name, res_list)
        res_group.sort()
        
        return res_group


class Struct:

    def __init__(self):
        self.struct = {}
        self.struct[NEW_GROUP_NAME] = Group(NEW_GROUP_NAME, [])
        self.struct[EASY_GROUP_NAME] = Group(EASY_GROUP_NAME, [])
        self.struct[FAMILIAR_GROUP_NAME] = Group(FAMILIAR_GROUP_NAME, [])
        self.struct[DIFFICULT_GROUP_NAME] = Group(DIFFICULT_GROUP_NAME, [])
        self.struct[ERROR_GROUP_NAME] = Group(ERROR_GROUP_NAME, [])

    def reset(self):
        self.struct[NEW_GROUP_NAME] = Group(NEW_GROUP_NAME, [])
        self.struct[EASY_GROUP_NAME] = Group(EASY_GROUP_NAME, [])
        self.struct[FAMILIAR_GROUP_NAME] = Group(FAMILIAR_GROUP_NAME, [])
        self.struct[DIFFICULT_GROUP_NAME] = Group(DIFFICULT_GROUP_NAME, [])
        self.struct[ERROR_GROUP_NAME] = Group(ERROR_GROUP_NAME, [])

    def add_group_raw(self, group_name, group_list):
        # self.structure[group_name] = group_list
        self.struct[group_name] = Group(group_name, group_list)
    
    def add_group(self, group):
        # self.structure[group._name] = group._list
        self.struct[group._name] = group

    def get_group(self, group_name):
        return self.struct[group_name]

    def load(self, file_name):
        with open(file_name, 'r') as file_handler:
            json_format = file_handler.read()

        struct_format = json.loads(json_format)

        self.struct[NEW_GROUP_NAME].add_list(struct_format[NEW_GROUP_NAME])
        self.struct[EASY_GROUP_NAME].add_list(struct_format[EASY_GROUP_NAME])
        self.struct[FAMILIAR_GROUP_NAME].add_list(struct_format[FAMILIAR_GROUP_NAME])
        self.struct[DIFFICULT_GROUP_NAME].add_list(struct_format[DIFFICULT_GROUP_NAME])
        self.struct[ERROR_GROUP_NAME].add_list(struct_format[ERROR_GROUP_NAME])

        

    def save(self, file_name):
        struct_format = {   NEW_GROUP_NAME: self.struct[NEW_GROUP_NAME]._list, 
                            EASY_GROUP_NAME: self.struct[EASY_GROUP_NAME]._list, 
                            FAMILIAR_GROUP_NAME: self.struct[FAMILIAR_GROUP_NAME]._list, 
                            DIFFICULT_GROUP_NAME: self.struct[DIFFICULT_GROUP_NAME]._list, 
                            ERROR_GROUP_NAME: self.struct[ERROR_GROUP_NAME]._list}

        json_format = json.dumps(struct_format, indent=4, separators=(',', ': '))
        # print(json_out)

        with open(file_name, 'w') as file_handler:
            file_handler.write(json_format)
