import json
import collections

class Policy:
    def __init__(self, policyFilename):
        try:
            data = open(policyFilename)
        except Exception as e:
            print("Failed to read file: ", policyFilename)
            raise e

        try:
            self.__policy = json.load(data)
        except Exception as e:
            print("Failed to pasrse json in: ", policyFilename)
            raise e

    def getBaseCharacters(self):
        baseChars = ""
        sortedCharacterTypes = collections.OrderedDict(sorted(self.__policy['character_types'].items()))
        for indx, c in enumerate(sortedCharacterTypes):
            baseChars += sortedCharacterTypes[c]

        return baseChars

    def isValidPassword(self, password):

        return True

    def applyRules(self, password):

        return password