# Cronograma de Execução do Projeto

## 1. Visão Geral

A execução do projeto é proposta de forma incremental, partindo da validação
dos dados e requisitos até a implantação assistida da solução.

O cronograma preliminar considera **16 semanas**, podendo ser ajustado após
a etapa inicial de diagnóstico, conforme complexidade da infraestrutura,
disponibilidade de dados, requisitos de integração e critérios de aceite
definidos com a empresa.

A estratégia busca reduzir riscos por meio de entregas intermediárias e
validação contínua com as equipes de manutenção, automação, instrumentação,
software e negócio.

---

## 2. Fases do Projeto

| Fase | Atividade principal | Semanas | Entregável principal |
|---|---|---:|---|
| 1 | Kickoff, requisitos e diagnóstico | 1–2 | Documento de requisitos e plano de execução |
| 2 | Engenharia e qualidade dos dados | 2–4 | Dataset validado e relatório de Data Quality |
| 3 | Análise exploratória e baseline | 3–5 | EDA e modelo baseline |
| 4 | Engenharia de atributos e modelagem | 5–8 | Pipeline de ML e modelos candidatos |
| 5 | Validação e seleção do modelo | 8–10 | Modelo candidato validado |
| 6 | Industrialização do pipeline | 9–12 | Pipeline modular e artefato versionado |
| 7 | API, persistência e dashboard | 11–13 | Protótipo integrado |
| 8 | Integração e homologação | 13–15 | Solução homologada em ambiente controlado |
| 9 | Operação assistida e entrega | 16 | Entrega técnica e plano de evolução |

As fases possuem sobreposição intencional para permitir desenvolvimento
iterativo e reduzir o tempo total do projeto.

---

## 3. Cronograma Detalhado

### Fase 1 — Kickoff, Requisitos e Diagnóstico
**Semanas 1–2**

Atividades:

- reunião de kickoff;
- identificação dos stakeholders;
- levantamento dos objetivos de negócio;
- entendimento do processo de manutenção;
- identificação das máquinas e ativos envolvidos;
- levantamento dos sensores e infraestrutura disponível;
- entendimento do banco de dados existente;
- definição dos estados ou eventos que deverão ser identificados;
- levantamento de restrições técnicas;
- definição preliminar das métricas de sucesso;
- identificação de requisitos de integração, segurança e disponibilidade.

**Entregáveis:**

- documento de requisitos;
- mapa das fontes de dados;
- arquitetura inicial;
- critérios preliminares de aceite;
- plano refinado de execução.

**Marco M1 — Requisitos e escopo validados**

---

### Fase 2 — Engenharia e Qualidade dos Dados
**Semanas 2–4**

Atividades:

- acesso e entendimento das fontes de dados;
- análise de integridade;
- avaliação de valores ausentes;
- avaliação da variabilidade dos sensores;
- sincronização temporal;
- análise de frequência de amostragem;
- avaliação de consistência dos rótulos;
- identificação de períodos, máquinas, ensaios e condições operacionais;
- definição das regras de Data Quality;
- definição da estratégia de segmentação.

**Entregáveis:**

- relatório de qualidade dos dados;
- regras de validação;
- dataset preparado para experimentação;
- documentação dos problemas encontrados.

**Marco M2 — Dados considerados adequados para modelagem**

Caso os dados não apresentem qualidade suficiente, o projeto retorna à
instrumentação, aquisição ou preparação dos dados antes de avançar para
modelagem.

---

### Fase 3 — Análise Exploratória e Baseline
**Semanas 3–5**

Atividades:

- análise estatística;
- análise temporal dos sinais;
- análise espectral;
- avaliação das distribuições;
- análise das classes;
- identificação de padrões;
- construção de um modelo baseline;
- definição do protocolo de validação.

**Entregáveis:**

- relatório de análise exploratória;
- baseline de desempenho;
- protocolo experimental.

**Marco M3 — Baseline e protocolo de validação aprovados**

---

### Fase 4 — Engenharia de Atributos e Modelagem
**Semanas 5–8**

