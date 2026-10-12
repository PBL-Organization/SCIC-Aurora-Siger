# Relatório técnico — SCIC Aurora Siger

O **Sistema de Comunicação Interplanetária da Colônia (SCIC) — Aurora Siger** é um protótipo em Python que combina leitura de telemetria, análise de erro de latência, regressão linear, fila de prioridade baseada em heap, busca textual por Trie e um cálculo simples de potência elétrica. O repositório apresenta o sistema como uma solução conceitual para apoiar a operação de uma colônia marciana, e não como um sistema de comunicação implantável ou um controlador de segurança [1].

## 1. Contexto e objetivo da solução

Em uma colônia remota, os módulos de habitação, agricultura, energia, laboratório, suporte médico e armazenamento dependem de comunicação e telemetria para coordenar decisões. Uma falha ou atraso em um módulo pode afetar outros serviços. Nesse cenário, o SCIC organiza informações operacionais e demonstra três capacidades complementares:

1. **Observar e comparar latências**, confrontando o valor medido com uma previsão.
2. **Estimar latência a partir de variáveis elétricas**, usando tensão e corrente como atributos de uma regressão linear.
3. **Apoiar a triagem operacional**, ordenando alertas por prioridade e localizando módulos ou sensores por prefixo.

O projeto é deliberadamente pequeno. Sua contribuição principal é integrar conceitos de análise de dados, estruturas de dados, aprendizado supervisionado e fundamentos de eletricidade em um fluxo único executável. A implementação está concentrada em `codigo_fonte.py`, com os registros em `dados_aurora_siger.csv` [2] [3].

## 2. Arquitetura e fluxo de execução

A função `executar_scic()` coordena o processamento em cinco módulos:

- **Carga de dados:** `pandas.read_csv()` lê o arquivo CSV.
- **Análise numérica:** `numpy.abs()` calcula o erro absoluto e uma divisão calcula o erro relativo.
- **Modelo preditivo:** `LinearRegression` recebe `tensao_v` e `corrente_a` como entradas e usa `latencia_observada` como alvo.
- **Priorização:** `heapq` armazena tuplas de prioridade, módulo e mensagem de alerta.
- **Busca:** uma Trie recebe o nome do módulo e o código do sensor e responde a consultas por prefixo.

Ao final, o código calcula a potência do segundo registro do CSV pela relação `P = V × I`. Essa escolha é fixa: o módulo analisado não é selecionado por risco, por prioridade ou por argumento de linha de comando. Portanto, o cálculo elétrico é uma demonstração pontual, não uma rotina geral de monitoramento.

A pilha declarada pelo projeto é Python 3.10+, Pandas, NumPy, Scikit-Learn e `heapq` [1]. Em uma execução limpa, o código-fonte compilou, mas a execução inicialmente falhou porque `scikit-learn` não estava instalado. Após a instalação das dependências indicadas no README, a execução foi concluída. Isso evidencia que o repositório deveria incluir um `requirements.txt` ou `pyproject.toml` para tornar o ambiente reproduzível.

## 3. Descrição dos dados

O arquivo possui **7 registros e 11 colunas**. Cada linha representa um módulo da colônia e seu sensor associado. Os campos são:

- `nome_modulo`: identificador legível do módulo.
- `tipo_modulo`: categoria funcional, como energia, agricultura ou laboratório.
- `latencia_observada`: latência medida, em milissegundos.
- `latencia_prevista`: referência ou previsão previamente registrada, também em milissegundos.
- `tensao_v`: tensão elétrica, em volts.
- `corrente_a`: corrente elétrica, em ampères.
- `status_operacional`: estado textual do módulo, como `ativo`, `alerta` ou `manutencao`.
- `prioridade`: nível inteiro de criticidade, de 1 a 5 neste conjunto.
- `codigo_sensor`: identificador do sensor.
- `mensagem_alerta`: descrição textual do estado ou do alerta.
- `ciclo`: identificador numérico do ciclo de telemetria.

A distribuição dos estados é de três módulos `ativo`, três em `alerta` e um em `manutencao`. Cada tipo de módulo aparece uma vez. Isso facilita a demonstração, mas impede inferências robustas por categoria. Também não há série temporal: os ciclos vão de 101 a 107, mas cada ciclo aparece uma única vez e não há histórico suficiente para medir tendência, sazonalidade ou persistência de falhas.

