import io
import numpy as np


# 判断一个unicode是否是汉字
def is_chinese(uchar):
    return '\u4e00' <= uchar <= '\u9fff'


# 判断一个unicode是否是数字
def is_number(uchar):
    return '\u0030' <= uchar <= '\u0039'


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    return '\u0041' <= uchar <= '\u005a' or '\u0061' <= uchar <= '\u007a'


# 判断是否非汉字，数字和英文字符
def is_other(uchar):
    return not (is_chinese(uchar) or is_number(uchar))


def is_useful(uchar):
    return not is_other(uchar)


def is_str_useful(ustr):
    return not any(is_other(x) for x in ustr)


def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ', maxsplit=1)
        # data[tokens[0]] = map(float, tokens[1:])
        data[tokens[0]] = line[len(tokens[0]) + 1: ]
    return data, n, d


def load_dicts(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    return {line.split()[0] for line in fin}


def intersection(vec):
    dic = load_dicts('common_words.txt')
    print('open dict')
    veck = set(vec.keys())
    return dic & veck


def judge(vec):
    veck = set(vec.keys())
    return set(filter(is_str_useful, veck))


def write_file(res, vec, n, d):
    randvec = np.random.randn(4, d)
    np.set_printoptions(precision=3, suppress=True, linewidth=10000)
    print('write')
    with open('word_embed_clean.vec', 'w', encoding='utf-8') as f:
        f.write(f'{len(res) + 4} {d}\n')
        f.write(f'UNK {str(randvec[0])[1:-2]}\n')
        f.write(f'GO {str(randvec[1])[1:-2]}\n')
        f.write(f'PAD {str(randvec[2])[1:-2]}\n')
        f.write(f'EOS {str(randvec[3])[1:-2]}\n')
        for k in res:
            f.write(f'{k} {vec[k]}')

def single_word(vec, n, d):
    with open('usually_word', encoding='utf-8') as f:
        characters = f.read()

    charac = set(characters)
    return {word for word in vec.keys() if set(word).issubset(charac)}

def main():
    vec, n, d = load_vectors('wiki.zh.vec')
    res = single_word(vec, n, d)
    write_file(res, vec, n, d)



if __name__ == '__main__':
    main()