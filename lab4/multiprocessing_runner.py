import multiprocessing
from three_phase_simulator import load_config, simulate_phase, calculate_neutral
import time


def phase_worker(config, phase_data, result_queue):
    name, indices, targets = phase_data
    try:
        result = simulate_phase(config, indices, name, targets, mode="multiprocessing")
        result_queue.put(result)
        print(f"[{name}] Завершена")
    except Exception as e:
        print(f"[{name}] Ошибка: {e}")
        result_queue.put((name, [], None))  # Пустой результат при ошибке


def run_multiprocessing():
    print("\nЗапуск режима многопроцессорного моделирования")
    start_time = time.time()

    try:
        config, phases_dict, plot_targets_dict = load_config("shema.json")
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return

    phase_data = [
        ("Фаза A", phases_dict["Фаза A"], plot_targets_dict["Фаза A"]),
        ("Фаза B", phases_dict["Фаза B"], plot_targets_dict["Фаза B"]),
        ("Фаза C", phases_dict["Фаза C"], plot_targets_dict["Фаза C"])
    ]

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    processes = []
    for data in phase_data:
        p = multiprocessing.Process(
            target=phase_worker,
            args=(config, data, result_queue)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    phase_results = []
    for _ in range(len(phase_data)):
        phase_results.append(result_queue.get())

    calculate_neutral(phase_results)
    print("\nРасчет нейтрали завершен")

    print(f"\nОбщее время выполнения: {time.time() - start_time:.2f} сек")
