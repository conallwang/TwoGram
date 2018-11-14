import math
import re
import sys
import getopt


def main(argv):
    pinyin = ""
    ff = ''

    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hp:f:", [])
    except getopt.GetoptError:
        print('Error: test.py -p')
        print('   or: test.py --pinyin=<pinyin>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Error: test.py -p <pinyin>')
            print('   or: test.py --pinyin=<pinyin>')

            sys.exit()
        elif opt in ('-p', '--pinyin'):
            pinyin = arg
        elif opt == '-f':
            ff = arg

    print(ff)
    print(pinyin)


if __name__ == "__main__":
    main(sys.argv[1:])


