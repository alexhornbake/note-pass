import hashlib
import base64
import json
import numpy as np
import collections

def getPassword(policyFilename, masterPass, bits):
    # TODO: policy loading/validation needs to happen in it's own class
    # load the policy
    try:
        data = open(policyFilename)
    except Exception as e:
        print("Failed to read file: ", policyFilename)
        print(e)

    try:
        policy = json.load(data)
    except Exception as e:
        print("Failed to pasrse json in: ", policyFilename)
        print(e)

    # get base charset from policy
    baseChars = ""
    sortedCharacterTypes = collections.OrderedDict(sorted(policy['character_types'].items()))
    for indx, c in enumerate(sortedCharacterTypes):
        baseChars += sortedCharacterTypes[c]

    # pack bits in to bytes
    decodedBytes = np.packbits(np.uint8(bits))
    decodedString = ""
    for indx, i in enumerate(decodedBytes):
        decodedString += chr(i)


    passwordSeed = hashlib.pbkdf2_hmac('sha512', masterPass, decodedBytes, 100000)
    password = ""
    for indx, i in enumerate(passwordSeed):
        password += baseChars[ord(i)%len(baseChars)]

    # TODO: apply the policy rules

    return password
