import json
import collections
import re

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
        return (
            self.isCorrectLength(password) and
            self.hasOnlyValidChars(password) and
            self.hasRequiredChars(password) and
            self.hasValidRepeatingChars(password) and
            self.hasValidConsecutiveChars(password)
        )

    def applyRules(self, password):

        return password

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
        # if policy does not have a restriction, ignore it
        if 'required_characters' not in self.__policy:
            return True

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
                return False

        return True

    # repeating, like "aaaaa" should not exceed max
    def hasValidRepeatingChars(self, password):
        if 'max_repeating_characters' not in self.__policy:
            return True

        maxCount = self.__policy['max_repeating_characters']
        count = 1
        prevChar = ""
        for char in password :
            if char == prevChar:
                count += 1
                prevChar = char

                if count > maxCount:
                    return False

                continue

            prevChar = char
            count=1

        return True


    # consecutive, like "abcdefg"
    def hasValidConsecutiveChars(self, password):
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
                    return False

        return True