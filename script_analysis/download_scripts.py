import requests
import os
import pyzipper
import shutil

class MalwareBazaarClient:
    BASE_URL = "https://mb-api.abuse.ch/api/v1/"
    ZIP_PASSWORD = b"infected"
    
    def __init__(self, output_dir: str = "malware_samples"):
        """
        Inicjalizacja klienta MalwareBazaar.
        :param output_dir: Katalog, w którym będą zapisywane pobrane próbki.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_sample_by_hash(self, file_hash: str):
        """
        Pobierz próbkę malware na podstawie hasha.
        :param file_hash: Hash pliku (MD5/SHA256).
        """
        payload = {"query": "get_file", "sha256_hash": file_hash}
        response = requests.post(self.BASE_URL, data=payload)
        
        if response.status_code == 200 and response.content:
            file_path = os.path.join(self.output_dir, f"{file_hash}.zip")
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Pobrano próbkę: {file_path}")
            self.decrypt_zip_without_extracting(file_path)
        else:
            print(f"Nie udało się pobrać próbki o hashu: {file_hash}")
    
    def search_by_tag(self, tag: str, limit: int):
        """
        Wyszukaj próbki malware na podstawie tagu (np. "javascript", "python").
        :param tag: Tag do wyszukiwania.
        :param limit: Maksymalna liczba próbek do pobrania.
        """
        payload = {"query": "get_taginfo", "tag": tag}
        response = requests.post(self.BASE_URL, data=payload)
        
        if response.status_code == 200:
            samples = response.json().get("data", [])
            for sample in samples[:limit]:
                file_hash = sample.get("sha256_hash")
                if file_hash:
                    self.fetch_sample_by_hash(file_hash)
        else:
            print(f"Nie udało się pobrać próbek dla tagu: {tag}")

    def decrypt_zip_without_extracting(self, zip_path: str):
        """
        Odszyfruj plik ZIP i zapisz go ponownie bez hasła, zastępując oryginał.
        :param zip_path: Ścieżka do zaszyfrowanego pliku ZIP.
        """
        temp_dir = os.path.join(self.output_dir, "temp_extract")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            with pyzipper.AESZipFile(zip_path, 'r') as zip_ref:
                zip_ref.pwd = self.ZIP_PASSWORD
                zip_ref.extractall(temp_dir)
            
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED) as new_zip:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        new_zip.write(file_path, arcname)
            print(f"Odszyfrowano ZIP: {zip_path}")
        except Exception as e:
            print(f"Błąd odszyfrowywania ZIP: {e}")
        finally:
            shutil.rmtree(temp_dir)

def main():
    client = MalwareBazaarClient(output_dir="malware_samples")
    
    print("Witaj w narzędziu MalwareBazaar!")
    print("Wybierz metodę pobierania próbek:")
    print("1. Pobierz próbkę na podstawie hashu (SHA256).")
    print("2. Pobierz próbki na podstawie tagu.")
    
    choice = input("Twój wybór (1/2): ")
    
    if choice == "1":
        file_hash = input("Podaj hash (SHA256): ").strip()
        client.fetch_sample_by_hash(file_hash)
    
    elif choice == "2":
        tag = input("Podaj tag (np. javascript, python): ").strip()
        limit = int(input("Podaj maksymalną liczbę próbek do pobrania: "))
        client.search_by_tag(tag, limit)
    
    else:
        print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
