from homework7 import *

# text ="hi, my name's martha, martha is my name"
# tokens = tokenize(text) 
# ngrams(1,["a", "b", "c"])
# m = NgramModel(1) 
# m.update("a b c d")
# m.update("a b a b")
# print [m.random_token(("<START>",))for i in range(6)]
# print [m.random_token(("b",)) for i in range(6)]
# # # print m.random_text(13)
m = create_ngram_model(13, "frankenstein.txt")
print m.random_text(15)
