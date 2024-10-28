from baselayer import Tokenizer,get_stats,merge_pair
with open('train.txt','r',encoding='utf-8') as f:
    text=f.read()
class Basic_Tokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    #train tokenizer

    def train(self,text,vocab_size):
        tokens=list(text.encode('utf-8')) 
        num_merge=vocab_size-256
        token_copy=tokens.copy()
        merges={}
        vocab={t:bytes([t]) for t in range(256)}
        for i in range(num_merge):
            stats=get_stats(token_copy) #get_stats returns dict(Pair:counts)
            pair=max(stats,key=lambda k: stats[k]) #pair having maximum counts
            element=256+i #mint new token
            token_copy=merge_pair(token_copy,pair,element) #new tokens after merge
            merges[pair]=element #store trained merges on dataset in dict
            vocab[element]=vocab[pair[0]]+vocab[pair[1]] #The byte strings get concatenated here
        self.merges=merges
        self.vocab=vocab

    def encode(self,text):
        tokens=list(text.encode('utf-8'))
        while len(tokens)>=2:
            stats=get_stats(tokens)
            pair=min(stats,key=lambda k: self.merges.get(k,float('inf'))) #get pair in stats that has the lowest minted token in merges dict
            if pair not in self.merges:
                break
            tokens=merge_pair(tokens,pair,self.merges[pair]) 
        return tokens
    
    def decode(self,tokens):
        vocab=self.vocab
        text=b"".join(vocab[token] for token in tokens )# byte string concantenation
        text=text.decode('utf-8',errors="replace")
        return text
 #test   
b=Basic_Tokenizer()
b.train(text,276)
c=b.decode([44,45,46])
print(c)