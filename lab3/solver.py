import numpy as np
from circuit import Circuit
from typing import Dict, List


class CircuitSolver:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit  # публичное поле, так как это входной параметр

        # Приватные поля для матриц состояния
        self.__I = np.zeros((circuit.branches, 1))  # Токи ветвей
        self.__U = np.zeros((circuit.branches, 1))  # Напряжения ветвей
        self.__F = np.zeros((circuit.nodes - 1, 1))  # Потенциалы узлов

        # Защищенное поле для истории расчетов
        self._history = {
            'time': [],
            'I': [],
            'U': [],
            'F': []
        }

    def __build_matrix_A(self) -> np.ndarray:
        """Построение матрицы инцидентности"""
        A = np.zeros((self.circuit.nodes - 1, self.circuit.branches))
        for elem in self.circuit.elements:
            if elem._start_node > 0:
                A[elem._start_node - 1, elem.branch] = 1
            if elem._end_node > 0:
                A[elem._end_node - 1, elem.branch] = -1
        return A

    def __build_matrix_Y(self, h: float) -> np.ndarray:
        """Построение матрицы проводимостей"""
        Y = np.zeros((self.circuit.branches, self.circuit.branches))
        for elem in self.circuit.elements:
            Y[elem.branch, elem.branch] = elem.calculate_conductivity(h)
        return Y

    def solve_step(self, time: float) -> Dict[str, np.ndarray]:
        """Выполнение одного шага расчета"""
        A = self.__build_matrix_A()
        Y = self.__build_matrix_Y(self.circuit.h)

        # Векторы ЭДС и источников тока
        E = np.array([[elem.calculate_emf(time, self.circuit.h)]
                     for elem in self.circuit.elements])
        J = np.array([[elem.calculate_current_source(time)]
                     for elem in self.circuit.elements])

        # Решение системы методом узловых потенциалов
        AY = np.dot(A, Y)
        self.__F = -np.linalg.solve(np.dot(AY, A.T), np.dot(A, J) + np.dot(AY, E))
        self.__U = np.dot(A.T, self.__F)
        self.__I = np.dot(Y, (self.__U + E)) + J

        # Обновление состояния элементов
        for elem in self.circuit.elements:
            elem.update_state(
                current=self.__I[elem.branch, 0],
                voltage=self.__U[elem.branch, 0]
            )

        # Сохранение в историю
        self._history['time'].append(time)
        self._history['I'].append(self.__I.copy())
        self._history['U'].append(self.__U.copy())
        self._history['F'].append(self.__F.copy())

        return {
            'I': self.__I.copy(),
            'U': self.__U.copy(),
            'F': self.__F.copy()
        }

    def simulate(self) -> None:
        """Запуск полного моделирования"""
        steps = int(self.circuit.simulation_time / self.circuit.h)

        for step in range(steps):
            time = step * self.circuit.h
            self.solve_step(time)

    # Геттеры для безопасного доступа к данным
    @property
    def currents(self) -> np.ndarray:
        """Токи ветвей"""
        return self.__I.copy() 

    @property
    def voltages(self) -> np.ndarray:
        """Напряжения ветвей"""
        return self.__U.copy()

    @property
    def potentials(self) -> np.ndarray:
        """Потенциалы узлов"""
        return self.__F.copy()

    @property
    def history(self) -> Dict[str, List]:
        """История расчетов"""
        return {
            'time': self._history['time'].copy(),
            'I': [arr.copy() for arr in self._history['I']],
            'U': [arr.copy() for arr in self._history['U']],
            'F': [arr.copy() for arr in self._history['F']]
        }
    