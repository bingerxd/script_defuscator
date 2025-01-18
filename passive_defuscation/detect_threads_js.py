#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
detect_threads_js.py

Skrypt w Pythonie wykrywający "wielowątkowość" w JavaScript:
np. 'new Worker(...)', 'new SharedWorker(...)', 'importScripts(...)',
'Worker Threads' (z Node.js), itp. – w kodzie JS.

Działa tak:
 1) Tworzy tymczasowy plik node.js (node_detect_threads.js),
    który korzysta z esprima do analizy kodu JS (AST).
 2) Uruchamia go w subprocess, przekazując kod JS przez stdin.
 3) Node wykrywa wystąpienia w AST (np. new Worker(...) -> NewExpression),
    zapisuje numer linii do tablicy.
 4) Python odbiera listę numerów linii w JSON i dopisuje w oryginalnym kodzie:
    //THREADING_DETECTED na końcu tych linii.

WYMAGANIA:
 - Zainstalowany Node.js,
 - npm install -g esprima
 - Python 3.x z 'subprocess', 'json', 'tempfile'

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import subprocess
import tempfile
import os
import json


NODE_DETECT_THREADS = r"""
/**
 * node_detect_threads.js
 * Wczytuje kod JS z stdin, parsuje esprima, wykrywa:
 *    new Worker(...), new SharedWorker(...), importScripts(...), itp.
 * Zwraca JSON listę numerów linii (1-based) na stdout.
 */

const esprima = require('esprima');

process.stdin.setEncoding('utf8');

let code = '';
process.stdin.on('data', (chunk) => {
  code += chunk;
});
process.stdin.on('end', () => {
  let linesDetected = [];

  try {
    // Parsujemy z lokacją
    const ast = esprima.parseScript(code, {
      loc: true,
      range: true,
      comment: true,
      tolerant: true
    });

    // Przechodzimy po AST rekurencyjnie
    function traverse(node) {
      if (!node || typeof node !== 'object') return;
      
      // Sprawdzamy typ node
      // 1) new Worker(...) / new SharedWorker(...)
      if (node.type === 'NewExpression' && node.callee && node.callee.type === 'Identifier') {
        // np. new Worker(...) => node.callee.name = "Worker"
        // np. new SharedWorker(...) => node.callee.name = "SharedWorker"
        const calleeName = node.callee.name;
        if (calleeName === 'Worker' || calleeName === 'SharedWorker') {
          linesDetected.push(node.loc.start.line);
        }
      }
      // 2) Wywołanie importScripts(...) => CallExpression { callee: { name: 'importScripts' } }
      else if (node.type === 'CallExpression' && node.callee && node.callee.type === 'Identifier') {
        if (node.callee.name === 'importScripts') {
          linesDetected.push(node.loc.start.line);
        }
      }
      // 3) Worker Threads (node) => "const { Worker } = require('worker_threads')"
      //    To trudniejsze do wykrycia wprost, bo AST zobaczy to w Import?
      //    W stylu require('worker_threads'), new Worker(...) => Ale to i tak new Worker.
      //    Ewentualnie sprawdzamy literal: 'worker_threads'. 
      // (Możemy też dodać Regex w stringach, ale zostawmy to proste)

      // rekurencja
      for (let key in node) {
        if (node.hasOwnProperty(key)) {
          traverse(node[key]);
        }
      }
    }

    traverse(ast);

    // Usuwamy duplikaty linii, sortujemy
    linesDetected = [...new Set(linesDetected)].sort((a,b) => a - b);

  } catch(e) {
    // nic
  }

  // Zwrot w JSON
  process.stdout.write(JSON.stringify(linesDetected));
});
"""

def detect_threads_js(js_code: str) -> str:
    """
    Wykrywa "wielowątkowość" w JS przez Node.js + esprima:
    - new Worker(...)
    - new SharedWorker(...)
    - importScripts(...)

    Zwraca oryginalny kod z dopisanym "//THREADING_DETECTED"
    na końcu linii, gdzie to wystąpiło.

    :param js_code: oryginalny kod JS
    :return: kod JS z dopisanymi komentarzami
    """
    # 1) Tworzymy plik tymczasowy node_detect_threads.js
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as f:
        node_file_path = f.name
        f.write(NODE_DETECT_THREADS)

    try:
        # 2) Uruchamiamy node, dajemy kod JS na stdin
        result = subprocess.run(
            ['node', node_file_path],
            input=js_code,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            # Błąd node / esprima?
            # Zwracamy oryginał lub
            # print("Node błąd:", result.stderr)
            return js_code

        # 3) Odbieramy listę linii w JSON
        try:
            lines = json.loads(result.stdout)
        except json.JSONDecodeError:
            lines = []

        if not lines:
            return js_code  # Nie znaleziono nic

        # 4) Dopisujemy "//THREADING_DETECTED" w tych liniach
        lines_js = js_code.splitlines(keepends=True)
        for lineno in lines:
            idx = lineno - 1  # 1-based -> 0-based
            if idx < len(lines_js):
                if "//THREADING_DETECTED" not in lines_js[idx]:
                    stripped = lines_js[idx].rstrip("\n")
                    lines_js[idx] = stripped + "  //THREADING_DETECTED\n"

        return "".join(lines_js)

    finally:
        # Sprzątamy plik tymczasowy
        if os.path.exists(node_file_path):
            os.remove(node_file_path)


def _test():
    """
    Test lokalny. Uruchom: python detect_threads_js.py
    """
    example_js = r"""
// new Worker
var w = new Worker("worker.js");
function f1() {
  new SharedWorker("shared.js");
}
importScripts("script1.js", "script2.js");
console.log("Hello Worker Threads"); // to nie wywołuje nic
"""

    print("=== Oryginalny kod JS ===")
    print(example_js)

    final = detect_threads_js(example_js)

    print("\n=== Kod po detect_threads_js() ===")
    print(final)


if __name__ == "__main__":
    _test()