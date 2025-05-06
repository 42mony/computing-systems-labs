import json
import numpy as np
from circuit import Circuit
from solver import CircuitSolver
from plotter import CircuitPlotter


def load_config(path):
    with open(path) as f:
        config = json.load(f)

    phase_names = {"1": "Фаза A", "2": "Фаза B", "3": "Фаза C"}
    phases_dict = {"Фаза A": [], "Фаза B": [], "Фаза C": []}
    plot_targets_dict = {"Фаза A": [], "Фаза B": [], "Фаза C": []}

    measure_list = config["scheme_parameters"].get("list_measurements_objects", [])

    for idx, elem in enumerate(config["scheme_elements"]):
        name = elem["name"]
        for key in phase_names:
            if name.endswith(key):
                phase = phase_names[key]
                phases_dict[phase].append(idx)
                if name in measure_list:
                    plot_targets_dict[phase].append(name)
                break

    return config, phases_dict, plot_targets_dict


def simulate_phase(config, indices, phase_name, plot_targets, mode="default"):
    try:
        circuit = build_phase_circuit(config, indices)
        solver = CircuitSolver(circuit)

        h = circuit.h
        steps = int(circuit.simulation_time / h)
        currents = []

        for step in range(steps):
            time = step * h
            result = solver.solve_step(time)

            load_branch = None
            for elem in circuit.elements:
                if elem.start_node != 0 and elem.get_type() in ["R", "L", "C"]:
                    load_branch = elem._branch

            if load_branch is not None:
                currents.append(result["I"][load_branch, 0])

        plotter = CircuitPlotter(solver, mode)
        for name in plot_targets:
            plotter.plot_element(name)

        r = next(
            (
                e.get_resistance()
                for e in circuit.elements
                if e.get_type() == "R" and e.start_node != 0
            ),
            0,
        )
        l = next(
            (
                e.get_inductance()
                for e in circuit.elements
                if e.get_type() == "L" and e.start_node != 0
            ),
            0,
        )
        c = next(
            (
                e.get_capacitance()
                for e in circuit.elements
                if e.get_type() == "C" and e.start_node != 0
            ),
            0,
        )

        parts = []
        if r:
            parts.append(f"R={r} Ом")
        if l:
            parts.append(f"L={l} мГн")
        if c:
            parts.append(f"C={c} мкФ")
        desc = ", ".join(parts)

        print(
            f"\n{phase_name}: макс. ток = {max(np.abs(currents)):.2f} А ({desc})",
            flush=True,
        )

        return (phase_name, currents, solver)

    except Exception as e:
        print(f"[{phase_name}] Ошибка: {e}", flush=True)
        return (phase_name, [], None)


def build_phase_circuit(config, elem_indices):
    phase_elements = [config["scheme_elements"][i] for i in elem_indices]

    unique_nodes = set()
    for e in phase_elements:
        unique_nodes.add(e["start_node"])
        unique_nodes.add(e["end_node"])

    node_map = {}
    for new, old in enumerate(unique_nodes):
        node_map[old] = new

    unique_branches = sorted(set(e["branch"] for e in phase_elements))

    branch_map = {}

    for new, old in enumerate(unique_branches):
        branch_map[old] = new

    new_elements = []
    for e in phase_elements:
        new_elem = dict(e)
        new_elem["start_node"] = node_map[e["start_node"]]
        new_elem["end_node"] = node_map[e["end_node"]]
        new_elem["branch"] = branch_map[e["branch"]]
        new_elements.append(new_elem)

    phase_params = dict(config["scheme_parameters"])
    phase_params["count_nodes"] = len(node_map)
    phase_params["count_branches"] = len(branch_map)

    return Circuit({"scheme_parameters": phase_params, "scheme_elements": new_elements})


def calculate_neutral(phases):

    valid_currents = [
        currents
        for _, currents, _ in phases
        if isinstance(currents, list) and len(currents) > 0
    ]
    if not valid_currents:
        print("Не удалось рассчитать ток в нейтрали — нет данных от фаз.", flush=True)
        return

    min_length = min(len(c) for c in valid_currents)

    neutral_currents = []
    for i in range(min_length):
        sum_i = 0
        for n, (_, currents, _) in enumerate(phases): 
            if i < len(currents):
                angle = np.radians(120 * n)
                sum_i += currents[i] * np.exp(1j * angle)
        neutral_currents.append(np.abs(sum_i))

    max_neutral = max(neutral_currents)
    print(f"\nТок в нейтрали: {max_neutral:.2f} А", flush=True)
