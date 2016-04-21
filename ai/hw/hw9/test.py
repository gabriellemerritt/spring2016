from homework9 import *



ex_data = [
    ((6.0, 2.2, 4.0, 1.0), "iris-versicolor"),
    ((6.9, 3.1, 5.4, 2.1), "iris-virginica"),
    ((5.5, 2.4, 3.7, 1.0), "iris-versicolor")]

print "Binary Classifier Test Case "
train = [({"x1": 1}, True), ({"x2": 1}, True),
         ({"x1": -1}, False), ({"x2": -1}, False)]

b = BinaryPerceptron(train, 1)
test = [{"x1": 1}, {"x1": 1, "x2": 1}, {
    "x1": -1, "x2": 1.5}, {"x1": -0.5, "x2": -2}]
print [b.predict(x) for x in test]
# train = [({"x1": 1}, True), ({"x2": 1}, True), ({"x1": -1}, False), ({"x2": -1}, False)]
print "\nMulticlass Perceptron"
train = [({"x1": 1}, 1), ({"x1": 1, "x2": 1}, 2), ({"x2": 1}, 3),
         ({"x1": -1, "x2": 1}, 4), ({"x1": -1}, 5), ({"x1": -1, "x2": -1}, 6),
         ({"x2": -1}, 7), ({"x1": 1, "x2": -1}, 8)]
p = MulticlassPerceptron(train, 10)
print [p.predict(x) for x, y in train]


print "\nIris Problem"
c = IrisClassifier(data.iris)
print c.classify((5.1, 3.5, 1.4, 0.2))
print c.classify((7.0, 3.2, 4.7, 1.4))

print "\nDigit Classifier"
# d = DigitClassifier(data.digits)
# print d.classify((0,0,5,13,9,1,0,0,0,0,13,15,10,15,5,0,0,3,15,2,0,11,8,0,0,4,12,0,0,8,8,0,0,5,8,0,0,9,8,0,0,4,11,0,1,12,7,0,0,2,14,5,10,12,0,0,0,0,6,13,10,0,0,0))

print "\nBias Classifier"
c = BiasClassifier(data.bias)
print 	[c.classify(x) for x in (-1, 0, 0.5, 1.5, 2)]
