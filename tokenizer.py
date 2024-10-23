import regex as re
from collections import Counter
with open('train.txt','r') as f:
    text=f.read()
print(text)
print(f'length:{len(text)}')
print("-----")
encoding=list(map(int,text.encode('utf-8')))
print(encoding)
print(f'length:{len(encoding)}')
max(encoding)


def max_pair(x):
    pairlists=[]
    for i in range(len(x)-1):
        pair=(x[i],x[i+1])
        pairlists.append(pair)
    f=Counter([p for p in pairlists])
    return f.most_common(1)[0][0]


def Byte_Pair_encode(x, vocab_size=276):
    x=x.copy()
    v = 0
    max_merge = vocab_size - 256
    merge = {}
    #iterate for the maximum number of merges
    for i in range(max_merge):
        hfelement = max_pair(x)  #find the most frequent pair
        j=0
        while j<len(x)-1:
            if (x[j],x[j+1])== hfelement:
                merge[(x[j], x[j+1])] = v + 256  #store the merge
                x[j] = v + 256  #replace the first element of the pair
                x.pop(j+1)
            else:
                j+=1
        v += 1
    return x, merge

a,merges=Byte_Pair_encode(encoding)

for key,values in merges.items():
  print(f"{key} merges with {values}")

def encode(text):
    #text=text.copy()
    encode=list(text.encode('utf-8'))
    i=0
    while i<len(encode)-1:
        if (encode[i],encode[i+1]) in merges:
            encode[i]=merges[(encode[i],encode[i+1])]
            encode.pop(i+1)
        else:
            i+=1 
    return encode    
            
b=encode("Guten Morgan.Ich bin Sayuj Chapagain.")
merge_inv={v:k for k,v in merges.items()}

def org_list(tokens,original):
    for i in tokens:
        if i<=255:
            original.append(i)
        else:
            org_list([merge_inv[i][0]],original)
            org_list([merge_inv[i][1]],original)
def decode(tokens):
    original=[]
    org_list(tokens,original)
    string=bytes(original).decode('utf-8',errors="replace")  
    return string
gpt2pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")

print(re.findall(gpt2pat, "Hello've world123 //!!HOW's     are you   "))

encode("Hello've worlds123")





