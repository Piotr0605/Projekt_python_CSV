# processor.py
import pandas as pd
import io
import logging

class DataProcessor:
    """
    Klasa do przetwarzania danych sprzedażowych z pliku CSV.

    Odpowiada za wczytywanie danych, walidację struktury, obliczanie
    kluczowych wskaźników wydajności (KPI) oraz generowanie raportu Excel.
    """
    REQUIRED_COLUMNS = ['Data', 'Produkt', 'Kategoria', 'Sprzedaż', 'Ilość']

    def __init__(self, uploaded_file):
        """
        Inicjalizuje procesor danych.

        Args:
            uploaded_file: Plik wgrany przez użytkownika (obiekt BytesIO).

        Raises:
            ValueError: Jeśli plik jest nieprawidłowy lub brakuje w nim kolumn.
        """
        self.logger = logging.getLogger(__name__)
        if uploaded_file is None:
            raise ValueError("Nie przekazano pliku.")
        
        try:
            self.df = pd.read_csv(uploaded_file)
            self.logger.info("Plik CSV został pomyślnie wczytany.")
            self._validate_columns()
            self._prepare_data()
        except Exception as e:
            self.logger.error(f"Błąd podczas wczytywania lub walidacji pliku: {e}")
            raise ValueError(f"Nie można przetworzyć pliku. Upewnij się, że to poprawny plik CSV. Błąd: {e}")

    def _validate_columns(self):
        """Sprawdza, czy DataFrame zawiera wszystkie wymagane kolumny."""
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Brak wymaganych kolumn w pliku: {', '.join(missing_cols)}")
        self.logger.info("Walidacja kolumn zakończona pomyślnie.")

    def _prepare_data(self):
        """Konwertuje typy danych w celu dalszej analizy."""
        self.df['Data'] = pd.to_datetime(self.df['Data'])
        self.df['Sprzedaż'] = pd.to_numeric(self.df['Sprzedaż'])
        self.df['Ilość'] = pd.to_numeric(self.df['Ilość'])
        self.logger.info("Konwersja typów danych zakończona.")

    def calculate_kpis(self) -> dict:
        """
        Oblicza kluczowe wskaźniki wydajności (KPI).

        Returns:
            Słownik zawierający sumę sprzedaży, średnią wartość transakcji
            oraz najlepiej sprzedający się produkt.
        """
        total_sales = self.df['Sprzedaż'].sum()
        average_sale = self.df['Sprzedaż'].mean()
        top_product = self.df.groupby('Produkt')['Ilość'].sum().idxmax()
        
        self.logger.info("KPI zostały obliczone.")
        return {
            'total_sales': total_sales,
            'average_sale': average_sale,
            'top_product': top_product
        }

    def get_descriptive_stats(self) -> pd.DataFrame:
        """
        Generuje statystyki opisowe i tłumaczy ich etykiety na język polski.

        Returns:
            DataFrame ze statystykami opisowymi.
        """
        stats = self.df[['Sprzedaż', 'Ilość']].describe()
        
        polish_labels = {
            'count': 'Liczba rekordów',
            'mean': 'Średnia',
            'std': 'Odch. standardowe',
            'min': 'Minimum',
            '25%': '1. kwartyl (25%)',
            '50%': 'Mediana (50%)',
            '75%': '3. kwartyl (75%)',
            'max': 'Maksimum'
        }
        stats = stats.rename(index=polish_labels)
        self.logger.info("Statystyki opisowe zostały wygenerowane.")
        return stats

    def generate_excel_report(self) -> bytes:
        """
        Generuje raport w formacie Excel w pamięci.

        Raport zawiera dwie zakładki: 'Dane' z surowymi danymi
        oraz 'Statystyki' ze statystykami opisowymi.

        Returns:
            Raport Excel jako obiekt bytes.
        """
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='Dane', index=False)
            self.get_descriptive_stats().to_excel(writer, sheet_name='Statystyki')
        
        self.logger.info("Raport Excel został wygenerowany w pamięci.")
        return output.getvalue()
