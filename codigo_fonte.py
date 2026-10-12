import pandas as pd
import numpy as np
import heapq
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =====================================================================
# ESTRUTURA DE DADOS: TRIE (Árvore de Prefixos para Busca de Sensores)
# =====================================================================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.dados_associados = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, info):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.dados_associados.append(info)

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all(node)

    def _collect_all(self, node):
        results = list(node.dados_associados)
        for child in node.children.values():
            results.extend(self._collect_all(child))
        return results

# =====================================================================
# FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO DO SCIC
# =====================================================================
def executar_scic():
    print("==========================================================")
    print("  AURORA SIGER — SISTEMA DE COMUNICAÇÃO INTERPLANETÁRIA (SCIC) ")
    print("==========================================================\n")

    # 1. Leitura da Base via Pandas
    try:
        df = pd.read_csv("dados_aurora_siger.csv")
        print("[SUCESSO] Base 'dados_aurora_siger.csv' carregada com Pandas.\n")
    except FileNotFoundError:
        print("[ERRO CRÍTICO] O arquivo dados_aurora_siger.csv não foi encontrado.")
        return

    # 2. Análise Numérica: Erro Absoluto e Relativo de Latência
    print("--- [MÓDULO 1] Análise Numérica (Erros de Latência) ---")
    df['erro_absoluto'] = np.abs(df['latencia_observada'] - df['latencia_prevista'])
    df['erro_relativo'] = df['erro_absoluto'] / df['latencia_observada']
    
    for _, row in df.iterrows():
        print(f"Módulo: {row['nome_modulo']} | Obs: {row['latencia_observada']}ms | Prev: {row['latencia_prevista']}ms | Erro Abs: {row['erro_absoluto']:.2f}ms | Erro Rel: {row['erro_relativo']*100:.1f}%")
    print("\n")

    # 3. Modelo de Regressão e Avaliação de Performance (Scikit-Learn)
    print("--- [MÓDULO 2] Modelo Preditivo & Métricas (Scikit-Learn) ---")
    X = df[['tensao_v', 'corrente_a']]
    y = df['latencia_observada']

    modelo = LinearRegression()
    modelo.fit(X, y)
    y_pred = modelo.predict(X)

    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)

    print(f"-> MAE (Erro Absoluto Médio): {mae:.2f}")
    print(f"-> MSE (Erro Quadrático Médio): {mse:.2f}")
    print(f"-> RMSE (Raiz do Erro Quadrático Médio): {rmse:.2f}")
    print(f"-> R² (Coeficiente de Determinação): {r2:.2f}\n")

    # 4. Priorização de Alertas Críticos via Heap (Fila de Prioridade)
    print("--- [MÓDULO 3] Priorização de Alertas Críticos (Min-Heap) ---")
    min_heap = []
    for _, row in df.iterrows():
        # Invertemos a prioridade (- prioridade) para que valores altos fiquem no topo do min-heap
        heapq.heappush(min_heap, (-row['prioridade'], row['nome_modulo'], row['mensagem_alerta']))

    print("Extração ordenada por grau de criticidade:")
    while min_heap:
        prio_neg, modulo, alerta = heapq.heappop(min_heap)
        print(f"[ALERTA URGENTE] Nível {-prio_neg} | Módulo: {modulo} -> {alerta}")
    print("\n")

    # 5. Busca Eficiente de Registros via Trie (Árvore de Prefixos)
    print("--- [MÓDULO 4] Busca por Prefixo (Trie) ---")
    trie = Trie()
    for _, row in df.iterrows():
        trie.insert(row['nome_modulo'], row.to_dict())
        trie.insert(row['codigo_sensor'], row.to_dict())

    termo_busca = "com"
    print(f"Buscando elementos com o prefixo '{termo_busca}':")
    resultados = trie.search_prefix(termo_busca)
    for res in resultados:
        print(f"-> Localizado: {res['nome_modulo']} (Código do Sensor: {res['codigo_sensor']})")
    print("\n")

    # 6. Eletricidade Básica Aplicada (Lei de Ohm e Potência)
    print("--- [MÓDULO 5] Eletricidade Básica (COA) ---")
    modulo_alvo = df.iloc[1]
    potencia_w = modulo_alvo['tensao_v'] * modulo_alvo['corrente_a']
    print(f"Módulo Analisado: {modulo_alvo['nome_modulo']}")
    print(f"Tensão: {modulo_alvo['tensao_v']}V | Corrente: {modulo_alvo['corrente_a']}A")
    print(f"Potência de Transmissão Calculada (P = V * I): {potencia_w} Watts")
    print("==========================================================")

if __name__ == "__main__":
    executar_scic()
