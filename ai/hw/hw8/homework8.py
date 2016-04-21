############################################################
# CIS 521: Homework 8
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

import math 
from operator import itemgetter

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    corpus = []
    model = []
    with open(path) as f:
        for line in f:
            word_list = line.split()
            tes = [tuple(word.split("=")) for word in word_list]
            corpus += [tes]
    return corpus


# combine these to be faster

def trans_prob(line, word_tag_dict):
    prev_tag = ''
    for i , (word, pos) in enumerate(line):
        if i == 0:
            prev_tag = pos
            continue
        if (prev_tag, pos) in word_tag_dict:
            word_tag_dict[(prev_tag, pos)] += 1
        else:
            word_tag_dict[(prev_tag, pos)] = 1
        prev_tag = pos
    return word_tag_dict


def emission_prob(line, tag_dict, context_dict):
    for word, tag in line:
        if tag in context_dict:
            context_dict[tag] += 1
        else:
            context_dict[tag] = 1
        if (word, tag) in tag_dict:
            tag_dict[(word, tag)] += 1
        else:
            tag_dict[(word, tag)] = 1
    return tag_dict, context_dict


def initial_prob(line, pi_dict):
    tag = line[0][1]
    if tag in pi_dict:
        pi_dict[tag] += 1
    else:
        pi_dict[tag] = 1
    return pi_dict 


def probs(corpus, smoothing=1e-5):
    word_tag_dict = {}
    pi_dict = {}
    tag_dict = {}
    emission_probs_dict = {}
    context_dict = {}
    trans_probs = {}
    pi_prob_dict = {}

    for line in corpus:
        pi_dict = initial_prob(line, pi_dict)
        tag_dict, context_dict = emission_prob(line, tag_dict, context_dict)
        word_tag_dict = trans_prob(line, word_tag_dict)

    den_bi_tag = sum(word_tag_dict.itervalues()) + smoothing * \
        (len(word_tag_dict.keys()) + 1.0)

    den_unk_tag = sum(word_tag_dict.itervalues()) + smoothing * \
        (len(word_tag_dict.keys()) + 1.0)

    den = sum(pi_dict.itervalues()) + smoothing * \
        (len(pi_dict.keys()) + 1.0)

    # TODO: check this 
    unknown_tag = smoothing / (smoothing * (sum(context_dict.itervalues()) + 1.0))

    trans_unk_tag = math.log(smoothing / den_unk_tag)

    # look into [word, "UNK"]
    for word, tag in tag_dict:
        emission_probs_dict[(word, tag)] = math.log(
            (tag_dict[(word, tag)] + smoothing) / (context_dict[tag] + (1.0 + len(context_dict.keys()))))
        emission_probs_dict[("<UNK>", tag)] = math.log(
            smoothing / (context_dict[tag] + (1.0 + len(context_dict.keys()))))

    # look at unknown probability
    for prev_tag, tag in word_tag_dict:
        trans_probs[(prev_tag, tag)] = math.log(((word_tag_dict[(prev_tag, tag)] + smoothing) / ((context_dict[prev_tag] + smoothing) * (len(context_dict.keys()) + 1.0))))
        trans_probs[(prev_tag, "<UNK>")] = math.log((smoothing / ((context_dict[prev_tag] + smoothing) * (len(context_dict.keys()) + 1.0))))
        # trans_probs[("<UNK>", "<UNK>")] = math.log(unknown_tag)
        # trans_probs[("<UNK>", tag)] = math.log(unknown_tag)

    for w in pi_dict:
        pi_prob_dict[w] = math.log((pi_dict[w] + smoothing)) / den
    pi_prob_dict["<UNK>"] = math.log((smoothing / den))

    return pi_prob_dict, trans_probs, emission_probs_dict, context_dict


class Tagger(object):

    def __init__(self, sentences):
       self.pi_state, self.trans_state, self.emission_state,  self.context_tags = probs(sentences)
       
    def most_probable_tags(self, tokens):
        tag_list = [None]*len(tokens)
        for i,word in enumerate(tokens):
            max_prob = - float("inf")
            for tag in self.context_tags:
                if (word,tag) in self.emission_state:
                    # print "word: %s , tag: %s, prob: %f" % (word, tag, self.emission_state[(word, tag)])
                    if self.emission_state[(word, tag)] > max_prob:
                        max_prob = self.emission_state[(word, tag)]
                        tag_list[i] = tag
                elif self.emission_state[("<UNK>",tag)] > max_prob:
                        max_prob = self.emission_state[("<UNK>", tag)]
                        tag_list[i] = tag
        return tag_list

    def t_get_prob(self, prev_tag, tag):
        if (prev_tag, tag) in self.trans_state: 
            return self.trans_state[(prev_tag, tag)]
        else: 
            return self.trans_state[(prev_tag, "<UNK>")]


    def e_get_prob(self,  word, tag):
        if (word, tag) in self.emission_state:
            return   self.emission_state[(word, tag)]
        else:
            return self.emission_state[("<UNK>", tag)]

    def i_get_prob(self, tag):
        if tag in self.pi_state: 
            return self.pi_state[tag]
        else: 
            return self.pi_state["<UNK>"]


    def viterbi_tags(self, tokens):
        prev_tag = ''
        answer = 0
        circle = {}
        path = {}
        max_val =  -float("inf")
        tag_list = [None]*len(tokens)
        for i,word in enumerate(tokens):
            # generate random sequences
            for tag in self.context_tags:  
                if i == 0:
                    circle[(tag, i )] = self.i_get_prob(tag)+self.e_get_prob(word,tag)
                    prev_tag = tag 
                    continue
                prev_circle_list = [tuple((tg, (circle[(tg, i-1)]+self.t_get_prob(tg, tag)))) for tg in self.context_tags]
                max_c = max(prev_circle_list, key=itemgetter(1))
                path[(tag, i )] = max_c
                circle[(tag,i)] = max_c[1]+ self.e_get_prob(word, tag)
        last_max_list = [tuple((tg, circle[(tg, len(tokens)-1)])) for tg in self.context_tags]
        last_max = max(last_max_list, key=itemgetter(1))
        tag_list[len(tokens)-1] = last_max[0]
        for i in range(len(tokens)-2,-1, -1):
            last_max = path[(last_max[0],i+1)]
            tag_list[i] = last_max[0]
         
        return tag_list


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent 10 hours 
"""

feedback_question_2 = """
back propagation / understanding viterbi_tags 
"""

feedback_question_3 = """
n/a
"""
