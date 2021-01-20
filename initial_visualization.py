import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
#from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


DATA_URL = ("D:\TICS-2021-1\MineriaDeDatos\Proyecto Final\muestra20000.csv")

st.title("Visualización de crímenes cometidos en la Ciudad de México (Primeros 20 mil registros)")
st.markdown("Los datos usados son públicos y están disponibles y actualizados [aquí](https://datos.cdmx.gob.mx/explore/dataset/carpetas-de-investigacion-pgj-cdmx/export/?dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJ5QXhpcyI6ImxvbiIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6InJhbmdlLUFjY2VudCJ9XSwieEF4aXMiOiJhb19oZWNob3MiLCJtYXhwb2ludHMiOjUwLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwic2VyaWVzQnJlYWtkb3duIjoiZGVsaXRvIiwic2VyaWVzQnJlYWtkb3duVGltZXNjYWxlIjoiIiwic3RhY2tlZCI6Im5vcm1hbCIsImNvbmZpZyI6eyJkYXRhc2V0IjoiY2FycGV0YXMtZGUtaW52ZXN0aWdhY2lvbi1wZ2otY2RteCIsIm9wdGlvbnMiOnsicmVmaW5lLmRlbGl0byI6IlZJT0xBQ0lPTiJ9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlLCJ0aW1lc2NhbGUiOiIifQ%3D%3D).")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL,na_values='NaN')#,nrows=20000)
    data = data.drop(columns=['año_hechos','mes_hechos','categoria_delito','Geopoint','calle_hechos2','calle_hechos','colonia_hechos','mes_inicio','ao_inicio'])
    data.fecha_hechos = pd.to_datetime(data.fecha_hechos)
    data.rename(columns={'longitud':'lon','latitud':'lat'}, inplace=True)
    return data

data = load_data()
delegaciones = ['ALVARO OBREGON',
 'AZCAPOTZALCO',
 'BENITO JUAREZ',
 'COYOACAN',
 'CUAJIMALPA DE MORELOS',
 'CUAUHTEMOC',
 'GUSTAVO A MADERO',
 'IZTACALCO',
 'IZTAPALAPA',
 'MIGUEL HIDALGO',
 'MILPA ALTA',
 'TLAHUAC',
 'TLALPAN',
 'VENUSTIANO CARRANZA',
 'XOCHIMILCO',
 'LA MAGDALENA CONTRERAS']
#delegaciones = list(data.alcaldia_hechos.unique())



# NÚMERO DE CRÍMENES POR DELEGACIÓN:
st.markdown("### Número de crímenes por delegación")
limit0 = st.number_input("Mostrar:", min_value=1, max_value=len(data.alcaldia_hechos.unique()),value=10, step=1)
crimenes_por_delegacion = data['alcaldia_hechos'].value_counts()[:limit0]
crimenes_por_delegacion = pd.DataFrame({'Delegación':crimenes_por_delegacion.index, 'Crímenes':crimenes_por_delegacion.values})
fig = px.bar(crimenes_por_delegacion, x='Delegación', y='Crímenes', height=500) #, color='Crímenes'
st.plotly_chart(fig)




# NÚMERO DE CRÍMENES POR TIPO DE CRIMEN:
st.markdown("### Número de crímenes por tipo de crimen")
crimenes_por_tipo = data['delito'].value_counts()
crimenes_por_tipo = pd.DataFrame({'Tipo':crimenes_por_tipo.index, 'Crímenes':crimenes_por_tipo.values})
limit = st.number_input("Mostrar:", min_value=1, max_value=len(data.delito.unique()),value=10, step=1)

fig = px.bar(crimenes_por_tipo[:limit], x='Tipo', y='Crímenes', height=500) #, color='Crímenes'
st.plotly_chart(fig)






# MAPEAR CRÍMENES:
st.sidebar.subheader('Mapa')
st.subheader('Mapa')
#if not st.sidebar.checkbox("Cerrar", True, key='da1'):
data_d = data.dropna()

