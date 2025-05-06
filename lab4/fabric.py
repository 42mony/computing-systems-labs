from elements import Resistor, Inductor, Capacitor, VoltageSource, CurrentSource
import copy


class ElementFabric:
    @staticmethod
    def create_element(config):
        element_config = copy.deepcopy(config)
        element_type = element_config['type_element']

        if element_type == 'R':
            return Resistor(element_config)
        elif element_type == 'L':
            return Inductor(element_config)
        elif element_type == 'C':
            return Capacitor(element_config)
        elif element_type in ('E_DC', 'E_AC'):
            return VoltageSource(element_config)
        elif element_type in ('J_DC', 'J_AC'):
            return CurrentSource(element_config)
        else:
            raise ValueError(f"Неизвестный тип элемента: {element_type}")