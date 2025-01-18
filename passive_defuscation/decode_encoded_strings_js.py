#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decode_encoded_strings_js.py

Deobfuskacja zakodowanych ciągów Base64 w kodzie JavaScript:
- Wykrywa i dekoduje poprawne ciągi Base64.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import re
import base64

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

def decode_encoded_strings_js(code):
    """
    Wyszukuje i dekoduje zakodowane Base64 ciągi w kodzie JavaScript.
    """
    base64_pattern = r'[`\"\']([A-Za-z0-9+/=]{8,})[`\"\']'

    def decode_match(match):
        s = match.group(1)
        if is_base64(s):
            decoded = decode_base64(s)
            return f'"{decoded}"  // DECODED_BASE64'
        else:
            return match.group(0)

    code = re.sub(base64_pattern, decode_match, code)

    return code

def _test():
    example_code = '''
const secretBase64 = "SGVsbG8gV29ybGQh";  // Hello World!
const normalString = "To jest zwykły tekst.";
let var = "Tojestzwyklytekst.";
const encodedFunction = "ImZ1bmN0aW9uIHNlY3JldEZ1bmN0aW9uKCkgew0KICAgIGNvbnNvbGUubG9nKCJUbyBqZXN0IHVrcnl0YSB3aWFkb21vxZvEhyIpOw0KfQ0Kc2VjcmV0RnVuY3Rpb24oKTsi";

'''

    print("=== Oryginalny kod ===")
    print(example_code)

    decoded_code = decode_encoded_strings_js(example_code)

    print("\n=== Kod po deobfuskacji ===")
    print(decoded_code)

if __name__ == "__main__":
    _test()
