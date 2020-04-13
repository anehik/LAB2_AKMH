# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: anehik
# -- repositorio: https://github.com/anehik/LAB2_AKMH.git
# -- ------------------------------------------------------------------------------------ -- #
#%%


#import visualizaciones as vs
import funciones as fn

#%%
#parte2
#%%
# Leer archivo
data = fn.f_leer_archivo('archivo_tradeview_1.xlsx')
#%%
# Columna de los tiempos
fn.f_columna_tiempos(data)
#%%
# Columna de pips
fn.f_columna_pips(data)
#%%
#Estadisticas basicas y ranking
df_estadistic = fn.f_estadistica_ba(data)
#%%
#parte3
# Capital acumulado
cap_acum= fn.f_capital_acm(data)
#%%
# Profits
df_profit = fn.f_profit_diario(data)

#%%
# Estadisticas de metricas de desempeño
df_profit_des = fn.f_estadisticas_mad(data)
#%%
#Parte4
# ocurrencias
sesgos = fn.f_be_de(data)
