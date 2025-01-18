import os
import requests
import json

# Stałe wartości: klucz API i ścieżka do katalogu
API_KEY = input("Wprowadz swoje VirusTotal API-key: ")
DEFAULT_DIRECTORY = "/home/kali/Desktop/projekt_IS/malware_samples"
REPORT_DIRECTORY = "/home/kali/Desktop/projekt_IS/reports"  # Katalog do zapisu raportów

# Funkcja pobiera pliki z określonego katalogu
def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        scripts = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        if not scripts:
            print("Brak skryptów w podanym katalogu.")
            return []
        print("Znalezione pliki w katalogu:")
        for i, script in enumerate(scripts, start=1):
            print(f"{i}. {script}")
        return scripts
    except Exception as e:
        print(f"Błąd podczas odczytu katalogu: {e}")
        return []

# Funkcja pozwala użytkownikowi wybrać pliki z listy
def select_files_from_list(files):
    selected_files = []
    print("Podaj numery plików, które chcesz przesłać (oddzielone przecinkami, np. 1,3,5):")
    selection = input("Wybór: ")
    try:
        indices = [int(idx) - 1 for idx in selection.split(",")]
        for idx in indices:
            if 0 <= idx < len(files):
                selected_files.append(files[idx])
            else:
                print(f"Niepoprawny numer: {idx + 1}")
    except ValueError:
        print("Nieprawidłowy format wejściowy. Używaj liczb oddzielonych przecinkami.")
    return selected_files

# Funkcja pobiera wyniki analizy z VirusTotal
def get_analysis_results(api_key, file_id):
    url = f"https://www.virustotal.com/api/v3/files/{file_id}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Zwraca odpowiedź JSON
        else:
            print(f"Błąd pobierania wyników: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania wyników: {e}")
        return None

# Funkcja pobiera szczegóły analizy zachowań
def get_behaviour_summary(api_key, file_id):
    url = f"https://www.virustotal.com/api/v3/files/{file_id}/behaviour_summary"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Zwraca odpowiedź JSON
        else:
            print(f"Błąd pobierania analizy zachowań: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Błąd podczas pobierania analizy zachowań: {e}")
        return None

# Funkcja generuje raport
def generate_report(file_path, analysis_data):
    try:
        print("Pełna odpowiedź API:")
        print(json.dumps(analysis_data, indent=4))

        sha256_hash = analysis_data['data']['id']

        report = json.dumps(analysis_data, indent=4)

        report_path = f"{REPORT_DIRECTORY}/{sha256_hash}_full_report.txt"

        with open(report_path, "w") as report_file:
            report_file.write(report)

        print(f"Raport zapisany do: {report_path}")
        return f"Raport zapisany do: {report_path}"

    except KeyError as e:
        print(f"Brak wymaganych danych w odpowiedzi: {e}")
        return f"Brak wymaganych danych w odpowiedzi: {e}"
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return f"Nieoczekiwany błąd: {e}"

# Funkcja generuje raport z analizy zachowań
def generate_behaviour_report(file_path, behaviour_data):
    try:
        print("Pełna analiza zachowań:")
        print(json.dumps(behaviour_data, indent=4))

        base_name = os.path.basename(file_path).split('.')[0]

        behaviour_report = json.dumps(behaviour_data, indent=4)

        report_path = os.path.join(REPORT_DIRECTORY, f"{base_name}_behaviour_summary.txt")

        with open(report_path, "w") as report_file:
            report_file.write(behaviour_report)

        print(f"Raport analizy zachowań zapisany do: {report_path}")
        return f"Raport analizy zachowań zapisany do: {report_path}"

    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return f"Nieoczekiwany błąd: {e}"

# Główna część programu
def main():
    if not os.path.exists(REPORT_DIRECTORY):
        os.makedirs(REPORT_DIRECTORY)

    print(f"Używam domyślnego klucza API: {API_KEY}")
    print(f"Używam domyślnego katalogu: {DEFAULT_DIRECTORY}")
    files = list_files_in_directory(DEFAULT_DIRECTORY)
    if not files:
        return
    
    selected_files = select_files_from_list(files)
    if not selected_files:
        print("Nie wybrano żadnych plików.")
        return

    print(f"Wybrano pliki: {', '.join(selected_files)}")
    for file_name in selected_files:
        file_path = os.path.join(DEFAULT_DIRECTORY, file_name)
        file_id = file_name.split('.')[0]
        analysis_data = get_analysis_results(API_KEY, file_id)
        if analysis_data:
            generate_report(file_path, analysis_data)

        behaviour_data = get_behaviour_summary(API_KEY, file_id)
        if behaviour_data:
            generate_behaviour_report(file_path, behaviour_data)

if __name__ == "__main__":
    main()