# Analizator Sprzedaży CSV

Prosta, ale profesjonalna aplikacja analityczna w Streamlit, stworzona jako projekt na studia. Aplikacja pozwala na wgranie pliku CSV z danymi sprzedażowymi, automatycznie go analizuje i prezentuje kluczowe wskaźniki oraz wizualizacje w czytelnym interfejsie.

## Kluczowe Funkcje

-   **Domyślne dane:** Aplikacja automatycznie wczytuje plik `dane.csv` przy starcie, jeśli jest obecny.
-   **Upload plików:** Możliwość wgrania własnego pliku CSV z danymi sprzedażowymi.
-   **Walidacja danych:** Sprawdzanie, czy wgrany plik zawiera wymagane kolumny (`Data`, `Produkt`, `Kategoria`, `Sprzedaż`, `Ilość`).
-   **Podgląd danych:** Wyświetlanie interaktywnej tabeli z wgranymi danymi.
-   **Kluczowe Wskaźniki Wydajności (KPI):** Prezentacja całkowitej sprzedaży, średniej wartości transakcji i produktu z największą sprzedażą ilościową.
-   **Wizualizacje:**
    -   Wykres liniowy trendu sprzedaży w czasie.
    -   Wykres słupkowy sumy sprzedaży według kategorii.
-   **Statystyki Opisowe:** Tabela ze szczegółowymi statystykami dla danych numerycznych.
-   **Generowanie Raportów:** Możliwość pobrania pełnego raportu w formacie Excel.
-   **Logowanie:** Zapisywanie kluczowych operacji i błędów do pliku `app.log` oraz wyświetlanie ich w konsoli.

## Struktura Projektu

```
.
├── app.py              # Główny plik aplikacji Streamlit (interfejs użytkownika)
├── processor.py        # Moduł do przetwarzania danych (wczytywanie, walidacja, KPI)
├── visualizer.py       # Moduł do generowania wykresów
├── requirements.txt    # Lista zależności Python
├── dane.csv            # Przykładowy plik z danymi, ładowany domyślnie
└── README.md           # Ten plik
```

## Wymagania Techniczne

-   Python 3.10+
-   Biblioteki: `pandas`, `plotly`, `streamlit`, `openpyxl`

## Instalacja

1.  Sklonuj repozytorium lub pobierz pliki projektu do jednego folderu.
2.  Otwórz terminal (np. `cmd` lub `PowerShell`) w głównym folderze projektu.
3.  Zainstaluj wymagane biblioteki za pomocą komendy:
    ```bash
    pip install -r requirements.txt
    ```

## Uruchomienie

1.  Upewnij się, że jesteś w głównym folderze projektu w terminalu.
2.  Uruchom aplikację za pomocą komendy:
    ```bash
    python -m streamlit run app.py
    ```
3.  Aplikacja otworzy się automatycznie w Twojej przeglądarce internetowej.

   Wykonali Piotr Sienkiewicz, Tomasz Złotkowski, Kacper Kopaczewski
