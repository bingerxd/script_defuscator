#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main_pipeline.py

Skrypt przeprowadza automatycznie:
- Usunięcie komentarzy + docstringów,
- Przywrócenie formatowania (Python/JS),
- Dekodowanie ciągów Base64,
- Usunięcie martwego kodu,
- Zamiana operacji bitowych na mnożenie/dzielenie,
- Rename zmiennych,
- Wykrywanie i oznaczanie zagnieżdżonych warunków,
- Wykrywanie inline logic,
- Upraszczanie warunków zawsze prawdziwych/fałszywych,
- Wykrywanie wątków,
- Optymalizacja warunków (dla JS),
- Łączenie konkatenacji stringów.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-11
"""

import os
import sys

# Moduły do usuwania komentarzy
import remove_comments_and_docstrings  # Python
import remove_js_comments              # JavaScript

# Moduły do przywracania formatowania
import restore_formatting              # Python
import restore_formatting_js           # JavaScript

# Moduły do dekodowania Base64
import decode_encoded_strings          # Python
import decode_encoded_strings_js       # JavaScript

# Moduły do usuwania martwego kodu
import remove_dead_code                # Python
import remove_dead_code_js             # JavaScript

# Moduły do zamiany operacji bitowych
import replace_bitwise_operations      # Python
import replace_bitwise_operations_js   # JavaScript

# Moduły do rename zmiennych
import rename_variables                # Python
import rename_variables_js             # JavaScript

# Moduły do wykrywania wątków
import detect_threads                  # Python
import detect_threads_js               # JavaScript

# Moduły do optymalizacji warunków
import detect_and_optimize_conditions      # Python
import detect_and_optimize_conditions_js  # JavaScript

# Moduły do łączenia konkatenacji stringów
import combine_strings                 # Python
import combine_strings_js             # JavaScript

# Moduły do usuwania niebezpiecznych funkcji
import remove_dangerous_code          # Python
import remove_dangerous_code_js       # JavaScript

import detect_external_connections      # Python
import detect_external_connections_js   # JavaScript

def main():

    output_dir = "/home/kali/Desktop/projekt_IS/defuscated_scripts"
    os.makedirs(output_dir, exist_ok=True)

    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Pipeline dla kodu Python")
        print("2. Pipeline dla kodu JavaScript")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ").strip()
        if choice == "0":
            print("Koniec programu.")
            sys.exit(0)

        elif choice == "1":
            # Pipeline dla Pythona
            file_path = input("Podaj ścieżkę do pliku .py: ").strip()
            if not os.path.isfile(file_path):
                print(f"Błąd: Plik '{file_path}' nie istnieje.")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_code = f.read()

                # 1) Usunięcie komentarzy i docstringów
                no_comments = remove_comments_and_docstrings.remove_comments_and_docstrings(original_code)

                # 2) Przywrócenie formatowania
                #restored_format = restore_formatting.restore_python_formatting(no_comments)

                # 3) Dekodowanie ciągów Base64
                decoded_base64 = decode_encoded_strings.decode_encoded_strings(no_comments)

                # 4) Usunięcie martwego kodu
                no_dead_code = remove_dead_code.remove_dead_code(decoded_base64)

                # 5) Zamiana operacji bitowych
                replaced_bitwise = replace_bitwise_operations.replace_bitwise_operations_py(no_dead_code)

                # 6) Rename zmiennych
                renamed_variables = rename_variables.rename_long_random_names(replaced_bitwise)

                # 7-9) Optymalizacja warunków + raport
                optimized_conditions_with_report = detect_and_optimize_conditions.optimize_conditions_with_report(renamed_variables)

                # 10) Łączenie konkatenacji stringów
                concatenated_strings = combine_strings.transform_concatenate_strings(optimized_conditions_with_report)

                # 11) Wykrywanie wątków
                thread_detector = detect_threads.detect_threads_ast(concatenated_strings)

                removed_dangerous = remove_dangerous_code.remove_dangerous_code_python(thread_detector)

                # 11) Wykrywanie i zabezpieczanie połączeń zewnętrznych (Python)
                final_code = detect_external_connections.detect_external_connections_python(removed_dangerous)
                python_report = detect_and_optimize_conditions.generate_report()
                python_report2 = remove_comments_and_docstrings.generate_report()
                python_report3 = remove_dead_code.generate_dead_code_report()
                python_report4 = rename_variables.generate_rename_report()
                python_report5 = replace_bitwise_operations.generate_bitwise_report()
                python_report6 = restore_formatting.generate_formatting_report()
                final_code += python_report + "\n\n" +python_report2 + python_report3 + python_report4 + python_report5 + python_report6
                # Zapis do pliku .py z przyrostkiem _final
                base = os.path.basename(file_path)
                output_file = os.path.join(output_dir, base.replace(".py", "_final.py"))

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(final_code)

                print(f"Zapisano przetworzony plik w: {output_file}")

            except Exception as e:
                print(f"Wystąpił błąd w pipeline (Python): {e}")

        elif choice == "2":
            # Pipeline dla JavaScript
            file_path = input("Podaj ścieżkę do pliku .js: ").strip()
            if not os.path.isfile(file_path):
                print(f"Błąd: Plik '{file_path}' nie istnieje.")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    original_code = f.read()

                # 1) Usunięcie komentarzy w JS
                no_comments_js = remove_js_comments.remove_comments_js(original_code)

                # 2) Przywrócenie formatowania JS
                restored_format_js = restore_formatting_js.restore_js_formatting(no_comments_js)

                # 3) Dekodowanie Base64 w JS
                decoded_base64_js = decode_encoded_strings_js.decode_encoded_strings_js(restored_format_js)

                # 4) Usunięcie martwego kodu w JS
                no_dead_code_js = remove_dead_code_js.remove_dead_code_js(decoded_base64_js)

                # 5) Zamiana operacji bitowych w JS
                replaced_bitwise_js = replace_bitwise_operations_js.replace_bitwise_operations_js(no_dead_code_js)

                # 6) Rename zmiennych w JS
                renamed_code_js = rename_variables_js.rename_long_random_names_js(replaced_bitwise_js)

                # 7) Wykrycie wątków w JS
                threads_detected_js = detect_threads_js.detect_threads_js(renamed_code_js)

                # 8) Optymalizacja warunków w JS
                optimized_js_code = detect_and_optimize_conditions_js.detect_and_optimize_conditions_js(threads_detected_js)

                # 9) Łączenie konkatenacji stringów w JS
                string_combine = combine_strings_js.transform_concatenate_strings_js(optimized_js_code)

                removed_dangerous_js = remove_dangerous_code_js.remove_dangerous_code_js(string_combine)

                # 11) Wykrywanie i zabezpieczanie połączeń zewnętrznych (JavaScript)
                concatenated_js_code = detect_external_connections_js.detect_external_connections_js(removed_dangerous_js)

                # Zapis do pliku .js z przyrostkiem _final
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(concatenated_js_code)

                print(f"Zapisano przetworzony plik w: {output_file}")

            except Exception as e:
                print(f"Wystąpił błąd w pipeline (JavaScript): {e}")

        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")


if __name__ == "__main__":
    main()