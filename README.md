# IA para Manutenção Preditiva Industrial

## Prova de Conceito de Inteligência Artificial para Manutenção Preditiva Industrial

Este repositório apresenta uma **Prova de Conceito (PoC) de Machine Learning aplicada a um cenário de manutenção preditiva industrial**, desenvolvida a partir de sinais multissensoriais de uma máquina.

O projeto contempla o ciclo de desenvolvimento de uma solução de Inteligência Artificial, incluindo **qualidade e análise dos dados, processamento de sinais, engenharia de atributos, avaliação e seleção de sensores, comparação de modelos, validação, demonstração funcional e proposta de arquitetura para evolução da PoC para um ambiente industrial**.

A configuração final utiliza os **Sensores 1, 2 e 3**, combinando características temporais e representação espectral detalhada por **Fast Fourier Transform (FFT)** com o algoritmo **HistGradientBoosting**.

### Principais resultados

| Métrica | Resultado |
|---|---:|
| **Accuracy — conjunto de teste** | **95,13%** |
| **Macro F1 — conjunto de teste** | **95,13%** |
| **Accuracy média — validação cruzada 5-fold** | **94,92%** |
| **Macro F1 médio — validação cruzada 5-fold** | **94,92%** |

> Os resultados representam evidência de viabilidade técnica da PoC sobre o conjunto de dados disponibilizado e não constituem garantia de desempenho em ambiente industrial de produção.

---

## 1. Contexto

O cenário considera uma empresa industrial com máquinas instrumentadas por sensores e sistemas de aquisição.

A camada de automação e instrumentação realiza a aquisição dos sinais, enquanto uma plataforma de software é responsável pelo armazenamento e disponibilização dos dados para a camada de Inteligência Artificial.

O objetivo da PoC é desenvolver e avaliar um pipeline de Machine Learning capaz de classificar os **cinco estados operacionais representados pelas Classes A, B, C, D e E**.

O conjunto disponibilizado possui:

- 50.000 observações;
- cinco classes balanceadas, com 10.000 observações por classe;
- cinco arquivos correspondentes aos sensores;
- frequência de amostragem de **10 kHz**;
- aquisição simultânea dos sensores.

Como não foi disponibilizada a semântica física das Classes A–E, elas são tratadas nesta PoC como **estados operacionais**, sem associá-las arbitrariamente a tipos específicos de falha.

---

## 2. Estratégia de desenvolvimento

A solução foi desenvolvida de forma incremental:

```text
Dados dos sensores
        ↓
Data Quality
        ↓
Análise Exploratória
        ↓
Pré-processamento
        ↓
Engenharia de Atributos
        ↓
Avaliação dos Sensores
        ↓
Comparação de Modelos
        ↓
Análise Temporal × Espectral
        ↓
Refinamento da FFT
        ↓
Modelo Final
        ↓
Validação
        ↓
Demonstração
        ↓
Arquitetura para Produção
```

A estratégia priorizou não apenas a escolha do algoritmo, mas também a **qualidade dos dados, seleção das fontes de informação e representação adequada dos sinais**.

---

## 3. Qualidade dos dados

A análise inicial identificou comportamentos distintos entre os sensores.

### Sensores 1, 2 e 3

Os arquivos foram disponibilizados originalmente com dimensão:

```text
(50000, 201)
```

Foram identificados **49.999 valores ausentes em cada sensor**, concentrados exclusivamente na última coluna, de índice 200.

Como essa coluna apresentava ausência de dados em praticamente todas as observações, ela foi removida antes das etapas subsequentes.

Após o tratamento:

```text
Sensor 1: (50000, 200)
Sensor 2: (50000, 200)
Sensor 3: (50000, 200)
```

Considerando a frequência de amostragem de 10 kHz, as 200 amostras utilizadas correspondem matematicamente a um intervalo de **20 ms**.

Como não foram fornecidos metadados sobre a estratégia original de segmentação das aquisições, não se assume que cada linha corresponda necessariamente a uma janela física independente de aquisição.

### Sensor 4

O Sensor 4 apresentou:

