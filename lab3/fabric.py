from typing import Dict, Any
from element import CircuitElement
from elements import Resistor, Inductor, Capacitor, VoltageSource, CurrentSource


class ElementFabric:
    """Фабрика для создания элементов схемы."""

    @staticmethod
    def create_element(config: Dict[str, Any]) -> CircuitElement:
        """Создать элемент схемы на основе конфигурации."""
        element_type = config['type_element']

        if element_type == 'R':
            return Resistor(config)
        elif element_type == 'L':
            return Inductor(config)
        elif element_type == 'C':
            return Capacitor(config)
        elif element_type in ('E', 'E_AC'):
            return VoltageSource(config)
        else:
            raise ValueError(f"Неизвестный тип элемента: {element_type}")