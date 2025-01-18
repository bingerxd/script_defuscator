#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
replace_bitwise_operations.py

Zamienia przesunięcia bitowe w kodzie Python na bardziej czytelne operacje:
- `x >> n` → `x // (2 ** n)`
- `x << n` → `x * (2 ** n)`

Dodaje raport o liczbie zamienionych operacji.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-12
"""

import re

# Liczniki operacji
right_shift_count = 0
left_shift_count = 0

def replace_bitwise_operations_py(py_code: str) -> str:
    """
    Zamienia przesunięcia bitowe w kodzie Python na bardziej czytelne operacje.
    Dodaje raport o liczbie zamienionych operacji.
    """
    global right_shift_count, left_shift_count

    # Resetowanie liczników
    right_shift_count = 0
    left_shift_count = 0

    # Funkcja do zliczania przesunięcia w prawo
    def count_right_shift(match):
        global right_shift_count
        right_shift_count += 1
        return f"{match.group(1)} // (2 ** {match.group(2)})"

    # Funkcja do zliczania przesunięcia w lewo
    def count_left_shift(match):
        global left_shift_count
        left_shift_count += 1
        return f"{match.group(1)} * (2 ** {match.group(2)})"

    # 1) Zamiana operatora przesunięcia w prawo (>>) na dzielenie całkowite
    py_code = re.sub(r'\b(\w+)\s*>>\s*(\d+)\b', count_right_shift, py_code)

    # 2) Zamiana operatora przesunięcia w lewo (<<) na mnożenie
    py_code = re.sub(r'\b(\w+)\s*<<\s*(\d+)\b', count_left_shift, py_code)

    # 3) Zamiana przesunięć bitowych na liczbach stałych (optymalizacja)
    py_code = re.sub(r'\b(\d+)\s*>>\s*(\d+)\b',
                     lambda m: str(int(m.group(1)) // (2 ** int(m.group(2)))), py_code)

    py_code = re.sub(r'\b(\d+)\s*<<\s*(\d+)\b',
                     lambda m: str(int(m.group(1)) * (2 ** int(m.group(2)))), py_code)

    # Dodanie raportu
    py_code += generate_bitwise_report()

    return py_code


def generate_bitwise_report() -> str:
    """
    Generuje raport o zamienionych operacjach przesunięcia bitowego.
    """
    report = "\n\n# === RAPORT O ZAMIENIONYCH OPERACJACH BITOWYCH ===\n"
    report += f"# Zamienione przesunięcia w prawo (>>): {right_shift_count}\n"
    report += f"# Zamienione przesunięcia w lewo (<<): {left_shift_count}\n"
    return report


def _test():
    """
    Test działania funkcji replace_bitwise_operations_py.
    """
    obfuscated_py = """
a = 9 >> 1    # Oczekiwane: 4
b = 5 << 1    # Oczekiwane: 10
c = x >> 3    # Oczekiwane: x // 8
d = y << 4    # Oczekiwane: y * 16
print(a, b, c, d)
"""

    print("=== Oryginalny kod Python ===\n")
    print(obfuscated_py)

    deobfuscated_py = replace_bitwise_operations_py(obfuscated_py)

    print("\n=== Kod po deobfuskacji ===\n")
    print(deobfuscated_py)


if __name__ == "__main__":
    _test()