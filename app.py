# app.py
import streamlit as st
import logging
import sys
import os
import time
from processor import DataProcessor
from visualizer import create_sales_trend_chart, create_sales_by_category_chart

def setup_logging():
    """Konfiguruje system logowania do pliku i konsoli."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("app.log", mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def process_and_display(file_object, file_name: str):
    """
    Przetwarza przekazany obiekt pliku i renderuje całą stronę wyników.
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Pasek postępu symulujący ładowanie przez 2 sekundy
        progress_text = "Analizowanie danych. Proszę czekać..."
        progress_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1, text=progress_text)
        progress_bar.empty() # Usunięcie paska postępu po zakończeniu

        processor = DataProcessor(file_object)

        st.header("Podgląd wgranych danych")
        st.info("Poniżej znajduje się interaktywna tabela z danymi z Twojego pliku. Możesz ją przewijać i sortować, klikając na nagłówki kolumn.")
        st.dataframe(processor.df, use_container_width=True, height=350)
        st.markdown("---")

        st.header("Kluczowe Wskaźniki Wydajności (KPI)")
        kpis = processor.calculate_kpis()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Całkowita Sprzedaż", 
                value=f"{kpis['total_sales']:.2f} PLN"
            )
        with col2:
            st.metric(
                label="Średnia Wartość Transakcji", 
                value=f"{kpis['average_sale']:.2f} PLN"
            )
        with col3:
            st.metric(
                label="Top Produkt (ilościowo)", 
                value=str(kpis['top_product'])
            )

        st.markdown("---")
        st.header("Wizualizacje")

        fig_trend = create_sales_trend_chart(processor.df)
        st.plotly_chart(fig_trend, use_container_width=True)

        fig_category = create_sales_by_category_chart(processor.df)
        st.plotly_chart(fig_category, use_container_width=True)

        st.markdown("---")
        st.header("Statystyki Opisowe Danych")
        stats_df = processor.get_descriptive_stats()
        st.dataframe(stats_df, use_container_width=True)
        
        st.markdown("---")
        st.header("Pobieranie Raportu")
        
        excel_data = processor.generate_excel_report()
        st.download_button(
            label="📥 Pobierz raport Excel",
            data=excel_data,
            file_name=f"raport_sprzedazy_{os.path.basename(file_name).split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        logger.info(f"Aplikacja zakończyła przetwarzanie pliku: {file_name}")

    except ValueError as e:
        st.error(f"Błąd przetwarzania pliku: {e}")
        logger.error(f"Błąd walidacji lub przetwarzania pliku {file_name}: {e}")
    except Exception as e:
        st.error(f"Wystąpił nieoczekiwany błąd podczas przetwarzania pliku {file_name}.")
        logger.critical(f"Nieoczekiwany błąd aplikacji dla pliku {file_name}: {e}", exc_info=True)

def main():
    """Główna funkcja aplikacji Streamlit."""
    setup_logging()
    logger = logging.getLogger(__name__)

    st.set_page_config(layout="wide", page_title="Analizator Sprzedaży CSV")

    st.title("📊 Analizator Sprzedaży CSV")
    st.markdown("---")

    st.sidebar.header("Panel Sterowania")
    uploaded_file = st.sidebar.file_uploader(
        "Wgraj plik CSV, aby zastąpić domyślny", type=["csv"]
    )

    if uploaded_file is not None:
        logger.info("Przetwarzanie pliku wgranego przez użytkownika.")
        process_and_display(uploaded_file, uploaded_file.name)
    else:
        default_file_path = 'dane.csv'
        logger.info(f"Brak pliku od użytkownika, próba wczytania domyślnego pliku: {default_file_path}")
        if os.path.exists(default_file_path):
            st.sidebar.success(f"Wczytano domyślny plik: `{default_file_path}`.")
            with open(default_file_path, 'rb') as f:
                process_and_display(f, default_file_path)
        else:
            st.info("Wgraj plik CSV za pomocą panelu bocznego, aby rozpocząć analizę.")
            st.sidebar.warning(f"Nie znaleziono domyślnego pliku `{default_file_path}`.")
            st.sidebar.info(
                """
                **Oczekiwane kolumny w pliku CSV:**
                - `Data` (np. 2023-01-15)
                - `Produkt`
                - `Kategoria`
                - `Sprzedaż` (wartość numeryczna)
                - `Ilość` (wartość numeryczna)
                """
            )

if __name__ == "__main__":
    main()