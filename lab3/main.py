import json
from circuit import Circuit
from solver import CircuitSolver
from plotter import CircuitPlotter


def load_config(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    # 1. Загрузка конфигурации
    config = load_config('scheme_4.json')

    # 2. Создание схемы
    circuit = Circuit(config)

    # # 3. Моделирование
    solver = CircuitSolver(circuit)
    solver.simulate()

    # 4. Визуализация
    plotter = CircuitPlotter(solver)
    plotter.plot_all(config['scheme_parameters']['list_measurements_objects'])

    # # 5. Вывод результатов
    print("\nРезультаты в конечный момент времени:")
    for element in circuit.elements:
        print(
            f"{element.get_name:<5} | Ток: {element.get_current():.3f} А | Напряжение: {element.get_voltage():.3f} В")


main()
