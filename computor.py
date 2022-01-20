import re
import argparse
from collections import defaultdict
import copy


class ProgramError(Exception):
    pass


class SolvingError(Exception):
    pass


class Polinominal:
    def __init__(self, equation: str):
        self.equation = equation
        self.elements = []
        try:
            self.parse_input()
            self.move_left()
            self.validate()
        except Exception as e:
            raise ProgramError(str(e))
        self.polinominal = self.set_polinominal()
        self.degree = self.set_degree()
        self.discriminant = None
        self.solutions = []
        self.error = None

    def set_discriminant(self):
        self.discriminant = self.polinominal[1] ** 2 - 4 * self.polinominal[2] * self.polinominal[0]

    def set_degree(self):
        self.polinominal = dict(reversed(sorted(self.polinominal.items())))
        return list(self.polinominal.keys())[0]

    @staticmethod
    def _remove_keys(polinominal):
        new_pol = {}
        for k, v in polinominal.items():
            if v != 0:
                new_pol[k] = v
        if new_pol == {}:
            new_pol[0] = 0
        return new_pol

    def set_polinominal(self):
        polinominal = defaultdict(list)
        for elem in self.elements:
            # print(elem)
            coef, power = elem.split('*X^')
            polinominal[int(power)].append(float(coef))
        for k, v in polinominal.items():
            polinominal[k] = sum(v)
        polinominal = self._remove_keys(polinominal)
        degree = list(reversed(sorted(polinominal.keys())))[0]
        for k in range(0, degree):
            if k not in polinominal.keys():
                polinominal[k] = 0.0
        return polinominal

    def make_reduced(self):
        reduced_dict = {}
        reduced = ''
        for k, v in self.polinominal.items():
            if v != 0:
                reduced_dict[k] = v
        reduced_dict = dict(reversed(sorted(reduced_dict.items())))
        sign = ['-', '+']
        for k, v in reduced_dict.items():
            bool_sign = v > 0
            v = v if v > 0 else -v
            degree = ''
            if k == 1:
                degree = f'X'
            elif k > 1:
                degree = f'X^{k}'
            mult = '*' if degree else ''
            if v == 1.0 and k != 0:
                reduced += f'{sign[bool_sign]} {degree} '
            else:
                reduced += f'{sign[bool_sign]} {v} {mult} {degree} '
        reduced += '= 0'
        reduced = reduced.strip('+ ')
        return reduced

    def solve_linear(self):
        self.solutions.append(self.polinominal[0] / self.polinominal[1] * (-1))

    def solve_complex(self):
        x1 = []
        x1.append(-1 * self.polinominal[1] / (2 * self.polinominal[2]))
        x1.append(((-self.discriminant) ** 0.5) / (2 * self.polinominal[2]))
        self.solutions.append(str(round(x1[0], 6)) + ' + ' + str(round(x1[1], 6)) + 'i')
        self.solutions.append(str(round(x1[0], 6)) + ' - ' + str(round(x1[1], 6)) + 'i')

    def solve_square(self):
        self.set_discriminant()
        if self.discriminant > 0:
            x1 = (-1 * self.polinominal[1] + self.discriminant ** 0.5) / (2 * self.polinominal[2])
            x2 = (-1 * self.polinominal[1] - self.discriminant ** 0.5) / (2 * self.polinominal[2])
            self.solutions.append(x1)
            self.solutions.append(x2)
        if self.discriminant == 0:
            x = (self.polinominal[0] / self.polinominal[2]) ** 0.5
            self.solutions.append(x)
        if self.discriminant < 0:
            self.solve_complex()

    def solve_zero(self):
        if self.polinominal[0] == 0:
            self.solutions.append("Every real number")
        else:
            raise SolvingError(f'{self.polinominal[0]} != 0.0.  No solution.')

    def solve(self):
        if self.degree >= 3:
            self.error = "The polynomial degree is strictly greater than 2, I can't solve."
        elif self.degree == 2:
            self.solve_square()
        elif self.degree == 1:
            self.solve_linear()
        else:
            self.solve_zero()

    def move_left(self):
        right_side = copy.copy(self.equation[1])
        for elem in right_side:
            self.equation[1].remove(elem)
            if '-' in elem:
                elem = re.sub(r'-', '+', elem)
            elif '+' in elem:
                elem = re.sub(r'\+', '-', elem)
            else:
                elem = '-' + elem
            self.equation[0].append(elem)
        self.elements = self.equation[0]
        # print(self.elements)

    def validate(self):
        elements = []
        for elem in self.elements:
            elem = self.validate_el(elem)
            elements.append(elem)
        self.elements = elements

    def validate_el(self, element):
        pattern = r"([+-])?(\d+(\.)?(\d+)?)?((\*)?([X]\^?\d?))?"
        check = re.match(pattern, element)
        if check.group() == element:
            if '^' not in element:
                if re.match(r'[-+]?[0-9]+?X[0-9]', element):
                    element = re.sub(r'X', 'X^', element)
                else:
                    element = re.sub(r'X', 'X^1', element)
            if 'X' not in element:
                element = element + 'X^0'
            if element.split('X')[0] == '':
                element = '1*' + element
            if '*' not in element:
                if re.match(r'[-+]?[0-9]+X', element):
                    element = re.sub(r'X', '*X', element)
                else:
                    element = re.sub(r'X', '1*X', element)
            # print(element)
            return element
        else:
            raise ProgramError(f'Can not parse "{element}" element')

    def prevalidate(self):
        pass

    def _split_eq(self):
        self.equation[0] = self.equation[0].split('+')
        self.equation[1] = self.equation[1].split('+')
        if self.equation[0][0] == '':
            del self.equation[0][0]
        if self.equation[1][0] == '':
            del self.equation[1][0]

    def substitute_signs(self):
        self.equation = re.sub(r"\++", "+", self.equation)
        self.equation = re.sub(r"-\+", "-", self.equation)
        self.equation = re.sub(r"-", "+-", self.equation)
        # self.equation = re.sub(r"=[^-\d]|=", "=+", self.equation)
        self.equation = re.sub(r"=", "=+", self.equation)
        self.equation = re.sub(r"\++", "+", self.equation)

    def parse_input(self):
        self.equation = self.equation.upper()
        self.equation = re.sub(r"\s", "", self.equation)
        if len(self.equation.split('=')) == 2:
            for elem in self.equation.split('='):
                if elem == "":
                    raise ProgramError('One side of the equation is missing.')
        self.substitute_signs()
        self.equation = self.equation.split('=')
        if len(self.equation) == 1:
            raise ProgramError("'=' sign not found.")
        elif len(self.equation) > 2:
            raise ProgramError("Only one '=' is possible.")
        self._split_eq()
        # print(*self.equation)

    def print_results(self):
        reduced = self.make_reduced()
        print(f'Reduced form: {reduced}')
        print(f'Polinominal degree: {self.degree}')
        if len(self.solutions) == 1:
            print(f'The solution is:\n{self.solutions[0]}')
        elif len(self.solutions) == 2 and self.discriminant > 0:
            print(f'Discriminant is strictly positive, the two solutions are:')
            print(*self.solutions, sep='\n')
        elif len(self.solutions) == 2 and self.discriminant < 0:
            print(f'Discriminant is strictly negative, the two complex solutions are:')
            print(*self.solutions, sep='\n')
        else:
            print(self.error)


def main():
    try:
        parser = argparse.ArgumentParser('Solve polinominal')
        parser.add_argument('equation',
                            type=str,
                            help='Equation to solve')
        arguments = parser.parse_args()
        polinom = Polinominal(arguments.equation)
        polinom.solve()
        polinom.print_results()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
