# LusoEnergia · Projeto Final de Análise de Dados

Grupo: Salvador Franco Sequeira (53912) e Ricardo Costa (53732).
Seed = 53912 + 53732 = 107644, janela de análise de 01/02/2008 a 31/07/2009 (18 meses, fim exclusivo em 01/08/2009).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `dados/` | dados brutos do UCI («Individual Household Electric Power Consumption»), nunca alterados |
| `src/dados.py` | carregamento, validação (asserts), janela do grupo, lacunas e consumo diário |
| `01_fundacao.ipynb` | Parte I: carregamento e tipagem (1.1) e auditoria de qualidade (1.2) |

## Dados

O ficheiro de dados não está no repositório (127 MB, acima do limite do GitHub). Descarregar o dataset «Individual Household Electric Power Consumption» do UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) e colocá-lo em:

```
dados/individual+household+electric+power+consumption/household_power_consumption.csv
```

## Como correr

```bash
pip install -r requirements.txt
```

Abrir `01_fundacao.ipynb` a partir da pasta `projeto/` (para o `import src` funcionar) e fazer Restart & Run All.

## Declaração de uso de IA

Claude (Anthropic) foi usado como assistente no Checkpoint 1 para propor a estrutura do notebook, o código de `src/dados.py` e um primeiro rascunho das respostas. (Rever e completar antes da entrega.)