As faixas observadas são:

- Latência observada: **15,0 a 120,5 ms**, média de **67,03 ms**.
- Latência prevista: **14,5 a 90,0 ms**, média de **55,36 ms**.
- Tensão: **12,0 a 110,0 V**.
- Corrente: **1,2 a 10,0 A**.
- Prioridade: **1 a 5**.

Os dados parecem ser sintéticos ou didáticos. Não há metadados de coleta, unidade de tempo do ciclo, identificação de missão, qualidade do sensor, valores ausentes, incerteza de medição ou definição formal de como a previsão de latência foi produzida. Assim, os resultados servem para validar o fluxo do programa, não para estabelecer desempenho real da rede.

## 4. Tratamento numérico e análise dos erros

Para cada registro, o código calcula:

\[
E_{abs} = |L_{observada} - L_{prevista}|
\]

\[
E_{rel} = \frac{E_{abs}}{L_{observada}}
\]

Os resultados reproduzidos foram:

| Módulo | Erro absoluto | Erro relativo |
|---|---:|---:|
| Habitacao-Alfa | 5,20 ms | 11,5% |
| Agricultura-Hidro | 30,50 ms | 25,3% |
| Comunicação-Central | 0,50 ms | 3,3% |
| Laboratorio-Bio | 13,40 ms | 15,2% |
| Suporte-Medico | 2,10 ms | 7,0% |
| Armazenamento-Dados | 5,00 ms | 8,3% |
| Modulo-Energia-B | 25,00 ms | 22,7% |

A média do erro absoluto entre as colunas `latencia_observada` e `latencia_prevista` é **11,67 ms**, e a média dos erros relativos é aproximadamente **13,33%**. Os maiores desvios são de `Agricultura-Hidro` e `Modulo-Energia-B`. Esses dois registros também têm prioridade 5 e status `alerta`, o que cria uma coerência operacional interessante: os módulos mais discrepantes são justamente os que merecem atenção imediata. Essa associação, porém, não prova causalidade; com apenas sete linhas não é possível afirmar que maior erro de previsão cause maior criticidade.

Há duas limitações técnicas importantes nesse cálculo:

- O denominador do erro relativo é a latência observada. A escolha é válida quando a observação é a referência, mas deve ser documentada porque outras aplicações podem usar a previsão como denominador ou adotar métricas simétricas.
- Não existe proteção contra `latencia_observada = 0`. Em dados reais, seria necessário tratar divisão por zero, valores ausentes, valores negativos e unidades inconsistentes.

## 5. Modelo simples de regressão

O modelo usa:

\[
X = [tensao\_v,\ corrente\_a]
\]

como variáveis de entrada e:

\[
y = latencia\_observada
\]

como variável-alvo. `LinearRegression` ajusta uma regressão linear ordinária com intercepto, minimizando a soma dos quadrados dos resíduos entre os valores observados e os valores previstos [4]. Em notação simplificada, o modelo é:

\[
\hat{L} = b_0 + b_1 V + b_2 I
\]

No conjunto analisado, o ajuste reproduzido foi aproximadamente:

\[
\hat{L} = 25,91 - 2,40V + 36,54I
\]

Os coeficientes não devem ser interpretados como leis físicas. O coeficiente negativo da tensão e o coeficiente positivo da corrente resultam de um conjunto minúsculo e de variáveis possivelmente correlacionadas com condições operacionais não observadas. Para uma aplicação real, seria necessário incluir carga da rede, distância, tamanho da mensagem, retransmissões, congestionamento, qualidade do enlace, temperatura, estado do equipamento e janela temporal.

### Métricas calculadas pelo código

O programa treina o modelo com todas as sete linhas e, em seguida, calcula `y_pred` sobre as mesmas sete linhas. A saída reproduzida é:

- **MAE:** 19,80 ms.
- **MSE:** 513,68 ms².
- **RMSE:** 22,66 ms.
- **R²:** 0,63.

MAE é a média dos valores absolutos dos erros; MSE é a média dos erros ao quadrado; RMSE é a raiz quadrada do MSE e retorna à unidade da latência; R² compara o erro residual com a variabilidade em torno da média. O módulo de métricas do Scikit-Learn fornece essas funções para avaliar regressões [5]. Em geral, MAE, MSE e RMSE menores são melhores, enquanto R² mais próximo de 1 indica maior aderência ao conjunto avaliado.

