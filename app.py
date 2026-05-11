import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import libreria_clase as lc

# =========================================================
# FUNCIONES AUXILIARES (Pueden ser modificadas en caso de que las ecuaciones si acepten valores negativos)
# =========================================================

def validar_positivo(valor: float, nombre: str, permitir_cero: bool = False) -> None:
    if permitir_cero:
        if valor < 0:
            raise ValueError(f"{nombre} no puede ser negativo.")
    else:
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero.")
 
def calcular_cac(gasto_marketing: float, gasto_ventas: float, nuevos_clientes: int) -> dict:
    """
    Calcula el Costo de Adquisición de Cliente (CAC).
    Fórmula:
    CAC = (gasto_marketing + gasto_ventas) / nuevos_clientes
    """
    validar_positivo(gasto_marketing, "gasto_marketing", permitir_cero=True)
    validar_positivo(gasto_ventas, "gasto_ventas", permitir_cero=True)
    validar_positivo(nuevos_clientes, "nuevos_clientes")

    cac = (gasto_marketing + gasto_ventas) / nuevos_clientes

    return {
        "cac": round(cac, 2)
    }

# =========================================================
# OPCIONES SEGUN EL MENU SELECCIONADO
# =========================================================

# Menú en la barra lateral
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox(
    "Selecciona una opción:",
    ("🏠 1: Home","📋 2: Carga del dataset","📋 3: Clase POO","📋 4: Conclusiones")
)

# Mostrar contenido según la opción elegida
if opcion == "🏠 1: Home":
    st.title("PROYECTO 2-Caso de Estudio N°2")
    st.write("**Breve descripción del objetivo del análisis**: Aplicar de manera integrada los conceptos vistos a lo largo del curso, desarrollando una herramienta funcional, clara y bien estructurada, similar a un producto analítico real.")
    st.write("**Datos del autor**: ")    
    st.markdown(""" - **Nombre completo** : Luis Anderson Polo Benites""")
    st.markdown(""" - **Curso / Especialización** : Especialización en Python for Analytics""")
    st.markdown(""" - **Año**: 2026""")
    st.write("**Breve explicación del dataset**: Ccontiene información sobre los clientes, sus servicios contratados, facturación mensual, tiempo de permanencia y estado actual en la empresa.")
    st.write("**Tecnologías utilizadas**: La libreria utilizada hasta el momento es : Python, Pandas, Streamlit,matplotlib.pyplot,seaborn")
