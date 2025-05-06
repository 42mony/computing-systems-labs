import numpy as np


class CircuitSolver:
    def __init__(self, circuit):
        self.circuit = circuit

        self.I = np.zeros((circuit.branches, 1))
        self.U = np.zeros((circuit.branches, 1))
        self.F = np.zeros((circuit.nodes - 1, 1))

        self.history = {
            'time': [],
            'I': [],
            'U': [],
            'F': []
        }

    def _build_matrix_A(self):
        A = np.zeros((self.circuit.nodes - 1, self.circuit.branches))
        for elem in self.circuit.elements:
            if elem.start_node > 0:
                A[elem.start_node - 1, elem._branch] = 1
            if elem.end_node > 0:
                A[elem.end_node - 1, elem._branch] = -1
        return A

    def _build_matrix_Y(self, h):
        Y = np.zeros((self.circuit.branches, self.circuit.branches))
        for elem in self.circuit.elements:
            Y[elem._branch, elem._branch] = elem.calculate_conductivity(h)
        return Y

    def solve_step(self, time):
        A = self._build_matrix_A()
        Y = self._build_matrix_Y(self.circuit.h)

        E = np.array([[elem.calculate_emf(time, self.circuit.h)]
                      for elem in self.circuit.elements])
        J = np.array([[elem.calculate_current_source(time)]
                      for elem in self.circuit.elements])

        AY = A @ Y
        self.F = -np.linalg.solve(AY @ A.T, A @ J + AY @ E)
        self.U = A.T @ self.F
        self.I = Y @ (self.U + E) + J

        for elem in self.circuit.elements:
            elem.update_state(
                current=self.I[elem._branch, 0],
                voltage=self.U[elem._branch, 0]
            )

        self.history['time'].append(time)
        self.history['I'].append(self.I.copy())
        self.history['U'].append(self.U.copy())
        self.history['F'].append(self.F.copy())

        return {'I': self.I, 'U': self.U, 'F': self.F}

    def simulate(self):
        steps = int(self.circuit.simulation_time / self.circuit.h)

        for step in range(steps):
            time = step * self.circuit.h
            self.solve_step(time)