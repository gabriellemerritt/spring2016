############################################################
# CIS 521: Homework 6
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import email
import math
import os
import re
import random
from string import translate, maketrans, punctuation
from collections import Counter

############################################################
# Section 1: Probability
############################################################

# Set the following variables to True or False.
section_1_problem_1a = True
section_1_problem_1b = True
section_1_problem_1c = False

B =.01
notB = .99
E =.005
notE =.995
PA_BE = [.97,.95,.23,.001]

A = PA_BE[0]*B*E + PA_BE[1]*B*notE + PA_BE[2]*notB*E + PA_BE[3]*notB*notE
notA  = 1.0 - A
J = .85*A + .1*notA
PA_E = (PA_BE[0]*B + PA_BE[2]*notB)
PA_B = (PA_BE[0]*E + PA_BE[1]*notE)
PnotA_B = ((1-PA_BE[0])*E + (1-PA_BE[1])*notE)
PE_A =  PA_E*E / A
PB_A = (PA_B)*B/A 
PnotA_notE = ((1-PA_BE[1])*B + (1-PA_BE[3])*notB)
PnotE_notA = PnotA_notE*notE/notA
PB_notA = PnotA_B*B/(notA)
P_BnotEnotAJM = (1-PA_BE[2])*0.1*.15*B*notE
P_notBEnotAnotJM = notB*E*(1-PA_BE[1])*(1 -(.1))*0.15

# Set the following variables to True or False.
section_1_problem_2a = True
section_1_problem_2b = False
section_1_problem_2c = False
section_1_problem_2d = False
section_1_problem_2e = True
section_1_problem_2f = False
section_1_problem_2g = False
section_1_problem_2h = True

# Set the following variables to probabilities, expressed as decimals between 0
# and 1.

section_1_problem_3a = PA_BE[0]*B*E + PA_BE[1]*B*notE + PA_BE[2]*notB*E + PA_BE[3]*notB*notE
section_1_problem_3b = notA
section_1_problem_3c = J
section_1_problem_3d = PE_A
section_1_problem_3e = PB_notA
section_1_problem_3f = P_BnotEnotAJM
section_1_problem_3g = P_notBEnotAnotJM


############################################################
# Section 2: Spam Filter
############################################################
def load_tokens(email_path):
    f = open(email_path)
    msg = email.message_from_file(f)
    word_list = []
    line_list = [" ".join(lines.split())
                 for lines in email.iterators.body_line_iterator(msg)]
    [[word_list.append(word) for word in line.split()] for line in line_list]
    return word_list

def load_all(email_path):
	line_list = [] 
	word_list = []
	with open(email_path) as f:
		for line in f:	
			line_list += re.findall(r"[\w']+|[.,!?;]",line)
	return line_list
	# for words in line_list:
 #        word_list += re.findall(r"[\w']+|[.,!?;]", words)


def load_advanced_tokens(email_path):
    f = open(email_path)
    msg = email.message_from_file(f)
    word_list = []
    line_list = []
    T = maketrans(punctuation, ' ' * len(punctuation))
    for lines in email.iterators.body_line_iterator(msg):
    	    line_list += translate(lines, T).split()
    for words in line_list:
        word_list.append(words)
    return word_list


def load_advanced_tokens2(email_path):
    f = open(email_path)
    msg = email.message_from_file(f)
    word_list = []
    line_list = [" ".join(lines.split())
                 for lines in email.iterators.body_line_iterator(msg)]
    for words in line_list:
        word_list += re.findall(r"[\w']+|[.,!?;]", words)
    return word_list

def bigram_tokens_all(email_path):
	bigram_list = []
	prev_word = " "
	for word in load_all(email_path):
		bigram_list += [prev_word + ' ' + word]
		prev_word = word
	return bigram_list

def bigram_tokens(email_path):
	bigram_list = []
	prev_word = " "
	for word in load_advanced_tokens2(email_path):
		bigram_list += [prev_word + ' ' + word]
		prev_word = word
	return bigram_list


def log_advanced_probs(email_paths, smoothing):
    prob_dict = {}
    word_count = {}
    for path in email_paths:
        for token in load_all(path):
            if(token in word_count):
                word_count[token] += 1
            else:
                word_count[token] = 1
    den = sum(word_count.itervalues()) + smoothing * \
        (len(word_count.keys()) + 1.0)
    prob_dict["<UNK>"] = math.log(smoothing / (den))
    for w in word_count:
        prob_dict[w] = math.log((word_count[w] + smoothing) / (den))
    return prob_dict


