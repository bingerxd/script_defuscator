# Passive Deobfuscation Pipeline

## 📖 Opis Projektu

Projekt **Passive Deobfuscation Pipeline** to zaawansowane narzędzie do automatycznej deobfuskacji i analizy kodu w językach Python i JavaScript.  
Głównym celem jest wykrywanie oraz neutralizacja złośliwych lub trudnych do analizy fragmentów kodu poprzez:

- Usuwanie komentarzy i docstringów  
- Dekodowanie Base64  
- Usuwanie martwego kodu  
- Zamianę operacji bitowych  
- Zmianę długich, losowych nazw zmiennych  
- Wykrywanie i oznaczanie zagnieżdżonych warunków  
- Wykrywanie i zabezpieczanie połączeń zewnętrznych (URL/IP)  
- Usuwanie niebezpiecznych funkcji (eval, exec, nieskończone pętle)  

---

## 📁 Instalacja

Sklonuj repozytorium:

```bash
git clone https://github.com/TwojNick/passive_defuscation.git
cd passive_defuscation
```

Zainstaluj wymagane biblioteki Python:
```bash
pip install -r requirements.txt
```
Zainstaluj pakiety Node.js do analizy JavaScript:
```bash
npm install -g esprima escodegen
```
