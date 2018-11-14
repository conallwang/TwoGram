import re
import math
import sys
import getopt

c_filename = '../data/characters.txt'
o_filename = '../result/2-gram-Laplace.txt'


def split_word(string):
    """
    分割拼音串为单个拼音，存入list
    :param string: 输入的连续拼音串
    :return: 拼音list
    """
    return string.split()


def get_dict():
    """
    获取key为词，value为概率的字典
    :return: 字典
    """
    dict = {}
    with open(o_filename, 'r') as fr:
        patternNum = re.compile(r'= (.*)')
        patternNextWord = re.compile(r'\(([\u4e00-\u9fa5])\|')
        patternWord = re.compile(r'\|([\u4e00-\u9fa5])\)')
        for line in fr.readlines():
            word = re.search(patternWord, line)
            nextWord = re.search(patternNextWord, line)
            num = re.search(patternNum, line)
            if word and nextWord and num:
                word = word.group(1)
                nextWord = nextWord.group(1)
                num = num.group(1)
                dict[word + nextWord] = math.log(float(num))
        fr.close()

    return dict


def function_p(dict, result):
    while True:
        pinyin = str(input('请输入拼音: '))
        if pinyin == 'exit':
            break
        li = split_word(pinyin)  # 将各个拼音分开
        M = 0  # 词表的列数     每个拼音可能出现的最多汉字数
        T = len(li)  # 词表的行数     即拼音的个数
        table = []  # 词表
        for item in li:  # 求得词表   以及词表的 M 参数
            pattern = re.compile('\n' + str(item) + '=([\u4e00-\u9fa5]+)')
            characters = re.search(pattern, result)
            if characters:
                characters = characters.group(1)
                if len(characters) > M:
                    M = len(characters)
                table.append(characters)

        prob = [[-1000000 for i in range(M)] for i in range(T)]  # 存储此时对应的最大概率
        ptr = [[0 for i in range(M)] for i in range(T)]  # 存储最大概率的路径

        if not table:  # 如果输入的不是合法的拼音或没输入则返回重新输入
            continue
        for j in range(len(table[0])):  # 将第一个拼音初始化
            ptr[0][j] = j
            prob[0][j] = 0

        for i in range(1, T):  # 对于每一个拼音   也就是词表的每一行
            for j in range(0, len(table[i])):  # 对于当前行的每一个汉字
                maxP = -1000000
                idx = 0
                for k in range(0, len(table[i - 1])):  # 遍历当前拼音的前一个拼音对应的所有汉字
                    if table[i - 1][k] + table[i][j] not in dict:  # 若在统计的词典中不存在 则加入
                        dict[table[i - 1][k] + table[i][j]] = -16.57585272128594
                    thisP = prob[i - 1][k] + dict[table[i - 1][k] + table[i][j]]
                    if thisP > maxP:
                        maxP = thisP
                        idx = k
                prob[i][j] = maxP
                ptr[i][j] = idx

        # 获取最后一行最大值的索引
        maxP = max(prob[T - 1])
        idx = prob[T - 1].index(maxP)

        # 输出结果
        i = T - 1
        string = ''
        while i >= 0:
            string += table[i][idx]
            idx = ptr[i][idx]
            i -= 1

        # 字符串逆序输出
        print(string[::-1])


def function_f(inputfile, outputfile, dict, result):
    fr = open(inputfile, 'r')
    fw = open(outputfile, 'w')
    lines = fr.readlines()
    res = []        # 要写入fw的内容
    if lines:
        print('开始拼音的转换,请稍等...')
        for pinyin in lines:
            li = split_word(pinyin)  # 将各个拼音分开
            M = 0  # 词表的列数     每个拼音可能出现的最多汉字数
            T = len(li)  # 词表的行数     即拼音的个数
            table = []  # 词表
            for item in li:  # 求得词表   以及词表的 M 参数
                pattern = re.compile('\n' + str(item) + '=([\u4e00-\u9fa5]+)')
                characters = re.search(pattern, result)
                if characters:
                    characters = characters.group(1)
                    if len(characters) > M:
                        M = len(characters)
                    table.append(characters)

            prob = [[-1000000 for i in range(M)] for i in range(T)]  # 存储此时对应的最大概率
            ptr = [[0 for i in range(M)] for i in range(T)]  # 存储最大概率的路径

            if not table:  # 如果输入的不是合法的拼音或没输入则返回重新输入
                continue
            for j in range(len(table[0])):  # 将第一个拼音初始化
                ptr[0][j] = j
                prob[0][j] = 0

            for i in range(1, T):  # 对于每一个拼音   也就是词表的每一行
                for j in range(0, len(table[i])):  # 对于当前行的每一个汉字
                    maxP = -1000000
                    idx = 0
                    for k in range(0, len(table[i - 1])):  # 遍历当前拼音的前一个拼音对应的所有汉字
                        if table[i - 1][k] + table[i][j] not in dict:  # 若在统计的词典中不存在 则加入
                            dict[table[i - 1][k] + table[i][j]] = -16.57585272128594
                        thisP = prob[i - 1][k] + dict[table[i - 1][k] + table[i][j]]
                        if thisP > maxP:
                            maxP = thisP
                            idx = k
                    prob[i][j] = maxP
                    ptr[i][j] = idx

            # 获取最后一行最大值的索引
            maxP = max(prob[T - 1])
            idx = prob[T - 1].index(maxP)

            # 输出结果
            i = T - 1
            string = ''
            while i >= 0:
                string += table[i][idx]
                idx = ptr[i][idx]
                i -= 1

            # 字符串逆序输出
            res.append(string[::-1] + '\n')
            print('转换完成: {0}'.format(string[::-1]))
        for item in res:
            fw.write(item)
        fw.close()
        fr.close()
        print('***成功完成输入文件中所有拼音的转换!\n***欢迎下次使用!')


def printUsage():
    """
    选项使用说明
    :return: None
    """
    print('''usage: run.py -p <pinyin> input 'exit' to quit p model
       run.py --infile=<inputfile> --outfile=<outputfile>''')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi", ['infile=', 'outfile='])
    except getopt.GetoptError:
        printUsage()
        sys.exit(-1)
    if ('-h', '') in opts:
        printUsage()
        return

    print('正在预生成字典...\n')
    dict = get_dict()  # 得到概率的字典  方便查找 加快速度
    fr = open(c_filename, 'r', encoding='utf-8')
    result = fr.read()
    fr.close()
    # 如果为文件输入
    inputfile = ''
    outputfile = ''

    for opt, arg in opts:
        if opt == '-i':
            function_p(dict, result)
        elif opt == '--infile':
            inputfile = arg
        elif opt == '--outfile':
            outputfile = arg


    if inputfile and outputfile:
        function_f(inputfile, outputfile, dict, result)


if __name__ == '__main__':
    main()
