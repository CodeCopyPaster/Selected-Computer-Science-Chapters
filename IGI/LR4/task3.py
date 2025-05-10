import math
import matplotlib.pyplot as plt
import input_checker
from statistics import mean, median, variance, stdev,mode
class LogCalculator:
    def __init__(self, x, eps):
        self.x = x
        self.eps = eps
        self.partial_sums = []
        self.exact_value = math.log(1-x)
        self.calculate_series()
    def arccos_series_term(self, n, prev_term):
        """Counts n-element of series"""
        if n == 1:
            return self.x
        return prev_term * ((-1) ** n) * (self.x ** n) / n

    def calculate_series(self):
        """Counts series with given eps"""
        sum_ = math.pi / 2
        self.partial_sums.append(sum_)
        term = self.x
        n = 1
        while abs(term) > self.eps:
            sum_ -= term
            self.partial_sums.append(sum_)
            n += 1
            term = self.arccos_series_term(n, term)

    def calculate_statistics(self):
        """Counts statistics"""
        data = self.partial_sums
        stats = {
            'mean': mean(data),
            'median': median(data),
            'mode': mode(data),
            'variance': variance(data),
            'stdev': stdev(data),
            'iterations': len(data)
        }
        return stats

    def plot_and_save(self):
        """Builds and saves a plot"""
        plt.figure(figsize=(10, 6), dpi=150)
        iterations = range(1, len(self.partial_sums) + 1)

        plt.plot(iterations, self.partial_sums,'b-o',
                 label=f'Ряд Тейлора (x={self.x:.2f})')
        plt.axhline(y=self.exact_value, color='r', linestyle='--',
                    label='Точное значение')
        plt.xlabel('Номер итерации')
        plt.ylabel('len(1-x)')
        plt.title(f'Сходимость ряда Тейлора для ln(1-x)({self.x:.2f})')
        plt.legend()
        plt.grid(True)

        last_error = abs(self.partial_sums[-1] - self.exact_value)
        plt.annotate(f'Ошибка: {last_error:.2e}',
                     xy=(iterations[-1],self.partial_sums[-1]),
                     xytext=(iterations[-2],1),arrowprops=dict(facecolor='black',shrink=0.05),
                     bbox=dict(boxstyle='round',color='y'))
        plt.savefig('plot.png')
        print("График сохранён")
        plt.show()

def task3():
    while True:
        x = input_checker.input_checker("Input \'x\' less than 1: ", float, 0,1)
        if x == 1:
            print("\'x\' must not be lower than 1")
        else:
            break
    eps = input_checker.input_checker("Input \'eps\' from 0 to 1: ", float, 1e-10, 1)
    calculator = LogCalculator(x, eps)
    stats = calculator.calculate_statistics()

    print("\nРезультаты:")
    print(f"Точное значение (math.ln): {calculator.exact_value:.8f}")
    if calculator.partial_sums:
        print(f"Приближенное значение: {calculator.partial_sums[-1]:.8f}")
        print(f"Количество итераций: {stats['iterations']}")

    print("\nСтатистика последовательности частичных сумм:")
    print(f"Среднее: {stats['mean']:.6f}")
    print(f"Медиана: {stats['median']:.6f}")
    print(f"Мода: {stats['mode']}")
    print(f"Дисперсия: {stats['variance']:.6f}")
    print(f"СКО: {stats['stdev']:.6f}")
    calculator.plot_and_save()



