from baselayer import Tokenizer,get_stats,merge_pair
import regex as re
GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
GPT2_SPLIT_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
with open('train.txt','r',encoding='utf-8') as f:
    text=f.read()
class RegexTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.pattern=GPT4_SPLIT_PATTERN
        self.compile_pattern=re.compile(self.pattern)
        self.special_tokens={}
        self.inverse_special_tokens={}
    def train(self,text,vocab_size):
        chunks=re.findall(self.compile_pattern,text) #regex splits string into list of chunks of string
        chunk_ids=[list(ch.encode('utf-8')) for ch in chunks]
        merges={}
        num_merges=vocab_size-256
        vocab={t:bytes([t]) for t in range(256)}
        for i in range(num_merges):
            stats={}
            for ch in chunk_ids: #makes sure that pair are created only from a chunk separately
                get_stats(ch,stats) #gets updated to stats itself as stats is an iterable object
            pair=max(stats,key=lambda k: stats[k])
            id=i+256
            chunk_ids=[merge_pair(ch,pair,id) for ch in chunk_ids]
            merges[pair]=id
            vocab[id]=vocab[pair[0]]+vocab[pair[1]]
        self.merges=merges
        self.vocab=vocab
    def register_special_tokens(self,special_token):# expects a dictionary of special tokens in the format {"token":tokenid}
        self.special_tokens=special_token
        self.inverse_special_tokens={i:k for k,i in special_token.items()}        
    def decode(self,tokens):
        bytelist=[]
        for t in tokens:
            if t in self.vocab:
                bytelist.append(self.vocab[t])
            elif t in self.inverse_special_tokens:
                bytelist.append(self.inverse_special_tokens[t])
            else:
                raise ValueError(f"Invalid token id: {t}")
        total=b"".join(bytelist)
        text=total.decode('utf-8',errors="replace")
        return text
    def encode_chunks(self,chunks):
        chunks=list(chunks)
        while len(chunks)>=2:
            stats=get_stats(chunks)
            pair=min(stats,key=lambda k: self.merges.get(k,float("inf")))
            if pair not in self.merges:
                break
            chunks=merge_pair(chunks,pair,self.merges[pair])
        return chunks
    def encode_ordinary(self,text):
        chunks=re.findall(self.compile_pattern,text)
        total=[]
        for ch in chunks:
            ch=ch.encode('utf-8')
            ch=self.encode_chunks(ch)
            total.extend(ch)
        return total
    def encode_test(self,text):
        tokens=list(text.encode('utf-8'))
        while len(tokens)>=2:
            stats=get_stats(tokens)
            pair=min(stats,key=lambda k: self.merges.get(k,float('inf'))) #get pair in stats that has the lowest minted token in merges dict
            if pair not in self.merges:
                break
            tokens=merge_pair(tokens,pair,self.merges[pair]) 
        return tokens
    def encode(self,text,special_value="none_raise"):
        special={}
        if special_value=="all":
            special=self.special_tokens
        elif special_value=="none":
            special=None
        elif special_value=="none_raise":
            special=None
            assert all(tokens not in text for tokens in self.special_tokens)
        elif isinstance(special_value,set):
            special={k:v for k,v in self.special_tokens.items() if k in special_value}
        else:
            raise ValueError(f"special value={special_value} is not recognized")
        if not special:
            return self.encode_ordinary(text)
        id=[]
        special_pattern = "(" + "|".join(re.escape(k) for k in special) + ")" #| and () are special characters in regex so needs to be escaped by prefixing them with \ 
        special_chunks = re.split(special_pattern, text)
        for ch in special_chunks:
            if ch in special_pattern:
                id.append(special[ch])
            else:
                id.extend(self.encode_ordinary(ch))
        return id


a=RegexTokenizer()
a.train(text,10000)
b=a.encode_ordinary("Servus, my friends!!!  ")
print(b)


