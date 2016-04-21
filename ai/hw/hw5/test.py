from homework5 import * 
from sklearn import metrics
import numpy as np
ham_dir = "/Users/gabriellemerritt/Documents/spring2016/ai/hw/hw5/data/train/ham"
spam_dir = "data/train/spam"
dev_ham_dir = "data/dev/ham"
dev_spam_dir = "data/dev/spam"

test_ham = search_dir(dev_ham_dir)
test_spam = search_dir(dev_spam_dir)
ham_label = np.array([[False for j in range(1)] for i in range(len(test_ham))])
spam_label = np.array([[True for j in range(1)] for i in range(len(test_spam))])
smoothing = 1e-5
# print load_tokens(spam_dir+"spam1")[1:5]
# paths = [ spam_dir+"spam%d" % i for i in range(1,11)]
# p = log_probs(paths,1e-5)
# print ("Probability of word the",  p["<UNK>"])
# print ("Probability of word line", p["Credit"])
# files = search_dir(spam_dir)
# print "Spam file len " ,files
# print p.keys()

# training
ham_pred = np.ones((len(ham_label),1), dtype = bool)
sf = SpamFilter(spam_dir, ham_dir, smoothing)
for i,path in enumerate(test_ham): 
	ham_pred[i] = sf.is_spam(path)

spam_pred = np.ones((len(spam_label),1), dtype = bool)
for i,path in enumerate(test_spam): 
	spam_pred[i] = sf.is_spam(path)

print " Test accuracy : %f" % (metrics.accuracy_score(ham_label,ham_pred)*metrics.accuracy_score(spam_label,spam_pred))
