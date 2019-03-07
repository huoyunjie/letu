
import json

if __name__ == '__main__':

    print('test txt2json...')

    data_in =   [   { 'easy': [ { 'word': "hello", 'number': 100, 'cn': "你好", 'phonetic uk': "[həˈləʊ]", 'phonetic us': "[helˈō]"},
                                { 'word': "play", 'number': 85, 'cn': "玩", 'phonetic uk': "[həˈləʊ]", 'phonetic us': "[helˈō]"},]
                    },
                    { 'error': [ { 'word': "hello", 'number': 100, 'cn': "你好", 'phonetic uk': "[həˈləʊ]", 'phonetic us': "[helˈō]"},
                                { 'word': "play", 'number': 85, 'cn': "玩", 'phonetic uk': "[həˈləʊ]", 'phonetic us': "[helˈō]"},]
                    },
                ]
    json_out = json.dumps(data_in, indent=4, separators=(',', ': '))
    print(json_out)

    with open('test.json', 'w') as file_handler:
        file_handler.write(json_out)

    # json_in = '[{"word": "hello", "number": 100, "cn": "\u4f60\u597d", "phonetic uk": "[h\u0259\u02c8l\u0259\u028a]", "phonetic us": "[hel\u02c8\u014d]"}]'
    with open('test.json', 'r') as file_handler:
        json_in = file_handler.read()

    data_out = json.loads(json_in)
    print(data_out[1])

    print('End...')