elif opcion == "📋 2: Carga del dataset":
    st.subheader("CARGA DEL DATASET")

    #Cargar el archivo csv
    archivo = st.file_uploader("Selecciona un archivo CSV",type=["csv"])

    # Validar que el archivo CSV fue cargado correctamente
    if archivo is not None:
        try:
            # Leemos el archivo
            df = pd.read_csv(archivo)

            # Archivo cargado correctamente
            st.success("Archivo cargado correctamente ✅")

            # Vista previa del dataset
            st.subheader("Vista previa del dataset")
            st.dataframe(df.head(5))

            # Dimensiones del dataset
            filas, columnas = df.shape

            st.subheader("Dimensiones del dataset")
            st.write(f"Filas: {filas}")
            st.write(f"Columnas: {columnas}")

            tab1, tab2, tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10 = st.tabs(["Ítem 1", "Ítem 2", "Ítem 3", "Ítem 4", "Ítem 5", "Ítem 6", "Ítem 7", "Ítem 8", "Ítem 9", "Ítem 10"])
            with tab1:
                st.header("Información general del dataset")
            
                #.info()
                import io

                buffer = io.StringIO()
                df.info(buf=buffer)

                s = buffer.getvalue()

                st.text(s)

                # Tipos de datos
                st.subheader("Tipos de datos")
                st.write(df.dtypes)

                # Conteo de valores nulos
                st.subheader("Valores nulos")
                st.write(df.isnull().sum())
            
            with tab2:
                st.header("Clasificación de variables")

                #Identificación de variables: Numéricas y Categóricas    
                
                # Variables numericas
                st.subheader("Variables numericas")
                variables_numericas = df.select_dtypes(include=['int64', 'float64']).nunique()
                st.write(variables_numericas)

                st.subheader("Variables Categóricas")
                variables_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).nunique()
                st.write(variables_categoricas)

                #Uso de una función personalizada
                st.subheader("Función para obtener el CAC: Costo de Adquisición de Clientes")

                st.subheader("Ingresar valores")

                val_marketing = st.number_input("Gastos de Marketing", value=0.0)
                val_ventas = st.number_input("Gastos de Ventas", value=0.0)
                val_clientes = st.number_input("Cantidad de Clientes", value=0.0)

                # ---- Botón para ejecutar ----
                if st.button("Ejecutar"):
                    resultado = calcular_cac(val_marketing, val_ventas, val_clientes)

                    # Mostrar resultado
                    st.success(f"Resultado: {resultado}")
                
                #Mostrar resultados con conteo
                st.subheader("Conteo por tipo de dato")
                tipos_datos = df.dtypes.value_counts().reset_index()        
                st.dataframe(tipos_datos)    

            with tab3:
                st.header("Estadísticas descriptivas")
                #Uso de .describe()
                st.write(df.describe())
                
                # Interpretación básica de medias, medianas y dispersión

                st.subheader("Media")
                st.write(df.groupby("Contract").mean(numeric_only=True))

                st.subheader("Mediana")
                st.write(df.groupby("Contract").median(numeric_only=True))

                st.subheader("Dispersión")
                st.write(df.groupby("Contract").std(numeric_only=True))

            with tab4:
                st.header("Análisis de valores faltantes")

                st.subheader("Conteo de valores faltantes")
                valores_faltantes = df.isnull().sum()
                st.dataframe(valores_faltantes.reset_index().rename(columns={"index": "Variable", 0: "Valores Faltantes"}))

                st.subheader("Visualización de valores faltantes")

                # Filtrar solo columnas con nulos
                faltantes = valores_faltantes[valores_faltantes > 0]

                if len(faltantes) > 0:
                    st.bar_chart(faltantes)
                else:
                    st.success("No existen valores faltantes en el dataset ✅")

                st.subheader("Discusión breve")

                total_nulos = valores_faltantes.sum()

                if total_nulos > 0:
                    st.write(f"El dataset presenta un total de {total_nulos} valores faltantes. Esto puede afectar el análisis si no se realiza un tratamiento adecuado.")
                else:
                    st.write("El dataset no tiene valores faltantes, por lo tanto eso ayuda al analisis")

            with tab5:
                st.header("Distribución de variables numéricas")

                st.subheader("Histogramas")
                
                # Crea figura
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(df.isna(), cbar=False, ax=ax)

                 # Muestra histograma
                st.pyplot(fig)
                

                st.subheader("Interpretación visual")
                st.write("El dataset no tiene valores faltantes, por eso muestra todo el contenido en negro.")

            with tab6:
                st.header("Análisis de variables categóricas")

                variables_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns

                # Validar si existen variables categóricas
                if len(variables_categoricas) > 0:

                    # Selector de variable
                    variable_cat = st.selectbox("Selecciona una variable categórica",variables_categoricas)
                    
                    # =====================================================
                    # CONTEOS
                    # =====================================================

                    st.subheader("Conteo de categorías")

                    conteos = df[variable_cat].value_counts()
                    st.dataframe(conteos.reset_index().rename(columns={"index": "Categoría",variable_cat: "Valores","count": "Cantidades"}))

                    st.subheader("Gráfico de barras")

                    fig, ax = plt.subplots(figsize=(8, 5))

                    conteos.plot(kind='bar',ax=ax)

                    ax.set_title(f"Distribución de {variable_cat}")
                    ax.set_xlabel("Valores")
                    ax.set_ylabel("Cantidades")

                    st.pyplot(fig)

                    st.subheader("Proporciones")

                    proporciones = (df[variable_cat].value_counts(normalize=True) * 100).round(2) #aplicamos redondeo en 2 decimales

                    st.dataframe(proporciones.reset_index().rename(columns={"index": "Categoria",variable_cat: "Valores","proportion": "Porcentaje(%)"}))

                else:
                    st.warning("No existen variables categóricas en el dataset.")

            with tab7:
                st.header("Análisis bivariado (numérico vs categórico)")

                variables_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                variables_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

                st.subheader("Ejemplo: MonthlyCharges vs Churn y/o tenure vs Churn")
                
                if variables_numericas != variables_categoricas:
                    variable_x = st.selectbox("Selecciona la variable numérica X",variables_numericas,key=1)
                    variable_y = st.selectbox("Selecciona la variable categórica Y",variables_categoricas,key=2)

                    tabla_cruzada_numxcat=pd.crosstab(df[variable_x],df[variable_y]) #tabla cruzada
                    st.dataframe(tabla_cruzada_numxcat)
                else:
                    st.warning("Selecciona variables diferentes.")                                      

            with tab8:
                st.header("Análisis bivariado (categórico vs categórico)")

                variables_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

                st.subheader("Ejemplo: Contract vs Churn y/o InternetService vs Churn")
                if len(variables_categoricas) >= 2:
                    variable_x = st.selectbox("Selecciona la variable categórico X",variables_categoricas,key=3)
                    variable_y = st.selectbox("Selecciona la variable categórico Y",variables_categoricas,key=4)

                    if variable_x != variable_y:
                        tabla_cruzada_catxcat=pd.crosstab(df[variable_x],df[variable_y]) #tabla cruzada
                        st.dataframe(tabla_cruzada_catxcat)
                    else:
                        st.warning("Selecciona variables diferentes.")
                else:
                    st.warning("No existen suficientes variables categóricas.")  
                

            with tab9:
                st.header("Análisis basado en parámetros seleccionados")

                columnas = df.columns.tolist()

                # Selectbox para variable categórica
                variable_categoria = st.selectbox("Selecciona una variable categórica",df.select_dtypes(include=['object', 'category', 'bool']).columns,key=5)

                # Multiselect para variables numéricas
                variables_numericas = st.multiselect("Selecciona variables numéricas",df.select_dtypes(include=['int64', 'float64']).columns,key=6)

                # =====================================================
                # VALIDAR SELECCIÓN
                # =====================================================

                if variable_categoria and len(variables_numericas) > 0:

                    # =====================================================
                    # AGRUPACIÓN DINÁMICA
                    # =====================================================

                    st.subheader("Análisis agrupado")

                    analisis = df.groupby(variable_categoria)[variables_numericas].mean()

                    st.dataframe(analisis.round(2))

                    # =====================================================
                    # GRÁFICO DINÁMICO
                    # =====================================================

                    st.subheader("Visualización gráfica")

                    fig, ax = plt.subplots(figsize=(10, 5))

                    analisis.plot(kind='bar',ax=ax)

                    ax.set_title(f"Promedio de variables numéricas por {variable_categoria}")

                    ax.set_xlabel(variable_categoria)
                    ax.set_ylabel("Promedio")

                    st.pyplot(fig)

                else:
                    st.info("Selecciona una variable categórica y al menos una variable numérica.")
                

            with tab10:
                st.header("Hallazgos clave")

                filas, columnas = df.shape

                st.write(f"El dataset contiene {filas} filas y {columnas} columnas.")


                # Crear histogramas
                auxiliar = df[["MonthlyCharges", "TotalCharges"]].hist(figsize=(12, 6),bins=30)
                st.pyplot(plt)

                st.write("""
                Los Insights principales derivados del EDA, fueron saber los valores faltantes, comportamiento de variables de variables
                numéricas y categóricas, así como relaciones importantes entre variables relacionadas con la cancelación de clientes (Churn).                
                """)

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    else:
        st.info("Por favor, selecciona un archivo CSV para continuar.")
