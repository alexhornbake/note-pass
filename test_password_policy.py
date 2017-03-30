import unittest
from password_policy import Policy

class TestPasswordPolicyMethods(unittest.TestCase):

    def test_isValidPassword(self):
        policy = Policy('./policies/example.json')

        # check for length
        self.assertFalse(policy.isValidPassword(''))
        self.assertFalse(policy.isValidPassword('1'))
        self.assertFalse(policy.isValidPassword('pass'))
        self.assertFalse(policy.isValidPassword('passwordpasswordpasswordpasswor'))

        # check for invalid character pointy bracket < not in policy character set
        self.assertFalse(policy.isValidPassword('hhAVa^Vzs,D4<}FV{*L_?IjC:KAxJune'))

        # check for required character types
        self.assertFalse(policy.isValidPassword('passwordpasswordpasswordpassword'))

        # check for repeating characters
        self.assertFalse(policy.isValidPassword('23nf|Le4444wjF@cTBNV_/j..^hhAVa^'))
        self.assertFalse(policy.isValidPassword('23nf|Le4wjF@cTBNV_/j..^hhAVa^VVV'))

        # check for sequential characters
        self.assertFalse(policy.isValidPassword('abcdefghijklmnopqrstuvwxyzABCDEF'))
        self.assertFalse(policy.isValidPassword('23nf|Le4wjF@cTBNV_/j..^123456789'))

        # check a valid password
        self.assertTrue(policy.isValidPassword('hhAVa^Vzs,D4}FV{*L_?IjC:KAxJune$'))

    def test_applyRules(self):
        policy = Policy('./policies/example.json')

        #test repeating password without special chars
        passwordSeed1 = 'SNRrrrrrgTN0BABwPz5y0Hkjcrc2t6l7Wnn4LM9UQPXSb24TYzdj9Z2u7Ls03IZQYhULb'
        output = policy.applyRules(passwordSeed1)
        self.assertTrue(policy.isValidPassword(output))

        #test consecutive, repeating, no specials, and multiple passes
        passwordSeed2 = 'abcdefgAWRNASBASRBASRABCDDDDabcdef#%JETANTEA3qjtee#Qe3eantteQn'

        output = policy.applyRules(passwordSeed2)
        self.assertTrue(policy.isValidPassword(output))

        #test really consecutive
        passwordSeed3 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        output = policy.applyRules(passwordSeed3)
        self.assertTrue(policy.isValidPassword(output))

        #test really repetetive
        passwordSeed4 = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        output = policy.applyRules(passwordSeed4)
        self.assertTrue(policy.isValidPassword(output))

if __name__ == '__main__':
    unittest.main()
