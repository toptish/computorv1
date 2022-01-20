import sys
import unittest
import computor
from computor import Polinominal, ProgramError, SolvingError
import pytest


class TestPolinominalSolver(unittest.TestCase):
    def test_no_root_1(self):
        polinom = Polinominal('X^2 + 6 = 2 + X^2')
        with self.assertRaises(SolvingError) as cm:
            polinom.solve()

    def test_no_root_2(self):
        polinom = Polinominal('4 * X^0 = 8 * X^0')
        with self.assertRaises(SolvingError) as cm:
            polinom.solve()

    def test_every_root_1(self):
        polinom = Polinominal('X^2 + 2 = 2 + X^2')
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 1)
        self.assertEqual(polinom.solutions[0], "Every real number")

    def test_every_root_2(self):
        polinom = Polinominal('X^2 + 2 + x = 2 + X^2 + x^1')
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 1)
        self.assertEqual(polinom.solutions[0], "Every real number")

    def test_every_root_3(self):
        polinom = Polinominal('5 * X^0 = 5 * X^0')
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 1)
        self.assertEqual(polinom.solutions[0], "Every real number")

    def test_one_root_1(self):
        polinom = Polinominal('5 * X^0 = 4 * X^0 + 7 * X^1')
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 1)
        self.assertEqual(polinom.solutions[0], 1/7)

    def test_one_root_2(self):
        polinom = Polinominal('5 = 4 + 7X')
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 1)
        self.assertEqual(polinom.solutions[0], 1/7)

    def test_one_root_3(self):

        "1 * X ^ 0 + 4 * X ^ 1 = 0"

    def test_two_roots(self):
        polinom = Polinominal("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
        polinom.solve()
        self.assertEqual(len(polinom.solutions), 2)

    @unittest.skip("Temporarily skip test_complex_roots")
    def test_complex_roots(self):
        pass


class TestInputErrors(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_empty_string(self):
        with self.assertRaises(ProgramError) as cm:
            polinom = Polinominal('')
        self.assertEqual(str(cm.exception), "'=' sign not found.")

    def test_no_equal_sign(self):
        with self.assertRaises(ProgramError) as cm:
            polinom = Polinominal('X2 + X2')
        self.assertEqual(str(cm.exception), "'=' sign not found.")

    def test_wrong_variable_names(self):
        with self.assertRaises(ProgramError) as cm:
            polinom = Polinominal('X^2 + 2z^2 = 5')
        self.assertRegex(str(cm.exception), r"Can not parse")

    def test_empty_right_side(self):
        with self.assertRaises(ProgramError) as cm:
            polinom = Polinominal('X2 + 2X2 = ')
        self.assertEqual(str(cm.exception), 'One side of the equation is missing.')

    def test_empty_left_side(self):
        with self.assertRaises(ProgramError) as cm:
            polinom = Polinominal('X2 + 2X2 = ')
        self.assertEqual(str(cm.exception), 'One side of the equation is missing.')

    def test_many_equal_signs(self):
        with self.assertRaises(ProgramError):
            polinom = Polinominal('X2 + 2X2 = 5 = 5x')

    # @unittest.skip("Temporarily skip test_wrong_symbols")
    def test_wrong_symbols(self):
        with self.assertRaises(ProgramError):
            polinom = Polinominal('X2 + 2X2 = 3?')

    @unittest.skip("Temporarily skip test_too_many_plus_signs")
    def test_too_many_plus_signs(self):
        with self.assertRaises(ProgramError):
            polinom = Polinominal('-X2 ++ 2X2 = 3+')

    @unittest.skip("Temporarily skip test_too_many_minus_signs")
    def test_too_many_minus_signs(self):
        with self.assertRaises(ProgramError):
            polinom = Polinominal('-X2 -- -2X2 = 3-')

    @unittest.skip("Temporarily skip test_too_many_minus_signs")
    def test_too_many_signs_combination(self):
        with self.assertRaises(ProgramError):
            polinom = Polinominal('-X2 --+ -2X2 = 3')


class TestCorrectInput(unittest.TestCase):
    def test_free_form(self):
        polinom = Polinominal('-X2 + 2X2 = 3')



class TestWholeProgram(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()