from abc import ABC, abstractmethod
from typing import Dict, Any


class CircuitElement(ABC):
    """Абстрактный базовый класс для элементов электрической схемы"""

    def __init__(self, config: Dict[str, Any]):
        """
        :param config: Конфигурация элемента
        """
        self._name = config['name']
        self._type = config['type_element']
        self._start_node = config['start_node']
        self._end_node = config['end_node']
        self._current = 0.0
        self._voltage = 0.0

    # Геттеры
    @property
    def get_name(self) -> str:
        """Получить имя элемента"""
        return self._name

    def get_type(self) -> str:
        """Получить тип элемента"""
        return self._type

    def get_current(self) -> float:
        """Получить текущий ток"""
        return self._current

    def get_voltage(self) -> float:
        """Получить текущее напряжение"""
        return self._voltage

    # Сеттеры
    def set_current(self, value: float) -> None:
        """Установить ток с валидацией"""
        if not isinstance(value, (int, float)):
            raise ValueError("Ток должен быть числом")
        self._current = float(value)

    def set_voltage(self, value: float) -> None:
        """Установить напряжение с валидацией"""
        if not isinstance(value, (int, float)):
            raise ValueError("Напряжение должно быть числом")
        self._voltage = float(value)

    @abstractmethod
    def calculate_conductivity(self) -> float:
        """Рассчитать проводимость"""
        pass

    @abstractmethod
    def calculate_emf(self, time: float) -> float:
        """Рассчитать ЭДС"""
        pass

    def update_state(self, current: float, voltage: float) -> None:
        """Обновить состояние элемента"""
        self.set_current(current)
        self.set_voltage(voltage)
