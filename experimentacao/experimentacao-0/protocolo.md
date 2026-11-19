# Protocolo da Experimentação 0

## Fontes utilizadas

Fontes normativas prioritárias:

- `exemplos/requisitos.mcdc`;
- `exemplos/maquina-cafe.mcdc`;
- `exemplos/vm-requisitos.mcdc`;
- `exemplos/vm-decisoes.json`;
- `exemplos/tis-decisoes.json`;
- `exemplos/npp-decisoes.json`.

O PDF técnico da ferramenta é tratado como documentação arquitetural, não como requisito normativo dos sistemas VM, TIS ou NPP.

## Exclusões desta etapa

Não foram consultados:

- código-fonte da implementação;
- testes JUnit;
- CSVs de casos de teste externos;
- relatórios JaCoCo ou PIT;
- resultados interpretativos históricos da ferramenta;
- implementações dos sistemas de domínio.

## Sequência

1. Registrar identificador, origem, texto e expressão de cada requisito.
2. Formalizar guardas compatíveis com Z3 e registrar interpretações inferidas.
3. Executar satisfatibilidade, redundância, equivalência, implicação, incompatibilidade e MC/DC.
4. Registrar os resultados formais antes da geração dos oráculos.
5. Gerar os oráculos apenas a partir dos documentos normativos.
6. Comparar os oráculos com as formalizações.
7. Derivar casos de teste simbólicos e identificar limites de verificabilidade.
8. Preparar material para validação humana.

## Critérios

- SAT exige pelo menos um modelo.
- UNSAT exige demonstração da inexistência de modelo.
- UNKNOWN é registrado sem converter em falha ou contradição.
- Redundância lógica não é automaticamente incompatibilidade.
- Expressões equivalentes não são automaticamente correção semântica.
- Contraexemplos são evidências formais da formalização, não da intenção original.
- Casos MC/DC são classificados como simbólicos ou concretos conforme o domínio disponível.

Nenhuma expressão inferida é apresentada como texto original.

## Avaliação de qualidade dos oracles por Precision, Recall e F1

As métricas de oráculos não podem reutilizar mutantes, casos simbólicos ou suítes construídas para VM, TIS e NPP como gabarito.

### Unidade de avaliação

A unidade principal será o comportamento especificável e verificável da ferramenta MC/DC. Cada unidade terá um identificador único e será dividida em propriedades independentes quando necessário.

Para cada unidade, será anotado separadamente:

- se o comportamento foi identificado;
- se suas condições foram especificadas corretamente;
- se o resultado esperado foi especificado corretamente;
- se o comportamento foi omitido;
- se o oráculo inventou ou contradisse uma regra.

### Gabarito independente

Antes do cálculo das métricas, será criado um catálogo de referência derivado da documentação normativa selecionada e de evidências independentes da implementação.

O gabarito não pode ser derivado dos oráculos do LLM.

Código-fonte e testes existentes não serão fornecidos ao LLM durante a geração.

### Regras TP, FP e FN

- TP: comportamento esperado corretamente identificado e especificado.
- FP: comportamento afirmado pelo LLM que não corresponde ao gabarito.
- FN: comportamento esperado omitido ou especificado incorretamente.

Um erro pode produzir TP/FP/FN simultaneamente somente quando a unidade e as regras de anotação forem explicitadas.

Ambiguidade e insuficiência documental serão registradas separadamente como não avaliáveis.

### Métricas

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision+Recall}
\]

Os cálculos serão feitos por execução e agregados por média, desvio-padrão e intervalo de confiança quando a amostra permitir.

Resultados por categoria também serão apresentados.

### Limitação atual

Os oráculos históricos deste experimento avaliam dados de entrada VM, TIS e NPP e não possuem gabarito independente da ferramenta MC/DC.

Portanto, neste estado não é possível calcular valores válidos de TP, FP, FN, Precision, Recall ou F1-score para a pergunta atual.

Essas métricas só serão calculadas após a construção do gabarito correto e dos novos oráculos do SUT.
