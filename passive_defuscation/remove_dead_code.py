#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remove_dead_code.py

Skrypt usuwa:
1. Nieużywane zmienne (wykrywa zmienne, które są wykorzystywane w całym kodzie),
2. Puste funkcje,
3. Puste warunki.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import ast
import sys

# Globalne zmienne do raportu
removed_variables_count = 0
removed_functions_count = 0
removed_conditions_count = 0

class UsedVariableCollector(ast.NodeVisitor):
    """
    Zbiera wszystkie zmienne używane w kodzie (np. w print(x), if x > 0).
    """

    def __init__(self):
        self.used_vars = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)


class DeadCodeRemover(ast.NodeTransformer):
    """
    Usuwa:
    - nieużywane zmienne,
    - puste funkcje,
    - puste warunki.
    """

    def __init__(self, used_vars):
        self.used_vars = used_vars

    def visit_Assign(self, node):
        global removed_variables_count
        # Sprawdzamy, czy zmienne są używane
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if not any(var in self.used_vars for var in targets):
            removed_variables_count += 1  # Zliczamy usuniętą zmienną
            return None  # Usuwamy, jeśli zmienna nie jest używana
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        global removed_functions_count
        # Usuwamy puste funkcje
        if not node.body or all(isinstance(stmt, ast.Pass) for stmt in node.body):
            removed_functions_count += 1  # Zliczamy usuniętą funkcję
            return None
        return self.generic_visit(node)

    def visit_If(self, node):
        global removed_conditions_count
        # Usuwamy puste warunki
        if not node.body or all(isinstance(stmt, ast.Pass) for stmt in node.body):
            removed_conditions_count += 1  # Zliczamy usunięty warunek
            return None
        return self.generic_visit(node)

    def visit_For(self, node):
        global removed_conditions_count
        # Usuwamy puste pętle for
        if not node.body or all(isinstance(stmt, ast.Pass) for stmt in node.body):
            removed_conditions_count += 1
            return None
        return self.generic_visit(node)

    def visit_While(self, node):
        global removed_conditions_count
        # Usuwamy puste pętle while
        if not node.body or all(isinstance(stmt, ast.Pass) for stmt in node.body):
            removed_conditions_count += 1
            return None
        return self.generic_visit(node)


def remove_dead_code(code: str) -> str:
    """
    Usuwa nieużywane zmienne, puste funkcje i puste warunki.
    Dodaje raport o usuniętych elementach.
    """
    global removed_variables_count, removed_functions_count, removed_conditions_count

    # Resetowanie liczników
    removed_variables_count = 0
    removed_functions_count = 0
    removed_conditions_count = 0

    try:
        tree = ast.parse(code)

        # 1) Zbieranie używanych zmiennych
        collector = UsedVariableCollector()
        collector.visit(tree)

        # 2) Usunięcie martwego kodu
        remover = DeadCodeRemover(collector.used_vars)
        optimized_tree = remover.visit(tree)
        ast.fix_missing_locations(optimized_tree)

        # 3) Kod po usunięciu martwego kodu
        optimized_code = ast.unparse(optimized_tree) if sys.version_info >= (3, 9) else code

        # 4) Dodanie raportu na końcu kodu
        optimized_code += generate_dead_code_report()

        return optimized_code

    except Exception as e:
        print(f"Błąd podczas deobfuskacji: {e}")
        return code


def generate_dead_code_report():
    """
    Generuje raport o usuniętych elementach (zmienne, funkcje, warunki).
    """
    report = "\n\n# === RAPORT O USUNIĘTYM MARTWYM KODZIE ===\n"
    report += f"# Usunięte zmienne: {removed_variables_count}\n"
    report += f"# Usunięte puste funkcje: {removed_functions_count}\n"
    report += f"# Usunięte puste warunki/pętle: {removed_conditions_count}\n"
    return report


def _test():
    """
    Przykładowy test działania funkcji remove_dead_code.
    """
    example_code = '''
def used_function():
    print("Używana funkcja")

def empty_function():
    pass

x = 10
y = 20  # nieużywana zmienna
print(x)

if True:
    pass

def function():
    print("1")

for i in range(5):
    pass

used_function()
'''

    print("=== Oryginalny kod ===")
    print(example_code)

    optimized_code = remove_dead_code(example_code)

    print("\n=== Kod po deobfuskacji ===")
    print(optimized_code)


if __name__ == "__main__":
    _test()