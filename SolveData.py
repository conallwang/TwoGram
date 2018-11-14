"""

    用于将 output.txt 进行平滑变换
"""

from utils.Smooth import Laplace


filename = './output/output.txt'


def main():
    Laplace(filename)


if __name__ == '__main__':
    main()