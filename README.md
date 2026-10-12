# Sistema de Comunicação Interplanetária da Colônia (SCIC) — Aurora Siger

## 🚀 Sobre o Projeto
Protótipo de software desenvolvido para a colônia marciana Aurora Siger, integrando análise de dados telemétricos, tratamento de erros numéricos, modelos preditivos de regressão, filas de prioridade com Heap, árvore de prefixos (Trie) e cálculos fundamentados em arquitetura de computadores e eletricidade básica.

O sistema visa otimizar a triagem de mensagens e alertas críticos de infraestrutura, avaliar a precisão de estimativas de latência nos enlaces de rádio, e garantir alta eficiência computacional no processamento de consultas telemétricas.

## 🛠️ Stack Tecnológica
- **Python 3.10+**
- **Pandas & NumPy**: Manipulação, limpeza e análise estruturada de dados operacionais telemétricos.
- **Scikit-Learn**: Modelagem preditiva de regressão linear e validação quantitativa por métricas (MAE, MSE, RMSE, R²).
- **Heapq (Min-Heap)**: Gerenciamento e extração de alertas críticos em tempo real por ordem de prioridade.
- **Trie (Árvore de Prefixos)**: Estrutura de dados em memória para otimização de consultas textuais rápidas por módulos e códigos de sensores.

## 📁 Estrutura de Arquivos do Repositório
- `codigo_fonte.py`: Script principal da aplicação contendo toda a lógica de ingestão, análise de erros, modelo preditivo, Min-Heap, Trie e cálculos elétricos.
- `dados_aurora_siger.csv`: Base de dados simulada com registros de telemática, latência e energia dos módulos de Marte.
- `relatorio_tecnico.md`: Documentação técnica aprofundada com a fundamentação teórica, análise de métricas, limitações e reflexão socioambiental.
- `README.md`: Manual de execução, dependências e visão geral da arquitetura do repositório.
- `link_video.txt`: Arquivo contendo a URL da demonstração em vídeo (YouTube "Não listado").

## ⚙️ Instruções de Execução

1. **Instale as dependências necessárias no terminal:**
   ```bash
   pip install pandas numpy scikit-learn
Verifique os arquivos no diretório:
Certifique-se de que o arquivo dados_aurora_siger.csv e o script codigo_fonte.py estão localizados na mesma pasta.

Execute o script principal:

Bash
python codigo_fonte.py
📊 Módulos do Sistema em Execução
Ao executar o script, o sistema realiza o seguinte fluxo automatizado no terminal:

Carregamento Telemétrico: Ingestão de dados com validação de colunas via Pandas.

Avaliação Numérica: Cálculo do Erro Absoluto e Erro Relativo da latência.

Avaliação do Modelo Preditivo: Extração das métricas MAE, MSE, RMSE e R² para a regressão.

Priorização de Alertas (Min-Heap): Reorganização e desempilhamento dos alertas em ordem de urgência.

Busca Eficiente (Trie): Varredura indexada por prefixo para códigos de sensores (SEN_...) e nomes de módulos.

Eletricidade Básica (COA): Cálculo da potência de transmissão (P=V⋅I) com base na Lei de Ohm.
