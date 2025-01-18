#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
detect_external_connections.py

Wykrywanie i zabezpieczanie zewnętrznych połączeń w kodzie Python:
- Wykrywa URL-e (HTTP/HTTPS, FTP) i adresy IP.
- Wykrywa dynamiczne połączenia (zmienne, konkatenacja).
- Zakomentowuje linie z połączeniami sieciowymi.
- Dodaje raport na końcu pliku.

Autor: [Patryk Zabawa, Matuesz Kolanko]
Data: 2025-01-12
"""

import re

def detect_external_connections_python(code):
    """
    Wyszukuje i zakomentowuje całe zewnętrzne adresy URL oraz IP w kodzie Python.
    Dodaje raport na końcu kodu.
    """

    # Wzorce do wykrywania URL-i, adresów IP i dynamicznych połączeń
    url_pattern = r'(.*?(requests\.get|requests\.post|urllib\.request|open)\(.*?(https?:\/\/[^\s\'"\)]+|ftp:\/\/[^\s\'"\)]+).*?\))'
    ip_pattern = r'(.*?\b(?:\d{1,3}\.){3}\d{1,3}\b.*)'
    dynamic_pattern = r'(.*?(fetch|axios\.get|axios\.post|XMLHttpRequest)\(.*?\).*)'

    # Wyszukiwanie wszystkich URL-i, IP i dynamicznych połączeń
    detected_urls = re.findall(url_pattern, code)
    detected_ips = re.findall(ip_pattern, code)
    detected_dynamic = re.findall(dynamic_pattern, code)

    # Zakomentowanie pełnych linii zawierających wykryte adresy
    def comment_line_with_match(match):
        return f"# ZAKOMENTOWANO: {match.group(0)}"

    code = re.sub(url_pattern, comment_line_with_match, code, flags=re.MULTILINE)
    code = re.sub(ip_pattern, comment_line_with_match, code, flags=re.MULTILINE)
    code = re.sub(dynamic_pattern, comment_line_with_match, code, flags=re.MULTILINE)

    # Generowanie raportu
    report = "\n\n# === RAPORT O WYKRYTYCH POŁĄCZENIACH ===\n"
    report += f"# Łączna liczba adresów URL: {len(detected_urls)}\n"
    for url in detected_urls:
        report += f"# - URL: {url[2]}\n"

    report += f"# Łączna liczba adresów IP: {len(detected_ips)}\n"
    for ip in detected_ips:
        report += f"# - IP: {ip.strip()}\n"

    report += f"# Łączna liczba dynamicznych połączeń: {len(detected_dynamic)}\n"
    for dyn in detected_dynamic:
        report += f"# - Dynamiczne połączenie: {dyn[1]}\n"

    return code + report


def _test():
    example_code = """
import requests

requests.get("http://malicious-site.com/data")
ip_address = "192.168.1.1"

dynamic_url = "http://" + "example.com"
fetch(dynamic_url)

axios.get('https://api.example.com/data')

def safe_function():
    print("Hello, safe world!")
"""

    print("=== Oryginalny kod Python ===")
    print(example_code)

    processed_code = detect_external_connections_python(example_code)

    print("\n=== Kod po zabezpieczeniu ===")
    print(processed_code)


if __name__ == "__main__":
    _test()
