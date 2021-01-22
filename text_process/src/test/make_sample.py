with open("raw.txt", "r") as f_read:
        sample = ""
        lines = f_read.readlines()
        count = 0
        for line in lines:
            count += 1
            sample = sample + line
            if(count > 10000):
                break
        with open("raw_sample.txt", "w") as f_write:
            for line in sample:
                f_write.write(line)
        print("原文本取样完毕")
