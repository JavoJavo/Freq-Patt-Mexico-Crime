import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import pydeck as pdk
import random


st.title("Crímenes cometidos en la Ciudad de México en el primer semestre del año 2019")
st.markdown("Los datos usados son públicos y están disponibles [aquí](https://datos.cdmx.gob.mx/explore/dataset/carpetas-de-investigacion-pgj-cdmx/export/?dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJ5QXhpcyI6ImxvbiIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6InJhbmdlLUFjY2VudCJ9XSwieEF4aXMiOiJhb19oZWNob3MiLCJtYXhwb2ludHMiOjUwLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwic2VyaWVzQnJlYWtkb3duIjoiZGVsaXRvIiwic2VyaWVzQnJlYWtkb3duVGltZXNjYWxlIjoiIiwic3RhY2tlZCI6Im5vcm1hbCIsImNvbmZpZyI6eyJkYXRhc2V0IjoiY2FycGV0YXMtZGUtaW52ZXN0aWdhY2lvbi1wZ2otY2RteCIsIm9wdGlvbnMiOnsicmVmaW5lLmRlbGl0byI6IlZJT0xBQ0lPTiJ9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlLCJ0aW1lc2NhbGUiOiIifQ%3D%3D).")

DATA_URL = ("data2019.csv")
#DATA_URL = ("muestra20000.csv")
#DATA_URL = ("D:\TICS-2021-1\MineriaDeDatos\Proyecto Final\carpetas-de-investigacion-pgj-cdmx.csv")

# VERSION LIGHT
#LIGHT = True
#st.sidebar.markdown('## Versión light      \n20,000 registros aleatorios de un total de 808,871')
#if st.sidebar.checkbox('Desactivar version light',False,key='light'):
#	LIGHT = False
#else:
#	LIGHT = True

@st.cache(persist=True)
def load_data():
	#data=pd.DataFrame()
	#if LIGHT:
	#	n = 808871 
	#	s = 30000 
	#	skip = sorted(random.sample(range(1,n),n-s))
	#	data = pd.read_csv(DATA_URL, skiprows=skip,na_values='NaN')
	#else:

	# EXPERIMENTO PARA LEER DATASET POR PARTES #
	#data = pd.read_csv('datasets/data0.csv',na_values='NaN',index_col=0)#,nrows=20000)
	#for i in range(1,6):
	#	data_url = 'datasets/data{}.csv'.format(i)
	#	data = data.append(pd.read_csv(data_url,na_values='NaN',index_col=0),ignore_index=True)
	#                                           #
	


	data = pd.read_csv(DATA_URL,na_values='NaN')#,nrows=20000)
		
	data = data.drop(columns=['año_hechos','mes_hechos','categoria_delito','Geopoint','calle_hechos2','calle_hechos','colonia_hechos','mes_inicio','ao_inicio'])
	data.fecha_hechos = pd.to_datetime(data.fecha_hechos)
	data.rename(columns={'longitud':'lon','latitud':'lat'}, inplace=True)
	return data

data = load_data()
data_d = data


#st.write(data_d.shape)


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


st.sidebar.markdown("# Usando dataset entero:")

# DELEGACIONES CON MÁS CRÍMENES:
st.sidebar.markdown("### Delegaciones con más crímenes")
if st.sidebar.checkbox("Mostrar", False, key='ncpd'):
	st.markdown("### Delegaciones con más crímenes")
	limit0 = st.number_input("Mostrar:", min_value=1, max_value=len(data_d.alcaldia_hechos.unique()),value=10, step=1)
	crimenes_por_delegacion = data_d['alcaldia_hechos'].value_counts()[:limit0]
	crimenes_por_delegacion = pd.DataFrame({'Delegación':crimenes_por_delegacion.index, 'Crímenes':crimenes_por_delegacion.values})
	fig = px.bar(crimenes_por_delegacion, x='Delegación', y='Crímenes', height=500) #, color='Crímenes'
	st.plotly_chart(fig)




# CRÍMENES MÁS COMETIDOS:
st.sidebar.markdown("### Crímenes más cometidos")
if st.sidebar.checkbox("Mostrar", False, key='ncptc'):
	st.markdown("### Crímenes más cometidos")
	crimenes_por_tipo = data_d['delito'].value_counts()
	crimenes_por_tipo = pd.DataFrame({'Tipo':crimenes_por_tipo.index, 'Crímenes':crimenes_por_tipo.values})
	limit = st.number_input("Mostrar:", min_value=1, max_value=len(data_d.delito.unique()),value=9, step=1)

	fig = px.bar(crimenes_por_tipo[:limit], x='Tipo', y='Crímenes', height=500) #, color='Crímenes'
	st.plotly_chart(fig)




