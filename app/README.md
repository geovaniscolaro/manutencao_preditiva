# Demonstração — Streamlit

Esta pasta contém a aplicação demonstrativa desenvolvida como preview da
camada de disponibilização da solução de Machine Learning para manutenção
preditiva.

## Arquivos

- `dashboard.py` — aplicação desenvolvida em Streamlit;
- `modelo_final.joblib` — modelo HistGradientBoosting treinado;
- `demo_data.csv` — subconjunto balanceado com 100 observações utilizado para
  demonstração da inferência.

## Funcionalidades

A interface permite selecionar uma observação e visualizar:

- classe operacional real;
- classe prevista pelo modelo;
- confiança da classificação;
- probabilidades associadas às cinco classes.

O modelo utiliza 324 atributos derivados dos Sensores 1, 2 e 3, combinando
características temporais e representação espectral detalhada por FFT.

## Execução

A partir da raiz do repositório, instale as dependências:

```bash
pip install -r requirements.txt
```

Em seguida:

```bash
cd app
streamlit run dashboard.py
```

O Streamlit informará no terminal o endereço local para acesso à aplicação.

## Resultados de referência

O desempenho de referência da PoC foi calculado sobre o conjunto de teste
estratificado com 10.000 observações:

- **Accuracy: 95,13%**
- **Macro F1: 95,13%**

A validação cruzada estratificada com 5 folds apresentou Accuracy média de
aproximadamente **94,92%**.

O arquivo `demo_data.csv` contém apenas 100 observações balanceadas para fins
de demonstração da interface. O desempenho observado nesse subconjunto não
substitui as métricas obtidas na avaliação principal do modelo.

## Escopo

Esta aplicação representa uma camada demonstrativa da PoC.

Em uma implantação industrial, a inferência deverá ser integrada à plataforma
de dados da organização, preferencialmente por meio de uma API, juntamente
com mecanismos de monitoramento, persistência, rastreabilidade, segurança e
governança do modelo.
