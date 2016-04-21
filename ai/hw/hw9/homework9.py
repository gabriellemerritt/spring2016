############################################################
# CIS 521: Homework 9
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

import homework9_data as data

# Include your imports here, if any are used.
from collections import OrderedDict
import copy


############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.iterations = iterations
        self.classes = {}
        self.w = {}
        self.feature = examples
        for vector, label in examples:
            for key in vector: 
                if key not in self.w: 
                    self.w[key] = 0
            if label not in self.classes:
                self.classes[label] = 1  
        self.train()


    def dot_product_sign(self, w_dict, x_dict):
        dot_p = 0 
        for x in x_dict:
            dot_p += float(x_dict[x])*w_dict[x]
        # print "Features: %s , Dot Product : %f, Weight Vector: %s" % (x_dict,dot_p, w_dict)
        return dot_p


    def train(self):
        label = False
        for i in range(self.iterations):
            for precp in self.feature:
                if self.dot_product_sign(self.w, precp[0]) > 0:
                    label = True
                if (label != precp[1]):
                    if(precp[1]):
                        for i in precp[0]:
                            self.w[i] += precp[0][i]
                    else: 
                        for i in precp[0]:
                            self.w[i] -= precp[0][i]

    def predict(self, x):
       return self.dot_product_sign(self.w, x) > 0


def arg_max(value_list):
    test = max(enumerate(value_list), key=lambda x: x[1])[0]
    return value_list[test][1]




class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.iterations = iterations
        self.w = {}
        self.features = examples
        self.b = BinaryPerceptron(examples, iterations)
        self.classes = self.b.classes
        init_w = self.b.w.fromkeys(self.b.w.keys(),0)
        for klass in self.b.classes:
            self.w[klass] = copy.deepcopy(init_w)
        self.train()

    def adj_weights(self,x,y,y_pred):
        for feat in x:
            self.w[y][feat] += x[feat]
        for ft in x: 
                self.w[y_pred][ft] -= x[ft]
        # print "After y_pred\n", w

    def train(self):
        for i in range(self.iterations): 
            for vector,y in self.features:
                y_pred = self.predict(vector)
                if(y != y_pred):
                    self.adj_weights(vector, y, y_pred)

    def predict(self, x):
        val = [tuple((self.b.dot_product_sign(self.w[klass], x), klass)) for klass in self.classes]
        y_pred = arg_max(val)
        return y_pred


############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        self.features = []
        self.iterations = 55 
        for features, label in data:
            self.features += [tuple((({"x1": features[0], "x2": features[1], "x3": features[2], "x4": features[3]}), label))]
        
        self.mc = MulticlassPerceptron(self.features, self.iterations)

    def classify(self, instance):
        x =  {"x1": instance[0], "x2": instance[1], "x3": instance[2], "x4": instance[3]}
        return self.mc.predict(x)


def create_dict(vector, a):
    for i, x in enumerate(vector):
        a["x"+str(i+1)] = x 
    # for key in sorted(a):
    #     print "Key %s: , Values : %s" % (key,a[key])
    return a


class DigitClassifier(object):

    def __init__(self, data):
        self.numbering = ["x"+str(i+1) for i in range(64)]
        self.feat_form = dict([(x, 0) for x in self.numbering])
        
        self.features = []
        for vector, label in data:
            self.features += [tuple((create_dict(vector, copy.deepcopy(self.feat_form)), label))]
        self.mc = MulticlassPerceptron(self.features, 20) 

    def classify(self, instance):
        x = create_dict(instance, copy.deepcopy(self.feat_form))
        return self.mc.predict(x)


class BiasClassifier(object):

    def __init__(self, data):
        self.instances = 10
        self.bias = 1.
        self.features = []
        for features, label in data:    
            self.features += [tuple(({"x1": features}, label))]
        self.b = BinaryPerceptron(self.features, self.instances)

    def classify(self, instance):
        x ={"x1": instance}
        return self.b.predict(x)

class MysteryClassifier1(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

class MysteryClassifier2(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
