


import sklearn.cross_validation
import random
import sklearn
import math
import collections

'''
    This class can be used for two labels classification tasks using the Naive Bayes rule.
    The priori probability
    is assumed to be 0.5 when not given

'''


class BayesClassifier:
    def __init__(self, train, test, target, rawdata, all = 0):
        if all == 1:
            print 'lol'

        if len(train) != len(target):
            raise Exception("Dimensions of training and target do not match")
        self._train = train
        self._test = test
        self._target = target
        self._classes = list(set(self._target))

        if len(self._classes) != 2:
            raise Exception("Target list should have two unique labels")


    def _count(self, listing):
        keys = [pairs.keys() for pairs in listing]
        keysf = list(set(reduce(lambda x, y: x+y, keys)))

        keyvals = collections.defaultdict(list)
        for key in keysf:
            for item in listing:
                keyvals[key].append(item[key])

        score = {}

        for key, val in keyvals.iteritems():
            for value in val:
                score[key, value] = val.count(value)
        return score


    def train(self, cv_scheme = 0):
        if cv_scheme not in [0, 1]:
            raise Exception("Only two cross validation schemes available")

        if cv_scheme == 1:
            print 'hi'

        test = [{'abc':2, 'def':5}, {'abc':5, 'def':3}, {'abc':2, 'def':10}]

        true_indices = [i for i in range(len(self._target)) if self._target[i] == 1]
        false_indices = [i for i in range(len(self._target)) if self._target[i] != 1]

        self._train_true = self._train[true_indices]
        self._train_false = self._train[false_indices]

        self.score_true = self._count(self._train_true)
        self.score_false = self._count(self._train_false)
        #for feature in self._train:
        #    for key in feature.keys():
        #        score[key][val] = sum([True for feature in features if feature[key] == val])

    def classify(self, feature):
        trueprob=[]
        falseprob = []
        for key, val in feature.iteritems():
            truecount = self.score_true[key, val]
            falsecount = self.score_false[key, val]

            if truecount == 0:
                truecount = 1

            if falsecount == 0:
                falsecount = 1
            dentrue = len(self._train_true)
            denfalse = len(self._train_false)
            trueprob.append(float(truecount)/dentrue)
            falseprob.append(float(falsecount)/denfalse)

        true_prob_val = reduce(lambda x,y: x*y, trueprob)
        false_prob_val = reduce(lambda x,y: x*y, falseprob)
        probscore = float(true_prob_val)/(false_prob_val + true_prob_val)
        return probscore







