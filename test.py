# match this
import tiktoken
enc = tiktoken.get_encoding("cl100k_base") # this is the GPT-4 tokenizer
ids = enc.encode("Servus!! My friend ")
print(ids)
# hello world!!!? (안녕하세요!) lol123 😉
a=[1,3,4,5]
b=[5,6]
a.extend(b)
print(a)