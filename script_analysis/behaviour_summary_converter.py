import json
import os

def generate_threat_report(data):
    report = """
    RAPORT Z ANALIZY ZAGROŻEŃ
    -------------------------
    """

    # Sygnatury zagrożeń
    report += "\nSYGNATURY ZAGROŻEŃ:\n"
    for signature in data['data'].get('signature_matches', []):
        report += f"- ID: {signature.get('id', 'Brak danych')}\n  Nazwa: {signature.get('name', 'Brak danych')}\n  Opis: {signature.get('description', 'Brak danych')}\n  Poziom zagrożenia: {signature.get('severity', 'Brak danych')}\n"
        if 'match_data' in signature and signature['match_data']:
            report += "  Dopasowania:\n"
            for match in signature['match_data']:
                report += f"    - {match}\n"
        report += "\n"

    # Drzewo procesów
    report += "\nDRZEWO PROCESÓW:\n"
    for process in data['data'].get('processes_tree', []):
        report += f"- PID: {process.get('process_id', 'Brak danych')} | Nazwa: {process.get('name', 'Brak danych')}\n"
        for child in process.get('children', []):
            report += f"    -> PID: {child.get('process_id', 'Brak danych')} | Nazwa: {child.get('name', 'Brak danych')}\n"

    # Ruch sieciowy
    report += "\nRUCH SIECIOWY:\n"
    ip_traffic = data['data'].get('ip_traffic', [])
    if ip_traffic:
        for traffic in ip_traffic:
            report += (f"- IP docelowy: {traffic.get('destination_ip', 'Brak danych')}, Port: {traffic.get('destination_port', 'Brak danych')}, Protokół: {traffic.get('transport_layer_protocol', 'Brak danych')}\n")
    else:
        report += "Brak danych o ruchu sieciowym.\n"

    # Alerty IDS
    report += "\nALERTY IDS:\n"
    ids_alerts = data['data'].get('ids_alerts', [])
    if ids_alerts:
        for alert in ids_alerts:
            report += (f"- ID Reguły: {alert.get('rule_id', 'Brak danych')}\n  Wiadomość: {alert.get('rule_msg', 'Brak danych')}\n  Kategoria: {alert.get('rule_category', 'Brak danych')}\n  Źródło: {alert.get('rule_source', 'Brak danych')}\n  Poziom zagrożenia: {alert.get('alert_severity', 'Brak danych')}\n")
            context = alert.get('alert_context', {})
            report += f"  Źródło IP: {context.get('src_ip', 'Brak danych')}, Port: {context.get('src_port', 'Brak danych')}\n"
    else:
        report += "Brak alertów IDS.\n"

    # Techniki MITRE ATT&CK
    report += "\nTECHNIKI MITRE ATT&CK:\n"
    mitre_techniques = data['data'].get('mitre_attack_techniques', [])
    if mitre_techniques:
        for technique in mitre_techniques:
            report += f"- ID: {technique.get('id', 'Brak danych')}\n  Opis: {technique.get('signature_description', 'Brak danych')}\n  Poziom zagrożenia: {technique.get('severity', 'Brak danych')}\n"
    else:
        report += "Brak danych o technikach MITRE ATT&CK.\n"

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
    
    files = [f for f in os.listdir(folder_path) if ('_behaviour_summary' in f and f.endswith(('.json', '.txt')))]
    
    if not files:
        print("Brak plików JSON lub TXT zawierających '_behaviour_summary' w nazwie.")
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
        report = generate_threat_report(data)
        print(report)
        save_report_to_file(selected_file.replace('.json', '_generated.txt'), report)
        print(f"Raport zapisany do pliku: {selected_file.replace('.json', '_generated.txt')}")
    except Exception as e:
        print(f"Wystąpił błąd podczas generowania raportu: {e}")

if __name__ == "__main__":
    main()
