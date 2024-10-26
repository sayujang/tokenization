# match this
import tiktoken
import regex as re
enc = tiktoken.get_encoding("cl100k_base") # this is the GPT-4 tokenizer
ids = enc.encode("Servus!! My friend ")
#print(ids)
special={'<|start|>':1000,'<|end|>':2000}
text="blablaba<|start|>iam sayuj chapagain"
special_pattern = "(" + "|".join(re.escape(k) for k in special) + ")" #| and () are special characters in regex so needs to be escaped by prefixing them with \ 
special_chunks = re.split(special_pattern, text)
# print(special_chunks)
# print(special_pattern)
# a="".join(re.escape(k) for k in special) #iterated over keys of dictionary 
# print(a)\
text="dkdakdkdl"
dictc={'a':45,'b':84,'c':90}
a=[a for a in dictc]
print(a)
assert all(token not in text for token in dictc)