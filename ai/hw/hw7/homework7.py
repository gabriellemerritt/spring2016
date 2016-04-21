############################################################
# CIS 521: Homework 7
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import re
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    regex = r"[\w]+|[%s]" % string.punctuation
    tokens = re.findall(regex, text)
    return tokens


def ngrams(n, tokens):
    for x in range(n-1):
        tokens.insert(x, "<START>")
    tokens.append("<END>")
    ngrams = []
    for i, token in enumerate(tokens):
            if(i-(n-1) < 0):
                ngrams += [(tuple(tokens[0:n-1]),token)]
            else: 
                ngrams += [(tuple(tokens[i-(n-1):i]),token)]
    return ngrams[n-1:]

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.token_counts = {}
        self.tokens = set()
        self.ngrams = []
        self.prob_dict = {}
        self.context_counts = {}

    def update(self, sentence):
        tokens = tokenize(sentence)
        grams = ngrams(self.n, tokens)
        self.ngrams += grams
        self.tokens.update(tokens)
        for context, token in grams:
            # print "Context is %s, Token is %s" % (context, token)
            if context in self.context_counts:
                self.context_counts[context] += 1
            else:
                self.context_counts[context] = 1
            if (context,token) in self.token_counts:
                self.token_counts[(context, token)] += 1
            else:
                self.token_counts[(context, token)] = 1

    def prob(self, context, token):
        den = 0
        num = 0
        if((context, token) in self.prob_dict):
            return self.prob_dict[(context, token)]
        if ((context, token) in self.token_counts):
            den = self.context_counts[context]
            num = self.token_counts[(context, token)]
            self.prob_dict[(context, token)] = float(num)/den
            return float(num)/den
        return 0.0

    def random_token(self, context):
        p_t = 0.0
        r = random.random()
        for token in sorted(self.tokens):
            p_t += self.prob(context, token)
            if(p_t > r):
                return token

    def random_text(self, token_count):
        sc = ()
        start = ()
        token_list = []
        if(self. n > 1):
            for x in range(self.n - 1):
                start += ("<START>", )
                sc = start
            for i in range(token_count):
                token = self.random_token(sc)
                token_list += [token]
                if token == "<END>":
                    sc = start
                else:
                    for ngram in self.ngrams:
                        if token == ngram[0][-1]:
                            sc = ngram[0]
                            break
        else:
            for i in range(token_count):
                token_list += [self.random_token(())]
        return ' '.join(token_list)


    def perplexity(self, sentence):
        perp_token = tokenize(sentence)
        m = len(perp_token)
        grams = ngrams(self.n, perp_token)
        sum_perp = 0
        for context, token in grams:
            p_w = self.prob(context, token)
            if p_w <= 0.0 :
                sum_perp += 0.0
            else:
                sum_perp += math.log(1.0/p_w)
        return math.exp(sum_perp)**(1.0/(m+1))

def create_ngram_model(n, path):
    i = 0
    model = NgramModel(n) 
    for line in open(path):
        model.update(line)
    return model

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
4 hours
"""

feedback_question_2 = """
getting the timing down was difficult
"""

feedback_question_3 = """
I liked hw short it was, I also liked learning how to quickly calculate n-grams
"""
