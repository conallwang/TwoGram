"""

    用于将变换后的 output.txt 文件生成 2-gram
"""

import re

w_filename = './result/2-gram'
r_filename = './output/output'
method = '-Laplace'
w_filename = w_filename + method + '.txt'
r_filename = r_filename + method + '.txt'

def get_all():
    with open(r_filename, 'r') as fr:
        pattern = re.compile(r': (\d+)')
        num = 0
        for line in fr.readlines():
            perNum = re.search(pattern, line)
            if perNum:
                perNum = int(perNum.group(1))
                num += perNum
        return num


def get_frequency(all):
    """
    获取2-gram
    :param all: 总字数
    :return: None
    """
    fw = open(w_filename, 'w')
    with open(r_filename, 'r') as fr:
        patternNum = re.compile(r': (\d+)')
        patternWord = re.compile(r'\'([\u4e00-\u9fa5]+)\'')
        for line in fr.readlines():
            perNum = re.search(patternNum, line)
            perWord = re.search(patternWord, line)
            if perNum and perWord:
                perNum = int(perNum.group(1))/all
                perWord = perWord.group(1)
                fw.write('P({0}|{1}) = {2}\n'.format(perWord[1], perWord[0], perNum))
        fr.close()
        fw.close()


def main():
    get_frequency(get_all())


if __name__ == '__main__':
    main()