def log_probs(email_paths, smoothing):
    prob_dict = {}
    word_count = {}
    for path in email_paths:
        for token in load_advanced_tokens2(path):
            if(token in word_count):
                word_count[token] += 1
            else:
                word_count[token] = 1
    den = sum(word_count.itervalues()) + smoothing * \
        (len(word_count.keys()) + 1.0)
    prob_dict["<UNK>"] = math.log(smoothing / (den))
    for w in word_count:
        prob_dict[w] = math.log((word_count[w] + smoothing) / (den))
    return prob_dict


def bigram_probs(email_paths, smoothing):
    bigram_probs = {}
    bigram_count = {}
    n_gram_dict = log_advanced_probs(email_paths, smoothing)
    for path in email_paths:
        for bigram in bigram_tokens_all(path):
            if(bigram in bigram_count):
                bigram_count[bigram] += 1
            else:
                bigram_count[bigram] = 1
    den = sum(bigram_count.itervalues()) + smoothing * (len(bigram_count.keys()) + 1.0)  
    for bi in bigram_count:
    	unigram = bi.split()[0]
        n_gram_dict[bi] = (math.log((bigram_count[bi] + smoothing) / (den))) - (n_gram_dict[unigram])
    return n_gram_dict




def search_dir(path):
    for _, _, files in os.walk(path):
        files = [path + "/%s" % f for f in files if not f[0] == '.']
    return files


class SpamFilter(object):

    # Note that the initialization signature here is slightly different than the
    # one in the previous homework. In particular, any smoothing parameters used
    # by your model will have to be hard-coded in.

    def __init__(self, spam_dir, ham_dir, smoothing=1e-150, testing=False, train_per=1):
        spam_paths = search_dir(spam_dir)
        ham_paths = search_dir(ham_dir)
        index = len(ham_paths)
        if(testing):
        	random.shuffle(spam_paths)
        	random.shuffle(ham_paths)
        	index = index/train_per

    	self.spam_paths = spam_paths[0:index]
    	self.ham_paths = ham_paths[0:index]

        self.smoothing = smoothing
        self.spam_dic_uni = log_advanced_probs(self.spam_paths, smoothing)
        self.ham_dic_uni = log_advanced_probs(self.ham_paths, smoothing)
        self.spam_dic = bigram_probs(self.spam_paths, smoothing)
        self.ham_dic = bigram_probs(self.ham_paths, smoothing)
        self.prob_not_spam = float(len(self.ham_paths)) / float(len(self.ham_paths) + float(len(self.spam_paths)))
        self.prob_spam = 1.0 - self.prob_not_spam

    def is_spam(self, email_path):
        c_ham = 0
        c_spam = 0
        for token in bigram_tokens_all(email_path):
            bigram  = token       
            if bigram in self.ham_dic:
                c_ham += self.ham_dic[bigram]
            else:
                c_ham += self.ham_dic["<UNK>"]
            if bigram in self.spam_dic:
                c_spam += self.spam_dic[bigram]
            else:
                c_spam += self.spam_dic["<UNK>"]
        c_ham += math.log(self.prob_not_spam)
        c_spam += math.log(self.prob_spam)
        return (c_spam > c_ham)

    def most_indicative_spam(self, n):
        indictive = {}
        for token in self.spam_dic:
            if token in self.ham_dic:
                pw = math.exp(self.spam_dic[token])*(self.prob_spam) +  math.exp(self.ham_dic[token])*(self.prob_not_spam)
                indictive[token] = self.spam_dic[token] - math.log(pw)
        values = Counter(indictive).most_common(n)
        return [v[0] for v in values]

    def is_spam_unigram(self, email_path):
    	c_ham = 0
        c_spam = 0
        for token in load_advanced_tokens2(email_path):
            bigram  = token       
            if bigram in self.ham_dic_uni:
                c_ham += self.ham_dic_uni[bigram]
            else:
                c_ham += self.ham_dic_uni["<UNK>"]
            if bigram in self.spam_dic_uni:
                c_spam += self.spam_dic_uni[bigram]
            else:
                c_spam += self.spam_dic_uni["<UNK>"]
        c_ham += math.log(self.prob_not_spam)
        c_spam += math.log(self.prob_spam)
        return (c_spam > c_ham)

