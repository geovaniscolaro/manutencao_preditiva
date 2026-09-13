# Arquitetura da Solução

## 1. Visão Geral

A solução proposta é estruturada em duas perspectivas:

1. **Arquitetura da Prova de Conceito (PoC)**, utilizada para análise, treinamento e validação do modelo com os dados disponibilizados.
2. **Arquitetura Industrial**, destinada à implantação contínua da solução em ambiente produtivo.

A PoC demonstra a viabilidade técnica da classificação dos estados operacionais, enquanto a arquitetura industrial incorpora aquisição contínua de dados, qualidade dos sensores, inferência, integração com sistemas corporativos, monitoramento e MLOps.

---

## 2. Arquitetura da PoC

A arquitetura utilizada na prova de conceito pode ser representada por:

```text
Arquivos .npy
     ↓
Carregamento dos Dados
     ↓
Data Quality
     ↓
Análise Exploratória
     ↓
Pré-processamento
     ↓
Processamento de Sinais
     ↓
Feature Engineering
     ↓
Seleção de Sensores
     ↓
Treinamento dos Modelos
     ↓
Comparação Experimental
     ↓
Modelo Final
     ↓
Avaliação e Validação
```

### 2.1 Entrada de Dados

Os dados de entrada são compostos pelos sinais dos sensores e pelas classes correspondentes aos estados de operação.

Na PoC, os arquivos são carregados diretamente em Python a partir dos arquivos disponibilizados para o desenvolvimento do case.

### 2.2 Data Quality

Antes do treinamento, são avaliados:

- dimensões dos dados;
- valores ausentes;
- variabilidade dos sensores;
- consistência das amostras;
- distribuição das classes;
- possíveis problemas de aquisição.

Essa etapa permitiu identificar comportamentos distintos entre os sensores e orientou a seleção das entradas utilizadas pelo modelo.

### 2.3 Pré-processamento

O pré-processamento inclui:

- tratamento de valores ausentes;
- adequação das dimensões das amostras;
- remoção da componente DC;
- aplicação de janela de Hann antes da análise espectral.

### 2.4 Engenharia de Atributos

Foram utilizadas informações dos domínios temporal e espectral.

As características temporais incluem medidas estatísticas, RMS, pico a pico, kurtosis, skewness, máximo absoluto e crest factor.

A representação espectral foi construída utilizando FFT, com resolução de 50 Hz para os dados disponibilizados.

### 2.5 Modelo

O modelo final da PoC utiliza:

- Sensores 1, 2 e 3;
- 24 características temporais;
- 300 características espectrais;
- HistGradientBoostingClassifier.

A representação final possui 324 atributos.

---

## 3. Arquitetura Industrial Proposta

A solução industrial deverá operar de forma contínua, integrando a infraestrutura já existente de automação, instrumentação e software.

```text
┌──────────────────────────────┐
│       Máquina Industrial     │
│                              │
│     Sensores / Instrumentação│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Aquisição / Edge / Automação │
│                              │
│ - aquisição dos sinais       │
│ - timestamp                  │
│ - identificação da máquina   │
│ - identificação do sensor    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Plataforma / Banco de Dados  │
│                              │
│ - dados brutos               │
│ - metadados                  │
│ - histórico                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Data Quality & Sensor Health │
│                              │
│ - dados ausentes             │
│ - sensor constante           │
│ - limites de operação        │
│ - integridade dos sinais     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Pré-processamento        │
│                              │
│ - tratamento de NaN          │
│ - remoção de DC              │
│ - segmentação                │
│ - janela de Hann             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Feature Engineering      │
│                              │
│ - atributos temporais        │
│ - FFT                        │
│ - atributos espectrais       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Modelo de ML            │
│                              │
│ HistGradientBoosting         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       API de Inferência      │
│                              │
│ /predict                     │
│ /health                      │
│ /model-info                  │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌───────────────┐ ┌──────────────────┐
│   Dashboard   │ │ Sistemas         │
│ Operacional   │ │ Industriais      │
└───────────────┘ └──────────────────┘
```

---

## 4. Camadas da Arquitetura

### 4.1 Aquisição e Edge

Responsável por coletar os sinais dos sensores e encaminhá-los para a infraestrutura de dados.

Em uma implantação industrial, cada registro deve possuir metadados mínimos, como:

- identificação da máquina;
- identificação do sensor;
- timestamp;
- frequência de amostragem;
- configuração da aquisição;
- condição de operação;
- lote ou sessão de aquisição, quando aplicável.

Esses metadados são fundamentais para rastreabilidade e validação do modelo.

---

### 4.2 Plataforma de Dados

Responsável pelo armazenamento dos dados de processo e sinais.

A plataforma deve permitir:

- armazenamento dos dados brutos;
- armazenamento dos dados processados;
- rastreabilidade;
- histórico de inferências;
- acesso controlado aos dados;
- recuperação dos dados para novos treinamentos.

---

### 4.3 Data Quality e Sensor Health

Antes que os dados sejam utilizados pelo modelo, uma camada de controle de qualidade deverá verificar automaticamente a integridade dos sinais.

Exemplos de verificações:

- percentual de valores ausentes;
- sinal sem variabilidade;
- valores fora dos limites esperados;
- alteração abrupta da distribuição;
- ausência de dados;
- problemas de sincronização;
- comportamento anormal de sensores.

