import re, copy, warnings

from pattern import collection

def main():
    warnings.filterwarnings("ignore")
    file_path = rawtxt_path()
    with open(file_path, "r") as f:
        lines = f.readlines()
        #print(sample, end='')
        text_match(lines)

def rawtxt_path():
    return "./raw_sample.txt"

def save_path():
    return "./processed.txt"

def text_match(lines):
    lines = copy.deepcopy(lines)
    patterns = collection.pattern()    # 返回一个包含各种正则模式的哈希
    old_list = lines
    for i, key in enumerate(patterns.keys()):
        if(i != 0):
            old_list = new_list
        new_list = []
        pattern = patterns[key]
        pattern = re.compile(pattern)
        print(f"\n***********************正在匹配含有「{key}」的行***********************")
        for i, line in enumerate(old_list):
            line = re.sub(pattern, "", line)
            print(line, end="")
            new_list.append(line)
        print(f"***********************包含有「{key}」的行已清除***********************")
    text_save(new_list)
    print("\n***********************文本清洗完毕～***********************\n")
    return

def text_save(lines):
    with open(save_path(), "a") as f:
        for line in lines:
            f.write(line)
    print("\n***********************文本存储完毕～***********************")

if __name__ == "__main__":
    main()
