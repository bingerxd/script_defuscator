#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remove_dangerous_code_js.py

Deobfuskacja niebezpiecznego kodu w JavaScript:
- Wykrywa i zakomentowuje eval(), Function().
- Wykrywa i zakomentowuje nieskończone pętle for(;;) i while(true).

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-12
"""

import re

def remove_dangerous_code_js(code):
    """
    Zakomentowuje eval, Function() i nieskończone pętle w kodzie JS.
    """
    # Wzorce dla eval() i Function()
    dangerous_functions = [
        r'(eval\s*\(.*?\))',
        r'(new\s+Function\s*\(.*?\))'
    ]

    # Wzorce dla nieskończonych pętli
    infinite_loops = [
        r'(for\s*\(\s*;\s*;\s*\))',
        r'(while\s*\(\s*true\s*\))'
    ]

    # Zakomentowanie eval i Function
    for pattern in dangerous_functions:
        code = re.sub(pattern, r'// ZAKOMENTOWANE: \1', code, flags=re.DOTALL | re.IGNORECASE)

    # Zakomentowanie nieskończonych pętli
    for pattern in infinite_loops:
        code = re.sub(pattern, r'// ZAKOMENTOWANA PĘTLA: \1', code, flags=re.IGNORECASE)

    return code

def _test():
    example_code = '''
let data = "console.log('Hello World!')";
eval(data);

let fn = new Function("console.log('Function constructor')");

for (;;) {
    console.log("Infinite loop");
}

while (true) {
    console.log("Another infinite loop");
}
'''

    print("=== Oryginalny kod JS ===")
    print(example_code)

    deobfuscated_code = remove_dangerous_code_js(example_code)

    print("\n=== Kod po deobfuskacji ===")
    print(deobfuscated_code)

if __name__ == "__main__":
    _test()