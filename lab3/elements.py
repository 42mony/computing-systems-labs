from typing import Dict, Any
from element import CircuitElement
import math


class Resistor(CircuitElement):
    """Реализация резистора (R)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.branch = config['branch']
        self._resistance = config['resistance']  # в Омах

    # Считать не в резистере 
    def calculate_conductivity(self, h: float) -> float:
        return 1.0 / self._resistance  # G = 1/R

    def calculate_emf(self, time: float, h: float) -> float:
        return 0.0  # Для резистора ЭДС нет

    def calculate_current_source(self, time: float) -> float:
        return 0.0  # Для резистора источник тока не нужен

    def get_resistance(self) -> float:
        return self._resistance


class Inductor(CircuitElement):
    """Реализация катушки индуктивности (L)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._inductance = config['inductance']  # в мГн
        self._initial_current = config.get('initial_current', 0.0)
        self.branch = config.get('branch')
        self._first_step = True

    def calculate_conductivity(self, h: float) -> float:
        if self._first_step:
            return 0  # На первом шаге - источник тока    
        return h / (2 * self._inductance * 1e-3)  # h/(2L)

    def calculate_emf(self, time: float, h: float) -> float:
        if self._first_step:
            self._first_step = False
            return 0.0
        return (2 * self._inductance * 1e-3 / h) * self._current + self._voltage

    def calculate_current_source(self, time: float) -> float:
        if self._first_step:
            return self._initial_current  # На первом шаге возвращаем начальный ток
        return 0.0

    def get_inductance(self) -> float:
        return self._inductance


class Capacitor(CircuitElement):
    """Реализация конденсатора (C)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._capacitance = config['capacitance']  # в мкФ
        self._initial_voltage = config.get('initial_voltage', 0.0)
        self.branch = config.get('branch')
        self._first_step = True

    def calculate_conductivity(self, h: float) -> float:
        if self._first_step:
            return 1e9  # На первом шаге - источник ЭДС (очень большая проводимость)
        return (2 * self._capacitance * 1e-6) / h  # (2C)/h

    def calculate_emf(self, time: float, h: float) -> float:
        if self._first_step:
            self._first_step = False
            return -self._initial_voltage  # На первом шаге возвращаем начальное напряжение
        return -self._voltage - (h / (2 * self._capacitance * 1e-6)) * self._current

    def calculate_current_source(self, time: float) -> float:
        return 0.0  # Для конденсатора источник тока не нужен

    def get_capacitance(self) -> float:
        return self._capacitance


class VoltageSource(CircuitElement):
    """Реализация источника напряжения (E)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.branch = config['branch']
        self._amplitude = config['amplitude']
        self._frequency = config.get('frequency', 0.0)  # в Гц
        self._phase = math.radians(config.get('initial_phase', 0.0))  # в радианах

    def calculate_conductivity(self, h: float) -> float:
        return 1e8  # Очень большая проводимость (идеальный источник)

    def calculate_emf(self, time: float, h: float) -> float:
        if self._type == "E":
            return self._amplitude  # Постоянное напряжение
        elif self._type == "E_AC":
            # Синусоидальное напряжение: U(t) = U_m * sin(ωt + φ)
            return self._amplitude * math.sin(2 * math.pi * self._frequency * time + self._phase)
        raise ValueError(f"Неизвестный тип источника: {self._type}")

    def calculate_current_source(self, time: float) -> float:
        return 0.0  # Для источника напряжения не нужен

    def get_amplitude(self) -> float:
        return self._amplitude


class CurrentSource(CircuitElement):
    """Реализация источника тока (J)"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._amplitude = config['amplitude']
        self._frequency = config.get('frequency', 0.0)  # в Гц
        self._phase = math.radians(config.get('initial_phase', 0.0))  # в радианах

    def calculate_conductivity(self, h: float) -> float:
        return 0.0  # Нулевая проводимость (идеальный источник тока)

    def calculate_emf(self, time: float, h: float):
        return 0.0  # Для источника тока ЭДС не нужна


    def get_amplitude(self) -> float:
        return self._amplitude