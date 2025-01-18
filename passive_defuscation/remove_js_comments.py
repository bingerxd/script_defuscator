#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remove_js_comments.py

Skrypt w Pythonie, który usuwa komentarze z kodu JavaScript, korzystając
z Node.js + esprima + escodegen (wywołanie przez subprocess).

Wymagania:
1) Node.js zainstalowany (node -v).
2) npm install -g esprima escodegen
   lub lokalnie w projekcie, o ile node_remove_comments.js też będzie
   w stanie je odnaleźć (np. w node_modules).

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import os
import subprocess
import tempfile

NODE_SCRIPT = r"""
// node_remove_comments.js
// Skrypt Node.js w JS, używający esprima + escodegen do usuwania komentarzy
// Odczytuje kod JS z stdin, wypluwa kod BEZ komentarzy na stdout.

const esprima = require('esprima');
const escodegen = require('escodegen');

// Wczytanie kodu z stdin:
let code = '';
process.stdin.on('data', chunk => {
  code += chunk;
});
process.stdin.on('end', () => {
  // Parsujemy kod z opcją komentarzy
  const ast = esprima.parseScript(code, {
    comment: true,
    tokens: true,
    range: true,
    attachComment: true
  });

  // Generujemy kod bez komentarzy
  const output = escodegen.generate(ast, {
    comment: false
  });

  // Wypluwamy wynik
  process.stdout.write(output);
});
"""

def remove_comments_js(js_code: str) -> str:
    """
    Usuwa komentarze z kodu JavaScript (//, /*...*/, /** ... */)
    używając Node.js + esprima + escodegen.

    :param js_code: oryginalny kod JS (string)
    :return: kod JS bez komentarzy
    """
    # 1. Tworzymy plik tymczasowy, w którym zapisujemy skrypt Node.js (node_remove_comments.js).
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as node_script_file:
        node_script_file.write(NODE_SCRIPT)
        node_script_path = node_script_file.name

    try:
        # 2. Uruchamiamy subprocess Node.js, przekazując skrypt node_remove_comments.js,
        #    a kod JS - przez stdin.
        result = subprocess.run(
            ['node', node_script_path],
            input=js_code,
            text=True,
            capture_output=True
        )

        # 3. Sprawdzamy, czy wystąpił błąd (np. brak Node.js, brak esprima).
        if result.returncode != 0:
            print("Błąd w wywołaniu Node.js:\n", result.stderr)
            # Możesz zwrócić oryginał lub rzucić wyjątek. Tu zwracam oryginał:
            return js_code

        # 4. Odczytujemy stdout, czyli kod JS bez komentarzy.
        cleaned_code = result.stdout
        return cleaned_code

    finally:
        # 5. Sprzątamy - usuwamy plik tymczasowy ze skryptem Node.js
        if os.path.exists(node_script_path):
            os.remove(node_script_path)


def _test():
    """
    Funkcja testowa demonstrująca działanie remove_comments_js na przykładowym kodzie JS,
    który wcześniej zawierał zagnieżdżone komentarze powodujące błąd w esprima.
    """
    example_js = r"""
// Komentarz linii
var x = 10; // Komentarz w tej samej linii

/*
   Wielolinijkowy komentarz
   docstring JSDoc
*/

/**
 * Funkcja
 * @param n
 */
function hello() {
  console.log("Hello // World"); // Problem dla regex? Tu nie.
  let url = "http://example.com";
  /** Kolejny JSDoc */
  return "done";
}
"""

    print("=== Oryginalny kod JS ===")
    print(example_js)

    cleaned = remove_comments_js(example_js)

    print("\n=== Kod JS po usunięciu komentarzy (Node.js + esprima) ===")
    print(cleaned)


if __name__ == "__main__":
    _test()