elif opcion == "📋 3: Clase POO":
    st.subheader("Programación Orientada a Objetos (POO)")
    #Cargar el archivo csv
    archivo = st.file_uploader("Selecciona un archivo CSV",type=["csv"])    

    if archivo is not None:
        df = pd.read_csv(archivo)

        st.dataframe(df.head())
        # Crear objeto
        analyzer = lc.DataAnalyzer(df)

        # Estadísticas descriptivas
        analyzer.descriptive_statistics()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

        # Clasificación de variables
        analyzer.classify_variables()

        # Valores nulos
        analyzer.missing_values()

        # Visualizaciones
        analyzer.plot_histogram("MonthlyCharges")
        analyzer.plot_boxplot("Contract")
        analyzer.plot_bar("PaperlessBilling")
    else:
        st.info("Por favor, selecciona un archivo CSV para continuar.")
elif opcion == "📋 4: Conclusiones":
    st.subheader("Conclusiones Finales")
    st.write("""
    1.- El analisis descriptivo refleja las variables numérica y categórica del dataset.
             
    2.- Se valida la calidad de la data, permitiendo determinar si es necesario realizar alguna limpieza o aplicar filtros necesarios
             para tener datos mas confiables.
    
    3.- Los histogramas y boxplots ayudaron a comprender la distribución de las variables numéricas.
             
    4.- Los gráficos de barras facilitaron el análisis de las variables categóricas.
             
    5.- El uso de clases, nos sirven para tener un codigo más limpio y centralizar contenido reutilizable.         
        
    """)
