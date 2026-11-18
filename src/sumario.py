from math import comb

import numpy as np
import pandas as pd

from src.dados import VARIAVEIS, tratar_lacunas

LIMIAR_ASSIMETRIA = 0.5   # |assimetria| acima disto: a média deixa de representar o valor típico


def resumo_forma(df, variaveis=VARIAVEIS):
    """Localização, dispersão e forma de cada variável (ignora NaN).

    mad: mediana dos desvios absolutos à mediana (dispersão robusta).
    medida_adequada: mediana + IQR se |assimetria| > LIMIAR_ASSIMETRIA, média + desvio-padrão se não.
    """
    linhas = {}
    for v in variaveis:
        x = df[v].dropna().astype('float64')
        q1, q3 = x.quantile([0.25, 0.75])
        assimetria = x.skew()
        linhas[v] = {'n': len(x), 'media': x.mean(), 'mediana': x.median(), 'desvio': x.std(),
                     'mad': (x - x.median()).abs().median(), 'iqr': q3 - q1,
                     'assimetria': assimetria, 'curtose_excesso': x.kurt(), '%_zeros': 100 * (x == 0).mean(),
                     'medida_adequada': 'mediana + IQR' if abs(assimetria) > LIMIAR_ASSIMETRIA else 'média + desvio'}
    return pd.DataFrame(linhas).T


def zscore_robusto(serie):
    """0,6745 × (x − mediana) / MAD. Se MAD = 0 (mais de metade dos valores iguais) não está definido: devolve NaN."""
    x = serie.astype('float64')
    mediana = x.median()
    mad = (x - mediana).abs().median()
    if mad == 0:
        return pd.Series(np.nan, index=x.index)
    return 0.6745 * (x - mediana) / mad


def outliers_iqr(serie, k=1.5):
    """True onde o valor sai de [Q1 − k·IQR, Q3 + k·IQR]. NaN nunca é outlier."""
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (serie < q1 - k * iqr) | (serie > q3 + k * iqr)


def eventos(mascara, separacao='30min'):
    """Agrupa os instantes True de uma máscara em eventos.

    Instantes consecutivos separados por no máximo `separacao` ficam no mesmo evento
    ('30min' para minutos, '1D' para dias). Devolve inicio, fim e n.º de instantes True.
    """
    instantes = mascara.index[mascara.to_numpy(dtype=bool)]
    if len(instantes) == 0:
        return pd.DataFrame(columns=['inicio', 'fim', 'n_true'])
    novo = np.r_[True, np.diff(instantes.to_numpy()) > pd.Timedelta(separacao).to_timedelta64()]
    grupo = np.cumsum(novo)
    t = pd.Series(instantes, index=instantes)
    tabela = t.groupby(grupo).agg(inicio='min', fim='max')
    tabela['n_true'] = t.groupby(grupo).size()
    return tabela.reset_index(drop=True)


def mascara_corridas_constantes(df, minimo=30):
    """True nos minutos que pertencem a uma corrida de `minimo` ou mais linhas IDÊNTICAS (as 7 variáveis iguais ao minuto anterior)."""
    igual = (df == df.shift()).all(axis=1) & df.notna().all(axis=1)
    bloco = (~igual).cumsum()
    tamanho = bloco.groupby(bloco).transform('size')
    return (tamanho >= minimo) & df.notna().all(axis=1)


def corridas_constantes(df, minimo=30):
    """Tabela (inicio, fim, minutos) das corridas de linhas idênticas com pelo menos `minimo` minutos."""
    mascara = mascara_corridas_constantes(df, minimo)
    return eventos(mascara, separacao='1min').rename(columns={'n_true': 'minutos'})


def pivot_hora_dia(serie):
    """Média e n (minutos com leitura) por hora do dia (linhas) × dia da semana (colunas, 0 = segunda)."""
    chaves = [serie.index.hour.rename('hora'), serie.index.dayofweek.rename('dia_semana')]
    grupos = serie.groupby(chaves)
    return grupos.mean().unstack(), grupos.count().unstack()


def p_binomial(n, k, p):
    """P(X >= k) para X ~ Binomial(n, p): probabilidade de ver k ou mais casos por acaso."""
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


def dados_tratados(df, max_minutos=10, minimo_colada=30):
    """Versão da janela pronta para análise: lacunas até `max_minutos` interpoladas (1.2e) e
    corridas de `minimo_colada` ou mais minutos idênticos anuladas (1.3d)."""
    limpo = tratar_lacunas(df, max_minutos)
    return limpo.mask(mascara_corridas_constantes(limpo, minimo_colada))
