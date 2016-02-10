############################################################
# CIS 521: Homework 1
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed because data types can not be 
implicitly cast to one another. For instance the operation 
2 + "hi" will return an error because it will not convert 
the string to an integer or vice a versa. However since python
is dynamically typed you may define variables that change type 
without error. For example one line may contain x = 20 and then
another line might declare x = "hi", this case x will point to a
string containing "hi". In other words variables do not need to be 
instanciated with a type. 
"""

python_concepts_question_2 = """
The problem is that we are trying to use a list as a key,
in python lists are mutable so they cannot be used as keys.
One solution is to either use a tuple instead of a list, or use 
the string as the key and return the value of the list. 
"""

python_concepts_question_3 = """
def concatenate2 is better for large inputs because it uses 
pythons built in function join. Since pythons built in functions
are optimized, and basically execute the same functionality as concatenate1 
but with a c implemenation. concatenate2 is better. 
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for elem in l if p(x)]

def concatenate(seqs):
    return[elem for lists in seqs for elem in lists]
    return result 

def transpose(matrix):
    trans = []
    for i in xrange(len(matrix[0])):
        trans += [[elem[i] for elem in matrix]]
    return trans 

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:] 

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    result = []
    for i in xrange(len(seq)+1): 
        result += [seq[:i]]
    return result

def suffixes(seq):
    result = [] 
    for i in xrange(len(seq)+1):
        result += [seq[i:]]
    return result 

def slices(seq):
    result = []
    for i in xrange(len(seq)):
        result +=[seq[i:]]
        for j in xrange(i+1, len(seq)):
            # result +=[seq[i:]]
            result +=[seq[i:j]]
    # result += [seq]
    return result


############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    return " ".join(text.lower().split())

def no_vowels(text):
    vowels = ["a","e","i","o","u","A","E","I","O","U"]
    text = list(text)
    for v in vowels:
        text = ["".join(elem) for elem in text if elem != v]
    return "".join(text)

def digits_to_words(text):
    words ={0: "zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",
            7:"seven", 8:"eight",9:"nine"}
    text = text.replace(".", " ")
    text = text.replace("-", " ")
    text = text.replace(",", " ")
    num_array = [letter for letter in text.split() if letter.isdigit()]
    num_array = "".join(num_array)
    result =["".join(words[int(num)]) for num in num_array]
    result = " ".join(result)
    return result

def to_mixed_case(name):
    name = name.lower()
    mix_case = ["".join(letter) for letter in name.split('_') if letter.isalnum]
    mix_case = " ".join(mix_case).strip().split()
    for i,word in enumerate(mix_case): 
        if(i>0): 
            mix_case[i] = mix_case[i].capitalize()
            # print mix_case[i]
    return "".join(mix_case)

    # print mix_case
    

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):
  
    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial 

    def __neg__(self):
        neg_list = [(-elem[0], elem[1]) for elem in self.polynomial]
        return Polynomial(tuple(neg_list))

    def __add__(self, other):
        results = tuple(self.polynomial + other.polynomial)
        return Polynomial(results)

    def __sub__(self, other):
        negate = -other
        return Polynomial((self.polynomial + negate.get_polynomial()))

    def __mul__(self, other):
        result = []
        poly = self.polynomial
        other_poly = other.polynomial
        for i in xrange(len(self.polynomial)):
            for j in xrange(len(other.polynomial)):
                result += [(poly[i][0]*other_poly[j][0], 
                            poly[i][1]+other_poly[j][1])]
        return Polynomial(tuple(result))

    def __call__(self, x):
        result = 0
        poly = self.polynomial
        for i in range(len(self.get_polynomial())):
            result += (x**poly[i][1])*poly[i][0]
        return result

    def simplify(self):
        poly = self.polynomial
        inter = list(poly[:])
        result = []
        for i, p in enumerate(inter):
            for j, q in enumerate(inter):         
                if((p[1] == q[1]) and i != j):
                    if(i >= len(inter)):
                        inter.insert(j,(p[0]+q[0], p[1]))
                        inter.pop(j+1)
                    else:
                        inter.insert(j,(p[0]+q[0], p[1]))
                        inter.pop(j+1)
                        inter.pop(i)
        result = [ply for ply in inter if (ply[0] != 0)]
        if(not result):
            self.polynomial = ((0,0),)
            return ((0,0),)
        else:
            self.polynomial = tuple(result)
            return tuple(result) 
   
    def __str__(self):
        result = ''
        poly = self.get_polynomial()
        term_list =[ str(abs(elem[0])) +'x^'+ str(elem[1]) for elem in poly]
        for i,p in enumerate(poly):
            if(p[1] == 0): 
                term_list[i] = str(p[0])
            if (p[0] ==1 or p[0] == -1):
                term_list[i] ='x^' + str(p[1])
            if(p[1] == 1):
                term_list[i] = str(p[0])+'x'
            if(i > 0):
                if(p[0] < 0):
                    result = ' - '.join([result, term_list[i]])
                else:
                    result = ' + '.join([result, term_list[i]])
            else:
                result = term_list[i]
        return result

############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
    5 hours, I had trouble remembering built in functions
"""

feedback_question_2 = """
    Polynomial simplify was most challenging, and remembering
    how the results should be returned
"""

feedback_question_3 = """
    I wouldn't change anything, I liked learning how to do 
    complicated list comprehension 
"""
