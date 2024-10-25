from baselayer import Tokenizer,get_stats,merge_pair
with open('train.txt','r',encoding='utf-8') as f:
    text=f.read()
class Basic_Tokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
    def train(self,text,vocab_size):
        tokens=list(text.encode('utf-8'))
        num_merge=vocab_size-256
        token_copy=tokens.copy()
        merges={}
        for i in range(num_merge):
            stats=get_stats(token_copy)
            pair=max(stats,key=lambda k: stats[k])
            element=256+i
            token_copy=merge_pair(token_copy,pair,element)
            merges[pair]=element
        self.merges=merges
    def encode(self,text):
        tokens=list(text.encode('utf-8'))
        while len(tokens)>=2:
            stats=get_stats(tokens)
            pair=min(stats,key=lambda k: self.merges.get(k,float('inf')))
            if pair not in self.merges:
                break
            tokens=merge_pair(tokens,pair,self.merges[pair])
        return tokens
    def decode(self,tokens):
        vocab=self.vocab
        text=b"".join(vocab[token] for token in tokens )
        text.decode('utf-8')
        return text
b=Basic_Tokenizer()
b.train(text,276)
a=b.encode("hello world!")
print(a)
