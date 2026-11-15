from pathlib import Path

import numpy as np
import pandas as pd

FICHEIRO = (Path(__file__).resolve().parents[1] / 'dados'
            / 'individual+household+electric+power+consumption' / 'household_power_consumption.csv')
VARIAVEIS = ['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity',
             'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
SUBMEDICOES = ['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']


def janela_do_grupo(seed):
    rng = np.random.default_rng(seed)
    inicio = pd.Timestamp(rng.choice(pd.date_range('2007-01-01', '2009-05-01', freq='MS')))
    return inicio, inicio + pd.DateOffset(months=18)


def carregar_dados(caminho=FICHEIRO):
    bruto = pd.read_csv(caminho, sep=';', na_values=['?', ''], keep_default_na=False,
                        dtype={'Date': str, 'Time': str} | {v: 'float32' for v in VARIAVEIS})
    instante = pd.to_datetime(bruto['Date'], format='%d/%m/%Y') + pd.to_timedelta(bruto['Time'])
    df = bruto.drop(columns=['Date', 'Time']).set_index(pd.DatetimeIndex(instante, name='instante'))
    validar(df)
    return df


def recortar(df, janela):
    inicio, fim = janela
    recorte = df[(df.index >= inicio) & (df.index < fim)]
    validar(recorte)
    return recorte


def validar(df):
    obs = df.dropna()
    passos = np.diff(df.index.to_numpy())
    energia_wh = obs['Global_active_power'] * 1000 / 60
    intensidade_estimada = np.hypot(obs['Global_active_power'], obs['Global_reactive_power']) * 1000 / obs['Voltage']

    assert isinstance(df.index, pd.DatetimeIndex), 'o índice tem de ser temporal'
    assert df.index.is_unique and df.index.is_monotonic_increasing, 'índice com instantes repetidos ou fora de ordem'
    assert (passos == np.timedelta64(1, 'm')).all(), 'grelha de 1 min com buracos: há minutos sem linha'
    assert (df.dtypes == 'float32').all(), 'as variáveis numéricas têm de ser float32'
    assert df.isna().any(axis=1).equals(df.isna().all(axis=1)), 'linha com falta parcial (esperado: tudo ou nada)'
    assert (obs.drop(columns='Voltage') >= 0).all().all(), 'potência, intensidade ou energia negativa'
    assert obs['Voltage'].between(200, 260).all(), 'tensão fora de 200 a 260 V (unidade errada?)'
    assert (obs[SUBMEDICOES] % 1 == 0).all().all(), 'submedição não inteira (esperado contador em Wh)'
    assert (obs[SUBMEDICOES].sum(axis=1) <= energia_wh + 3).all(), 'submedições acima da energia total do minuto'
    assert (obs['Global_intensity'] - intensidade_estimada).abs().median() < 0.2, 'I diferente de S/V: unidades incoerentes'


def duracao_lacuna(df):
    falta = df['Global_active_power'].isna()
    bloco = (falta != falta.shift()).cumsum()
    return falta.groupby(bloco).transform('sum')


def lacunas(df):
    duracao = duracao_lacuna(df)
    falta = duracao > 0
    comeca = falta & ~falta.shift(fill_value=False)
    tabela = pd.DataFrame({'inicio': df.index[comeca], 'minutos': duracao[comeca].to_numpy()})
    tabela['fim'] = tabela['inicio'] + pd.to_timedelta(tabela['minutos'] - 1, unit='min')
    return tabela[['inicio', 'fim', 'minutos']]


def tratar_lacunas(df, max_minutos=10):
    curtas = duracao_lacuna(df).between(1, max_minutos)
    tratado = df.copy()
    tratado.loc[curtas] = df.interpolate(method='time').loc[curtas]
    return tratado


def consumo_diario(df, cobertura_min=0.9):
    potencia = df['Global_active_power'].astype('float64')
    dia = pd.DataFrame({'kWh': potencia.resample('D').mean() * 24,
                        'cobertura': potencia.notna().resample('D').mean()})
    dia.loc[dia['cobertura'] < cobertura_min, 'kWh'] = np.nan
    return dia
