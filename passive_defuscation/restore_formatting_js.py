#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
restore_formatting_js.py

Przywracanie formatowania dla obfuskowanego kodu JavaScript:
- Rozdzielanie instrukcji w jednej linii.
- Dodawanie poprawnych wcięć dla bloków kodu.
- Usuwanie zbędnych spacji.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import re

def manual_formatting_js(code: str) -> str:
    """
    Ręczne formatowanie kodu JavaScript:
    - Rozdziela instrukcje po średnikach.
    - Dodaje wcięcia dla bloków kodu.
    """
    # 1. Dodanie nowej linii po średnikach (;)
    code = re.sub(r';', ';\n', code)

    # 2. Dodanie nowej linii po klamrach
    code = re.sub(r'\{', '{\n', code)
    code = re.sub(r'\}', '\n}\n', code)

    # 3. Dodanie nowej linii po słowach kluczowych
    keywords = ['if', 'else', 'for', 'while', 'function', 'switch', 'case', 'default', 'try', 'catch', 'finally']
    for kw in keywords:
        code = re.sub(rf'(\s*{kw}\s*)', r'\n\1', code)

    # 4. Uporządkowanie wcięć
    lines = code.split('\n')
    indent_level = 0
    formatted_lines = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        # Zmniejszenie wcięcia po zamknięciu bloku
        if stripped.startswith('}'):
            indent_level = max(indent_level - 1, 0)

        # Dodanie wcięcia
        formatted_lines.append('    ' * indent_level + stripped)

        # Zwiększenie wcięcia po otwarciu bloku
        if stripped.endswith('{'):
            indent_level += 1

    return '\n'.join(formatted_lines)

def restore_js_formatting(code: str) -> str:
    """
    Przywraca formatowanie kodu JavaScript.
    """
    try:
        formatted_code = manual_formatting_js(code)
        return formatted_code
    except Exception as e:
        print(f"Błąd podczas formatowania kodu JavaScript: {e}")
        return code

def _test():
    obfuscated_js_code = "function hello(){console.log('Hello');if(true){console.log('World');for(let i=0;i<5;i++){console.log(i);if(true){console.log('World');for(let i=0;i<5;i++){console.log(i);if(true){console.log('World');for(let i=0;i<5;i++){console.log(i);}}}"

    print("=== OBFUSKOWANY KOD JAVASCRIPT ===")
    print(obfuscated_js_code)

    formatted_code = restore_js_formatting(obfuscated_js_code)

    print("\n=== PO PRZYWRÓCENIU FORMATOWANIA ===")
    print(formatted_code)

if __name__ == "__main__":
    _test()