- 10.000 valores ausentes;
- mínimo dos valores válidos: 50,0;
- máximo dos valores válidos: 50,0;
- desvio-padrão: 0;
- apenas um valor válido distinto.

A ausência completa de variabilidade torna o sinal não discriminativo para a classificação nesta PoC.

Por esse motivo, o Sensor 4 não foi utilizado na modelagem.

Em uma aplicação industrial, esse comportamento deveria motivar uma investigação da aquisição, configuração e condição do sensor, sem atribuir uma causa física apenas a partir dos dados disponíveis.

### Sensor 5

O Sensor 5 apresentou **241.512 valores ausentes**, aproximadamente **2,415% dos dados**, mas manteve variabilidade nos valores válidos.

Portanto, ele não foi descartado inicialmente por um problema de variabilidade. Sua contribuição foi posteriormente avaliada de forma experimental durante a seleção dos sensores.

---

## 4. Análise exploratória dos sinais

A análise no domínio do tempo mostrou elevada sobreposição visual entre exemplos das cinco classes.

Características como RMS e desvio-padrão apresentaram diferenças entre as distribuições das classes, porém com sobreposição considerável.

A análise espectral, por sua vez, mostrou diferenças de magnitude entre as classes em diferentes regiões do espectro.

Essas observações motivaram a investigação quantitativa das informações presentes nos domínios **temporal e espectral**.

Como não foram disponibilizadas informações sobre significado físico das classes, tipo e posicionamento dos sensores, rotação, carga ou condições mecânicas da máquina, os componentes espectrais não foram associados a modos específicos de falha.

---

## 5. Engenharia inicial de atributos

Para cada sensor inicialmente considerado foram extraídas características nos domínios do tempo e da frequência.

### Características temporais

Foram utilizadas:

- média;
- desvio-padrão;
- RMS;
- pico a pico;
- kurtosis;
- skewness;
- valor máximo absoluto;
- crest factor.

### Características espectrais agregadas

A representação inicial também incluiu atributos derivados do espectro do sinal.

Com os Sensores 1, 2, 3 e 5, a matriz inicial resultou em:

```text
50.000 observações × 64 atributos
```

Após o pré-processamento e a extração de atributos:

```text
NaNs: 0
Infinitos: 0
Features constantes: 0
```

---

## 6. Avaliação da contribuição dos sensores

Foi realizada uma análise de ablação para avaliar a contribuição individual e combinada dos sensores.

| Configuração | Accuracy | Macro F1 |
|---|---:|---:|
| Sensor 1 | 57,67% | 57,27% |
| Sensor 2 | 61,32% | 61,25% |
| Sensor 3 | 57,21% | 56,91% |
| Sensor 5 | 20,01% | 20,00% |
| **Sensores 1 + 2 + 3** | **81,12%** | **80,99%** |
| Sensores 1 + 2 + 3 + 5 | 79,99% | 79,86% |

Os Sensores 1, 2 e 3 apresentam informações complementares: individualmente possuem desempenho moderado, mas sua combinação alcançou **81,12% de Accuracy**.

O Sensor 5 isoladamente apresentou desempenho próximo ao nível de chance para um problema balanceado de cinco classes. Além disso, sua inclusão reduziu a Accuracy da combinação de 81,12% para 79,99%.

Dessa forma, foram selecionados os **Sensores 1, 2 e 3**, resultando inicialmente em:

```text
50.000 observações × 48 atributos
```

A exclusão do Sensor 5 foi, portanto, baseada em sua contribuição empírica para a classificação, e não simplesmente na presença de valores ausentes.

---

## 7. Comparação de modelos

Utilizando os 48 atributos dos Sensores 1, 2 e 3, foram comparados três algoritmos sob a mesma estratégia de treinamento e teste.

| Modelo | Accuracy | Macro F1 |
|---|---:|---:|
| Random Forest | 81,12% | 80,99% |
| Extra Trees | 81,96% | 81,84% |
| **HistGradientBoosting** | **84,22%** | **84,17%** |

O **HistGradientBoosting** apresentou o melhor desempenho entre os modelos avaliados nessa etapa e foi selecionado para o refinamento da solução.

