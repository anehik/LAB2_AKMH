# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: anehik
# -- repositorio: https://github.com/anehik/LAB2_AKMH.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd
import numpy as np
# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
def f_leer_archivo(param_archivo):
    """
    Parameters
    ----------
    pa´´
    ram_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.csv'
    """
    df_data = pd.read_csv('archivos/' + param_archivo)
    df_data.columns = [i.lower() for i in list(df_data.columns)]
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)
    return df_data
# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento
def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : nombre de instrumento
    Returns
    -------
    Debugging
    -------
    param_ins = 'usdjpy'
    """
    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')
    # transformar a minusculas
    inst = param_ins.lower()
    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}
    return pips_inst[inst]
# -- ------------------------------------------------------ FUNCION: Convertir a datetime -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- convertir los datos de fechas en formato datetime
def f_columnas_tiempos(param_data):
    """
    Parameters:
    param_data : str : nombre del archivo a leer.
    Return : pd DataFrame :
    Debugging
    --------
    param_data = datos
    """
    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]
    return param_data
# -- ------------------------------------------------------------ FUNCION: Columnas Pips --- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Calcula los pips acumulados y el profit acumulado.
def f_columnas_pips(datos):
    datos['pips_acm'] = [(datos.closeprice[i]-datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips_acm'][datos.type=='sell'] *= -1
    datos['profit_acm'] = datos['profit'].cumsum()
    return datos
# -- ------------------------------------------------------ FUNCION: Estadísticas básicas -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Calcula algunas estadísticas entre las operaciones generadas.
def f_estadisticas_ba(datos):
    return pd.DataFrame({
        'Ops totales': [len(datos['order']), 'Operaciones totales'],
        'Ganadoras': [len(datos[datos['pips_acm']>=0]), 'Operaciones ganadoras'],
        'Ganadoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de compra'],
        'Ganadoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de venta'],
        'Perdedoras': [len(datos[datos['pips_acm'] < 0]), 'Operaciones perdedoras'],
        'Perdedoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de compra'],
        'Perdedoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de venta'],
        'Mediana_profit': [datos['profit'].median(), 'Mediana de rendimeintos de las operaciones'],
        'Mediana_pips': [datos['pips_acm'].median(), 'Mediana de pips de las operaciones'],
        'r_efectividad': [len(datos[datos['pips_acm']>=0])/len(datos['order']),
                          'Operaciones Totales Vs Ganadoras Totales'],
        'r_proporcion': [len(datos[datos['pips_acm']>=0])/len(datos[datos['pips_acm'] < 0]),
                            'Ganadoras Totales Vs Perdedoras Totales'],
        'r_efectividad_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)])/len(datos['order']),
                            'Totales Vs Ganadoras Compras'],
        'r_efectividad_v': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)])/len(datos['order']),
                            'Totales Vs Ganadoras Ventas']
    })

# Parte 3) Calcular Medidas de Atribución al Desempeño expresadas semanalmente de una cuenta de trading y
# de la actividad del trader como persona.

def f_columna_capital_acm(param_data):
    """
    Parameters
    ---------
    :param:
        param_data: DataFrame : archivo de operaciones
    Returns
    ---------
    :return:
        param_data: DataFrame : archivo de operaciones
    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    param_data['capital_acm'] = [float(5000.0 + param_data['profit_acm'][i]) for i in
                                 range(len(param_data['profit_acm']))]
    return param_data

#Funcion para sacar las perdidas o ganacias diarias

def f_profit_diario(param_data):
    """
    Parameters
    ---------
    :param
        param_data: DataFrame : archivo
    Returns
    ---------
    :return:
        df_profit: DataFrame
    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    dates = pd.DataFrame(
        {
            'timestamp': (pd.date_range(param_data['closetime'].min(),
                                        param_data['closetime'].max(), normalize=True))
        }
    )
    profit_d = pd.DataFrame(
        [
            [i[0],
             round(sum(i[1]['profit']), 2)
             ] for i in (list(param_data.groupby(pd.DatetimeIndex
                                                 (param_data['closetime']).normalize())))],
        columns=['timestamp', 'profit_d'])
    df_profit = dates.merge(profit_d, how='outer', sort=True).fillna(0)
    df_profit['profit_acm'] = round(5000.0 + np.cumsum(df_profit['profit_d']), 2)
    return df_profit



#Funcion para calcular rendimientos diarios:

def log_dailiy_rends(param_profit):
    """
    Parameters
    ---------
    :param
        param_profit: DataFrame : archivo
    Returns
    ---------
    :return:
        df: DataFrame
    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    param_profit['rends'] = np.log(
        param_profit['profit_acm'] /
        param_profit['profit_acm'].shift(1)).iloc[1:]
    return param_profit

'''Funcion para sacar las Medidas de Atribución al Desempeño
    1.- Sharpe Ratio: (rp - rf)/std
    2.- Sortino Ratio: (rp - rf)/std(-)
'''

def f_estadisticas_mad(param_profit):
    rp = param_profit['rends']
    rf = 0.08 / 12
    benchmark = 0.10
    df_estadistic = pd.DataFrame(
        {
            'Sharpe':
                [(rp.mean() - rf) / rp.std()],
            'Sortino_c':
                [(rp.mean() - rf) / rp[rp < 0].std()],
            'Sortino_v':
                [(rp.mean() - rf) / rp[rp > 0].std()],
            'Drawdown_capi_c':
                [1 - param_profit['profit_acm'].min() / 5000],
            'Drawdown_capi_u':
                [1 - param_profit['profit_acm'].max() / 5000],
            'Information':
                [rp.mean() / benchmark]
        }
    )
    return df_estadistic.T

