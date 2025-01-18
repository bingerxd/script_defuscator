#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import tokenize
import textwrap

# Globalne zmienne do zliczania
removed_comments_count = 0
removed_docstrings_count = 0

def remove_comments_and_docstrings(source_code: str) -> str:
    global removed_comments_count, removed_docstrings_count
    removed_comments_count = 0
    removed_docstrings_count = 0

    out_tokens = []
    reader = io.StringIO(source_code)
    tokens_gen = tokenize.generate_tokens(reader.readline)

    for tok in tokens_gen:
        token_type = tok.type
        token_string = tok.string

        # 1. Pomijamy komentarze (# ...).
        if token_type == tokenize.COMMENT:
            removed_comments_count += 1
            continue

        # 2. Pomijamy docstringi ("""...""" lub '''...''').
        if token_type == tokenize.STRING:
            if token_string.startswith('"""') or token_string.startswith("'''"):
                removed_docstrings_count += 1
                continue

        out_tokens.append(tok)

    # Odtwarzamy kod i usuwamy zbędne wcięcia
    cleaned_code = tokenize.untokenize(out_tokens)
    cleaned_code = textwrap.dedent(cleaned_code).strip()

    return cleaned_code

def generate_report() -> str:
    """
    Generuje czytelny raport o usuniętych komentarzach i docstringach.
    """
    report = "# === RAPORT O USUNIĘTYCH ELEMENTACH ===\n"
    report += f"# Usunięte komentarze: {removed_comments_count}\n"
    report += f"# Usunięte docstringi: {removed_docstrings_count}\n"
    return report

def _test():
    """
    Test funkcji remove_comments_and_docstrings.
    """
    example_python_code = (
        """
# Komentarz na początku
def funkcja():
    \"\"\"Docstring funkcji\"\"\"
    x = 10  # Komentarz w tej samej linii
    print("Hello")  # Następny komentarz

    # Ten komentarz jest poza definicją funkcji, ale też powinien zniknąć.

class Klasa:
    \"\"\"Docstring klasy\"\"\"
    pass
"""
    )

    print("=== Oryginalny kod ===")
    print(example_python_code)

    cleaned = remove_comments_and_docstrings(example_python_code)

    print("\n=== Po usunięciu komentarzy i docstringów ===")
    print(cleaned)

    report = generate_report()
    print("\n=== Raport ===")
    print(report)

if __name__ == "__main__":
    _test()