---

## 8. Contribuição temporal e espectral

As 48 características selecionadas foram separadas em:

```text
24 características temporais
24 características espectrais agregadas
```

A contribuição de cada representação foi então avaliada.

| Representação | Nº de atributos | Accuracy | Macro F1 |
|---|---:|---:|---:|
| Temporais | 24 | 50,46% | 50,35% |
| Espectrais | 24 | 81,64% | 81,58% |
| Temporal + Espectral | 48 | 84,22% | 84,17% |

Os resultados mostram que a maior parte da informação discriminativa está presente no **domínio da frequência**.

Ao mesmo tempo, a combinação com características temporais acrescentou informação complementar, elevando a Accuracy de 81,64% para 84,22%.

Esse resultado motivou o refinamento da representação espectral.

---

## 9. Refinamento espectral por FFT

Para preservar maior detalhamento do conteúdo espectral, foi construída uma representação baseada nos componentes da FFT dos Sensores 1, 2 e 3.

O processamento inclui:

```text
Sinal
  ↓
Tratamento de valores ausentes
  ↓
Remoção da componente DC
  ↓
Janela de Hann
  ↓
FFT
  ↓
Magnitude do espectro
  ↓
Remoção do bin DC
```

Foram mantidos **100 atributos espectrais por sensor**:

```text
100 × 3 = 300 atributos espectrais
```

A representação FFT detalhada apresentou:

```text
Dimensão: (50000, 300)
NaNs: 0
Infinitos: 0
```

Utilizando somente essa representação com HistGradientBoosting:

| Métrica | Resultado |
|---|---:|
| Accuracy | **94,07%** |
| Macro F1 | **94,07%** |

Em comparação com os 84,22% obtidos com características agregadas, o refinamento espectral produziu um ganho de **9,85 pontos percentuais de Accuracy**, mantendo o mesmo tipo de classificador.

---

## 10. Representação e modelo final

A representação final combina:

```text
24 características temporais
+
300 atributos da FFT detalhada
=
324 atributos
```

A matriz final possui:

```text
(50000, 324)
```

O modelo final utiliza:

```text
Sensores: S1 + S2 + S3
Modelo: HistGradientBoostingClassifier
Representação: Temporal + FFT detalhada
```

A divisão holdout foi realizada de forma estratificada:

```text
Treinamento: 80%
Teste:       20%
```

O conjunto de teste contém **10.000 observações**, sendo 2.000 de cada classe.

### Resultado final

| Métrica | Resultado |
|---|---:|
| **Accuracy** | **95,13%** |
| **Macro F1** | **95,13%** |

### Desempenho por classe

| Classe | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Classe A | 97,05% | 97,20% | 97,13% |
| Classe B | 94,07% | 94,45% | 94,26% |
| Classe C | 93,47% | 93,70% | 93,58% |
| Classe D | 98,05% | 98,25% | 98,15% |
| Classe E | 92,98% | 92,05% | 92,51% |

O desempenho é consistente entre as cinco classes, com F1-score superior a 92% em todas elas.

A principal região de confusão ocorre entre as Classes C e E, com 74 observações de C classificadas como E e 74 observações de E classificadas como C.

Sem a semântica física das classes, não é possível associar essa confusão a condições mecânicas específicas.

---

## 11. Evolução experimental

A evolução do pipeline evidencia o impacto das decisões tomadas durante o desenvolvimento.

| Experimento | Accuracy |
|---|---:|
| Random Forest — S1 + S2 + S3 + S5 | 79,99% |
| Random Forest — S1 + S2 + S3 | 81,12% |
| HistGradientBoosting — features agregadas | 84,22% |
| HistGradientBoosting — FFT detalhada | 94,07% |
| **HistGradientBoosting — Temporal + FFT detalhada** | **95,13%** |

O principal ganho ocorreu com o **refinamento da representação dos sinais**, particularmente no domínio da frequência, e não apenas pela substituição do algoritmo de classificação.

---

## 12. Validação cruzada

Foi realizada validação cruzada estratificada com **5 folds**.

### Accuracy por fold

