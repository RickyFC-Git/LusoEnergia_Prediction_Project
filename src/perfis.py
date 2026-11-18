import numpy as np
import pandas as pd

ESTACOES = ['inverno', 'primavera', 'verão', 'outono']
_MES_ESTACAO = {12: 'inverno', 1: 'inverno', 2: 'inverno', 3: 'primavera', 4: 'primavera', 5: 'primavera',
                6: 'verão', 7: 'verão', 8: 'verão', 9: 'outono', 10: 'outono', 11: 'outono'}


def estacao_do_ano(indice):
    """Estação meteorológica (inverno = dez-fev, primavera = mar-mai, verão = jun-ago, outono = set-nov)."""
    return pd.Series(indice.month, index=indice).map(_MES_ESTACAO)


def tipo_de_dia(indice):
    """'dia útil' (segunda a sexta) ou 'fim de semana' (sábado e domingo)."""
    return pd.Series(np.where(indice.dayofweek < 5, 'dia útil', 'fim de semana'), index=indice)


def matriz_perfis(serie):
    """Uma linha por dia, 24 colunas com a média da `serie` em cada hora.

    Para a potência ativa (kW), a média de uma hora é a energia consumida nessa hora (kWh).
    Dias com alguma hora sem leitura (NaN) são descartados: a PCA não aceita NaN e
    preencher horas inteiras seria inventar dados.
    """
    horaria = serie.resample('h').mean()
    perfis = horaria.groupby([horaria.index.normalize(), horaria.index.hour]).first().unstack()
    perfis.columns.name = 'hora'
    perfis.index.name = 'dia'
    return perfis.dropna()
