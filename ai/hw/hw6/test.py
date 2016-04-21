from homework6 import * 
from sklearn import metrics
import numpy as np
ham_dir = "data/train/ham"
spam_dir = "data/train/spam"
dev_ham_dir = "data/dev/ham"
dev_spam_dir = "data/dev/spam"

test_ham = search_dir(dev_ham_dir)
test_spam = search_dir(dev_spam_dir)
ham_label = np.array([[False for j in range(1)] for i in range(len(test_ham))])
spam_label = np.array([[True for j in range(1)] for i in range(len(test_spam))])
# print load_tokens(spam_dir+"spam1")[1:5]
# paths = [ spam_dir+"spam%d" % i for i in range(1,11)]
# p = log_probs(paths,1e-5)
# print ("Probability of word the",  p["<UNK>"])
# print ("Probability of word line", p["Credit"])
# files = search_dir(spam_dir)
# print "Spam file len " ,files
# print p.keys()

# training
# load_all(dev_spam_dir+"/dev296")
ham_count = 0 
spam_count =0

bigram_ham_count = 0
bigram_spam_count = 0 
print len(ham_label)
ham_pred = np.ones((len(ham_label),1), dtype = bool)
ham_pred_uni = np.ones((len(ham_label),1), dtype = bool)
sf = SpamFilter(spam_dir, ham_dir)

for i,path in enumerate(test_ham): 
	ham_pred[i] = sf.is_spam(path)
	ham_pred_uni[i] = sf.is_spam_unigram(path)
	if(ham_pred[i] == True):
		bigram_ham_count += 1
		print path
	if(ham_pred_uni[i] == True):
		ham_count += 1

spam_pred_uni = np.ones((len(spam_label),1), dtype = bool)
spam_pred = np.ones((len(spam_label),1), dtype = bool)
for i,path in enumerate(test_spam): 
	spam_pred[i] = sf.is_spam(path)
	spam_pred_uni[i] = sf.is_spam_unigram(path)
	if(spam_pred[i] == False): 
		bigram_spam_count += 1
		print path
	if(spam_pred_uni[i] == False):
		spam_count += 1
print " Indictive of spam : ", sf.most_indicative_spam(1000)[990:-1]
print "Unigram Ham Incorrect %i , Unigram Spam Incorrect %i" % (ham_count, spam_count)
print "Bigram Ham Incorrect %i , Bigram Spam Incorrect %i" % (bigram_ham_count, bigram_spam_count)
print " Ham  Test Bigram Accuracy : %f" % (metrics.accuracy_score(ham_label,ham_pred))
print " Spam Test Bigram  Accuracy : %f" % (metrics.accuracy_score(spam_label,spam_pred))
print " Overall Test Accuracy : %f" % (metrics.accuracy_score(ham_label,ham_pred)*metrics.accuracy_score(spam_label,spam_pred))