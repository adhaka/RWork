__author__ = 'akashdhaka'

import re, random


class Filter:

    emailPatternReg = "[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*" + "[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$"
    phonePatternReg = r"\d+"
    emailDomains = ['gmail', 'yahoo', 'msn', '.com', '.in']
    numWords = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundred']

    def __init__(self, text=False):
        if text:
            self.text = text
            self.processedText = self.text.lower().rstrip()

        self.emailPattern = re.compile(self.emailPatternReg)
        self.phonePattern = re.compile(self.phonePatternReg)


    #def setEmailPattern(self, pattern):
    #    self.pattern = pattern
    def setText(self, text):
        self.text = text
        self.processedText = self.text.lower().rstrip()

    def emailIdentify(self):
        if not self.processedText:
            print("Set a description.")
            raise Exception
        emailMatch = self.emailPattern.match(self.processedText)
        domainMatch = len([word for word in self.emailDomains if word in self.processedText]) > 0
        emailPresent = emailMatch or domainMatch
        return emailPresent

    def phoneIdentify(self):
        if not self.processedText:
            print("Set a description.")
            raise Exception
        phoneMatch = self.phonePattern.match(self.processedText)
        phoneWordCount = len([word for word in self.numWords if word in self.processedText])
        phoneWordsDigit = [word for word in self.processedText.split() if word.isdigit()]
        phoneWordsDigitSub = [word for word in phoneWordsDigit if word > 100]

        phonePresent = phoneMatch or phoneWordCount > 3 or len(phoneWordsDigit) > 3 or len(phoneWordsDigitSub) > 1
        return phonePresent

    def test(self):
        teststr = 'abc123'






