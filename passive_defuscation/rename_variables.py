#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rename_variables.py

Moduł do wykrywania i zmiany losowych nazw zmiennych, funkcji, klas w kodzie Python.
Dodaje raport o liczbie zmienionych nazw.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import ast
import re

# Statystyki zmian
renamed_variables_count = 0
renamed_functions_count = 0
renamed_classes_count = 0


class _NameRenamer(ast.NodeTransformer):
    """
    Transformer AST, który rename’uje losowe nazwy:
    - zmiennych,
    - funkcji,
    - klas.
    """

    def __init__(self):
        super().__init__()
        self.replacements = {}
        self.var_count = 0

    def _is_random_name(self, name: str) -> bool:
        """Sprawdza, czy nazwa wygląda na losową."""
        if len(name) < 11:
            return False

        uppercase_count = sum(1 for ch in name if ch.isupper())
        lowercase_count = sum(1 for ch in name if ch.islower())
        digit_count = sum(1 for ch in name if ch.isdigit())

        return uppercase_count >= 2 and lowercase_count >= 2 and digit_count >= 2

    def _get_new_name(self, old_name: str) -> str:
        """Generuje nową nazwę i zapamiętuje ją."""
        global renamed_variables_count
        if old_name not in self.replacements:
            new_name = f"var{self.var_count}"
            self.var_count += 1
            self.replacements[old_name] = new_name
            renamed_variables_count += 1
        return self.replacements[old_name]

    def visit_Name(self, node: ast.Name):
        """Zmienia nazwy zmiennych."""
        if self._is_random_name(node.id):
            node.id = self._get_new_name(node.id)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Zmienia nazwy funkcji."""
        global renamed_functions_count
        if self._is_random_name(node.name):
            node.name = self._get_new_name(node.name)
            renamed_functions_count += 1
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        """Zmienia nazwy klas."""
        global renamed_classes_count
        if self._is_random_name(node.name):
            node.name = self._get_new_name(node.name)
            renamed_classes_count += 1
        self.generic_visit(node)
        return node


def rename_long_random_names(script_content: str) -> str:
    """
    Zmienia losowe nazwy zmiennych, funkcji i klas.
    Dodaje raport o liczbie zmian na końcu kodu.
    """
    global renamed_variables_count, renamed_functions_count, renamed_classes_count

    # Resetowanie liczników
    renamed_variables_count = 0
    renamed_functions_count = 0
    renamed_classes_count = 0

    try:
        tree = ast.parse(script_content)

        renamer = _NameRenamer()
        new_tree = renamer.visit(tree)

        optimized_code = ast.unparse(new_tree)

        # Dodanie raportu
        optimized_code += generate_rename_report()

        return optimized_code

    except SyntaxError as e:
        print(f"[rename_variables] Błąd składni: {e}")
        return script_content


def generate_rename_report() -> str:
    """
    Generuje raport o liczbie zmienionych zmiennych, funkcji i klas.
    """
    report = "\n\n# === RAPORT O ZMIENIONYCH NAZWACH ===\n"
    report += f"# Zmienione zmienne: {renamed_variables_count}\n"
    report += f"# Zmienione funkcje: {renamed_functions_count}\n"
    report += f"# Zmienione klasy: {renamed_classes_count}\n"
    return report


def _test():
    """
    Test lokalny działania rename_long_random_names.
    """
    test_code = r'''
class MyClassAbCD12xy99:
    def ABCD12xy99Func(self, paramAb12XYZ99=10):
        localAb12xy99Var = 100
        AnotherAb12XY99 = localAb12xy99Var + paramAb12XYZ99
        return AnotherAb12XY99

AB12xy99Global = 123

def AB12XY99myFunction():
    for i in range(3):
        print("Loop", i, AB12xy99Global)
    return AB12xy99Global
'''

    print("=== Oryginalny kod ===")
    print(test_code)

    result = rename_long_random_names(test_code)

    print("\n=== Kod po rename ===")
    print(result)


if __name__ == "__main__":
    _test()