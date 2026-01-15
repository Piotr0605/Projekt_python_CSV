# visualizer.py
import plotly.express as px
import pandas as pd

def create_sales_trend_chart(df: pd.DataFrame):
    """
    Tworzy wykres liniowy trendu sprzedaży w czasie.

    Args:
        df (pd.DataFrame): DataFrame z danymi sprzedażowymi.

    Returns:
        Obiekt figury Plotly.
    """
    daily_sales = df.groupby(df['Data'].dt.date)['Sprzedaż'].sum().reset_index()
    fig = px.line(
        daily_sales,
        x='Data',
        y='Sprzedaż',
        title='Trend Sprzedaży w Czasie',
        labels={'Data': 'Data', 'Sprzedaż': 'Suma Sprzedaży'},
        template='plotly_dark'
    )
    fig.update_layout(title_x=0.5, xaxis_title="Data", yaxis_title="Suma Sprzedaży [PLN]")
    return fig

def create_sales_by_category_chart(df: pd.DataFrame):
    """
    Tworzy wykres słupkowy sumy sprzedaży według kategorii.

    Args:
        df (pd.DataFrame): DataFrame z danymi sprzedażowymi.

    Returns:
        Obiekt figury Plotly.
    """
    category_sales = df.groupby('Kategoria')['Sprzedaż'].sum().reset_index().sort_values('Sprzedaż', ascending=False)
    fig = px.bar(
        category_sales,
        x='Kategoria',
        y='Sprzedaż',
        title='Suma Sprzedaży wg Kategorii',
        labels={'Kategoria': 'Kategoria', 'Sprzedaż': 'Suma Sprzedaży'},
        template='plotly_dark'
    )
    fig.update_layout(title_x=0.5, xaxis_title="Kategoria Produktu", yaxis_title="Suma Sprzedaży [PLN]")
    return fig
