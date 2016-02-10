
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
        print len(inter)
        for i, p in enumerate(inter):
            for j, q in enumerate(inter):         
                if((p[1] == q[1]) and i != j):
                    print(i,j, len(inter))
                    if(i >= len(inter)):
                        inter.insert(j,(p[0]+q[0], p[1]))
                        inter.pop(j+1)
                    else:
                        inter.insert(j,(p[0]+q[0], p[1]))
                        inter.pop(j+1)
                        inter.pop(i)
            print inter
        self.polynomial = tuple(inter)
        return tuple(inter) 
   
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
            if(p[0] < 0):
                result = ' - '.join([result, term_list[i]])
            if(i > 0):
                    result = ' + '.join([result, term_list[i]])
            else:
                result = term_list[i]
        return result











