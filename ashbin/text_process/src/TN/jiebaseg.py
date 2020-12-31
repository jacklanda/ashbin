import sys,os
import time
#sys.path.append("../../")
import jieba
jieba.set_dictionary('pplmdict.txt')
jieba.enable_parallel(20)

#url = sys.argv[1]
#for root, dirs, f in os.walk(url):
#    for fname in f:
#        filename = os.path.join(root,fname)
#        print(filename)
#        content = open(filename,"rb").read()
#        t1 = time.time()
#        words = "  ".join(jieba.cut(content,HMM=False))
#        
#        t2 = time.time()
#        tm_cost = t2-t1
#        
#        log_f = open(filename+".seg","wb")
#        log_f.write(words.encode('utf-8'))
#    
#        print('speed %s bytes/second' % (len(content)/tm_cost))

url = sys.argv[1]
content = open(url,"rb").read()
#jieba.load_userdict("dict.txt")
words = "  ".join(jieba.cut(content,HMM=False))
#print(words)
log_f = open(url+".seg","wb")
log_f.write(words.encode('utf-8'))
