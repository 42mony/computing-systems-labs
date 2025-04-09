import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Union

class CircuitPlotter:
    def __init__(self, solver):
        self._solver = solver  # Защищенное поле
        self._time_ms = np.array(solver.history['time']) * 1000  # Приватное поле
        self._styles = {  # Приватный словарь стилей
            'current': {'color': 'r', 'linestyle': '-'},
            'voltage': {'color': 'g', 'linestyle': '-'},
            'potential': {'color': 'b', 'linestyle': '-.'}
        }

    @property
    def time_data(self) -> np.ndarray:
        """Геттер для временных данных (возвращает копию)"""
        return self._time_ms.copy()

    @property
    def styles(self) -> Dict[str, Dict]:
        """Геттер для стилей графиков (возвращает копию)"""
        return self._styles.copy()

    @property
    def solver(self):
        """Геттер для доступа к решателю (без копирования)"""
        return self._solver

    def _create_plot(self, y_data: np.ndarray, title: str, ylabel: str, style: str):
        """Приватный метод для построения графика"""
        plt.figure(figsize=(10, 5))
        plt.plot(self._time_ms, y_data, **self._styles[style])
        plt.title(title)
        plt.xlabel('Время, мс')
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_element(self, element_name: str):
        """Построение графиков для элемента схемы"""
        element = self.solver.circuit.get_element_by_name(element_name)
        branch = element.branch
      
        currents = [I[branch, 0] for I in self.solver.history['I']]
        self._create_plot(currents, f'Ток через {element_name}', 'Ток, А', 'current')
        
        voltages = [U[branch, 0] for U in self.solver.history['U']]
        self._create_plot(voltages, f'Напряжение на {element_name}', 'Напряжение, В', 'voltage')

    def plot_node(self, node: int):
        """Построение графика потенциала узла"""
        potentials = [f[node-1, 0] for f in self.solver.history['F']]
        self._create_plot(potentials, f'Потенциал узла {node}', 'Потенциал, В', 'potential')

    def plot_all(self, objects: List[str]):
        """Автоматическое построение всех графиков"""
        for obj in objects:
            if isinstance(obj, str):
                self.plot_element(obj)
            else:
                print(f"Неизвестный тип объекта: {obj}")