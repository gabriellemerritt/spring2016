import homework8 as hw
test_corp = hw.load_corpus("brown_corpus.txt")
t = hw.Tagger(test_corp)
s = "I am waiting to reply".split()
s = "I saw the play".split()
print "Most Prob Tags: %s" %(t.most_probable_tags(s))
print "Viterbi Tags: %s " %(t.viterbi_tags(s))
# print t.most_probable_tags(["The", "man", "walks", "."])
# print t.most_probable_tags(["The", "blue", "bird", "sings"])