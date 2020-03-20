# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Francisco ME
# -- repositorio: https://github.com/IFFranciscoME/LAB_2_JFME
# -- ------------------------------------------------------------------------------------ -- #
import funciones as fn

datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
fn.f_pip_size(param_ins='usdjpy')
datos = fn.f_columnas_datos(param_data=datos)
datos_col = fn.f_columnas_pips(param_data=datos)