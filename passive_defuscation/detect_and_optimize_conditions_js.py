#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
detect_and_optimize_conditions_js.py

Optymalizacja kodu JavaScript:
1) Usuwa warunki zawsze prawdziwe/fałszywe.
2) Wykrywa głębokie zagnieżdżenie.
3) Wykrywa złożone warunki logiczne.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import subprocess
import tempfile
import os
import json
import re

NODE_DETECT_CONDITIONS = r"""
const esprima = require('esprima');

process.stdin.setEncoding('utf8');

let code = '';
process.stdin.on('data', (chunk) => {
  code += chunk;
});
process.stdin.on('end', () => {
  let linesDetected = { nested: [], inlineLogic: [], alwaysTrue: [], alwaysFalse: [] };

  try {
    const ast = esprima.parseScript(code, { loc: true });

    function traverse(node, depth = 0, maxDepth = 3, maxOps = 4) {
      if (!node || typeof node !== 'object') return;

      // 1) Głębokie zagnieżdżenia
      if (depth > maxDepth && node.loc && ['IfStatement', 'ForStatement', 'WhileStatement'].includes(node.type)) {
        linesDetected.nested.push(node.loc.start.line);
      }

      // 2) Inline logic (dużo operatorów)
      if (node.type === 'IfStatement' && node.test) {
        const opsCount = countOperators(node.test);
        if (opsCount > maxOps && node.loc) {
          linesDetected.inlineLogic.push(node.loc.start.line);
        }
      }

      // 3) Always True/False (static evaluation)
      if (node.type === 'IfStatement' && node.test) {
        const evalResult = evaluateExpression(node.test);
        if (evalResult === true) {
          linesDetected.alwaysTrue.push(node.loc.start.line);
        } else if (evalResult === false) {
          linesDetected.alwaysFalse.push(node.loc.start.line);
        }
      }

      for (let key in node) {
        const child = node[key];
        if (Array.isArray(child)) {
          for (const subNode of child) traverse(subNode, depth + 1, maxDepth, maxOps);
        } else if (typeof child === 'object') {
          traverse(child, depth + 1, maxDepth, maxOps);
        }
      }
    }

    function countOperators(node) {
      if (!node || typeof node !== 'object') return 0;
      let count = 0;
      if (['LogicalExpression', 'BinaryExpression'].includes(node.type)) {
        count += 1 + countOperators(node.left) + countOperators(node.right);
      }
      return count;
    }

    function evaluateExpression(node) {
      try {
        if (node.type === 'Literal') return node.value;
        if (node.type === 'BinaryExpression') {
          const left = evaluateExpression(node.left);
          const right = evaluateExpression(node.right);
          switch (node.operator) {
            case '==': return left == right;
            case '===': return left === right;
            case '!=': return left != right;
            case '!==': return left !== right;
            case '<': return left < right;
            case '<=': return left <= right;
            case '>': return left > right;
            case '>=': return left >= right;
            case '+': return left + right;
            case '-': return left - right;
            case '*': return left * right;
            case '/': return left / right;
            case '%': return left % right;
            default: return undefined;
          }
        }
        return undefined;
      } catch (e) {
        return undefined;
      }
    }

    traverse(ast);

    for (let key in linesDetected) {
      linesDetected[key] = [...new Set(linesDetected[key])].sort((a, b) => a - b);
    }

  } catch (e) {
    // ignorujemy błędy
  }

  process.stdout.write(JSON.stringify(linesDetected));
});
"""

def detect_and_optimize_conditions_js(js_code: str) -> str:
    """
    Wykrywa i optymalizuje warunki w kodzie JS:
    - Usuwa zawsze prawdziwe/fałszywe warunki,
    - Oznacza zagnieżdżenia i inline logic.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.js') as f:
        node_file_path = f.name
        f.write(NODE_DETECT_CONDITIONS)

    try:
        result = subprocess.run(
            ['node', node_file_path],
            input=js_code,
            text=True,
            capture_output=True,
        )

        if result.returncode != 0:
            return js_code  # W razie błędu zwracamy oryginał

        try:
            detections = json.loads(result.stdout)
        except json.JSONDecodeError:
            detections = {}

        lines_js = js_code.splitlines(keepends=True)

        for lineno in detections.get('alwaysFalse', []):
            idx = lineno - 1
            brace_count = 0
            while idx < len(lines_js):
                line = lines_js[idx]
                brace_count += line.count('{') - line.count('}')
                lines_js[idx] = ""
                if brace_count <= 0:
                    break
                idx += 1

        for lineno in detections.get('alwaysTrue', []):
            idx = lineno - 1
            if idx < len(lines_js):
                lines_js[idx] = re.sub(r'if\s*\(.*?\)\s*{', '{', lines_js[idx])

        return "".join(lines_js)

    finally:
        if os.path.exists(node_file_path):
            os.remove(node_file_path)

def _test():
    example_js = r"""
function example() {
    if (31 - 1 == 30) {
        console.log("Zawsze się wykona");
    }

    if (2 != 2) {
        console.log("Nigdy się nie wykona");
    }

    if ((3 * 2) == 6) {
        console.log("Zawsze prawda");
    }
}
"""

    print("=== Oryginalny kod JS ===")
    print(example_js)

    final = detect_and_optimize_conditions_js(example_js)

    print("\n=== Kod po optymalizacji ===")
    print(final)

if __name__ == "__main__":
    _test()
