#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remove_dead_code_js.py

Poprawiona wersja:
- Usuwa nieużywane zmienne,
- Usuwa puste funkcje,
- Usuwa puste bloki warunkowe i pętle.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import subprocess
import tempfile
import os


NODE_REMOVE_DEAD_CODE = r"""
const esprima = require('esprima');
const escodegen = require('escodegen');

process.stdin.setEncoding('utf8');

let code = '';
process.stdin.on('data', chunk => {
  code += chunk;
});

process.stdin.on('end', () => {
  try {
    const ast = esprima.parseScript(code, { loc: true });

    let declaredVars = new Set();
    let usedVars = new Set();

    // 1) Zbieranie wszystkich deklaracji zmiennych i funkcji
    function collectDeclaredVariables(node) {
      if (!node || typeof node !== 'object') return;

      if (node.type === 'VariableDeclarator') {
        declaredVars.add(node.id.name);
      }

      if (node.type === 'FunctionDeclaration') {
        declaredVars.add(node.id.name);
      }

      for (let key in node) {
        const child = node[key];
        if (Array.isArray(child)) {
          child.forEach(collectDeclaredVariables);
        } else if (typeof child === 'object') {
          collectDeclaredVariables(child);
        }
      }
    }

    // 2) Zbieranie używanych zmiennych i funkcji
    function collectUsedVariables(node) {
      if (!node || typeof node !== 'object') return;

      if (node.type === 'Identifier') {
        usedVars.add(node.name);
      }

      for (let key in node) {
        const child = node[key];
        if (Array.isArray(child)) {
          child.forEach(collectUsedVariables);
        } else if (typeof child === 'object') {
          collectUsedVariables(child);
        }
      }
    }

    // 3) Usuwanie martwego kodu
    function removeDeadCode(node) {
      if (!node || typeof node !== 'object') return null;

      // Usuwanie pustych funkcji
      if (node.type === 'FunctionDeclaration' && (!usedVars.has(node.id.name) || node.body.body.length === 0)) {
        return null;
      }

      // Usuwanie nieużywanych zmiennych
      if (node.type === 'VariableDeclaration') {
        node.declarations = node.declarations.filter(decl => usedVars.has(decl.id.name));
        if (node.declarations.length === 0) {
          return null;
        }
      }

      // Usuwanie pustych bloków if/for/while
      if ((node.type === 'IfStatement' || node.type === 'ForStatement' || node.type === 'WhileStatement') &&
          (!node.consequent || (node.consequent.body && node.consequent.body.length === 0))) {
        return null;
      }

      for (let key in node) {
        if (Array.isArray(node[key])) {
          node[key] = node[key].map(removeDeadCode).filter(Boolean);
        } else if (typeof node[key] === 'object') {
          node[key] = removeDeadCode(node[key]);
        }
      }

      return node;
    }

    // 1) Zbieranie deklaracji i użyć zmiennych
    collectDeclaredVariables(ast);
    collectUsedVariables(ast);

    // 2) Usuwanie nieużywanych zmiennych i pustych bloków
    const cleanedAst = removeDeadCode(ast);

    // 3) Generowanie kodu po optymalizacji
    const optimizedCode = escodegen.generate(cleanedAst, { format: { indent: { style: '  ' } } });
    process.stdout.write(optimizedCode);

  } catch (error) {
    process.stdout.write(code);
  }
});
"""


def remove_dead_code_js(js_code: str) -> str:
    """
    Usuwa martwy kod z JavaScript:
    - nieużywane zmienne,
    - puste funkcje,
    - puste bloki warunkowe/pętle.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as f:
        node_file_path = f.name
        f.write(NODE_REMOVE_DEAD_CODE)

    try:
        result = subprocess.run(
            ['node', node_file_path],
            input=js_code,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            return js_code

        return result.stdout

    finally:
        if os.path.exists(node_file_path):
            os.remove(node_file_path)


def _test():
    """
    Test skryptu.
    """
    example_js = r'''
function usedFunction() {
    console.log("Używana funkcja");
}

function emptyFunction() {}

let x = 10;
let y = 20;

if (true) {}

for (let i = 0; i < 5; i++) {}

usedFunction();
'''

    print("=== Oryginalny kod JS ===")
    print(example_js)

    optimized_code = remove_dead_code_js(example_js)

    print("\n=== Kod po deobfuskacji ===")
    print(optimized_code)


if __name__ == "__main__":
    _test()