Passive Deobfuscation Pipeline

📖 Opis Projektu

Projekt Passive Deobfuscation Pipeline to zaawansowane narzędzie do automatycznej deobfuskacji i analizy kodu w językach Python i JavaScript. Głównym celem jest wykrywanie oraz neutralizacja złośliwych lub trudnych do analizy fragmentów kodu poprzez:

Usuwanie komentarzy i docstringów

Dekodowanie Base64

Usuwanie martwego kodu

Zamianę operacji bitowych

Zmianę długich, losowych nazw zmiennych

Wykrywanie i oznaczanie zagnieżdżonych warunków

Wykrywanie i zabezpieczanie połączeń zewnętrznych (URL/IP)

Usuwanie niebezpiecznych funkcji (eval, exec, nieskończone pętle)

📁 Instalacja

Sklonuj repozytorium:

https://github.com/TwojNick/passive_defuscation.git
cd passive_defuscation

Zainstaluj wymagane biblioteki Python:

pip install -r requirements.txt

Zainstaluj pakiety Node.js do analizy JavaScript:

npm install -g esprima escodegen

🔄 Użycie

Uruchom główny skrypt:

python main.py

Wybierz:

1 - Pipeline dla kodu Python

2 - Pipeline dla kodu JavaScript

Podaj ścieżkę do pliku.

Wynik zostanie zapisany w folderze defuscated_scripts.

📊 Przykładowy Raport

# === RAPORT O WYKRYTYCH WARUNKACH ===
# Nadmierne zagnieżdżenia: 2
# Złożone warunki logiczne: 1
# Upraszczalne warunki True/False: 3

# === RAPORT O WYKRYTYCH POŁĄCZENIACH ===
# URL: 2
# IP: 1
# Dynamiczne połączenia: 0

📊 Użyte Biblioteki

Python

ast — Analiza i manipulacja drzewem składniowym.

re — Wyszukiwanie i zamiana wzorców tekstowych (Regex).

base64 — Dekodowanie ciągów Base64.

tokenize — Usuwanie komentarzy i docstringów.

os, sys — Operacje na plikach i systemie.

JavaScript (w Pythonie)

Esprima — Parsowanie kodu JavaScript.

Escodegen — Generowanie kodu JavaScript.

👥 Autor

Patryk Zabawa Data: 2025-01-12