Atividades:

- desenvolvimento do pré-processamento;
- engenharia de atributos temporais;
- engenharia de atributos espectrais;
- seleção e avaliação dos sensores;
- treinamento de modelos candidatos;
- ajuste de hiperparâmetros quando necessário;
- comparação de desempenho;
- análise de custo computacional;
- análise de interpretabilidade e requisitos de inferência.

Modelos candidatos poderão incluir, conforme os dados:

- Random Forest;
- Extra Trees;
- Gradient Boosting;
- HistGradientBoosting;
- outros algoritmos adequados identificados durante a experimentação.

**Entregáveis:**

- pipeline experimental;
- matriz comparativa dos modelos;
- conjunto de atributos selecionado;
- modelo candidato.

---

### Fase 5 — Validação e Seleção do Modelo
**Semanas 8–10**

Atividades:

- validação do modelo;
- análise de Accuracy, Precision, Recall e F1-score;
- matriz de confusão;
- análise de erros;
- avaliação por máquina, período ou ensaio independente, quando os metadados permitirem;
- análise de robustez;
- definição dos thresholds operacionais quando aplicável;
- avaliação conjunta com especialistas da empresa.

**Entregáveis:**

- relatório de validação;
- modelo selecionado;
- critérios de aceite técnico.

**Marco M4 — Modelo aprovado para industrialização**

O avanço para implantação somente deverá ocorrer caso os critérios de
desempenho e robustez acordados sejam atendidos.

---

### Fase 6 — Industrialização do Pipeline
**Semanas 9–12**

Atividades:

- modularização do código;
- separação entre treinamento e inferência;
- automatização do pré-processamento;
- persistência do modelo;
- versionamento dos artefatos;
- criação de testes;
- tratamento de exceções;
- logging;
- documentação técnica.

**Entregáveis:**

- pipeline modular;
- artefato do modelo;
- código versionado;
- documentação de execução;
- testes básicos do pipeline.

---

### Fase 7 — API, Persistência e Dashboard
**Semanas 11–13**

Atividades:

- desenvolvimento da API de inferência;
- endpoint de predição;
- endpoint de health check;
- identificação da versão do modelo;
- persistência das inferências;
- desenvolvimento do dashboard;
- visualização dos estados estimados;
- histórico de inferências;
- indicadores de qualidade dos sensores.

**Entregáveis:**

- API funcional;
- estrutura de persistência;
- dashboard funcional;
- documentação dos endpoints.

**Marco M5 — Protótipo integrado disponível**

---

### Fase 8 — Integração e Homologação
**Semanas 13–15**

Atividades:

- integração com a infraestrutura da empresa;
- testes de comunicação;
- testes de carga quando necessários;
- avaliação de latência;
- validação do fluxo ponta a ponta;
- testes de falha;
- ajustes de segurança;
- homologação com usuários;
- ajustes finais.

**Entregáveis:**

- solução integrada;
- relatório de testes;
- registro de não conformidades e correções;
- versão candidata à produção.

**Marco M6 — Solução homologada**

---

### Fase 9 — Operação Assistida e Entrega
**Semana 16**

Atividades:

- implantação controlada;
- acompanhamento inicial;
- treinamento dos usuários;
- transferência de conhecimento;
- documentação final;
- definição dos indicadores de monitoramento;
- definição do processo de suporte;
- definição da estratégia de atualização do modelo.

**Entregáveis:**

- solução implantada em ambiente acordado;
- documentação técnica;
- documentação operacional;
- treinamento;
- plano de monitoramento e evolução.

**Marco M7 — Encerramento da implantação inicial**

---

## 4. Visão Temporal

```text
Atividade                                  01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
------------------------------------------------------------------------------------------------
Requisitos e diagnóstico                   ██ ██
Engenharia / qualidade dos dados              ██ ██ ██
EDA e baseline                                   ██ ██ ██
Feature engineering / modelagem                        ██ ██ ██ ██
Validação do modelo                                             ██ ██ ██
Industrialização do pipeline                                       ██ ██ ██ ██
API / persistência / dashboard                                           ██ ██ ██
Integração e homologação                                                       ██ ██ ██
Operação assistida / entrega                                                            ██
```

