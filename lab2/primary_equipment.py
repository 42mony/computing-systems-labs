from abc import ABC, abstractmethod

class PrimaryEquipment(ABC):
    def __init__(self, name, voltage):
        self.__name = name
        self.__voltage = voltage

    @abstractmethod
    def get_info(self):
        pass

    def get_name(self):
        return self.__name

    def get_voltage(self):
        return self.__voltage

    def set_name(self, name):
        self.__name = name

    def set_voltage(self, voltage):
        self.__voltage = voltage
