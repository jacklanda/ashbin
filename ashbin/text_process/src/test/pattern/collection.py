def pattern_test(pattern_name):
    return{
            "html": ".*<.*>.*",
            "js_var": ".*var.*",
            "js_func": ".*function().*",
            "js_if": ".*if.*",
            "js_method": ".*;.*",
            "js_comment": ".*(//).*",
            "js_hash": ".*{.*}.*",
            "css": ".*[{.*:;+}]+.*",
            "date": ".*[\d]{1,4}[-||/||年][\d]{1,4}[-||/||月][\d]{1,4}[日]?.*",
            "punctuation": ".*[==||`||\|].*",
            "phrase": None,
            "copyright": ".*[c|C]opy[r|R]ight.[^\s].*",
            "price": "[$||￥]\d*[.]?[\d]*",
            "phone": "(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}",
            "telephone": "\d{3}-\d{8}|\d{4}-\d{7}",
            "email": ".*@[\w]*.*",
            "idnum": ".*\d{18}.*",
            "tradzh": None,
            "url": "[\"||\']{0,1}[a-zA-z]+://[^\s]*[\"}||\']{0,1}",
            #"domain": ".*[a-zA-Z0-9]+([a-zA-Z0-9-.]+)?.(aero|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zr|zw|AERO|BIZ|COM|COOP|EDU|GOV|INFO|INT|MIL|MUSEUM|NAME|NET|ORG|AC|).*",
            "ip": ".*\d+\.\d+\.\d+\.\d+.*"
            }.get(pattern_name, "RETURN_ERROR!NO SUCH PATTERN U WANT!")

def pattern():
    return{
            "html": ".*<.*>.*",
            "js_var": ".*var.*",
            "js_func": ".*function().*",
            "js_if": ".*if.*",
            "nbsp": "&nbsp;?",
            "js_method": ".*;.*||.*alert(.*).*",
            "js_comment": ".*(//).*",
            "js_comment2": "\/\*.*\*\/",
            "js_hash": ".*\{.*\}.*||.*title\:.*||.*[\'||\"]query[\'||\"].*||.*capture_error.*",
            #"css": ".*[\{.*;+\}]+.*",
            "date": "[\d]{1,4}[-||/||年][\d]{1,4}[-||/||月][\d]{1,4}[日]?",#[\s*\d+\s*:\s*\d*]",
            "time": "\d{0,2}:\d{0,2}:\d{0,2}",
            "punctuation": ".*[==||`||\|].*",
            "copyright": ".*[c|C]opy[r|R]ight.[^\s].*",
            "price": "[$||￥]\d*[.]?[\d]*",
            "phone": "(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}",
            "telephone": "\d{3}-\d{8}|\d{4}-\d{7}",
            "email": ".*@[\w]*.*",
            "idnum": ".*\d{18}.*",
            "url": "[\"||\']{0,1}[a-zA-z]+://[^\s]*[\"}||\']{0,1}",
            "domain": "[a-zA-Z0-9]+([a-zA-Z0-9\-\.]+)?\.(aero|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly| ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk| pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr| st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zr|zw|AERO|BIZ|COM|COOP|EDU|GOV|INFO|INT|MIL|MUSEUM|NAME|NET|ORG|AC)",
            "ip": ".*\d+\.\d+\.\d+\.\d+.*",
            #-------------------
            "copyright2": ".*版权所有.*||.*©.*||.*ICP.*",
            "punctuation": ".*[>>||<<].*",
            "parentheses": "[\(||（]\d{0,10}[\)||）]",    # 圆括号及其内容 
            "single_punctuation": "·||•||【||】||～||~||#||\*",
            "table_head": "(\|.*\|?)+",
            "less_than_two_word": "^[\u4e00-\u9fa5]{0,3}[:||：]?$",
            "qq_number": "[qq]?[QQ]?\d{8,12}",
            "phrase_zh": "\[回复\]||\d+楼||\(楼主\)||\(管理员\)||\d+次",
            "phrase_zh_line": ".*正在加载.*||.*加载中.*||.*请稍后.*||.*公网安备.*||.*首页.*||.*上一页.*||.*下一页.*||.*完善密码.*", 
            "key_val": "\w+:\s\".*\"," 
            #"trad_zh"
            }
