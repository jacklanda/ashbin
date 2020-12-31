def num_year(text):
    try:
        pattern = re.compile(r'((\d0)年代)')
        matchers = pattern.findall(text)
        if matchers:
            for matcher in matchers:
                if '00年代'==matcher[0]:
                    text = text.replace('00年代',  '零零年代', 1)
                else:
                    if matcher:
                        if matcher[1]:
                            result = prev_deal(matcher[1])
                            text = text.replace(matcher[0], result + '年代', 1)
        return text
    except:
        pass


def num_chinese(text):
    pattern = re.compile(r'([$￥]((\d+,)*\d+(\.+\d+)?))')
    matchers = pattern.findall(text)
    if matchers:
        for matcher in matchers:
            if '￥' in matcher[0]:
                text = text.replace(matcher[0], matcher[1] + '元', 1)
            if '$' in matcher[0]:
                text = text.replace(matcher[0], matcher[1] + '美元', 1)
    return text