```text
[0.9485, 0.9492, 0.9496, 0.9489, 0.9497]
```

### Resultados médios

| Métrica | Média | Desvio-padrão |
|---|---:|---:|
| Accuracy | **94,92%** | **0,0445 p.p.** |
| Macro F1 | **94,92%** | **0,0456 p.p.** |

A pequena variação entre os folds indica estabilidade do desempenho dentro da estratégia de validação utilizada.

Entretanto, o conjunto disponibilizado não contém identificadores de máquina, sessão, ensaio, período de aquisição ou outros metadados que permitam estabelecer grupos independentes.

Assim, a validação estratificada deve ser interpretada como **avaliação de viabilidade técnica da PoC**, e não como validação definitiva de generalização industrial.

Em produção, a avaliação deverá utilizar dados independentes separados, quando aplicável, por máquina, período de operação, ensaio, lote de aquisição ou condição operacional.

---

## 13. Demonstração funcional

Como **preview da implementação**, foi desenvolvida uma aplicação funcional em **Streamlit**.

A interface permite selecionar uma observação e visualizar:

- classe operacional real;
- classe prevista pelo modelo;
- confiança da classificação;
- distribuição de probabilidades entre as cinco classes.

A demonstração utiliza:

```text
Modelo: HistGradientBoosting
Sensores: S1 + S2 + S3
Representação: 324 atributos
Amostra demonstrativa: 100 observações
Distribuição: 20 observações por classe
```

A Accuracy de 93% observada nas 100 observações da interface refere-se exclusivamente ao subconjunto demonstrativo e **não substitui a avaliação principal de 95,13% obtida nas 10.000 observações do conjunto de teste**.

A aplicação está disponível em:

```text
app/
├── dashboard.py
├── modelo_final.joblib
├── demo_data.csv
└── README.md
```

### Executar a demonstração

A partir da raiz do repositório:

```bash
pip install -r requirements.txt
cd app
streamlit run dashboard.py
```

---

## 14. Arquitetura proposta para produção

A PoC representa a camada analítica e demonstrativa de uma solução que, em produção, deverá ser integrada à infraestrutura industrial.

```text
┌─────────────────────────────┐
│     Máquina Industrial      │
│          Sensores           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Aquisição / Edge / Automação│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Banco / Plataforma de Dados │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Data Quality & Sensor Health│
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Pré-processamento      │
│       Temporal + FFT        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Modelo de Machine       │
│          Learning           │
│ HistGradientBoosting        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      API de Inferência      │
│ /predict | /health | info   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Dashboard / Sistemas        │
│ Industriais / Manutenção    │
└─────────────────────────────┘
```

Uma solução de produção deverá acrescentar mecanismos de:

- persistência das inferências;
- monitoramento da qualidade dos dados e dos sensores;
- versionamento de dados e modelos;
- monitoramento de drift;
- monitoramento de desempenho;
- logging e observabilidade;
- rastreabilidade;
- segurança e controle de acesso;
- CI/CD;
- política de re-treinamento;
- governança do ciclo de vida do modelo.

A arquitetura detalhada está documentada em:

```text
docs/architecture.md
```

---

## 15. Evolução da PoC para produção

A implantação industrial requer etapas adicionais além do desempenho do classificador.

### Engenharia de dados

- integração com a fonte de dados industrial;
- validação automática dos dados;
- sincronização dos sensores;
- armazenamento histórico;
- rastreabilidade das aquisições.

### Machine Learning

- definição da semântica industrial das classes;
- validação com máquinas e períodos independentes;
- análise do custo dos diferentes tipos de erro;
- versionamento do modelo;
- monitoramento de drift;
- política de re-treinamento.

### Software e integração

- API de inferência;
- persistência das predições;
- dashboard operacional;
- integração com sistemas corporativos;
- testes automatizados;
- observabilidade.

### Operação

- definição de responsáveis;
- níveis de criticidade;
- regras para tratamento de alertas;
- procedimentos de manutenção;
- acompanhamento de indicadores.

---

## 16. Cronograma proposto

