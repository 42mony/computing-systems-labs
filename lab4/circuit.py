from fabric import ElementFabric


class Circuit:
    def __init__(self, config):
        self.name = config['scheme_parameters']['name']
        self.nodes = config['scheme_parameters']['count_nodes']
        self.branches = config['scheme_parameters']['count_branches']
        self.h = config['scheme_parameters']['step']
        self.simulation_time = config['scheme_parameters']['simulation_time']
        self.elements = []

        for element_config in config['scheme_elements']:
            self.elements.append(ElementFabric.create_element(element_config))

    def get_element_by_name(self, name):
        for elem in self.elements:
            if elem.get_name() == name:
                return elem
        raise ValueError(f"Элемент {name} не найден")

    def get_potential(self, node):
        # Получeние потенциала узла (для узла 0 возвращает 0).
        return 0.0  # Реализуется в solver