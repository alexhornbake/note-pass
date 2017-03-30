import json
import collections
import re

class Policy:
    def __init__(self, policyFilename):
        try:
            data = open(policyFilename)
        except Exception as e:
            print("Failed to read policy file: ", policyFilename)
            raise e

        try:
            self.__policy = json.load(data)
        except Exception as e:
            print("Failed to parse policy json: ", policyFilename)
            raise e

    def getBaseCharacters(self):
        baseChars = ""
        sortedCharacterTypes = collections.OrderedDict(sorted(self.__policy['character_types'].items()))
        for indx, c in enumerate(sortedCharacterTypes):
            baseChars += sortedCharacterTypes[c]

        return baseChars

    def getBaseCharacterMap(self):
        baseChars = self.getBaseCharacters()
        baseCharsMap = {}
        for indx, c in enumerate(baseChars):
            baseCharsMap[c]=indx

        return baseCharsMap

    def isValidPassword(self, password):
        return (
            self.isCorrectLength(password) and
            self.hasOnlyValidChars(password) and
            self.hasRequiredChars(password) and
            self.hasValidRepeatingChars(password) and
            self.hasValidConsecutiveChars(password)
        )

    def applyRules(self, password):
        if self.isValidPassword(password):
            return password

        password = self.applyLength(password)
        password = self.applyRequiredChars(password)
        password = self.applyRepeatingChars(password)
        password = self.applyConsecutiveChars(password)

        return self.applyRules(password)

    ############ ENFORCEMENT METHODS ########

    def applyLength(self, password):
        return password[:self.__policy['character_length']]

    def applyRequiredChars(self, password):
        missingChars = self.getMissingReqChars(password)
        if missingChars == '':
            return password

        password = missingChars + password
        return self.applyRequiredChars(password)

    def applyRepeatingChars(self, password):
        indx = self.getRepeatingCharIndex(password)
        if indx == -1:
            return password

        return self.applyRepeatingChars(self.incrementCharacter(password, indx))

    def applyConsecutiveChars(self, password):
        indx = self.getConsecutiveCharsIndex(password)
        if indx == -1:
            return password

        return self.applyConsecutiveChars(self.incrementCharacter(password, indx))

    def incrementCharacter(self, password, indx):
        baseCharMap = self.getBaseCharacterMap()
        baseChars = self.getBaseCharacters()

        charToFix = password[indx]

        # lookup the charToFix in the map, to find it's index in the charset
        # then increment the character.
        # ie. a -> b ... "abc" becomes "abd", or 'aaa' becomes 'aab'
        password = list(password)
        password[indx] = baseChars[(baseCharMap[charToFix] + 1) % len(baseChars)]

        return ''.join(password)

    ############ helpers ####################

    # returns the first missing characters required error
    # can be used recursively to find/fix all errors
    # or can be used once to know if requirement is met
    def getMissingReqChars(self, password):
        # if policy does not have a restriction, ignore it
        if 'required_characters' not in self.__policy:
            return ''

        for rule in self.__policy['required_characters']:
            types = rule['types']
            reqCount = rule['count']
            reqChars = ""
            for charType in types:
                reqChars += self.__policy['character_types'][charType]

            charMap = {}
            for char in reqChars:
                charMap[char] = True

            count = 0
            for char in password:
                if char in charMap:
                    count += 1

            if count < reqCount:
                return reqChars[:reqCount - count]

        return ''

    def getRepeatingCharIndex(self, password):
        if 'max_repeating_characters' not in self.__policy:
            return True

        maxCount = self.__policy['max_repeating_characters']
        count = 1
        prevChar = ""
        for indx, char in enumerate(password) :
            if char == prevChar:
                count += 1
                prevChar = char

                if count > maxCount:
                    return indx

                continue

            prevChar = char
            count=1

        return -1

    # for 'abcdefg' and maxCount of 3
    # return index of 'c' so that we can change it.
    def getConsecutiveCharsIndex(self, password):
        if 'max_consecutive_characters' not in self.__policy:
            return True

        maxCount = self.__policy['max_consecutive_characters'] + 1

        for i, char in enumerate(password):
            if i+maxCount >= len(password):
                break

            # grab a chunk of possibly sequential chars
            substr = password[i:i+maxCount]

            # check required char sequences for that substring
            for charType in self.__policy['character_types']:
                if substr in self.__policy['character_types'][charType]:
                    return i+maxCount-1 # index of the last character in the sequence

        return -1

    ############ VALIDATION METHODS #########

    def isCorrectLength(self, password):
        return len(password) == self.__policy['character_length']

    def hasOnlyValidChars(self, password):
        # generate a regex that will search for groups of valid characters
        regex = r"[" + re.escape(self.getBaseCharacters()) + "]+"

        # find all the matching groups
        matches = re.findall(regex, password)

        # there should only be one valid match, ie... invalid chars would split the group.
        return len(matches) == 1

    # check that the password meets the required_character rules
    def hasRequiredChars(self, password):
        missingChars = self.getMissingReqChars(password)
        if missingChars == '':
            return True

        return False

    # repeating, like "aaaaa" should not exceed max
    def hasValidRepeatingChars(self, password):
        repeatingIndx = self.getRepeatingCharIndex(password)

        if repeatingIndx == -1:
            return True

        return False

    # consecutive, like "abcdefg"
    def hasValidConsecutiveChars(self, password):
        consecutiveIndx = self.getConsecutiveCharsIndex(password)

        if consecutiveIndx == -1:
            return True

        return False
