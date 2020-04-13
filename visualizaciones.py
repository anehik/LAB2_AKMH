
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - graficas para el proyecto
# -- mantiene: anehik
# -- repositorio: https://github.com/anehik/LAB2_AKMH.git
# -- ------------------------------------------------------------------------------------ -- #

import plotly.graph_objects as go
import plotly.io as pio                           # renderizador para visualizar imagenes
pio.renderers.default = "browser"                 # render de imagenes para correr en script
import plotly.express as px
import pandas as pd
import funciones as fn
from principal import df_profit
from funciones import f_drawdown
import principal as prin

#%%
'''Gráfica 1: Ranking
+ Una gráfica de pastel (pie chart) con la información del dataframe que obtienes al mandar llamar la función df_1_ranking.

+ Leyenda en la parte derecha de la gráfica.

+ El valor más grande de la gráfica está "extraido" o "flotando" fuera del pastel

Nota: Revisa la sección de "Pie chart" y dentro busca la parte donde dice "Pulling sectors out from the center" en la documentación oficial en línea de plotly'''   
#Grafico de pastel 

rank = pd.DataFrame(prin.df_estadistic['ranking'])
rank['index']=rank.index
fig1 = go.Figure()
labels = rank.index
values = rank.ranking
fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0])])
fig1.update_layout(title='RANKING')
fig1.show()
#%%
'''Gráfica 2: DrawDown y DrawUp
+ Una gráfica de linea de color negro que represente la evolución del capital acumulado diario

+ Una línea recta punteada de color verde que represente el DrawUp, que va desde la fecha inicial hasta la fecha final de ocurrencia del máximo DrawUp.

+ Una línea recta punteada de color rojo que represente el DrawDown, que va desde la fecha inicial hasta la fecha final de ocurrencia del máximo DrawDown.'''
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_profit.timestamp, y=df_profit.profit_acm_d, mode = 'lines',
                             name = 'profit diario', line=dict(color='black')))
fig2.show()
#%%
fig2.add_trace(go.Scatter(x=df_profit['timestamp'][down[1:]], 
                          y=df_profit['profit_acm_d'][down[1:]],
                          mode='lines', name = 'drawdown', line=dict(color='Red',dash='dash')))
fig2.add_trace(go.Scatter(x=df_profit['timestamp'][up[1:]], y=df_profit['profit_acm_d'][up[1:]], mode='lines', name = 'drawup',line=dict(color='Green',dash='dash')))
fig2.update_layout(
        title="DrawUp y DrawDown",
        xaxis_title="Tiempo",
        yaxis_title="Portfolio acumulado diario",
        )
fig2.show()

#%%
'''Gráfica 3: Disposition Effect
+ Una gráfica de barras verticales

+ Hay 3 barras, cada una representa la cantidad de veces que se observó cada principio del disposition effect

+ Cada barra tendrá de nombre en el eje de las X los siguientes: status_quo, aversion_perdida, sensibilidad_decreciente'''
res = pd.DataFrame(sesgos['resultados'])
res['index1']=res.index
fig3 = go.Figure()
fig3 = px.bar(x=res.index1, y=res.Valor)
fig3.update_layout(
    title="Sesgos",
    xaxis_title="Variables",
    yaxis_title="cantidad/porcentage",
    )
fig3.show()