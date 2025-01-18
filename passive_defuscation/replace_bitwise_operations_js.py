import re

def replace_bitwise_operations(js_code: str) -> str:
    """
    Ulepszona zamiana przesunięć bitowych na czytelne operacje dzielenia/mnożenia.
    """
    # Zamiana >> na dzielenie z zaokrągleniem w dół
    js_code = re.sub(r'\b(\d+)\s*>>\s*(\d+)\b',
                     lambda m: str(int(int(m.group(1)) // (2 ** int(m.group(2))))),
                     js_code)

    js_code = re.sub(r'\b(\w+)\s*>>\s*(\d+)\b',
                     r'Math.floor(\1 / (2 ** \2))',
                     js_code)

    # Zamiana << na mnożenie
    js_code = re.sub(r'\b(\d+)\s*<<\s*(\d+)\b',
                     lambda m: str(int(m.group(1)) * (2 ** int(m.group(2)))),
                     js_code)

    js_code = re.sub(r'\b(\w+)\s*<<\s*(\d+)\b',
                     r'\1 * (2 ** \2)',
                     js_code)

    return js_code

def _test():
    obfuscated_js = """
let a = 9 >> 1;    // Oczekiwane: 4
let b = 5 << 1;    // Oczekiwane: 10
let c = x >> 3;    // Oczekiwane: Math.floor(x / 8)
let d = y << 4;    // Oczekiwane: (y * 16)
console.log(a, b, c, d);
"""

    print("=== Oryginalny kod JavaScript ===\n")
    print(obfuscated_js)

    deobfuscated_js = replace_bitwise_operations(obfuscated_js)

    print("\n=== Kod po ulepszonej deobfuskacji ===\n")
    print(deobfuscated_js)

if __name__ == "__main__":
    _test()