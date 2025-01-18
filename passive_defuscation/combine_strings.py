#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
concat_strings.py

Funkcja:
    transform_concatenate_strings(script_content: str) -> str

Działanie:
    - Parsuje kod do AST (Python).
    - Śledzi przypisania zmiennych.
    - Łączy literalne stringi oraz zmienne zawierające stringi.
    - Na końcu ast.unparse => nowy kod w postaci tekstu.
    - UWAGA: Usuwa oryginalne komentarze i formatowanie.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import ast
import sys

class _StringConcatTransformer(ast.NodeTransformer):
    """
    Łączy literalne łańcuchy znaków i zmienne typu string w wyrażeniach typu:
    'abc' + var + 'def' => 'abcdef' (jeśli var = 'b').
    """

    def __init__(self):
        self.string_vars = {}
        self.concatenated_strings = []

    def visit_Assign(self, node):
        # Śledzenie przypisań zmiennych stringowych
        if (isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)):
            var_name = node.targets[0].id
            self.string_vars[var_name] = node.value.value
        self.generic_visit(node)
        return node

    def visit_BinOp(self, node):
        # Rekurencja w lewo/prawo
        self.generic_visit(node)

        if isinstance(node.op, ast.Add):
            left_value = self._resolve_value(node.left)
            right_value = self._resolve_value(node.right)

            if isinstance(left_value, str) and isinstance(right_value, str):
                combined = left_value + right_value
                self.concatenated_strings.append(f'"{left_value}" + "{right_value}" -> "{combined}"')
                return ast.Constant(value=combined)
        return node

    def _resolve_value(self, node):
        # Rozwiązywanie wartości: stałe i zmienne
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.Name):
            return self.string_vars.get(node.id, node)
        return node

def transform_concatenate_strings(script_content: str) -> str:
    """
    Łączy literalne stringi i zmienne typu string w kodzie Python.
    Dodaje raport o połączonych stringach.

    :param script_content: Kod Python
    :return: Nowy kod z raportem
    """
    try:
        tree = ast.parse(script_content)
    except SyntaxError:
        return script_content

    transformer = _StringConcatTransformer()
    new_tree = transformer.visit(tree)

    if sys.version_info >= (3, 9):
        transformed_code = ast.unparse(new_tree)
    else:
        return script_content

    # Tworzenie raportu
    report = "\n\n# === RAPORT O POŁĄCZONYCH STRINGACH ===\n"
    report += f"# Łączna liczba połączonych ciągów: {len(transformer.concatenated_strings)}\n"
    for concat in transformer.concatenated_strings:
        report += f"# - {concat}\n"

    return transformed_code + report

def _test():
    """
    Test lokalny.
    Uruchom: python concat_strings.py
    """
    code = r'''
def hello():
    msg = 'Hello' + ' ' + "World!"
    var = "abc"
    x = "abc" + var + "abc"
    y = var + "-" + var
'''

    print("=== Oryginalny kod ===")
    print(code)

    new_code = transform_concatenate_strings(code)

    print("\n=== Kod po transform_concatenate_strings (unparse) ===")
    print(new_code)

if __name__ == "__main__":
    _test()