# DISTRIBUCIÓN DE CRÍMENES POR HORA Y POR DIA DE LA SEMANA



# MAPEAR CRÍMENES:
# Definiendo rango de valores
años = [data.fecha_hechos[i].year for i in range(data.shape[0])]
minaños, maxaños = min(años), max(años)



data_d = data_d.dropna()#subset=['lat','lon'])
#st.write(data_d.iloc[200000])


st.sidebar.markdown('# Parámetros:')
# TIPO DEL DELITO
choice = st.sidebar.multiselect('Escoge categoría(s) de crimen', (sorted(list(data_d.delito.unique()))), key='0')
if len(choice) > 0:
	data_d = data_d[data_d.delito.isin(choice)]

# DELEGACIÓN DEL DELITO
dele = st.sidebar.selectbox('Delegación', ['TODAS']+delegaciones, key='ddel')
if dele != 'TODAS':
	data_d = data_d[data_d['alcaldia_hechos'] == dele]


# AÑO DEL DELITO	
#st.sidebar.markdown('Año:')
#if not st.sidebar.checkbox("Todos los años", True, key='1das'):
#	year = st.sidebar.slider("Año", minaños, maxaños)
#	data_d = data_d.dropna()[data_d['fecha_hechos'].dt.year == year]


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


# MOSTRAR CUÁNTOS CRÍMENES HAY CON LOS PARÁMETROS ESPECIFICADOS
st.sidebar.markdown('### {} delitos'.format(data_d.shape[0]))



# MAPEAR
#st.map(data_d.dropna())
st.sidebar.markdown("## Usando parámetros:")
st.sidebar.markdown("### Mapa")
if st.sidebar.checkbox("Mostrar", False, key='mapa'):

	#st.button('Mapear')
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
						get_radius= 25,
					),
				]
			)
		)	
	else:
		st.map(data_d.dropna())


# DISTRIBUCIÓN DE CRÍMENES POR HORA
#st.sidebar.markdown("### Usando parámetros especificados:")
st.sidebar.markdown("### Distribución por hora")
if st.sidebar.checkbox("Mostrar", False, key='dcph'):
	st.markdown("### Distribución por hora")
	horas = [i for i in range(0,24)]
	distribucion = []
	for i,h in enumerate(horas):
		subdata = data_d[data_d['fecha_hechos'].dt.hour == h]
		distribucion.append( subdata.shape[0])
	df = pd.DataFrame(
						{'hora': horas,
						'delitos': distribucion
						})
	fig = px.bar(df, x='hora', y='delitos', height=500) #, color='Crímenes'
	st.plotly_chart(fig)


# DISTRIBUCIÓN DE CRÍMENES POR DIA DE LA SEMANA
st.sidebar.markdown("### Distribución por día de la semana")
if st.sidebar.checkbox("Mostrar", False, key='dcpds'):
	st.markdown("### Distribución por día de la semana")
	dia_semana = [i for i in range(0,7)]
	dia_str = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
	distribucion = []
	for i,d in enumerate(dia_semana):
		subdata = data_d[data_d['fecha_hechos'].dt.dayofweek == d]
		distribucion.append( subdata.shape[0])
	df = pd.DataFrame(
						{'dia': dia_str,
						'delitos': distribucion
						})
	fig = px.bar(df, x='dia', y='delitos', height=500) #, color='Crímenes'
	st.plotly_chart(fig)


# DISTRIBUCIÓN DE CRÍMENES POR MES
st.sidebar.markdown("### Distribución por mes")
if st.sidebar.checkbox("Mostrar", False, key='dpm'):
	st.markdown("### Distribución por mes")
	mes = [i for i in range(1,13)]
	mes_str = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
	distribucion = []
	for i,m in enumerate(mes):
		subdata = data_d[data_d['fecha_hechos'].dt.month == m]
		distribucion.append( subdata.shape[0])
	df = pd.DataFrame(
						{'mes': mes_str,
						'delitos': distribucion
						})
	fig = px.bar(df, x='mes', y='delitos', height=500) #, color='Crímenes'
	st.plotly_chart(fig)