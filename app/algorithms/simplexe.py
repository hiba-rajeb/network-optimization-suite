import logging

logger = logging.getLogger(__name__)


def creer_probleme():
    """
    Maximiser Z = 4x1 + 5x2 + 3x3  (production électrique en MWh)
    Sous contraintes :
        6x1 + 4x2 + 2x3 <= 240   (capacité réseau Nord)
        3x1 + 2x2 + 5x3 <= 270   (capacité réseau Centre)
        5x1 + 6x2 + 5x3 <= 420   (capacité réseau Sud)
        x1, x2, x3 >= 0
    """
    return {
        'variables':   ['x₁ (Région Nord)', 'x₂ (Région Centre)', 'x₃ (Région Sud)'],
        'objectif':    'Maximiser  Z = 4x₁ + 5x₂ + 3x₃   (MWh distribués)',
        'contraintes': [
            '6x₁ + 4x₂ + 2x₃  ≤  240   (Capacité réseau Nord)',
            '3x₁ + 2x₂ + 5x₃  ≤  270   (Capacité réseau Centre)',
            '5x₁ + 6x₂ + 5x₃  ≤  420   (Capacité réseau Sud)',
            'x₁, x₂, x₃  ≥  0',
        ],
        'c': [4, 5, 3],
        'A': [[6, 4, 2], [3, 2, 5], [5, 6, 5]],
        'b': [240, 270, 420],
    }


def executer_simplexe(c, A, b):
    """Méthode du Simplexe — maximisation, contraintes ≤, variables ≥ 0."""
    m = len(b)
    n = len(c)
    total = n + m          # variables de décision + écarts

    # Construction du tableau initial
    tableau = []
    for i in range(m):
        row = [float(x) for x in A[i]] + [0.0] * m + [float(b[i])]
        row[n + i] = 1.0
        tableau.append(row)
    tableau.append([-float(ci) for ci in c] + [0.0] * m + [0.0])

    headers = [f'x{i+1}' for i in range(n)] + [f's{i+1}' for i in range(m)] + ['b']
    basic   = list(range(n, n + m))   # variables de base initiales = écarts

    iterations = [_snapshot(tableau, basic, headers)]

    for _ in range(200):
        obj_row  = tableau[-1]
        pivot_col = min(range(total), key=lambda j: obj_row[j])
        if obj_row[pivot_col] >= -1e-9:
            break   # solution optimale

        # Règle du minimum ratio
        pivot_row = -1
        min_ratio = float('inf')
        for i in range(m):
            if tableau[i][pivot_col] > 1e-9:
                ratio = tableau[i][-1] / tableau[i][pivot_col]
                if ratio < min_ratio - 1e-9:
                    min_ratio = ratio
                    pivot_row = i

        if pivot_row == -1:
            raise ValueError("Problème non borné")

        # Pivot
        pv = tableau[pivot_row][pivot_col]
        tableau[pivot_row] = [x / pv for x in tableau[pivot_row]]
        for i in range(len(tableau)):
            if i != pivot_row:
                f = tableau[i][pivot_col]
                if abs(f) > 1e-12:
                    tableau[i] = [tableau[i][j] - f * tableau[pivot_row][j]
                                  for j in range(len(tableau[i]))]

        basic[pivot_row] = pivot_col
        iterations.append(_snapshot(tableau, basic, headers))

    # Extraction de la solution
    solution = [0.0] * n
    for j in range(n):
        for i in range(m):
            if basic[i] == j:
                solution[j] = max(0.0, round(tableau[i][-1], 4))

    valeur_opt = round(tableau[-1][-1], 4)
    logger.info(f"Simplexe: solution={solution}, Z={valeur_opt}")
    return solution, valeur_opt, iterations, headers


def _snapshot(tableau, basic, headers):
    return {
        'tableau': [row[:] for row in tableau],
        'basic':   basic[:],
        'headers': headers[:],
    }
