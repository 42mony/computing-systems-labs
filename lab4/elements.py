from element import CircuitElement
import math


class Resistor(CircuitElement):
    def __init__(self, config):
        super().__init__(config)
        self._resistance = config['resistance']

    def calculate_conductivity(self, h):
        return 1.0 / self._resistance

    def calculate_emf(self, time, h):
        return 0.0

    def calculate_current_source(self, time):
        return 0.0

    def get_resistance(self):
        return self._resistance


class Inductor(CircuitElement):
    def __init__(self, config):
        super().__init__(config)
        self._inductance = config['inductance']
        self._initial_current = config.get('initial_current', 0.0)
        self._first_step = True

    def calculate_conductivity(self, h):
        if self._first_step:
            return 0.0
        return h / (2 * self._inductance * 1e-3)

    def calculate_emf(self, time, h):
        if self._first_step:
            self._first_step = False
            return 0.0
        return (2 * self._inductance * 1e-3 / h) * self._current + self._voltage

    def calculate_current_source(self, time):
        if self._first_step:
            return self._initial_current
        return 0.0

    def get_inductance(self) -> float:
        return self._inductance


class Capacitor(CircuitElement):
    def __init__(self, config):
        super().__init__(config)
        self._capacitance = config['capacitance']
        self._initial_voltage = config.get('initial_voltage', 0.0)
        self._first_step = True

    def calculate_conductivity(self, h):
        if self._first_step:
            return 1e9
        return (2 * self._capacitance * 1e-6) / h

    def calculate_emf(self, time, h):
        if self._first_step:
            self._first_step = False
            return -self._initial_voltage
        return -self._voltage - (h / (2 * self._capacitance * 1e-6)) * self._current

    def calculate_current_source(self, time: float) -> float:
        return 0.0

    def get_capacitance(self) -> float:
        return self._capacitance


class VoltageSource(CircuitElement):
    def __init__(self, config):
        super().__init__(config)
        self._amplitude = config['amplitude']
        self._frequency = config.get('frequency', 0.0)
        self._phase = math.radians(config.get('initial_phase', 0.0))

    def calculate_conductivity(self, h):
        return 1e8

    def calculate_emf(self, time, h):
        if self._type == "E_DC":
            return self._amplitude
        elif self._type == "E_AC":
            return self._amplitude * math.sin(2 * math.pi * self._frequency * time + self._phase)
        raise ValueError(f"Неизвестный тип источника: {self._type}")

    def calculate_current_source(self, time):
        return 0.0

    def get_amplitude(self):
        return self._amplitude


class CurrentSource(CircuitElement):
    def __init__(self, config):
        super().__init__(config)
        self._amplitude = config['amplitude']
        self._frequency = config.get('frequency', 0.0)
        self._phase = math.radians(config.get('initial_phase', 0.0))

    def calculate_conductivity(self, h):
        return 0.0

    def calculate_emf(self, time, h):
        return 0.0

    def calculate_current_source(self, time):
        if self._type == "J_DC":
            return self._amplitude
        elif self._type == "J_AC":
            return self._amplitude * math.sin(2 * math.pi * self._frequency * time + self._phase)
        raise ValueError(f"Неизвестный тип источника: {self._type}")

    def get_amplitude(self):
        return self._amplitude