from substaion import Bus, Transformer, Line
from relay_protection import RelayProtection
from short_circuit import ShortCircuit

import os 
import json
import logging
import random as rnd


# Получаем путь к директории, в которой находится main.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Настройка логирования
logging.basicConfig(
    # filename= os.path.join(current_dir, "substation_events.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)



# Строим путь к файлу equipment.json
file_path = os.path.join(current_dir, "equipment.json")

# Загрузка конфигурации из JSON
with open(file_path, 'r') as file:
    config = json.load(file)

# Создание оборудования подстанции
buss_array = []

for bus_params in config["buses"]:
    tmp_bus = Bus(
        bus_params["name"],
        bus_params["voltage"],
        bus_params["sections"],
        bus_params["section_breaker"],
    )
    buss_array.append(tmp_bus)

hv_bus, lv_bus = buss_array

transformator_array = []

for transformator in config["transformers"]:
    tmp_transformer = Transformer(
        transformator["name"],
        transformator["high_voltage"],
        transformator["low_voltage"],
        transformator["breaker"],
    )
    transformator_array.append(tmp_transformer)

transformator1, transformator2 = transformator_array


# Создание линий высокого напряжения
hv_lines = [
    Line(line["name"], config["substaion"]["high_voltage"], line["breaker"])
    for line in config["lines"]["high_voltage"]
]

# Создание линий низкого напряжения
lv_lines = [
    Line(line["name"], config["substaion"]["low_voltage"], line["breaker"])
    for line in config["lines"]["low_voltage"]
]

# Создание защит
main_protection = []

for protaction in config["protections"]:
    tmp_protaction = RelayProtection(
        protaction["name"],
        config["substaion"]["high_voltage"], 
        protaction["settings"]
    )
    main_protection.append(tmp_protaction)

protaction1, protaction2 = main_protection



# Список оборудования для случайного выбора места КЗ
equipment_list = [hv_bus, lv_bus, transformator1, transformator2] + hv_lines + lv_lines

# Моделирование 10 итераций
i = 1

while i <= 10:
    logging.info(f"\nIteration {i}")

    # Случайный выбор оборудования для КЗ
    faulted_equipment = rnd.choice(equipment_list)
    voltage = faulted_equipment.get_voltage()

    # Создание КЗ
    fault = ShortCircuit(faulted_equipment, voltage)
    logging.info(f"Short circuit on {faulted_equipment.get_info()}")
    logging.info(fault.get_info())
    if fault.self_elimination_probability():
        logging.info("Short circuit has been eliminated by itself")
        i += 1
        continue

    # Срабатывание защит
    main_result = RelayProtection.activation(
        config["protections"][0]["settings"]["failure_probability"]
    )
    logging.info(f"Main protection: {main_result}")

    if main_result == "Protection failed":
        backup_result = RelayProtection.activation(
            config["protections"][1]["settings"]["failure_probability"]
        )
        logging.info(f"Backup protection: {backup_result}")

    i += 1

logging.info("Simulation completed")
