# Predictive Maintenance AI

## Proof of Concept for Industrial Equipment Condition Classification

Prova de conceito de uma solução de Inteligência Artificial aplicada ao contexto de **manutenção preditiva industrial**, utilizando sinais adquiridos simultaneamente por múltiplos sensores instalados em uma máquina.

O projeto contempla análise da qualidade dos dados, processamento de sinais, engenharia de atributos, seleção de sensores, comparação de modelos de Machine Learning, validação experimental e proposta de arquitetura para evolução da PoC até uma solução industrial.

---

## 1. Objetivo

Desenvolver um pipeline de Machine Learning capaz de identificar diferentes estados de operação de uma máquina industrial a partir de sinais multissensoriais adquiridos a uma frequência de amostragem de **10 kHz**.

A solução foi desenvolvida como uma **Proof of Concept (PoC)**. Portanto, os resultados apresentados representam evidência de viabilidade técnica sobre o conjunto de dados disponibilizado e não uma estimativa definitiva de desempenho em ambiente produtivo.

---

## 2. Dados

O conjunto disponibilizado contém:

- cinco arquivos correspondentes aos sinais dos sensores;
- um arquivo contendo as classes associadas às observações;
- 50.000 observações;
- cinco classes balanceadas;
- frequência de amostragem de 10 kHz.

Os arquivos originais de dados não são versionados neste repositório.

### Análise de qualidade dos sensores

A inspeção inicial identificou comportamentos distintos entre os sensores:

- **Sensores 1, 2 e 3:** sinais válidos e com informação discriminativa;
- **Sensor 4:** ausência de variabilidade, apresentando valor constante nas observações válidas;
- **Sensor 5:** sinal variável, porém sem contribuição discriminativa relevante para a classificação nesta PoC.

A seleção dos sensores foi baseada tanto em critérios de qualidade dos dados quanto em avaliação experimental.

---

## 3. Pipeline de Machine Learning

O pipeline experimental foi estruturado nas seguintes etapas:

```text
Dados brutos
    ↓
Data Quality
    ↓
Análise Exploratória
    ↓
Pré-processamento
    ↓
Processamento de Sinais
    ↓
Engenharia de Atributos
    ↓
Seleção de Sensores
    ↓
Comparação de Modelos
    ↓
Refinamento da Representação Espectral
    ↓
Modelo Final
    ↓
Avaliação e Validação
```

### Pré-processamento

O processamento inclui:

- tratamento de valores ausentes;
- remoção da componente DC;
- aplicação de janela de Hann;
- Transformada Rápida de Fourier (FFT).

### Engenharia de atributos

Foram investigadas duas categorias principais.

**Domínio temporal:**

- média;
- desvio-padrão;
- RMS;
- pico a pico;
- kurtosis;
- skewness;
- máximo absoluto;
- crest factor.

**Domínio da frequência:**

- frequência dominante;
- centroide espectral;
- energia em bandas;
- representação detalhada da magnitude da FFT.

---

## 4. Seleção dos Sensores

Foi realizado um estudo de ablação para avaliar a contribuição dos sensores.

| Configuração | Accuracy | Macro F1 |
|---|---:|---:|
| Sensor 1 | 57,67% | 57,27% |
| Sensor 2 | 61,32% | 61,25% |
| Sensor 3 | 57,21% | 56,91% |
| Sensor 5 | 20,01% | 20,00% |
| Sensores 1 + 2 + 3 | **81,12%** | **80,99%** |
| Sensores 1 + 2 + 3 + 5 | 79,99% | 79,86% |

Os resultados indicam complementaridade entre os Sensores 1, 2 e 3.

O Sensor 5 apresentou desempenho próximo ao nível de chance para um problema balanceado de cinco classes e sua inclusão reduziu o desempenho do modelo combinado. Por esse motivo, a configuração final utiliza os **Sensores 1, 2 e 3**.

---

## 5. Comparação de Modelos

Utilizando inicialmente atributos temporais e espectrais agregados dos Sensores 1, 2 e 3:

| Modelo | Accuracy | Macro F1 |
|---|---:|---:|
| Random Forest | 81,12% | 80,99% |
| Extra Trees | 81,96% | 81,84% |
| HistGradientBoosting | **84,22%** | **84,17%** |

O **HistGradientBoosting** apresentou o melhor resultado e foi selecionado para os experimentos seguintes.

---

## 6. Análise Temporal × Espectral

Um estudo de ablação foi realizado para avaliar a contribuição dos diferentes domínios de representação.

| Representação | Nº de atributos | Accuracy | Macro F1 |
|---|---:|---:|---:|
| Temporal | 24 | 50,46% | 50,35% |
| Espectral agregada | 24 | 81,64% | 81,58% |
| Temporal + Espectral agregada | 48 | **84,22%** | **84,17%** |

Os resultados demonstraram que a maior parte da informação discriminativa encontra-se no **domínio da frequência**, motivando o refinamento da representação espectral.

---

## 7. Refinamento Espectral

Considerando uma frequência de amostragem de 10 kHz e 200 amostras por observação, a FFT apresenta resolução de **50 Hz**.

Foi utilizada uma representação detalhada da magnitude da FFT entre 50 Hz e 5 kHz:

- 100 atributos espectrais por sensor;
- 3 sensores selecionados;
- 300 atributos de FFT.

A combinação desses atributos com 24 características temporais resultou em uma representação final de **324 atributos**.

---

## 8. Resultados

A evolução experimental foi:

