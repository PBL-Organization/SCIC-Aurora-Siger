# Sistema de Comunicação Interplanetária da Colônia (SCIC) — Aurora Siger

## 🚀 Sobre o Projeto

O **Sistema de Comunicação Interplanetária da Colônia (SCIC)** é um protótipo de software desenvolvido para a colônia marciana Aurora Siger. O sistema integra análise de dados telemétricos, tratamento de erros numéricos, modelos preditivos de regressão, filas de prioridade com Heap, árvores de prefixos (Trie) e cálculos fundamentados em arquitetura de computadores e eletricidade básica.

O objetivo é otimizar a triagem de mensagens e alertas críticos de infraestrutura, avaliar a precisão das estimativas de latência nos enlaces de rádio e garantir alta eficiência computacional no processamento de consultas telemétricas.

## 🛠️ Stack Tecnológica

- **Python 3.10+:** linguagem principal de desenvolvimento.
- **Pandas e NumPy:** manipulação, limpeza e análise estruturada de dados operacionais telemétricos.
- **Scikit-learn:** modelagem preditiva por regressão linear e validação quantitativa por meio de métricas como MAE, MSE, RMSE e R².
- **Heapq (Min-Heap):** gerenciamento e extração de alertas críticos em ordem de prioridade.
- **Trie (Árvore de Prefixos):** estrutura de dados em memória para otimizar consultas textuais por módulos e códigos de sensores.

## 📁 Estrutura de Arquivos do Repositório

O repositório está organizado da seguinte forma:

- `codigo_fonte.py`: script principal da aplicação, contendo a lógica de ingestão e análise de dados, tratamento de erros, modelo preditivo, Min-Heap, Trie e cálculos elétricos.
- `dados_aurora_siger.csv`: base de dados simulada com registros de telemetria, latência e energia dos módulos de Marte.
- `relatorio_tecnico.md`: documentação técnica com fundamentação teórica, análise de métricas, limitações e reflexão socioambiental.
- `README.md`: manual de execução, dependências e visão geral da arquitetura do repositório.
- `link_video.txt`: arquivo contendo a URL da demonstração em vídeo no YouTube, publicada como **não listada**.

## ⚙️ Instruções de Execução

### 1. Instalação das dependências

Instale as bibliotecas necessárias utilizando o terminal:

```bash
pip install pandas numpy scikit-learn
```

### 2. Verificação dos arquivos

Certifique-se de que os seguintes arquivos estejam localizados no mesmo diretório:

- `codigo_fonte.py`
- `dados_aurora_siger.csv`

### 3. Execução do sistema

No terminal, execute o comando:

```bash
python codigo_fonte.py
```

## 📊 Módulos do Sistema em Execução

Ao executar o script principal, o sistema realiza automaticamente as seguintes operações:

### 1. Carregamento Telemetrico

Ingestão dos dados por meio do Pandas, com validação das colunas necessárias para o processamento.

### 2. Avaliação Numérica

Cálculo do erro absoluto e do erro relativo das estimativas de latência, permitindo avaliar a diferença entre os valores estimados e os valores de referência.

### 3. Avaliação do Modelo Preditivo

Treinamento e avaliação do modelo de regressão por meio das seguintes métricas:

- **MAE (Mean Absolute Error):** erro absoluto médio.
- **MSE (Mean Squared Error):** erro quadrático médio.
- **RMSE (Root Mean Squared Error):** raiz do erro quadrático médio.
- **R² (Coeficiente de Determinação):** medida da capacidade explicativa do modelo em relação aos dados utilizados na avaliação.

### 4. Priorização de Alertas — Min-Heap

Organização e extração de alertas utilizando uma fila de prioridade baseada em Min-Heap, permitindo processar os eventos conforme seus níveis de urgência.

### 5. Busca Eficiente — Trie

Utilização de uma árvore de prefixos para realizar buscas indexadas por prefixo em códigos de sensores, como `SEN_...`, e nomes de módulos.

### 6. Eletricidade Básica — COA

Cálculo da potência de transmissão com base na tensão e na corrente elétrica, utilizando a relação:

$$
P = V \cdot I
$$

Onde:

- \(P\) = potência elétrica, em watts (W).
- \(V\) = tensão elétrica, em volts (V).
- \(I\) = corrente elétrica, em ampères (A).

O cálculo é fundamentado na relação entre tensão, corrente e potência elétrica, considerando os princípios básicos da Lei de Ohm quando aplicáveis.

---

**Projeto:** Sistema de Comunicação Interplanetária da Colônia (SCIC) — Aurora Siger.
