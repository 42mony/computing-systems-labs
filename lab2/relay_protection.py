from primary_equipment import PrimaryEquipment

import random as rnd


class RelayProtection(PrimaryEquipment):
    def __init__(self, name, voltage, settings):
        super().__init__(name, voltage)
        self.__settings = settings

    def set_settings(self, settings):
        self.__settings = settings

    def get_settings(self):
        return self.__settings

    @staticmethod
    def activation(failure_probability):
        ratio = rnd.uniform(0, 1)
        if ratio > failure_probability:
            return "Protection succeed"

        return "Protection failed"

    def get_info(self):
        return f"Rele - {self.__name}"