# TIPO DEL DELITO
choice = st.sidebar.multiselect('Escoge categoría(s) de crimen', (sorted(list(data_d.delito.unique()))), key='0')
if len(choice) > 0:
	data_d = data_d[data_d.delito.isin(choice)]

# DELEGACIÓN DEL DELITO
dele = st.sidebar.selectbox('Delegación', ['TODAS']+delegaciones, key='ddel')
if dele != 'TODAS':
	data_d = data_d[data_d['alcaldia_hechos'] == dele]


# AÑO DEL DELITO	
st.sidebar.markdown('Año:')
if not st.sidebar.checkbox("Todos los años", True, key='1das'):
	años = [data.fecha_hechos[i].year for i in range(data.shape[0])]
	year = st.sidebar.slider("Año", min(años), max(años))
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.year == year]


# MES DEL DELITO	
st.sidebar.markdown('Mes:')
if not st.sidebar.checkbox("Todo los meses", True, key='1dms'):
	meses = [data.fecha_hechos[i].month for i in range(data.shape[0])]
	month = st.sidebar.slider("Hora del día",  min(meses), max(meses))
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.month == month]

# HORA DEL DELITO	
st.sidebar.markdown('Hora:')
if not st.sidebar.checkbox("Todo el dia", True, key='1ds'):
	hour = st.sidebar.slider("Hora del día", 0, 23)
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.hour == hour]


# MAPEAR
st.map(data_d.dropna())





	
#st.sidebar.subheader('Lugar y hora de crímenes')

#if not st.sidebar.checkbox("Cerrar", True, key='1'):
#	dele = st.selectbox('Delegación', ['TODAS']+delegaciones, key='del')
#	if dele != 'TODAS':
#		st.write('asldjfalds')
#		data_d = data[data['alcaldia_hechos'] == dele]
#	else:
#		data_d = data
#	choice = []
#	hour = 1
#	if st.sidebar.checkbox("Todo el dia", True, key='1'):
#		choice = st.sidebar.multiselect('Escoge categoría(s)', (sorted(list(data_d.delito.unique()))), key='0')
#		if len(choice) > 0:
#			modified_data = data_d.dropna()#[data['fecha_hechos']]#.dt.hour == hour]
#			modified_data = modified_data[modified_data.delito.isin(choice)]
#			st.markdown("### Lugar de crímenes")
#			st.map(modified_data)
#			if st.sidebar.checkbox("Mostrar datos (RAW)",False):
#			    st.write(modified_data)
#		else:
#			modified_data = data_d.dropna()#[data['fecha_hechos']]#.dt.hour == hour]
#			st.markdown("### Lugar de crímenes")
#			st.map(modified_data)
#			if st.sidebar.checkbox("Mostrar datos (RAW)",False):
#			    st.write(modified_data)
#	else:
#		hour = st.sidebar.slider("Hora del día", 0, 23)
##		if len(choice) > 0:
#			modified_data = data_d.dropna()[data_d['fecha_hechos'].dt.hour == hour]
#			modified_data = modified_data[modified_data.delito.isin(choice)]
#			st.markdown("### Lugar y hora de crímenes")
#			st.markdown("%i crímenes entre %i:00 y %i:00" %(len(modified_data),hour,(hour+1)%24))
##			if st.sidebar.checkbox("Mostrar datos (RAW)",False):
#			    st.write(modified_data)
#		else:
#			modified_data = data_d.dropna()[data_d['fecha_hechos'].dt.hour == hour]
#			st.markdown("### Lugar y hora de crímenes")
#			st.markdown("%i crímenes entre %i:00 y %i:00" %(len(modified_data),hour,(hour+1)%24))
#			st.map(modified_data)
#			if st.sidebar.checkbox("Mostrar datos (RAW)",False):
#			    st.write(modified_data)		
#