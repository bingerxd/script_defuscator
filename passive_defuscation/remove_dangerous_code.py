#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remove_dangerous_code.py

Deobfuskacja niebezpiecznego kodu w Pythonie:
- Wykrywa i zakomentowuje funkcje eval(), exec().
- Wykrywa i zakomentowuje nieskończone pętle while True.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-12
"""

import re

# Globalne zmienne do zliczania
dangerous_eval_count = 0
dangerous_exec_count = 0
infinite_loop_count = 0

def remove_dangerous_code_python(code):
    """
    Zakomentowuje eval, exec i nieskończone pętle w kodzie Python.
    Dodaje raport o wykrytych zagrożeniach.
    """
    global dangerous_eval_count, dangerous_exec_count, infinite_loop_count

    # Resetowanie liczników
    dangerous_eval_count = 0
    dangerous_exec_count = 0
    infinite_loop_count = 0

    # Wzorce dla eval() i exec()
    dangerous_patterns = [
        (r'(eval\s*\(.*?\))', 'ZAKOMENTOWANE: ', 'eval'),
        (r'(exec\s*\(.*?\))', 'ZAKOMENTOWANE: ', 'exec')
    ]

    # Wzorzec dla nieskończonej pętli while True
    infinite_loop_pattern = (r'(while\s+True\s*:)', 'ZAKOMENTOWANE PĘTLA: ', 'while_true')

    # Zakomentowanie eval i exec
    for pattern, comment, label in dangerous_patterns:
        matches = re.findall(pattern, code, flags=re.DOTALL)
        count = len(matches)
        if label == 'eval':
            dangerous_eval_count += count
        elif label == 'exec':
            dangerous_exec_count += count

        code = re.sub(pattern, fr'# {comment}\1', code, flags=re.DOTALL)

    # Zakomentowanie nieskończonej pętli
    matches = re.findall(infinite_loop_pattern[0], code)
    infinite_loop_count += len(matches)
    code = re.sub(infinite_loop_pattern[0], fr'# {infinite_loop_pattern[1]}\1', code)

    # Dodanie raportu
    code += generate_dangerous_code_report()

    return code

def generate_dangerous_code_report():
    """
    Tworzy raport o wykrytych niebezpiecznych elementach.
    """
    report = "\n\n# === RAPORT O WYKRYTYCH ZAGROŻENIACH ===\n"
    report += f"# Funkcja eval(): {dangerous_eval_count}\n"
    report += f"# Funkcja exec(): {dangerous_exec_count}\n"
    report += f"# Nieskończone pętle while True: {infinite_loop_count}\n"
    return report

def _test():
    """
    Przykładowy test działania funkcji remove_dangerous_code_python.
    """
    example_code = '''
data = "print('Hello World!')"
eval(data)

exec("print('Exec executed')")

while True:
    print("Infinite loop")
'''

    print("=== Oryginalny kod ===")
    print(example_code)

    deobfuscated_code = remove_dangerous_code_python(example_code)

    print("\n=== Kod po deobfuskacji ===")
    print(deobfuscated_code)

if __name__ == "__main__":
    _test()