# LusoEnergia · Projeto Final de Análise de Dados

Grupo: Salvador Franco Sequeira (53912) e Ricardo Costa (53732).
Seed = 53912 + 53732 = 107644, janela de análise de 01/02/2008 a 31/07/2009 (18 meses, fim exclusivo em 01/08/2009).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `dados/` | dados brutos do UCI («Individual Household Electric Power Consumption»), nunca alterados |
| `src/dados.py` | carregamento, validação (asserts), janela do grupo, lacunas e consumo diário |
| `src/sumario.py` | sumário estatístico, outliers (IQR e z robusto), corridas coladas e versão tratada dos dados |
| `src/perfis.py` | estação do ano, tipo de dia e matriz de perfis diários (24 h) |
| `01_fundacao.ipynb` | Parte I: carregamento e tipagem (1.1), auditoria de qualidade (1.2) e sumário estatístico (1.3) |
| `02_compreender.ipynb` | Parte II: sazonalidade e padrão intrigante (2.1), PCA, t-SNE e UMAP (2.2), pergunta livre e plano das Partes III e IV |

## Dados

O ficheiro de dados não está no repositório (127 MB, acima do limite do GitHub). Descarregar o dataset «Individual Household Electric Power Consumption» do UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) e colocá-lo em:

```
dados/individual+household+electric+power+consumption/household_power_consumption.csv
```

## Como correr

Python 3.12 ou 3.13, num ambiente virtual próprio do projeto (a partir da raiz do repositório):

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows; em macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt jupyter
```

Abrir os notebooks a partir da raiz do repositório (para o `import src` funcionar), por ordem, e fazer Restart & Run All. No VS Code, escolher o kernel `.venv`.

## Declaração de uso de IA

Claude (Anthropic) foi usado como assistente no Checkpoint 1 para propor a estrutura do notebook, o código de `src/dados.py` e um primeiro rascunho das respostas.
