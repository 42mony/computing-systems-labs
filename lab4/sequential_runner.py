from three_phase_simulator import load_config, simulate_phase, calculate_neutral
import time


def run_sequential():
    print("\nЗапуск режима последовательного моделирования")
    start_time = time.time()

    try:
        config, phases_dict, plot_targets_dict = load_config("shema.json")
    except Exception as err:
        print(f"Ошибка загрузки конфигурации: {err}")
        return

    results = []
    for name in ["Фаза A", "Фаза B", "Фаза C"]:
        result = simulate_phase(
            config,
            phases_dict[name],
            name,
            plot_targets_dict[name],
            mode="sequential"
        )
        results.append(result)

    calculate_neutral(results)

    total_time = time.time() - start_time
    print(f"\nОбщее время выполнения: {total_time:.2f} сек")