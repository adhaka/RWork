__author__ = 'akashdhaka'

from filter import hardfilters
import csv
import re
import nltk
from classifier import Classifier

class CheckOwner:

    def addPd(self, pd):
        self.pd = pd


    def addFeatures(self, features):
        self.features = features

    def check(self):
        self.filter = hardfilters.Filter(self.pd)
        emailStatus = self.filter.emailIdentify()
        phoneStatus = self.filter.phoneIdentify()
        self.classifier = Classifier.Classify()
        self.classifier.train()
        (predLabel, predScore) = self.classifier.predict(self.pd)
        return [emailStatus, phoneStatus, predLabel, predScore]


    def test(self):
        testSentence = 'Price and size  : Booking open call us \\\
        2 bhk&2t;2bhk&2st;,3bhk&2t;, 3bhk&2t;3bhk&2t;4bhk&3t;951 sqft   1168 sqft  125555 sqft  1310 sqft  1435 sqft \\\
        1545 sqft  (2300) per sq ft 10th floor park facing Call us us for more information.'
        self.addPd(testSentence)
        print(self.check())



if __name__ == '__main__':
    CO = CheckOwner()
    CO.addPd('hello my name is akash, this project is great.')
    CO.check()
    #CO.test()