Essa camada evita que problemas de instrumentação sejam interpretados diretamente como alterações no estado da máquina.

---

## 5. Pipeline de Inferência

O fluxo de inferência poderá ser executado de forma online ou em micro-lotes.

```text
Novo sinal
    ↓
Validação do dado
    ↓
Pré-processamento
    ↓
Extração de características
    ↓
Modelo
    ↓
Classe estimada
    ↓
Probabilidade / confiança
    ↓
Registro da inferência
    ↓
Dashboard / Sistema Industrial
```

O pipeline utilizado em produção deverá ser exatamente compatível com o pipeline utilizado durante o treinamento.

---

## 6. API de Inferência

A disponibilização do modelo por API desacopla a camada de Machine Learning dos sistemas consumidores.

Endpoints propostos:

### `POST /predict`

Recebe os dados necessários para inferência e retorna a classificação estimada.

Exemplo conceitual de resposta:

```json
{
  "predicted_class": "Classe C",
  "confidence": 0.96,
  "model_version": "v1.0",
  "timestamp": "..."
}
```

### `GET /health`

Verifica se o serviço de inferência está operacional.

### `GET /model-info`

Retorna informações como:

- versão do modelo;
- data de treinamento;
- métricas de validação;
- sensores utilizados;
- versão do pipeline.

---

## 7. Dashboard Operacional

O dashboard poderá disponibilizar:

- estado estimado atual da máquina;
- probabilidade das classes;
- histórico das classificações;
- evolução temporal;
- indicadores de sensores;
- alertas de qualidade dos dados;
- versão do modelo em produção;
- indicadores de desempenho da solução.

O dashboard deve atuar como suporte à decisão e não substituir automaticamente a avaliação da equipe de manutenção sem validação operacional prévia.

---

## 8. Persistência das Inferências

Cada inferência deverá ser registrada com informações suficientes para auditoria e análise posterior.

Exemplo:

```text
timestamp
machine_id
sensor_set
model_version
predicted_class
prediction_probability
data_quality_status
```

Esse histórico permitirá avaliar a evolução da máquina, investigar eventos e construir novos conjuntos de treinamento.

---

## 9. MLOps

A solução produtiva deve incorporar mecanismos de monitoramento e gestão do ciclo de vida do modelo.

```text
Dados em Produção
       ↓
Monitoramento
       ↓
┌───────────────────────┐
│ Data Drift            │
│ Model Drift           │
│ Sensor Health         │
│ Qualidade das Entradas│
└───────────┬───────────┘
            ↓
       Avaliação
            ↓
     Necessita atualizar?
        ↓          ↓
       Não        Sim
       ↓           ↓
 Continuar     Novo treinamento
 operação          ↓
                 Validação
                    ↓
               Versionamento
                    ↓
                  Deploy
```

---

## 10. Monitoramento

A solução deverá monitorar pelo menos três grupos de indicadores.

### Dados

- percentual de dados ausentes;
- distribuição das características;
- estabilidade dos sinais;
- comportamento dos sensores.

### Modelo

- distribuição das classes previstas;
- confiança das previsões;
- desempenho quando rótulos reais estiverem disponíveis;
- mudanças relevantes no padrão de inferência.

### Infraestrutura

- disponibilidade da API;
- tempo de resposta;
- erros de processamento;
- volume de inferências.

---

## 11. Retreinamento

O retreinamento não deve ocorrer automaticamente apenas pela passagem do tempo.

A atualização deve ser orientada por evidências, por exemplo:

- degradação de desempenho;
- mudança da distribuição dos dados;
- mudança de processo;
- instalação de novos sensores;
- manutenção significativa na máquina;
- surgimento de novas condições operacionais.

Antes de substituir o modelo em produção, o novo modelo deverá passar por validação e aprovação.

---

## 12. Versionamento

Deverão ser versionados:

- código;
- pipeline de pré-processamento;
- modelo;
- conjunto ou versão dos dados;
- configuração de treinamento;
- métricas;
- documentação.

Esse procedimento permite rastreabilidade e reprodução dos resultados.

---

## 13. Segurança e Governança

Uma implantação industrial deverá ainda considerar:

- autenticação da API;
- controle de acesso;
- registro de operações;
- proteção dos dados;
- gestão de credenciais;
- rastreabilidade das versões;
- políticas de backup;
- segregação entre ambientes de desenvolvimento, homologação e produção.

---

## 14. Evolução da PoC para Produção

A evolução proposta pode ser resumida em:

```text
PoC
 ↓
Validação com dados independentes
 ↓
Pipeline modular
 ↓
Persistência do modelo
 ↓
API de inferência
 ↓
Dashboard
 ↓
Integração com sistemas industriais
 ↓
Monitoramento
 ↓
MLOps
 ↓
Operação assistida
 ↓
Produção
```

A passagem da PoC para produção deverá ocorrer de forma incremental, com validação técnica e operacional em cada etapa.

---

## 15. Consideração Final

A arquitetura foi concebida para separar responsabilidades entre aquisição, dados, processamento, Machine Learning, integração e visualização.

Essa separação facilita manutenção, escalabilidade, monitoramento e evolução da solução.

A PoC atual valida principalmente a camada analítica e de Machine Learning. As demais camadas representam a evolução proposta para uma solução industrial completa.
