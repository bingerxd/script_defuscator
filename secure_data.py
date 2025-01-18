import os
import secrets
import string
import subprocess

def zip_file_with_password(file_path):
    # Sprawdzanie, czy plik istnieje
    if not os.path.isfile(file_path):
        print("Podana ścieżka nie prowadzi do pliku.")
        return
    
    # Generowanie 13-znakowego hasła
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(13))
    
    # Nazwa ZIP-a taka jak plik, w tej samej lokalizacji
    file_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    zip_name = os.path.join(dir_name, os.path.splitext(file_name)[0] + '.zip')
    
    # Tworzenie ZIP-a z hasłem za pomocą polecenia systemowego (Linux), bez ścieżki
    command = [
        'zip', '-j', '-P', password, zip_name, file_path
    ]
    subprocess.run(command, check=True)
    
    # Usunięcie oryginalnego pliku
    os.remove(file_path)
    
    print(f"Plik został spakowany do: {zip_name}")
    print(f"Hasło do archiwum: {password}")

# Instrukcja dla użytkownika
print("Ten program spakuje wybrany plik do archiwum ZIP z losowym hasłem.")
print("Po spakowaniu oryginalny plik zostanie usunięty, a w jego miejscu pojawi się archiwum ZIP.")
print("Podaj pełną ścieżkę do pliku, który chcesz spakować.")

# Przykład użycia
file_path = input("Podaj ścieżkę do pliku: ")
zip_file_with_password(file_path)
