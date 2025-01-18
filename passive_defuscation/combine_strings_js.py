#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
concat_strings_js.py

Funkcja:
    transform_concatenate_strings_js(script_content: str) -> str

Działanie:
    - Parsuje kod JavaScript do AST (Node.js + Esprima).
    - Śledzi przypisania zmiennych.
    - Łączy literalne stringi oraz zmienne zawierające stringi.
    - Rekurencyjnie rozwiązuje zmienne w zagnieżdżonych konkatenacjach.
    - Na końcu zwraca zoptymalizowany kod JS.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import subprocess
import tempfile
import os
import json

declare_js_concat_analyzer = r"""
const esprima = require('esprima');
const escodegen = require('escodegen');

process.stdin.setEncoding('utf8');

let code = '';
process.stdin.on('data', (chunk) => {
  code += chunk;
});

process.stdin.on('end', () => {
  try {
    const ast = esprima.parseScript(code, { loc: true });
    let stringVars = {};

    function traverse(node) {
      if (!node || typeof node !== 'object') return;
      
      if (node.type === 'VariableDeclarator' && node.init) {
        const resolved = resolveConcat(node.init);
        if (resolved !== null) {
          stringVars[node.id.name] = resolved;
          node.init = { type: 'Literal', value: resolved };
        }
      }
      
      if (node.type === 'BinaryExpression' && node.operator === '+') {
        const resolved = resolveConcat(node);
        if (resolved !== null) {
          node.type = 'Literal';
          node.value = resolved;
          delete node.left;
          delete node.right;
          delete node.operator;
        }
      }
      
      for (let key in node) {
        if (Array.isArray(node[key])) {
          node[key].forEach(child => traverse(child));
        } else if (typeof node[key] === 'object') {
          traverse(node[key]);
        }
      }
    }

    function resolveConcat(node) {
      if (node.type === 'BinaryExpression' && node.operator === '+') {
        const left = resolveConcat(node.left);
        const right = resolveConcat(node.right);
        if (typeof left === 'string' && typeof right === 'string') {
          return left + right;
        }
        return null;
      }
      return resolveValue(node);
    }

    function resolveValue(node) {
      if (node.type === 'Literal' && typeof node.value === 'string') {
        return node.value;
      } else if (node.type === 'Identifier' && stringVars[node.name]) {
        return stringVars[node.name];
      }
      return null;
    }

    traverse(ast);
    const optimizedCode = escodegen.generate(ast);
    process.stdout.write(optimizedCode);
  } catch (err) {
    process.stdout.write(code);
  }
});
"""

def transform_concatenate_strings_js(script_content: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as js_file:
        js_file.write(declare_js_concat_analyzer)
        js_path = js_file.name

    try:
        result = subprocess.run(
            ['node', js_path],
            input=script_content,
            text=True,
            capture_output=True
        )
        
        if result.returncode != 0 or not result.stdout:
            return script_content

        optimized_code = result.stdout
        return optimized_code

    finally:
        if os.path.exists(js_path):
            os.remove(js_path)

def _test():
    js_code = r'''
function greet() {
    let hello = "x";
    let world = "World";
    let message = hello + ", " + world + "!";
    let complex = "Start" + hello + "End";
    let x = "Start" + hello + world;
    let y = "Z" + x + x;
    console.log(message);
    console.log(complex);
}
'''

    print("=== Oryginalny kod JS ===")
    print(js_code)

    optimized_js = transform_concatenate_strings_js(js_code)

    print("\n=== Kod po optymalizacji ===")
    print(optimized_js)

if __name__ == "__main__":
    _test()
