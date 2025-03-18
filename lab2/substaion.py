from primary_equipment import PrimaryEquipment

class Bus(PrimaryEquipment):
    def __init__(self, name, voltage, sections, breaker):
        super().__init__(name, voltage)
        self.__sections = sections
        self.__breaker = breaker
        
    def set_sections(self, sections):
        self.__sections = sections
        
    def set_breaker(self, breaker):
        self.__breaker = breaker
        
    def get_sections(self):
        return self.__sections
        
    def get_breaker(self):
        return self.__breaker
    
    def get_info(self):
        return f"Bus - {self.get_name()}"
    
class Line(PrimaryEquipment):
    def __init__(self, name, voltage, breaker):
        super().__init__(name, voltage)
        self.__breaker = breaker
        
    def set_breaker(self, breaker):
        self.__breaker = breaker
        
    def get_breaker(self):
        return self.__breaker
    
    def get_info(self):
        return f"Line - {self.get_name()}"
        
class Transformer(PrimaryEquipment):
    def __init__(self, name, high_voltage, low_voltage, breaker):
        super().__init__(name, high_voltage)
        self.__low_voltage = low_voltage
        self.__breaker = breaker
        
    def set_low_voltage(self, low_voltage):
        self.__low_voltage = low_voltage
        
    def set_breaker(self, breaker):
        self.__breaker = breaker
        
    def get_low_voltage(self):
        return self.__low_voltage
        
    def get_breaker(self):
        return self.__breaker
    
    def get_info(self):
        return f"Transformer - {self.get_name()}"
    
class Breaker(PrimaryEquipment):
    def __init__(self, name):
        super().__init__(name, None)  # У выключателя нет напряжения
        self.__state = True
        
    def set_state(self, state):
        self.__state = state
        
    def get_state(self):
        return self.__state
        
    def disconnect(self):
        self.__state = False
        
    def get_info(self):
        return f"Breaker - {self.get_name()}"
