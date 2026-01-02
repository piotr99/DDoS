import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

url = "https:example.com"
json_data = {
    "uLogin": "amFua293YWxza2lAZ21haWwuY29t",
    "uPassword": "TmlnZ2VyMTIzMTIzJA=="
}

def wyslij_jedno_zapytanie(numer):
    try:
        response = requests.post(url, json=json_data, timeout=2)
        return (numer, response.status_code, "OK")
    except requests.exceptions.Timeout:
        return (numer, None, "Timeout")
    except requests.exceptions.ConnectionError:
        return (numer, None, "Connection Error")
    except requests.exceptions.RequestException as e:
        return (numer, None, f"Błąd: {e}")

def wyslij_wiele_zapytan(ilosc_zapytan, max_workers):
    print(f"Startuję wysyłanie {ilosc_zapytan} zapytań z {max_workers} wątkami jednocześnie...\n")
    
    start_time = time.time()
    wyniki = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_nr = {executor.submit(wyslij_jedno_zapytanie, i): i for i in range(ilosc_zapytan)}
        
        for future in as_completed(future_to_nr):
            wynik = future.result()
            wyniki.append(wynik)
            nr, status, info = wynik
            print(f"Zapytanie #{nr+1}: {status if status else info}")

    czas_calosci = time.time() - start_time
    sukcesy = sum(1 for w in wyniki if w[1] == 200)
    print(f"\n=== PODSUMOWANIE ===")
    print(f"Wysłano: {ilosc_zapytan} zapytań w {czas_calosci:.2f} sekund")
    print(f"Sukces (200): {sukcesy}")
    print(f"Błędy/Timeout: {ilosc_zapytan - sukcesy}")
    print(f"Średnio zapytań na sekundę: {ilosc_zapytan / czas_calosci:.1f}")


if __name__ == "__main__":
    wyslij_wiele_zapytan(ilosc_zapytan=100, max_workers=100)
