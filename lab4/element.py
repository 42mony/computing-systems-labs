from abc import ABC, abstractmethod


class CircuitElement(ABC):
    def __init__(self, config):
        self._name = config['name']
        self._type = config['type_element']
        self.start_node = config['start_node']
        self.end_node = config['end_node']
        self._branch = config['branch']
        self._current = 0.0
        self._voltage = 0.0

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_current(self):
        return self._current

    def get_voltage(self):
        return self._voltage

    def set_current(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Ток должен быть числом")
        self._current = float(value)

    def set_voltage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Напряжение должно быть числом")
        self._voltage = float(value)

    @abstractmethod
    def calculate_conductivity(self, h):
        pass

    @abstractmethod
    def calculate_emf(self, time, h):
        pass

    @abstractmethod
    def calculate_current_source(self, time):
        pass

    def update_state(self, current, voltage):
        self.set_current(current)
        self.set_voltage(voltage)