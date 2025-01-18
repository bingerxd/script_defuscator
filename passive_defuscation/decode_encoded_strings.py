#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decode_encoded_strings.py

Deobfuskacja zakodowanych ciągów Base64 w kodzie Python:
- Wykrywa i dekoduje poprawne ciągi Base64.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import re
import base64

# Lista do przechowywania wykrytych ciągów Base64
decoded_strings_report = []

def is_base64(s):
    """Sprawdza, czy ciąg jest poprawnym kodem Base64."""
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False

def decode_base64(s):
    """Dekoduje ciąg Base64."""
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return s

def decode_encoded_strings(code):
    """
    Wyszukuje i dekoduje zakodowane Base64 ciągi w kodzie Python.
    """
    base64_pattern = r'"([A-Za-z0-9+/=]{8,})"'

    def decode_match(match):
        s = match.group(1)
        if s == "ScreenLocker":
            return match.group(0)
        if is_base64(s):
            decoded = decode_base64(s)
            decoded_strings_report.append((s, decoded))
            return f'"{decoded}"  # DECODED_BASE64'
        else:
            return match.group(0)

    code = re.sub(base64_pattern, decode_match, code)

    report = "\n\n# === RAPORT O WYKRYTYCH BASE64 ===\n"
    report += f"# Łączna liczba zdekodowanych ciągów Base64: {len(decoded_strings_report)}\n"
    for original, decoded in decoded_strings_report:
        report += f"# - Oryginał: \"{original}\"\n"
        report += f"# - Zdekodowany: \"{decoded}\"\n\n"

    return code + report

def _test():
    """
    Test lokalny.
    Uruchom: python decode_encoded_strings.py
    """
    example_code = '''
secret_base64 = "SGVsbG8gV29ybGQh"  # Hello World!
normal_string = "To jest zwykły tekst."
normal_string = "MTA5LjcwLjEwMC41"
normal_string = "CmRlZiBzZWNyZXRfZnVuY3Rpb24oKToKICAgIHByaW50KCJUbyBqZXN0IHVrcnl0YSB3aWFkb21vxZvEhyEiKQo="

'''

    print("=== Oryginalny kod ===")
    print(example_code)

    decoded_code = decode_encoded_strings(example_code)

    print("\n=== Kod po deobfuskacji ===")
    print(decoded_code)

if __name__ == "__main__":
    _test()
