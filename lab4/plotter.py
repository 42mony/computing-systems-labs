import os
import threading
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plot_lock = threading.Lock()


class CircuitPlotter:
    def __init__(self, solver, mode = "default"):
        self.solver = solver
        self.history = solver.history
        self.circuit = solver.circuit
        self.mode = mode
        os.makedirs("plots", exist_ok=True)

    def plot_element(self, element_name):
        try:
            branch = self._get_branch_by_name(element_name)

            times = self.history["time"]
            currents = [I[branch, 0] for I in self.history["I"]]
            voltages = [U[branch, 0] for U in self.history["U"]]

            with plot_lock:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(times, currents, label="Ток, А")
                ax.plot(times, voltages, label="Напряжение, В")
                ax.set_xlabel("Время, с")
                ax.set_title(f"Ток и напряжение через элемент {element_name}")
                ax.grid(True)
                ax.legend()

                filename = os.path.join("plots", f"plot_{element_name.replace(' ', '_')}_{self.mode}.png")
                fig.savefig(filename)
                plt.close(fig)

            print(f"[График] Успешно сохранён: {filename}", flush=True)

        except Exception as e:
            print(f"[Ошибка графики] {element_name}: {str(e)}", flush=True)

    def _get_branch_by_name(self, element_name):
        for element in self.circuit.elements:
            if element.get_name() == element_name:
                return element._branch
        raise ValueError(f"Элемент {element_name} не найден")