A interpretação correta dos números é restrita: **R² = 0,63 é um ajuste dentro da amostra**, não uma evidência de que o modelo explicará 63% da variação em novos ciclos. Como não há divisão treino-teste, validação cruzada ou conjunto temporal de teste, as métricas são otimistas e não medem generalização. Além disso, elas avaliam a previsão do modelo contra `latencia_observada`, enquanto o erro de 11,67 ms da seção anterior compara a observação com a coluna externa `latencia_prevista`. São duas avaliações diferentes e não devem ser misturadas.

Uma versão adequada para validação deveria separar os ciclos por tempo, treinar em ciclos anteriores e testar em ciclos posteriores. Com uma base tão pequena, a alternativa mínima seria validação cruzada com relatório da dispersão das métricas, sempre deixando claro que o resultado ainda teria alta incerteza.

## 6. Gerenciamento inteligente da comunicação

O gerenciamento implementado é um **protótipo de triagem**, não um gerenciador completo de comunicação. A ideia é transformar a telemetria em uma ordem de atendimento: alertas com prioridade maior devem ser retirados primeiro da fila. Isso é útil em cenários com banda, tempo de processamento ou atenção humana limitados.

O fluxo atual é:

1. Para cada linha, formar a tupla `(-prioridade, nome_modulo, mensagem_alerta)`.
2. Inserir a tupla no min-heap.
3. Retirar itens com `heappop()` até esvaziar a fila.
4. Negar o primeiro campo para mostrar a prioridade original em ordem decrescente.

A biblioteca `heapq` implementa uma fila de prioridade baseada em min-heap: o menor elemento fica na raiz e `heappush()`/`heappop()` preservam a invariável da estrutura [6]. O código usa a negação da prioridade para converter o maior nível de criticidade em menor valor interno.

A ordem observada foi:

1. `Agricultura-Hidro` — prioridade 5.
2. `Modulo-Energia-B` — prioridade 5.
3. `Armazenamento-Dados` — prioridade 4.
4. `Laboratorio-Bio` — prioridade 4.
5. `Suporte-Medico` — prioridade 3.
6. `Habitacao-Alfa` — prioridade 2.
7. `Comunicação-Central` — prioridade 1.

Em empates, o nome do módulo e a mensagem funcionam como critérios secundários por causa da comparação lexicográfica da tupla. O custo de inserção e remoção é logarítmico no tamanho da fila; a extração de todos os registros produz uma ordenação com custo total de ordem `O(n log n)` [6].

Para se tornar realmente inteligente, a fila deveria considerar mais que um inteiro fixo. Uma política possível combinaria prioridade de segurança, idade do alerta, risco de perda de dados, dependência entre módulos, prazo de validade da mensagem e custo energético de transmissão. Também seriam necessários mecanismos de confirmação, retentativa, deduplicação, expiração, justiça para evitar starvation de alertas de baixa prioridade e registro de auditoria.

## 7. Trie e busca de sensores

A Trie é uma árvore de prefixos. Cada caractere de uma palavra corresponde a uma aresta, e cada nó pode manter filhos e uma lista de dados associados. No projeto, `insert()` percorre a palavra em minúsculas, cria nós quando necessário e armazena o dicionário da linha no nó final. `search_prefix()` percorre o prefixo e depois chama `_collect_all()` para visitar a subárvore inteira.

A estrutura é carregada duas vezes por registro: uma vez com `nome_modulo` e outra com `codigo_sensor`. A consulta fixa é o prefixo `com`, que retorna `Comunicação-Central` e `SEN_COM_03` por meio do registro associado ao módulo.

O benefício esperado é que a localização do nó do prefixo dependa do comprimento do prefixo, e não da comparação completa com todos os nomes. A coleta dos resultados ainda depende do número de nós e registros encontrados. O custo de memória é proporcional ao total de caracteres armazenados, com compartilhamento de prefixos. Em uma base pequena, a diferença de desempenho é irrelevante; em uma base grande e com muitas consultas por prefixo, a estrutura pode ser útil.

A implementação ainda precisa de cuidados para produção:

