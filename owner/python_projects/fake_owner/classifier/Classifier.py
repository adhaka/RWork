__author__ = 'akashdhaka'

import nltk
import re

class Classify:
    def train(self):
        punctuation = re.compile(r'[-.?!,":;()]')
        filetext = open("filter/pdRealOwner.csv", 'r')
        rawRealText = filetext.read()
        filetext.close()
        rawRealTextPro = re.sub(r'\n', ' ', rawRealText)
        #rawRealTextPro = re.sub(r',', '', rawRealTextPro)
        realSentences = re.findall('".+?"', rawRealTextPro)
        tokensReal = nltk.wordpunct_tokenize(rawRealTextPro)

        tokensReal = [word.lower() for word in tokensReal]
        fdReal = nltk.FreqDist([word.lower() for word in tokensReal])
        fdRealSub = fdReal.keys()[:20]
        self.realBg = nltk.FreqDist(nltk.bigrams(tokensReal))
        #print(realBg.keys()[:20])


        filetext = open("filter/pdFakeOwner.csv", 'r')
        rawFakeText = filetext.read()
        filetext.close()
        rawFakeTextPro = re.sub(r'\n', ' ', rawFakeText)
        #rawFakeTextPro = re.sub('.', '', rawFakeTextPro)
        fakeSentences = re.findall('".+?"', rawFakeTextPro)
        tokensFake = nltk.wordpunct_tokenize(rawFakeTextPro)
        tokensFake = [word.lower() for word in tokensFake]
        fdFake = nltk.FreqDist([word.lower() for word in tokensFake])
        fdFakeSub = fdFake.keys()[:30]
        self.fakeBg = nltk.FreqDist(nltk.bigrams(tokensFake))
        self.success = 0;
        print len(fakeSentences+realSentences)
        for sent in fakeSentences:
            (predLabel, predScore) = self.predict(sent)
            if predLabel == 'fake':
                self.success = self.success + 1
        for sent in realSentences:
            predLabel = self.predict(sent)
            if predLabel == 'real':
                self.success = self.success + 1
        print (self.success)


    #def _extractFeatures(self, sentences, label):
    #    featList = []
    #    for sentence in sentences:
    #        feature = self._extractFeature(sentence)
    #        featVal = (feature, label)
    #        featList.append(featVal)
    #    return featList


    def predict(self, sentence):
        words = nltk.word_tokenize(sentence)
        words = [word.lower() for word in words]
        bigrams = nltk.bigrams(words)
        #print(self.fakeBg)
        #print self.fakeBg[('greater', 'noida')]
        #bigrams = [('project', 'is')]
        probScore = []
        for bg in bigrams:
            #print bg
            #print self.fakeBg[bg]+self.realBg[bg]
            occur = self.fakeBg[bg] + self.realBg[bg]
            prob = self.fakeBg[bg]/(self.fakeBg[bg] + self.realBg[bg] +0.1 )
            if occur > 3:
                probScore.append(prob)

        probScore = [val for val in probScore if val > 0]
        probScore = sorted(probScore, reverse = True)
        if len(probScore)> 5:
            probScore = probScore[0:6]

        if not probScore:
            return ('real', 0)
        fakeProduct = reduce(lambda x,y:x*y, probScore)
        realProduct = reduce(lambda x,y:(1-x)*(1-y), probScore)

        fakeScore = fakeProduct/(realProduct+fakeProduct)
        if fakeScore > 0.3:
            predLabel = 'fake'
        else:
            predLabel = 'real'

        print (fakeScore, predLabel, sentence)
        return (predLabel, fakeScore)
        #return {'label':predLabel, 'score':fakeScore}


    #def calculateFreq(self):

    def _processSentences(self, sentences):
        processedSentList = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            processedSent = ' '.join([word.lower().strip('.') for word in words])

        processedSentList.append(processedSent)
        return processedSentList


if __name__ == '__main__':
    Cl = Classify()
    Cl.train()