O cronograma representa uma referência inicial. Atividades podem ocorrer
em paralelo quando não houver dependência técnica impeditiva.

---

## 5. Critérios de Sucesso

Os critérios definitivos deverão ser acordados com a empresa durante a
fase de requisitos.

Como referência, deverão considerar:

### Desempenho do modelo

- métricas por classe;
- Macro F1;
- taxa de falsos positivos e falsos negativos;
- desempenho em dados independentes.

### Qualidade dos dados

- disponibilidade dos sensores;
- percentual de dados válidos;
- consistência da aquisição;
- rastreabilidade.

### Desempenho operacional

- disponibilidade do serviço;
- latência de inferência;
- capacidade de processamento;
- estabilidade da integração.

### Valor para manutenção

- capacidade de identificar condições relevantes;
- antecedência útil para tomada de decisão, quando aplicável;
- redução de inspeções desnecessárias;
- suporte ao planejamento de manutenção.

Não é recomendado definir antecipadamente uma meta única de Accuracy sem
considerar o custo operacional dos diferentes tipos de erro.

---

## 6. Gestão de Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Dados insuficientes ou inconsistentes | Alto | Data Quality antes da modelagem e revisão da aquisição |
| Problemas ou falhas de sensores | Alto | Sensor Health e regras automáticas de validação |
| Rótulos incorretos | Alto | Validação com especialistas e rastreabilidade |
| Data leakage | Alto | Separação adequada de treinamento e validação |
| Baixa generalização | Alto | Validação por máquina, período ou ensaio independente |
| Mudança do processo | Médio/Alto | Monitoramento de drift |
| Integração complexa | Médio | API desacoplada e testes incrementais |
| Latência incompatível | Médio | Benchmark e otimização do pipeline |
| Baixa adoção pelos usuários | Médio | Envolvimento da manutenção desde as fases iniciais |

---

## 7. Governança do Projeto

São propostas reuniões periódicas de acompanhamento com representantes de:

- manutenção;
- automação e instrumentação;
- software/TI;
- dados/IA;
- negócio ou gestão industrial.

O acompanhamento deverá considerar:

- atividades concluídas;
- atividades em andamento;
- riscos;
- impedimentos;
- decisões técnicas;
- resultados experimentais;
- próximos entregáveis.

As decisões relevantes deverão ser registradas para manter rastreabilidade
ao longo do projeto.

---

## 8. Estratégia de Entrega

A implantação não é tratada como uma única entrega ao final das 16 semanas.

A estratégia proposta utiliza entregas incrementais:

```text
Requisitos
    ↓
Dados validados
    ↓
Baseline
    ↓
Modelo candidato
    ↓
Modelo validado
    ↓
Pipeline industrializado
    ↓
Protótipo integrado
    ↓
Homologação
    ↓
Operação assistida
```

Cada marco funciona como um ponto de decisão para confirmar a continuidade,
revisar premissas ou corrigir problemas antes da etapa seguinte.

---

## 9. Relação com a PoC Desenvolvida

A prova de conceito já antecipa parte das fases de:

- Data Quality;
- análise exploratória;
- processamento de sinais;
- engenharia de atributos;
- seleção de sensores;
- comparação de modelos;
- avaliação;
- validação cruzada.

Na execução contratada, essas etapas deverão ser repetidas e aprofundadas
utilizando dados industriais acompanhados dos metadados necessários para
uma validação representativa do ambiente real.

---

## 10. Consideração Final

O cronograma de 16 semanas deve ser entendido como um planejamento inicial
para evolução da PoC até uma primeira implantação industrial controlada.

A duração definitiva dependerá principalmente da disponibilidade e qualidade
dos dados, maturidade da infraestrutura existente, requisitos de integração
e critérios de homologação definidos com a empresa.