Foi elaborado um cronograma preliminar de **16 semanas**, sujeito a refinamento após o levantamento detalhado dos requisitos e diagnóstico do ambiente industrial.

| Fase | Período |
|---|---|
| Kickoff, requisitos e diagnóstico | Semanas 1–2 |
| Engenharia e qualidade dos dados | Semanas 2–4 |
| EDA e baseline | Semanas 3–5 |
| Feature engineering e modelagem | Semanas 5–8 |
| Validação e seleção do modelo | Semanas 8–10 |
| Industrialização do pipeline | Semanas 9–12 |
| API, persistência e dashboard | Semanas 11–13 |
| Integração e homologação | Semanas 13–15 |
| Operação assistida e entrega | Semana 16 |

A proposta utiliza entregas incrementais e checkpoints técnicos ao longo do desenvolvimento.

O cronograma detalhado está disponível em:

```text
docs/schedule.md
```

---

## 17. Estrutura do repositório

```text
manutencao_preditiva/
│
├── app/
│   ├── dashboard.py
│   ├── demo_data.csv
│   ├── modelo_final.joblib
│   └── README.md
│
├── data/
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── schedule.md
│   └── README.md
│
├── models/
│   └── README.md
│
├── notebooks/
│   ├── 01_PoC_Manutencao_Preditiva.ipynb
│   └── README.md
│
├── src/
│   └── README.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

Os arquivos brutos `.npy` fornecidos para o desenvolvimento da PoC **não são versionados no repositório**.

A pasta `app/` contém apenas os artefatos necessários para execução da demonstração.

---

## 18. Tecnologias utilizadas

- Python
- NumPy
- Pandas
- SciPy
- scikit-learn
- Matplotlib
- Joblib
- Streamlit

A arquitetura proposta para produção prevê adicionalmente uma camada de API e componentes de integração, persistência, monitoramento e MLOps.

---

## 19. Reproduzindo a PoC

Instale as dependências:

```bash
pip install -r requirements.txt
```

O pipeline completo de análise, treinamento e avaliação está disponível em:

```text
notebooks/01_PoC_Manutencao_Preditiva.ipynb
```

Os dados brutos não estão incluídos no repositório.

Para executar apenas a demonstração, não é necessário reexecutar o treinamento:

```bash
cd app
streamlit run dashboard.py
```

---

## 20. Principais conclusões

A PoC demonstrou que:

1. **qualidade dos dados deve preceder a modelagem**, como evidenciado pela inconsistência estrutural dos Sensores 1, 2 e 3 e pela ausência de variabilidade do Sensor 4;

2. **mais sensores não significam necessariamente melhor desempenho**, como demonstrado experimentalmente pelo Sensor 5;

3. os **Sensores 1, 2 e 3 apresentam informações complementares**;

4. a informação no **domínio da frequência é particularmente relevante** para a classificação dos estados operacionais;

5. o refinamento da representação espectral elevou a Accuracy de **84,22% para 94,07%**, mantendo o HistGradientBoosting;

6. a combinação da FFT detalhada com características temporais elevou o resultado final para **95,13% de Accuracy e 95,13% de Macro F1**;

7. a validação cruzada apresentou resultado médio de **94,92%**, com baixa variação entre os folds;

8. a implantação industrial requer, além do modelo, **engenharia de dados, integração, validação independente, monitoramento, observabilidade, segurança e governança**.

---

## Conclusão

A solução apresentada demonstra uma abordagem de ponta a ponta para aplicação de Inteligência Artificial em um cenário de manutenção preditiva industrial.

Mais do que alcançar uma métrica elevada de classificação, a PoC evidencia um processo de engenharia orientado por **qualidade dos dados, processamento de sinais, experimentação, avaliação quantitativa, seleção de informações, validação e planejamento da evolução para produção**.

O resultado final de **95,13% de Accuracy e 95,13% de Macro F1**, aliado à estabilidade observada na validação cruzada, demonstra viabilidade técnica para continuidade do desenvolvimento.

A evolução para uma solução industrial deverá ser condicionada à definição da semântica operacional das classes, validação com dados independentes e integração do pipeline de Inteligência Artificial ao ambiente de produção.
