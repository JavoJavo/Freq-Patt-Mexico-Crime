import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import pydeck as pdk


DATA_URL = ("D:\TICS-2021-1\MineriaDeDatos\Proyecto Final\muestra20000.csv")
#DATA_URL = ("D:\TICS-2021-1\MineriaDeDatos\Proyecto Final\carpetas-de-investigacion-pgj-cdmx.csv")

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

data_d = data.sample(20000)
# VERSION LIGHT
st.sidebar.markdown('## Versión light      \n20,000 registros aleatorios de un total de ...')
if st.sidebar.checkbox('Desactivar version light',False,key='light'):
	data_d = data

# NÚMERO DE CRÍMENES POR DELEGACIÓN:
st.markdown("### Número de crímenes por delegación")
limit0 = st.number_input("Mostrar:", min_value=1, max_value=len(data_d.alcaldia_hechos.unique()),value=10, step=1)
crimenes_por_delegacion = data_d['alcaldia_hechos'].value_counts()[:limit0]
crimenes_por_delegacion = pd.DataFrame({'Delegación':crimenes_por_delegacion.index, 'Crímenes':crimenes_por_delegacion.values})
fig = px.bar(crimenes_por_delegacion, x='Delegación', y='Crímenes', height=500) #, color='Crímenes'
st.plotly_chart(fig)




# NÚMERO DE CRÍMENES POR TIPO DE CRIMEN:
st.markdown("### Número de crímenes por tipo de crimen")
crimenes_por_tipo = data_d['delito'].value_counts()
crimenes_por_tipo = pd.DataFrame({'Tipo':crimenes_por_tipo.index, 'Crímenes':crimenes_por_tipo.values})
limit = st.number_input("Mostrar:", min_value=1, max_value=len(data_d.delito.unique()),value=10, step=1)

fig = px.bar(crimenes_por_tipo[:limit], x='Tipo', y='Crímenes', height=500) #, color='Crímenes'
st.plotly_chart(fig)






# MAPEAR CRÍMENES:
# Definiendo rango de valores
años = [data.fecha_hechos[i].year for i in range(data.shape[0])]
minaños, maxaños = min(años), max(años)


st.sidebar.subheader('Mapa')
st.subheader('Mapa')
#if not st.sidebar.checkbox("Cerrar", True, key='da1'):
data_d = data_d.dropna()

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
	year = st.sidebar.slider("Año", minaños, maxaños)
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.year == year]


# MES DEL DELITO	
st.sidebar.markdown('Mes:')
if not st.sidebar.checkbox("Todo los meses", True, key='1dms'):
	month = st.sidebar.slider("Mes",  1, 12)
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.month == month]

# HORA DEL DELITO	
st.sidebar.markdown('Hora:')
if not st.sidebar.checkbox("Todo el dia", True, key='1ds'):
	hour = st.sidebar.slider("Hora del día", 0, 23)
	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.hour == hour]


# MAPEAR
#st.map(data_d.dropna())
if data_d.shape[0] > 3:
	coor = data_d[['lat','lon']]
	ini_view = pdk.data_utils.viewport_helpers.compute_view(coor, view_proportion=.95)
	#st.write('lat:',ini_view.latitude,'lon:',ini_view.longitude, ini_view.zoom, ini_view.pitch)

	st.pydeck_chart(
		pdk.Deck(
			map_style='mapbox://styles/mapbox/streets-v11',
			initial_view_state = pdk.ViewState(
				latitude = ini_view.longitude,
				longitude=ini_view.latitude,
				zoom=ini_view.zoom,
				pitch=25,
			),
			layers=[
				pdk.Layer(
					'ScatterplotLayer',
					data = coor,
					get_position='[lon,lat]',
					get_fill_color='[200,20,0,400]',
					get_radius= 20,
				),
			]
		)
	)	
else:
	st.map(data_d.dropna())