| Experimento | Accuracy |
|---|---:|
| Random Forest — S1 + S2 + S3 + S5 | 79,99% |
| Random Forest — S1 + S2 + S3 | 81,12% |
| HistGradientBoosting — atributos agregados | 84,22% |
| HistGradientBoosting — FFT detalhada | 94,07% |
| **HistGradientBoosting — Temporal + FFT detalhada** | **95,13%** |

### Modelo final

**Sensores:** 1, 2 e 3  
**Representação:** atributos temporais + FFT detalhada  
**Algoritmo:** HistGradientBoosting

Resultados no conjunto de teste estratificado:

- **Accuracy: 95,13%**
- **Macro F1: 95,13%**

O F1-score por classe permaneceu superior a 92%.

### Validação cruzada

Na validação cruzada estratificada com cinco folds:

- **Accuracy média: aproximadamente 94,92%**
- **Macro F1 médio: aproximadamente 94,92%**
- **Desvio-padrão da Accuracy: aproximadamente 0,04 ponto percentual**

A baixa variabilidade entre os folds indica estabilidade do desempenho nos particionamentos avaliados.

---

## 9. Principal Insight Técnico

O maior ganho de desempenho não foi obtido simplesmente pela utilização de um algoritmo de Machine Learning mais complexo.

A evolução de aproximadamente **84,2% para 95,1%** ocorreu principalmente pelo refinamento da **representação dos sinais**, após a análise experimental demonstrar que a informação discriminativa estava predominantemente no domínio da frequência.

A estratégia adotada foi:

```text
Análise
   ↓
Hipótese
   ↓
Experimento
   ↓
Evidência
   ↓
Decisão técnica
```

Essa abordagem orientada por evidências guiou tanto a seleção dos sensores quanto a engenharia de atributos e a escolha do modelo.

---

## 10. Arquitetura Industrial Proposta

A PoC representa apenas a camada analítica inicial de uma solução completa.

A evolução para ambiente industrial é proposta conforme a arquitetura:

```text
Sensores da Máquina
        ↓
Aquisição / Edge
        ↓
Automação e Instrumentação
        ↓
Banco de Dados / Plataforma de Dados
        ↓
Data Quality & Sensor Health
        ↓
Pré-processamento
        ↓
Feature Engineering
   Temporal + FFT
        ↓
Modelo de Machine Learning
 HistGradientBoosting
        ↓
API de Inferência
       /predict
      ↙        ↘
 Dashboard    Sistemas Industriais
```

A arquitetura produtiva deverá incorporar ainda práticas de **MLOps**, incluindo:

```text
Novos dados
    ↓
Monitoramento
    ↓
Data Drift / Model Drift
    ↓
Avaliação
    ↓
Retreinamento
    ↓
Validação
    ↓
Versionamento
    ↓
Deploy
```

---

## 11. Limitações

O conjunto de dados disponibilizado não contém informações suficientes para identificar:

- tipo e posicionamento físico dos sensores;
- rotação da máquina;
- carga de operação;
- significado físico das Classes A–E;
- máquina ou equipamento de origem;
- ensaio ou sessão de aquisição;
- período de aquisição.

Por esse motivo, não são atribuídos diagnósticos físicos específicos às classes ou aos componentes espectrais observados.

Além disso, a ausência de identificadores de máquina, ensaio ou sessão impede uma validação baseada em grupos fisicamente independentes.

Os resultados devem, portanto, ser interpretados como evidência de **viabilidade técnica da PoC** sobre os dados fornecidos.

---

## 12. Evolução para Produção

Em uma implantação industrial, são recomendadas as seguintes etapas:

1. validação da qualidade e confiabilidade dos sensores;
2. definição da estratégia de segmentação dos sinais;
3. integração automatizada com a infraestrutura de dados;
4. validação utilizando máquinas, ensaios ou períodos independentes;
5. desenvolvimento da API de inferência;
6. desenvolvimento de dashboard operacional;
7. armazenamento do histórico de inferências;
8. monitoramento de qualidade dos dados;
9. monitoramento de data drift e model drift;
10. versionamento e governança de modelos;
11. estratégia controlada de retreinamento e redeploy;
12. integração dos resultados ao processo de manutenção.

---

## 13. Estrutura do Repositório

```text
predictive-maintenance-ai/
│
├── api/          # Camada de disponibilização do modelo
├── app/          # Aplicação e visualização
├── data/         # Documentação dos dados
├── docs/         # Arquitetura e documentação
├── models/       # Artefatos de modelos
├── notebooks/    # Análise e desenvolvimento da PoC
├── src/          # Código-fonte do pipeline
│
├── .gitignore
└── README.md
```

O notebook principal está disponível em:

`notebooks/01_PoC_Manutencao_Preditiva.ipynb`

---

## 14. Tecnologias

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib
- Scikit-learn
- Google Colab
- GitHub

Para a evolução da solução para produção, a arquitetura prevê tecnologias para disponibilização via API, visualização, persistência e monitoramento do modelo.

---

## 15. Conclusão

A prova de conceito demonstrou a viabilidade da utilização de processamento de sinais e Machine Learning para classificação dos cinco estados presentes no conjunto de dados disponibilizado.

A solução final alcançou **95,13% de Accuracy e Macro F1** no conjunto de teste estratificado e aproximadamente **94,92% de Accuracy média em validação cruzada de cinco folds**.

Além do desempenho do modelo, a PoC evidencia a importância de qualidade dos dados, seleção de sensores, engenharia de atributos, validação e arquitetura de implantação para a construção de uma solução de Inteligência Artificial industrial robusta.
