import re


def Laplace(filename):
    pattern = re.compile(r'(.*?)\.txt')
    forename = re.search(pattern, filename)
    if forename:
        forename = forename.group(1)
        newfilename = forename + '-Laplace.txt'
        fw = open(newfilename, 'w')
        with open(filename, 'r') as fr:
            pattern = re.compile(': (\d+)')
            patternWord = re.compile('(.*?)\d+')
            for line in fr.readlines():
                perNum = re.search(pattern, line)
                perWord = re.search(patternWord, line)
                if perNum and perWord:
                    perNum = int(perNum.group(1)) + 1
                    perWord = str(perWord.group(1))
                    fw.write(perWord + str(perNum) + '\n')
            fr.close()
            fw.close()