- normalização consistente de acentos, hífens, maiúsculas e espaços;
- distinção entre o tipo do resultado e o registro original;
- remoção e atualização de registros;
- paginação quando um prefixo retornar muitos resultados;
- prevenção de duplicidades quando o mesmo registro for indexado por vários campos;
- limites de tamanho para evitar consumo excessivo de memória.

## 8. Cálculo elétrico e relação com operação

Para o registro `Agricultura-Hidro`, selecionado por `df.iloc[1]`, o programa calcula:

\[
P = V \times I = 48,0\ V \times 5,0\ A = 240,0\ W
\]

O cálculo é coerente com a potência elétrica de um circuito ideal em corrente contínua. Ele pode servir como indicador inicial de carga do módulo, mas não representa sozinho a potência de transmissão de uma rede de comunicação. Faltam, por exemplo, eficiência do conversor, fator de potência quando aplicável, consumo em espera, perdas nos cabos, perfil temporal e separação entre potência do sensor, do computador e do transmissor.

A base também contém `Modulo-Energia-B` com 110 V e 10 A, resultando em 1.100 W pela mesma relação. Esse valor chama atenção para uma possível regra futura de sobrecarga, mas o código atual não compara o resultado com limites nem gera uma ação automática. A mensagem `Sobrecarga de pico` é apenas um dado textual do CSV.

## 9. Reflexão social, cultural e sustentável

### Dimensão social

Um sistema de prioridade influencia quais necessidades recebem atenção primeiro. Isso pode proteger serviços críticos, como suporte médico, água, alimentos e energia. Contudo, a prioridade não deve ser definida apenas por uma pontuação técnica. A governança precisa documentar quem define os pesos, quem pode alterá-los e como a população da colônia pode contestar decisões automatizadas.

O sistema também deve evitar que um indicador de latência seja usado como substituto de pessoas. Um módulo com baixa prioridade numérica pode sustentar um grupo vulnerável ou uma atividade essencial. A interface deveria mostrar a justificativa do alerta, a idade do dado, o grau de confiança e a consequência esperada da decisão.

### Dimensão cultural

Aurora Siger é apresentada como uma comunidade, não apenas como um conjunto de sensores. Nomes de módulos, mensagens e regras de atendimento podem carregar valores culturais. Uma solução responsável deve permitir vocabulários multilíngues, preservar acentos e convenções de identificação, e evitar que a linguagem operacional apague diferenças entre grupos ou transforme pessoas em meros indicadores.

A participação humana é especialmente importante para definir o que significa “crítico”. Segurança física, cuidado, privacidade, autonomia e preservação de práticas culturais podem entrar em conflito. A fila deve, portanto, ser configurável e auditável, com decisões reversíveis quando possível.

### Dimensão sustentável

A priorização pode reduzir retransmissões desnecessárias, processar primeiro mensagens com maior valor operacional e evitar desperdício de energia em comunicações de baixo benefício. O cálculo de potência também pode apoiar limites de consumo e planejamento de carga.

Por outro lado, uma política que sempre favoreça o alerta mais urgente pode gerar retentativas, congestionamento e gasto energético excessivo. Melhorias sustentáveis incluem compactação de telemetria, agregação de medidas, processamento local, transmissão orientada a eventos, modos de baixo consumo e retenção de dados com prazo definido. Essas decisões devem ser medidas por consumo energético por mensagem, taxa de retransmissão, volume de dados e disponibilidade dos serviços essenciais.

## 10. Limitações identificadas

As principais limitações do protótipo são:

- **Base muito pequena:** sete linhas não sustentam conclusões estatísticas ou operacionais.
- **Ausência de validação externa:** o modelo é avaliado nos mesmos dados usados no ajuste.
- **Dados sem proveniência:** não há descrição da coleta, da instrumentação, das incertezas ou da origem das previsões.
- **Modelo incompleto:** apenas tensão e corrente são usadas para explicar latência.
- **Sem tratamento de qualidade:** não há validação de esquema, tipos, valores ausentes, outliers ou duplicatas.
- **Fila estática:** todas as mensagens são carregadas de uma vez e a fila é destruída ao final; não há chegada contínua de eventos.
- **Prioridade simplificada:** o sistema não incorpora idade, dependência, prazo, risco ou confirmação de entrega.
- **Trie limitada:** não oferece atualização, remoção, normalização avançada ou interface de consulta.
- **Cálculo elétrico pontual:** analisa sempre o segundo registro e não aplica limites de segurança.
- **Tratamento de falhas mínimo:** apenas `FileNotFoundError` é tratado na leitura do CSV.
- **Reprodutibilidade incompleta:** as dependências aparecem no README, mas não estão fixadas em arquivo de ambiente.
- **Ausência de testes:** não há testes automatizados para métricas, heap, Trie, entrada inválida ou regressão.
- **Sem comunicação real:** o protótipo não implementa protocolo, transporte, criptografia, autenticação, relógio, sincronização, armazenamento persistente ou tolerância a partições.

