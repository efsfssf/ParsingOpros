
import unittest   # The test framework
import main

class Test_TestIncrementDecrement(unittest.TestCase):

    def test_run(self):
        self.assertEqual(main.get_user_id_in_opros(str(309424939)) is not None, True)

    def test_balance(self):
        self.assertEqual(any(map(str.isdigit, main.get_balance(str(309424939)))), True)
if __name__ == '__main__':
    unittest.main()