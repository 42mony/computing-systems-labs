import random as rnd

class ShortCircuit:
    def __init__(self, equipment, voltage):
        self.__equipment = equipment
        self.__voltage = voltage
        self.__fault_type = self._get_fault_type()
        self.__elimination_ratio = 0.3
        
    def _get_fault_type(self):
        FAULT_TYPES = ["Three Phases", "Single Phase", "Two Phases", "Phase-to-Phase"]
        return rnd.choices(FAULT_TYPES, weights=[5, 75, 10, 10])[0]
    
    def set_equipment(self, equipment):
        self.__equipment = equipment
        
    def set_voltage(self, voltage):
        self.__voltage = voltage
        
    def set_fault_type(self, fault_type):
        self.__fault_type = fault_type
        
    def set_elimination_ratio(self, ratio):
        self.__elimination_ratio = ratio
        
    def get_equipment(self):
        return self.__equipment
        
    def get_voltage(self):
        return self.__voltage
        
    def get_fault_type(self):
        return self.__fault_type
        
    def get_elimination_ratio(self):
        return self.__elimination_ratio
    
    def self_elimination_probability(self):
        if rnd.uniform(0, 1) < self.__elimination_ratio:
            return True
        return False
        
    def get_info(self):
        return f"Short circuit: Type - {self.__fault_type}"
        
