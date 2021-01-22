import os

from pattern import collection
from script import data_cleanse

def main():
    data_cleanse.controller(4)    # 数据清洗模块（由该模块启动日志模块）
    return

if __name__ == "__main__":
    try:
        os.remove("../output/processed.txt")
    except:
        print("processed文件不存在，无须删除")
    main()
