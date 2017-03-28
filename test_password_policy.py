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



if __name__ == '__main__':
    unittest.main()
