#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
detect_and_optimize_conditions.py

Jedna funkcja:
    - Wykrywa nadmierne zagnieżdżenia,
    - Wykrywa inline logic,
    - Upraszcza warunki True/False,
    - Generuje raport.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import ast
import sys

# Raportowanie wykrytych elementów
report_data = {
    "deep_nesting": 0,
    "inline_logic": 0,
    "always_true_false": 0
}

class _DepthVisitor(ast.NodeVisitor):
    def __init__(self, max_depth=3):
        super().__init__()
        self.max_depth = max_depth
        self.lines_to_mark = set()
        self.current_depth = 0

    def _increase_depth(self, node):
        self.current_depth += 1
        if self.current_depth > self.max_depth and hasattr(node, 'lineno'):
            self.lines_to_mark.add(node.lineno)
            report_data["deep_nesting"] += 1
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_If(self, node):
        self._increase_depth(node)

    def visit_For(self, node):
        self._increase_depth(node)

    def visit_While(self, node):
        self._increase_depth(node)


class _InlineLogicVisitor(ast.NodeVisitor):
    def __init__(self, max_ops=4):
        super().__init__()
        self.max_ops = max_ops
        self.lines_to_mark = set()

    def _count_operators(self, node) -> int:
        count = 0
        if isinstance(node, ast.BinOp):
            count += 1 + self._count_operators(node.left) + self._count_operators(node.right)
        elif isinstance(node, ast.BoolOp):
            count += len(node.values) - 1
            for val in node.values:
                count += self._count_operators(val)
        elif isinstance(node, ast.Compare):
            count += len(node.ops)
        return count

    def visit_If(self, node):
        ops_count = self._count_operators(node.test)
        if ops_count >= self.max_ops and hasattr(node, 'lineno'):
            self.lines_to_mark.add(node.lineno)
            report_data["inline_logic"] += 1
        self.generic_visit(node)


class _SimplifyConditionsTransformer(ast.NodeTransformer):
    def visit_If(self, node):
        self.generic_visit(node)
        if self._is_always_true(node.test):
            report_data["always_true_false"] += 1
            return node.body
        elif self._is_always_false(node.test):
            report_data["always_true_false"] += 1
            return node.orelse
        return node

    def _is_always_true(self, node):
        try:
            return eval(compile(ast.Expression(body=node), filename="", mode="eval")) is True
        except:
            return False

    def _is_always_false(self, node):
        try:
            return eval(compile(ast.Expression(body=node), filename="", mode="eval")) is False
        except:
            return False

def generate_report():
    report = "\n\n# === RAPORT O WYKRYTYCH WARUNKACH ===\n"
    report += f"# Nadmierne zagnieżdżenia: {report_data['deep_nesting']}\n"
    report += f"# Złożone warunki logiczne: {report_data['inline_logic']}\n"
    report += f"# Upraszczalne warunki True/False: {report_data['always_true_false']}\n"
    return report

def optimize_conditions_with_report(script_content: str, max_depth=2, max_ops=4) -> str:
    global report_data
    report_data = {
        "deep_nesting": 0,
        "inline_logic": 0,
        "always_true_false": 0
    }

    try:
        tree = ast.parse(script_content)
    except SyntaxError:
        return script_content

    depth_visitor = _DepthVisitor(max_depth)
    depth_visitor.visit(tree)
    lines = script_content.splitlines(keepends=True)
    for lineno in depth_visitor.lines_to_mark:
        idx = lineno - 1
        if idx < len(lines):
            lines[idx] = lines[idx].rstrip("\n") + "  # DEEP_NESTING_DETECTED\n"

    inline_visitor = _InlineLogicVisitor(max_ops)
    inline_visitor.visit(tree)
    for lineno in inline_visitor.lines_to_mark:
        idx = lineno - 1
        if idx < len(lines):
            lines[idx] = lines[idx].rstrip("\n") + "  # INLINE_LOGIC_DETECTED_SUGGEST_SPLIT\n"

    transformer = _SimplifyConditionsTransformer()
    optimized_tree = transformer.visit(tree)
    ast.fix_missing_locations(optimized_tree)
    optimized_code = ast.unparse(optimized_tree) if sys.version_info >= (3, 9) else script_content

    optimized_code += generate_report()
    return optimized_code

def _test():
    example_code = r'''
def example():
    if (33-1 == 32):
        if True:
            if (2 == 2):
                print("To zawsze się wykona")

    if (True) and (1 == 1) and (2 == 2):
        print("Redundantne warunki")

    if (False) or (2 != 2):
        print("Nigdy się nie wykona")
'''

    print("=== Oryginalny kod ===")
    print(example_code)

    final_code = optimize_conditions_with_report(example_code)

    print("\n=== Kod po optymalizacji ===")
    print(final_code)

if __name__ == "__main__":
    _test()
