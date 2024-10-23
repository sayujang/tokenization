import regex as re
from collections import Counter
with open('train.txt','r',encoding='utf-8') as f:
    text=f.read()

class Byte_Pair_Tokenizer:
    def __init__(self,vocab_size):
        self.vocab_size=vocab_size
        self.merges={}
    
    def max_pair(self,x):
        pairlists=[a for a in zip(x,x[1:])]
        f=Counter([p for p in pairlists])
        return f.most_common(1)[0][0]


    def train(self,text):
        x=list(map(int,text.encode('utf-8')))
        v = 0
        max_merge = self.vocab_size - 256
        merge = {}
        #iterate for the maximum number of merges
        for i in range(max_merge):
            hfelement = self.max_pair(x)  #find the most frequent pair
            j=0
            while j<len(x)-1:
                if (x[j],x[j+1])== hfelement:
                    self.merges[(x[j], x[j+1])] = v + 256  #store the merge
                    x[j] = v + 256  #replace the first element of the pair
                    x.pop(j+1)
                else:
                    j+=1
            v += 1
        return x
    def encode(self,text):
        #text=text.copy()
        encode=list(text.encode('utf-8'))
        i=0
        while i<len(encode)-1:
            if (encode[i],encode[i+1]) in self.merges:
                encode[i]=self.merges[(encode[i],encode[i+1])]
                encode.pop(i+1)
            else:
                i+=1 
        return encode    
    def decode(self,tokens):
        original=[]
        merge_inv={v:k for k,v in self.merges.items()}
        def org_list(tokens,original):
            for i in tokens:
                if i<=255:
                    original.append(i)
                else:
                    org_list([merge_inv[i][0]],original)
                    org_list([merge_inv[i][1]],original)
        org_list(tokens,original)
        string=bytes(original).decode('utf-8',errors="replace")  
        return string
a=Byte_Pair_Tokenizer(276)
a.train(text)
encodings=a.encode("Servous!! My friend ")
print(encodings)
# gpt2pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")

# print(re.findall(gpt2pat, "Hello've world123 //!!HOW's     are you   "))






