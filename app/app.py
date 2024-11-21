import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os

# Obtener la ruta absoluta del archivo
ruta_archivo = os.path.abspath("vehicles_us.csv")

df = pd.read_csv(ruta_archivo, sep=',') # Leer los datos

columnas_espanol = {
    'price': 'precio',
    'model': 'fabricante',
    'model_year': 'año_modelo',
    'condition': 'condicion',
    'cylinders': 'cilindros',
    'fuel': 'combustible',
    'odometer': 'kilometraje',
    'transmission': 'transmision',
    'type': 'tipo',
    'paint_color': 'color_pintura',
    'is_4wd': 'es_4x4',
    'date_posted': 'fecha_publicacion',
    'days_listed': 'dias_publicados'
}

# Cambiar los nombres de las columnas utilizando el diccionario
df.rename(columns=columnas_espanol, inplace=True)


# Título de la aplicación
st.title("Aplicación de Visualización de Datos")


# Crear el gráfico de dispersión
fig = px.scatter(
    df,
    x="precio",  # Eje x: Precio
    y="año_modelo",  # Eje y: Año del modelo
    color="condicion",  # Color de los puntos según la condición
    title="Relación entre Precio, Año del Modelo y Condición de Vehículos"
)

# Personalizar el diseño del gráfico
fig.update_layout(
    title_x=0.1,  # Centra el título horizontalmente
    title_y=0.9,  # Ajusta la posición vertical del título
    title_font=dict(size=20, color='white'),  # Personaliza la fuente del título
    title_pad=dict(t=20, b=10)  # Agrega espacio arriba y abajo del título
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)



# Título para el histograma
st.title("Distribución del kilometraje de los vehículos")

# Botón para crear el histograma
if st.button("Crear Histograma"):
    # Crear el histograma
    figura = px.histogram(df, x="kilometraje", title="Distribución del kilometraje")
    figura.update_layout(
        xaxis_title="Kilometraje",
        yaxis_title="Cantidad de vehículos"
    )
    st.plotly_chart(figura, use_container_width=True)


# Título de la aplicación (nuevamente, para separar secciones)
st.title("Análisis de vehículos: explora y compara")

df['marca'] = df['fabricante'].str.split().str[0]

# Obtener las columnas numéricas del DataFrame
columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()

# Crear el selectbox para elegir la columna
columna_x = st.selectbox("Selecciona la columna para el histograma", columnas_numericas)

# Obtener los conteos de la columna seleccionada
conteo = df[columna_x].value_counts().reset_index(name="count")
conteo.rename(columns={'index': columna_x}, inplace=True)

# Crear el histograma
fig = px.bar(conteo, x=columna_x, y="count", title=f"Distribución de {columna_x}")

# Mostrar el gráfico
st.plotly_chart(fig)


# Título de la aplicación (nuevamente, para separar secciones)
st.title("Composición del Mercado Automotriz por Fabricante y Modelo")


x1 = df['año_modelo']
y1 = df['precio']

# Crear un gráfico de barras agrupado
grouped = df.groupby(['marca', 'tipo']).size().reset_index(name='cantidad')
fig = px.bar(grouped, x='marca', y='cantidad', color='tipo',
           barmode='group', title='Vehículos por Fabricante y Tipo')
st.plotly_chart(fig)

# Título de la aplicación(nuevamente, para separar secciones)
st.title("Comparación de Distribución de Precios entre Fabricantes")

# Crear los selectboxes para seleccionar los fabricantes
manufacturer1 = st.selectbox("Seleccionar fabricante 1", df['marca'].unique())
manufacturer2 = st.selectbox("Seleccionar fabricante 2", df['marca'].unique())

# Filtrar los datos según los fabricantes seleccionados
df_filtered = df[(df['marca'] == manufacturer1) | (df['marca'] == manufacturer2)]

# Crear el histograma
fig = px.histogram(
    df_filtered,
    x='precio',
    color='marca',
    barmode='group',
    histnorm='percent',
    title='Comparación de Distribución de Precios'
)

# Personalizar el gráfico
fig.update_layout(
    xaxis_title='Precio',
    yaxis_title='Porcentaje',
    legend_title='Fabricante'
)

# Mostrar el gráfico
st.plotly_chart(fig)

print(df.columns)
