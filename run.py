"""

    用于统计各个词在数据库中出现的次数
    生成 output.txt 文件
"""

from utils.config import *
import pymongo


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
table = db[MONGO_TABLE]

o_filename = './output/output.txt'

def is_Chinese(ch):
    """
    判断是否为中文
    :param word: 待判断字符
    :return: True表示是中文      False表示不是中文
    """
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def statistics():
    result = {}
    count = 0
    for content in table.find().batch_size(500):
        content = content['content'].strip()
        count += 1
        i = 0
        for i in range(len(content)-2):
            if is_Chinese(content[i]) and is_Chinese(content[i+1]):
                pText = '{0}{1}'.format(content[i], content[i + 1])
                if pText in result:
                    result[pText] += 1
                else:
                    result[pText] = 1
        print('统计完成数据: {0}'.format(count))
        # print('完成统计: {0}.'.format(content))
    return result


def write_to_file(filename, result):
    with open(filename, 'w') as fw:
        for key, value in result.items():
            fw.write('\'{0}\'在数据库中出现的次数为: {1}\n'.format(key, value))
        fw.close()


def main():
    write_to_file(o_filename, statistics())


if __name__ == '__main__':
    main()