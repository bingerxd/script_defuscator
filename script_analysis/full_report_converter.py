import json
from datetime import datetime
import os

def generate_report(data):
    attributes = data["data"]["attributes"]
    
    # Konwersja dat
    first_submission = datetime.utcfromtimestamp(attributes["first_submission_date"]).strftime('%Y-%m-%d %H:%M:%S')
    last_submission = datetime.utcfromtimestamp(attributes["last_submission_date"]).strftime('%Y-%m-%d %H:%M:%S')
    last_analysis = datetime.utcfromtimestamp(attributes["last_analysis_date"]).strftime('%Y-%m-%d %H:%M:%S')
    last_modification = datetime.utcfromtimestamp(attributes["last_modification_date"]).strftime('%Y-%m-%d %H:%M:%S')

    # Główne informacje
    report = f"""
    RAPORT O PLIKU
    ---------------------
    Nazwa pliku: {attributes.get('meaningful_name')}
    Typ pliku: {attributes.get('type_description')} ({attributes.get('type_extension')})
    Rozmiar pliku: {attributes.get('size')} bajtów
    Magic: {attributes.get('magic')}
    
    Identyfikatory:
    - MD5: {attributes.get('md5')}
    - SHA1: {attributes.get('sha1')}
    - SHA256: {attributes.get('sha256')}
    - TLSH: {attributes.get('tlsh')}
    
    Daty:
    - Pierwsze zgłoszenie: {first_submission}
    - Ostatnie zgłoszenie: {last_submission}
    - Ostatnia analiza: {last_analysis}
    - Ostatnia modyfikacja: {last_modification}
    
    Klasyfikacja zagrożeń:
    - Sugerowana etykieta zagrożenia: {attributes['popular_threat_classification'].get('suggested_threat_label')}
    - Kategorie zagrożeń: {', '.join([cat['value'] for cat in attributes['popular_threat_classification'].get('popular_threat_category', [])])}
    
    Statystyki analizy:
    - Złośliwe: {attributes['last_analysis_stats'].get('malicious')}
    - Podejrzane: {attributes['last_analysis_stats'].get('suspicious')}
    - Niewykryte: {attributes['last_analysis_stats'].get('undetected')}
    
    Wyniki skanowania:
    """
    
    for engine, result in attributes["last_analysis_results"].items():
        status = result.get("category")
        detection = result.get("result") or "Brak"
        report += f"    - {engine}: {status.upper()} ({detection})\n"
    
    report += f"""
    ---------------------
    Źródło analizy: {data['data']['links']['self']}
    """
    
    return report

def load_json_from_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_report_to_file(filepath, report):
    with open(filepath, 'w') as file:
        file.write(report)

def main():
    folder_path = "/home/kali/Desktop/projekt_IS/reports"
    
    if not os.path.exists(folder_path):
        print(f"Ścieżka {folder_path} nie istnieje.")
        return
    
    # Filtr plików zawierających '_full_report' w nazwie
    files = [f for f in os.listdir(folder_path) if ('_full_report' in f and f.endswith(('.json', '.txt')))]
    
    if not files:
        print("Brak plików JSON lub TXT zawierających '_full_report' w nazwie.")
        return
    
    print("Dostępne pliki:")
    for idx, file_name in enumerate(files, 1):
        print(f"{idx}. {file_name}")
    
    try:
        choice = int(input("Wybierz numer pliku do analizy: "))
        if choice < 1 or choice > len(files):
            print("Nieprawidłowy wybór. Proszę wybrać poprawny numer.")
            return
    except ValueError:
        print("Nieprawidłowy input. Proszę podać numer.")
        return
    
    selected_file = os.path.join(folder_path, files[choice - 1])
    
    try:
        data = load_json_from_file(selected_file)
        report = generate_report(data)
        print(report)
        save_report_to_file(selected_file, report)
        print(f"Raport zapisany do pliku: {selected_file}")
    except Exception as e:
        print(f"Wystąpił błąd podczas generowania raportu: {e}")

if __name__ == "__main__":
    main()
