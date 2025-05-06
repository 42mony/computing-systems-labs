import threading
import queue
from three_phase_simulator import load_config, simulate_phase, calculate_neutral
import time


def run_threading():
    print("\nЗапуск режима многопоточного моделирования")
    start_time = time.time()

    try:
        config, phases, plot_targets = load_config("shema.json")
    except Exception as e:
        print(f"\nОшибка загрузки схемы: {e}")
        return

    results_queue = queue.Queue()
    phase_names = ["Фаза A", "Фаза B", "Фаза C"]

    def calculate_phase(name):
        try:
            result = simulate_phase(
                config=config,
                indices=phases[name],
                phase_name=name,
                plot_targets=plot_targets[name],
                mode="threading"
            )
            results_queue.put(result)
            print(f"\n[{name}] Расчет завершен")
        except Exception as e:
            print(f"[{name}] Ошибка: {e}")
            results_queue.put((name, [], None))

    phase_threads = []
    for name in phase_names:
        thread = threading.Thread(target=calculate_phase, args=(name,))
        thread.start()
        phase_threads.append(thread)

    for thread in phase_threads:
        thread.join()

    phase_results = []
    for _ in phase_names:
        phase_results.append(results_queue.get())

    calculate_neutral(phase_results)
    print("\nРасчет нейтрали завершен")

    total_time = time.time() - start_time
    print(f"\nОбщее время выполнения: {total_time:.2f} сек")
