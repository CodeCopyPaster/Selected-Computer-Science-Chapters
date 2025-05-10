import numpy as np


class BaseMatrix:
    def __init__(self, n, m):
        self.matrix = np.random.randint(low=-100, high=100, size=(n, m))

    def get_column(self, index):
        '''Returns column of given index'''
        return self.matrix[:, index]

    def swap_elements(self, pos1, pos2):
        '''Swaps two elements'''
        self.matrix[pos1[0], pos1[1]], self.matrix[pos2[0], pos2[1]] = \
            self.matrix[pos2[0], pos2[1]], self.matrix[pos1[0], pos1[1]]

    def calculate_correlation(self, col1, col2):
        '''Counts correletion coefficient'''
        return np.corrcoef(col1, col2)[0, 1].round(2)

    def __str__(self):
        return str(self.matrix)


class MatrixOperations(BaseMatrix):
    def __init__(self, n, m):

        super().__init__(n, m)

    def swap_max_elements(self):
        '''Swaps max elemnts in first and last row'''
        first_col = super().get_column(0)
        last_col = super().get_column(-1)

        max_first_pos = (np.argmax(first_col), 0)
        max_last_pos = (np.argmax(last_col), self.matrix.shape[1] - 1)

        super().swap_elements(max_first_pos, max_last_pos)

    def get_correlation(self):
       '''Returns correlation coefficient of first and last rows'''
       return super().calculate_correlation(
            super().get_column(0),
            super().get_column(-1),
        )


def task5():
    n = int(input('Введите кол-во строк: '))
    m = int(input('Введите кол-во столбцов: '))

    matrix = MatrixOperations(n, m)
    print('Исходная матрица:\n', matrix)

    matrix.swap_max_elements()
    print('Матрица после обмена:\n', matrix)

    print('Коэффициент корреляции:', matrix.get_correlation())