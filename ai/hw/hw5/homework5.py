############################################################
# CIS 521: Homework 5
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
from collections import Counter 
############################################################
# Section 1: Spam Filter
############################################################


def load_tokens(email_path):
    f = open(email_path)
    msg = email.message_from_file(f)
    word_list = []
    line_list = [" ".join(lines.split())
                 for lines in email.iterators.body_line_iterator(msg)]
    [[word_list.append(word) for word in line.split()] for line in line_list]
    return word_list


def log_probs(email_paths, smoothing):
    prob_dict = {}
    word_count = {}
    for path in email_paths:
        for token in load_tokens(path):
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


def search_dir(path):
    for _, _, files in os.walk(path):
        files = [path + "/%s" % f for f in files if not f[0] == '.']
    return files


class SpamFilter(object):

    def __init__(self, spam_dir , ham_dir, smoothing):
        self.spam_paths = search_dir(spam_dir)
        self.ham_paths = search_dir(ham_dir)
        self.smoothing = smoothing
        self.spam_dic = log_probs(self.spam_paths, smoothing)
        self.ham_dic = log_probs(self.ham_paths, smoothing)
        self.prob_not_spam = float(len(self.ham_paths)) / float(len(self.ham_paths) + float(len(self.spam_paths)))
        self.prob_spam = 1.0 - self.prob_not_spam

    def is_spam(self, email_path):
        c_ham = 0
        c_spam = 0
        for token in load_tokens(email_path):
            if token in self.ham_dic:
                c_ham += self.ham_dic[token]
            else:
                c_ham += self.ham_dic["<UNK>"]
            if token in self.spam_dic:
                c_spam += self.spam_dic[token]
            else:
                c_spam += self.spam_dic["<UNK>"]
        c_ham += math.log(self.prob_not_spam)
        c_spam += math.log(self.prob_spam)
        return (c_spam > c_ham)

#TODO
    def most_indicative_spam(self, n):
        indictive = {}
        for token in self.spam_dic:
            if token in self.ham_dic:
                pw = math.exp(self.spam_dic[token])*(self.prob_spam) +  math.exp(self.ham_dic[token])*(self.prob_not_spam)
                indictive[token] = self.spam_dic[token] - math.log(pw)
        values = Counter(indictive).most_common(n)
        return [v[0] for v in values]

    def most_indicative_ham(self, n):
        indictive = {}
        for token in self.ham_dic:
            if token in self.spam_dic:
                pw = math.exp(self.ham_dic[token])*self.prob_not_spam + math.exp(self.spam_dic[token])*self.prob_spam
                indictive[token] = self.ham_dic[token] - math.log(pw)
        values = Counter(indictive).most_common(n)
        return [v[0] for v in values]

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Strangely only 4 hours
"""

feedback_question_2 = """
Optimization
"""

feedback_question_3 = """
I like how short it was 
"""
