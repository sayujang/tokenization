def get_stats(x):
    count={}
    for pair in zip(x,x[1:]):
        count[pair]=count.get(pair,0)+1
    return count
def merge_pair(tokens,pair,element):
    new_tokens=[]
    i=0
    while i<len(tokens):
        if  i<len(tokens)-1 and tokens[i]==pair[0] and tokens[i+1]==pair[1]:
            new_tokens.append(element)
            i+=2
        else:
            new_tokens.append(tokens[i])
            i+=1
    return new_tokens
class Tokenizer:
    def __init__(self):
        self.merges={}
        self.vocab=self.build_vocab()
        self.splits=''
        self.special_tokens={}
    def train(self,text,vocab_size):
        raise NotImplementedError # raises an error when the derived class calls this function without overwriting
    def encode(self,text):
        raise NotImplementedError
    def decode(self,tokens):
        raise NotImplementedError
    def build_vocab(self,):
        vocab={token:bytes([token]) for token in range(256)}
        for (p1,p0),index in self.merges.items():
            vocab[index]=vocab[p1]+vocab[p0]
        return vocab