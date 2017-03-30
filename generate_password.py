import hashlib
import numpy as np
from password_policy import Policy

def getPassword(policyFilename, masterPass, bits):
    policy = Policy(policyFilename)
    
    baseChars = policy.getBaseCharacters()
    
    # pack bits in to bytes
    decodedBytes = np.packbits(np.uint8(bits))
    decodedString = ""
    for indx, i in enumerate(decodedBytes):
        decodedString += chr(i)

    # generate 64 bytes derived from masterPass, and decodedBytes.
    passwordSeed = hashlib.pbkdf2_hmac('sha512', masterPass, decodedBytes, 100000)

    # use those 64 bytes to select characters from our base character set.
    password = ""
    for indx, i in enumerate(passwordSeed):
        # select a character from our base character set. This is likely smaller
        # than 256 chars, so we modulo by length to wrap around.
        password += baseChars[ord(i)%len(baseChars)]

    print(password)

    # TODO: apply remaining rules
    # currently, only length is applied
    password = policy.applyRules(password)

    if policy.isValidPassword(password):
        return password 

    raise Exception("Invalid password generated. This should never happen.")