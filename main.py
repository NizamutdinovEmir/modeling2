import math
import matplotlib.pyplot as plt


# Функция для проверки, выйдет ли электрон из конденсатора при заданном U
def func(U):
    toch = 1000  # точность разбиения по времени
    e = 1.6 * 10 ** (-19)  # заряд электрона
    m = 9.1 * 10 ** (-31)  # масса электрона
    v = 2.5 * 10 ** 6  # начальная скорость, м/с
    l = 0.23  # длина конденсатора, м
    R1 = 0.07  # радиус внутренней обкладки, м
    R2 = 0.15  # радиус внешней обкладки, м
    d = R2 - R1  # расстояние между обкладками
    a_koef = e * U / (m * math.log(R2 / R1))  # коэффициент ускорения
    pos = d / 2  # начальное положение электрона (посередине между обкладками)
    r = pos + R1  # текущий радиус
    a = a_koef / r  # начальное ускорение
    vy = 0  # начальная скорость по оси y
    t = 0  # начальное время
    dt = l / (v * toch)  # шаг по времени

    for _ in range(toch):
        pos = max(pos - vy * dt - a * dt ** 2 / 2, 0)
        vy = 0 if pos == 0 else vy + a * dt
        r = pos + R1
        a = a_koef / r if pos != 0 else 0
        t += dt
        if t > (l / v):
            break

    return pos == 0


# Основной класс программы
class MyClass:
    def __init__(self):
        # Константы задачи
        self.toch = 1000
        self.e = 1.6 * 10 ** (-19)
        self.m = 9.1 * 10 ** (-31)
        self.v = 2.5 * 10 ** 6  # начальная скорость, м/с
        self.l = 0.19  # длина конденсатора, м
        self.R1 = 0.07  # радиус внутренней обкладки, м
        self.R2 = 0.15  # радиус внешней обкладки, м
        self.d = self.R2 - self.R1  # расстояние между обкладками
        self.U = 0  # разность потенциалов, будет вычислена позже
        self.x_ = []  # x координаты
        self.y_ = []  # y координаты
        self.t_ = []  # время
        self.Vy = []  # скорость по y
        self.Ay = []  # ускорение по y
        self.t_ans = 0  # время полета
        self.v_ans = 0  # конечная скорость
        self.U_ans = self.BinPoisk()  # вычисляем минимальное U
        self.U = self.U_ans  # устанавливаем U для расчетов

    def clean(self):
        """Очистка списков для повторных расчетов"""
        self.x_ = []
        self.y_ = []
        self.t_ = []
        self.Vy = []
        self.Ay = []

    def DO(self):
        """Проводит расчет траектории электрона"""
        self.clean()
        a_koef = self.e * self.U / (self.m * math.log(self.R2 / self.R1))
        pos = self.d / 2  # начальное положение
        r = pos + self.R1
        a = a_koef / r
        vy = 0
        t = 0
        dt = self.l / (self.v * self.toch)

        for _ in range(self.toch):
            self.t_.append(t)
            self.Ay.append(a)
            self.Vy.append(vy)
            self.x_.append(self.v * t)
            self.y_.append(pos)

            if pos == 0:  # электрон ударился о внутреннюю обкладку
                break

            pos = max(pos - vy * dt - a * dt ** 2 / 2, 0)
            vy = vy if pos == 0 else vy + a * dt
            r = pos + self.R1
            a = a if pos == 0 else a_koef / r
            t += dt

            if t > (self.l / self.v):
                break

        self.v_ans = math.sqrt(self.v ** 2 + vy ** 2)  # конечная скорость
        self.t_ans = t  # время полета

    def GetGrap(self):
        """Построение графиков"""
        plt.subplot(2, 2, 1)
        plt.plot(self.x_, self.y_)
        plt.axis((0, self.l, 0, self.R2 - self.R1))
        plt.title("y(x)")

        plt.subplot(2, 2, 2)
        plt.plot(self.t_, self.Vy)
        plt.title("Vy(t)")

        plt.subplot(2, 2, 3)
        plt.plot(self.t_, self.Ay)
        plt.title("Ay(t)")

        plt.subplot(2, 2, 4)
        plt.plot(self.t_, self.y_)
        plt.title("y(t)")

        plt.tight_layout()
        plt.show()

    def BinPoisk(self):
        """Бинарный поиск минимального U"""
        left = 2  # минимальное значение U
        right = 100  # максимальное значение U
        while right - left > 0.00001:  # точность поиска
            mid = (left + right) / 2
            if func(mid):
                right = mid
            else:
                left = mid
        return right


# Главный блок программы
if __name__ == "__main__":
    my_obj = MyClass()
    print(f"Минимальное значение U: {my_obj.U_ans:.5f} В")
    my_obj.DO()
    print(f"Время полета: {my_obj.t_ans:.5e} с")
    print(f"Конечная скорость: {my_obj.v_ans:.5e} м/с")
    my_obj.GetGrap()
