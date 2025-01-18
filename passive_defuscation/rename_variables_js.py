#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rename_variables.py

Moduł zawierający funkcję do wykrywania i rename’owania długich,
'losowych' nazw zmiennych/funkcji/klas w kodzie JavaScript.
Realizowane czysto przez operacje na tekście (regex),
bez użycia parsera AST.

Funkcja:
    rename_long_random_names(js_code: str) -> str

Heurystyka "losowości":
- Identyfikator musi mieć >= 11 znaków.
- Co najmniej 2 wielkie litery, 2 małe litery, 2 cyfry.
- (Opcjonalnie) brak podkreślenia '_' - aby nie łapać typowych, krótszych
  nazw w stylu my_var, itp.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import re


def rename_long_random_names(js_code: str) -> str:
    """
    Wyszukuje w kodzie JavaScript identyfikatory (słowa z [a-zA-Z0-9]),
    sprawdza czy są 'długie i losowe', i zamienia je systematycznie
    na var0, var1, var2...

    KROKI:
    1. Szukamy wszystkich ciągów alfanumerycznych \b[a-zA-Z0-9]+\b.
    2. Dla każdego sprawdzamy heurystykę "losowości":
       - długość >= 11
       - co najmniej 2 duże litery (A-Z), 2 małe litery (a-z) i 2 cyfry (0-9)
       - (opcjonalnie) brak znaku '_'
    3. Jeśli spełnia, dopisujemy do mapy zamian (old -> new).
    4. Zamieniamy w całym kodzie, używając re.sub z \b, aby tylko
       całe słowa zostały podmienione.

    :param js_code: Treść kodu JavaScript (jako string).
    :return: Nowy kod JS z rename'owanymi nazwami.
    """

    def is_random_name_js(name: str) -> bool:
        """Sprawdza, czy nazwa wygląda na 'losową' wg. ustalonej heurystyki."""
        if len(name) < 11:
            return False

        uppercase_count = sum(1 for ch in name if ch.isupper())
        lowercase_count = sum(1 for ch in name if ch.islower())
        digit_count     = sum(1 for ch in name if ch.isdigit())

        # Jeżeli nie chcemy łapać nazw ze znakiem '_', to:
        if '_' in name:
            return False

        return (uppercase_count >= 2 and
                lowercase_count >= 2 and
                digit_count >= 2)

    # 1. Znajdujemy wszystkie słowa alfanumeryczne
    pattern = r'\b[a-zA-Z0-9]+\b'
    all_matches = re.findall(pattern, js_code)

    # 2. Budujemy mapę 'stara_nazwa' -> 'varX'
    replacements = {}
    var_count = 0

    # Przechodzimy po wszystkich znalezionych słowach
    for match in all_matches:
        if match not in replacements and is_random_name_js(match):
            new_name = f"var{var_count}"
            replacements[match] = new_name
            var_count += 1

    # 3. Zamieniamy w całym kodzie
    #    Re.sub z \b old_name \b aby uniknąć podmian wewnątrz innego słowa
    new_js_code = js_code
    for old, new in replacements.items():
        new_js_code = re.sub(r'\b' + re.escape(old) + r'\b', new, new_js_code)

    return new_js_code


def _test():
    """
    Test lokalny funkcji rename_long_random_names() - użycie:
      python rename_variables.py
    """
    test_js = r'''
    // Przykładowy kod z 'losowymi' nazwami:
    let ABCD12xy99 = 10;
    function EF12GHxy99Func() {
      let localAb12xy99Var = ABCD12xy99 + 5;
      console.log("Wynik:", localAb12xy99Var);
      return localAb12xy99Var;
    }
    // Poniższa klasa też ma 'losową' nazwę:
    class XY99Ab12ClassTest {
      constructor() {
        this.id = 1;
      }
      methodAb12XY99() {
        return "Hello " + this.id;
      }
    }
    '''
    print("=== Oryginalny kod JavaScript ===\n", test_js)

    renamed_code = rename_long_random_names(test_js)

    print("=== Kod po rename ===\n", renamed_code)


if __name__ == "__main__":
    _test()