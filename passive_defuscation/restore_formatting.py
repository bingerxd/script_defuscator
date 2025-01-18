#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
restore_formatting_python.py

Zaawansowane przywracanie formatowania kodu Python:
- Rozdzielanie instrukcji w jednej linii,
- Dodawanie poprawnych wcięć,
- Formatowanie kodu bez użycia Black, jeśli wystąpi błąd.

Dodano raport o dokonanych zmianach formatowania.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-12
"""

import re

# Liczniki zmian
semicolon_splits = 0
colon_splits = 0
indent_adjustments = 0

def manual_formatting(code: str) -> str:
    """
    Ręczne rozdzielenie kodu na poprawne instrukcje i dodanie wcięć.
    """
    global semicolon_splits, colon_splits, indent_adjustments

    # Resetowanie liczników
    semicolon_splits = 0
    colon_splits = 0
    indent_adjustments = 0

    # 1. Rozdzielenie instrukcji po średnikach
    semicolon_splits = len(re.findall(r';', code))
    code = re.sub(r';', ';\n', code)

    # 2. Dodanie nowej linii po dwukropkach (dla bloków kodu)
    colon_splits = len(re.findall(r':(?!\n)', code))
    code = re.sub(r':(?!\n)', ':\n', code)

    # 3. Rozdzielenie bloków kodu
    keywords = ['def', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'class']
    for kw in keywords:
        code = re.sub(rf'(\s*)({kw})(\s+)', r'\n\2 ', code)

    # 4. Dodanie wcięć dla bloków
    lines = code.split('\n')
    indent_level = 0
    formatted_lines = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        # Zmniejszenie wcięcia po zakończeniu bloku
        if stripped.startswith(('else', 'elif', 'except', 'finally')):
            indent_level -= 1

        formatted_lines.append('    ' * indent_level + stripped)

        # Zwiększenie wcięcia po dwukropku
        if stripped.endswith(':'):
            indent_level += 1
            indent_adjustments += 1

        # Zmniejszenie wcięcia po return/break/continue/pass
        if stripped.startswith(('return', 'break', 'continue', 'pass')):
            indent_level = max(indent_level - 1, 0)

    return '\n'.join(formatted_lines)


def restore_python_formatting(code: str) -> str:
    """
    Przywraca formatowanie kodu Python i dodaje raport o zmianach.
    """
    try:
        formatted_code = manual_formatting(code)
        formatted_code += generate_formatting_report()
        return formatted_code
    except Exception as e:
        print(f"Błąd podczas ręcznego formatowania: {e}")
        return code


def generate_formatting_report() -> str:
    """
    Generuje raport o przeprowadzonym formatowaniu.
    """
    report = "\n\n# === RAPORT O PRZYWRÓCONYM FORMATOWANIU ===\n"
    report += f"# Rozdzielone instrukcje po średnikach (;): {semicolon_splits}\n"
    report += f"# Dodane nowe linie po dwukropkach (:): {colon_splits}\n"
    report += f"# Dodane poprawne wcięcia: {indent_adjustments}\n"
    return report


def _test():
    """
    Test lokalny działania funkcji restore_python_formatting.
    """
    obfuscated_code = "def hello():print('Hello');if True:print('World');for i in range(5):print(i);if True:print('World');for i in range(5):print(i)"

    print("=== OBFUSKOWANY KOD PYTHON ===")
    print(obfuscated_code)

    formatted_code = restore_python_formatting(obfuscated_code)

    print("\n=== PO PRZYWRÓCENIU FORMATOWANIA ===")
    print(formatted_code)


if __name__ == "__main__":
    _test()