from typing import Dict, List, Any
import numpy as np
from element import CircuitElement
from fabric import ElementFabric


class Circuit:
    """Класс для представления электрической схемы."""

    def __init__(self, config: Dict[str, Any]): 
        """
        :param config: Конфигурация схемы из JSON.
        """
        self.branches = config['scheme_parameters']['count_branches']
        self.name = config['scheme_parameters']['name']
        self.simulation_time = config['scheme_parameters']['simulation_time']
        self.h = config['scheme_parameters']['sampling_time']
        self.elements: List[CircuitElement] = []
        self.nodes = len(config['scheme_parameters']['list_measurements_objects'])

        scheme_elements = config['scheme_elements']
        # Создание элементов через фабрику        
        for element_config in scheme_elements:
            self.elements.append(ElementFabric.create_element(element_config))

    def get_element_by_name(self, name: str) -> CircuitElement:
        """Найти элемент по имени."""
        for elem in self.elements:
            if elem.get_name == name:
                return elem
        raise ValueError(f"Элемент {name} не найден")

    def get_potential(self, node: int) -> float:
        """Получить потенциал узла (для узла 0 возвращает 0)."""
        return 0.0  # Реализуется в Solver