import unittest
import generate_password

class TestGeneratePasswordMethods(unittest.TestCase):

	def test_generatePassword(self):

		# policy + master pass + decodedBits = password
		password = generate_password.getPassword('./policies/example.json', 'thisIsALongAndMemorableMasterPassword', [False, False, False, True, False, False, True, True, True, False, False, False, True, False, False, False, False, False, False, False, True, True, True, False, True, False, False, True, False, True, False, False, False, False, False, False, False, True, True, False, True, False, True, True, True, False, True, True, False, True, False, True, True, True, False, False, False, False, True, False, True, False, False, False, False, True, True, True, False, True, True, False, True, True, False, False, False, False, True, True, False, False, False, False, True, True, False, False, True, False, False, True, True, True, False, False, True, True, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, True, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, True, False, False, False, True, False, True, False, True, False, False, True, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, False, False, False, True, False, True, False, False, True, True, False, True, False, False, False, False, False, False, True, False, False, True, False, False, False, False, True, False, True, False, False, True, True, False, False])

		self.assertEquals(password, "K4^gm)`hF9Og+2Yk%CHK7X`8`:g;[Z,.6*yhb,A:7=Vbz_s$kVTb0==Q+:KPe5Tq")

if __name__ == '__main__':
    unittest.main()
