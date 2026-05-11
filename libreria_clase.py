import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class DataAnalyzer:

    def __init__(self, dataframe):

        self.df = dataframe

    # 1. Estadísticas descriptivas
    def descriptive_statistics(self):
        st.subheader("ESTADÍSTICAS DESCRIPTIVAS")
        st.dataframe(self.df.describe(include='all'))

    # 2. Clasificación de variables
    def classify_variables(self):
        
        numericas = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        categoricas = self.df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        st.subheader(" VARIABLES NUMÉRICAS ")
        st.dataframe(numericas)

        st.subheader(" VARIABLES CATEGÓRICAS ")
        st.dataframe(categoricas)

        return numericas, categoricas

    # 3. Visualización - Histograma
    def plot_histogram(self, column):
        
        fig, ax = plt.subplots(figsize=(8,5))

        sns.histplot(self.df[column], kde=True, ax=ax)

        ax.set_title(f'Histograma de {column}')

        st.pyplot(fig)

    # 4. Visualización - Boxplot
    def plot_boxplot(self, column):
        
        fig, ax = plt.subplots(figsize=(8,5))

        sns.boxplot(x=self.df[column], ax=ax)

        ax.set_title(f'Boxplot de {column}')

        st.pyplot(fig)

    # 5. Visualización - Barras
    def plot_bar(self, column):
        fig, ax = plt.subplots(figsize=(8,5))

        self.df[column].value_counts().plot(kind='bar',ax=ax)

        ax.set_title(f'Gráfico de barras de {column}')

        st.pyplot(fig)

    # 6. Valores nulos
    def missing_values(self):
        st.subheader(" VALORES NULOS ")

        st.dataframe(self.df.isnull().sum().reset_index())