#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
detect_threads.py

Wykrywa użycie wielowątkowości i współbieżności w kodzie Python.
Dodaje raport podsumowujący wykryte przypadki.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-10
"""

import ast

class _ThreadingDetector(ast.NodeVisitor):
    """
    Wyszukuje importy i wywołania związane z threading, multiprocessing, asyncio.
    """
    def __init__(self):
        super().__init__()
        self.lines_to_mark = set()
        self.detected_calls = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ("threading", "multiprocessing", "concurrent.futures", "asyncio"):
                self.lines_to_mark.add(node.lineno)
                self.detected_calls.append(f"Import: {alias.name} (linia {node.lineno})")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in ("threading", "multiprocessing", "concurrent.futures", "asyncio"):
            self.lines_to_mark.add(node.lineno)
            self.detected_calls.append(f"Import: {node.module} (linia {node.lineno})")
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            base_name = func.value.id
            attr_name = func.attr
            if base_name in ("threading", "multiprocessing", "asyncio"):
                self.lines_to_mark.add(node.lineno)
                self.detected_calls.append(f"Wywołanie: {base_name}.{attr_name} (linia {node.lineno})")
            if base_name == "concurrent" and attr_name == "ThreadPoolExecutor":
                self.lines_to_mark.add(node.lineno)
                self.detected_calls.append(f"Wywołanie: concurrent.futures.ThreadPoolExecutor (linia {node.lineno})")
        elif isinstance(func, ast.Name):
            if func.id in ("ThreadPoolExecutor", "Pool", "run"):
                self.lines_to_mark.add(node.lineno)
                self.detected_calls.append(f"Wywołanie: {func.id} (linia {node.lineno})")
        self.generic_visit(node)

def detect_threads_ast(script_content: str) -> str:
    """
    Wykrywa użycie wielowątkowości i współbieżności oraz generuje raport.
    """
    try:
        tree = ast.parse(script_content)
    except SyntaxError:
        return script_content

    detector = _ThreadingDetector()
    detector.visit(tree)

    lines = script_content.splitlines(keepends=True)
    for lineno in detector.lines_to_mark:
        idx = lineno - 1
        if idx < len(lines) and "#THREADING_DETECTED" not in lines[idx]:
            lines[idx] = lines[idx].rstrip("\n") + "  #THREADING_DETECTED\n"

    # Tworzenie raportu
    report = "\n\n# === RAPORT O WYKRYTYCH WĄTKACH/WSPÓŁBIEŻNOŚCI ===\n"
    report += f"# Łączna liczba wykrytych przypadków: {len(detector.lines_to_mark)}\n"
    for call in detector.detected_calls:
        report += f"# - {call}\n"

    return "".join(lines) + report

def _test():
    """
    Test wykrywania wielowątkowości.
    """
    example_code = r'''
import threading
import os
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

def worker():
    print("Working...")

p = Process(target=worker)
p.start()

with ThreadPoolExecutor(max_workers=5) as executor:
    pass

import asyncio

threading.Thread(target=worker).start()

class MyPool:
    def __init__(self):
        pass

Pool()
'''

    print("=== Oryginalny kod Pythona ===")
    print(example_code)

    ast_result = detect_threads_ast(example_code)

    print("\n=== Kod po detect_threads_ast() ===")
    print(ast_result)

if __name__ == "__main__":
    _test()