## 11. Possíveis melhorias

### Curto prazo

1. Adicionar `requirements.txt` com versões compatíveis e um comando de execução reproduzível.
2. Separar leitura, validação, análise, modelo, fila, Trie e relatório em funções testáveis.
3. Validar colunas obrigatórias, tipos, unidades, nulos, latências não negativas e prioridade dentro do intervalo permitido.
4. Parametrizar o caminho do CSV, o prefixo da busca e o módulo do cálculo elétrico.
5. Exportar resultados em JSON ou CSV, em vez de apenas imprimir no terminal.
6. Adicionar testes unitários para erro relativo, ordenação de prioridade e busca por prefixo.

### Médio prazo

1. Dividir os dados por tempo ou por missão e avaliar o modelo em dados não usados no treinamento.
2. Comparar a regressão com um baseline ingênuo, como a mediana histórica da latência.
3. Incluir intervalos de previsão, análise de resíduos, gráficos e detecção de deriva.
4. Modelar alertas como eventos com identificador, timestamp, TTL, tentativas e confirmação.
5. Substituir a prioridade única por uma função de pontuação documentada e auditável.
6. Criar uma Trie normalizada ou usar um índice apropriado para busca textual em bases maiores.
7. Implementar limites elétricos por módulo, alarmes de sobrecarga e histórico de consumo.

### Longo prazo

1. Incorporar um pipeline de telemetria com armazenamento temporal, versionamento de esquema e observabilidade.
2. Definir um protocolo de comunicação tolerante a atrasos, perdas, interrupções e largura de banda limitada.
3. Adicionar autenticação, autorização, criptografia, rotação de chaves e proteção contra replay.
4. Usar simulação de falhas para testar congestionamento, indisponibilidade de módulos e mensagens duplicadas.
5. Criar governança sociotécnica: revisão humana, trilhas de auditoria, explicações, controle de acesso e participação da comunidade.
6. Medir desempenho energético e disponibilidade por serviço, não apenas por dispositivo.

## 12. Conclusão técnica

O SCIC Aurora Siger cumpre bem o papel de protótipo integrador. Ele lê telemetria estruturada, calcula discrepâncias de latência, ajusta uma regressão linear, ordena alertas por criticidade, indexa nomes e sensores por prefixo e relaciona tensão e corrente à potência. A execução reproduzida confirma a saída esperada depois da instalação das dependências declaradas.

O resultado mais importante da análise é a distinção entre **demonstração algorítmica** e **evidência operacional**. O heap e a Trie demonstram estruturas adequadas para suas operações. O cálculo elétrico é matematicamente simples e correto sob suas hipóteses. Já o modelo preditivo e suas métricas precisam de dados maiores e validação fora da amostra antes de apoiar decisões. Com validação, segurança, governança e telemetria real, o protótipo poderia evoluir para uma base experimental de um sistema de comunicação inteligente, responsável e energeticamente consciente.

## Referências

[1]: https://github.com/PBL-Organization/SCIC-Aurora-Siger "Repositório SCIC-Aurora-Siger — descrição e stack tecnológica"

[2]: https://github.com/PBL-Organization/SCIC-Aurora-Siger/blob/main/codigo_fonte.py "SCIC-Aurora-Siger — código-fonte principal"

[3]: https://github.com/PBL-Organization/SCIC-Aurora-Siger/blob/main/dados_aurora_siger.csv "SCIC-Aurora-Siger — conjunto de dados de telemetria"

[4]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html "Scikit-Learn LinearRegression — documentação oficial"

[5]: https://scikit-learn.org/stable/modules/model_evaluation.html "Scikit-Learn — métricas e avaliação de modelos"

[6]: https://docs.python.org/3/library/heapq.html "Python heapq — documentação oficial de filas de prioridade"
