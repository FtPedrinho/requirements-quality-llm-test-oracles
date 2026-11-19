# Proposta metodológica inicial

## Desenho

Comparar condições documentais sobre o mesmo corpus da ferramenta MC/DC:

- C0: documentação original;
- C1: revisão controlada com maior clareza, sem alterar comportamento;
- C2-C4: manipulações futuras, após fechar a base.

## Condições

Os documentos fornecidos ao LLM devem ser separados do código e dos testes usados como gabarito.

## Geração

Para cada comportamento documentado:

- identificar SUT;
- registrar requisito ou trecho de origem;
- declarar entradas;
- declarar pré-condições;
- declarar resultado esperado;
- declarar saída ou efeito observável;
- registrar limitações.

## Validação independente

Uma validação pode usar:

- testes JUnit existentes;
- execução da CLI;
- comparação com relatórios produzidos pela implementação;
- PIT sobre módulos Java;
- uma matriz de rastreabilidade revisada.

## Mutation Testing

Usar:

- mutantes Java/PIT da implementação da ferramenta;
- mutantes internos de expressões, separados do PIT;
- não usar mutantes JSON VM/TIS/NPP como substitutos.

## Métricas

Somente com gabarito independente adequado:

- correção do oráculo;
- completude;
- especificidade;
- rastreabilidade;
- taxa de oráculos não avaliáveis;
- detecção de defeitos por suítes ou Mutation Score da implementação.

Precision, Recall e F1 exigem unidade claramente definida e gabarito suficiente.

## Precision, Recall e F1 dos oráculos

O indicador principal da qualidade semântica dos oráculos será baseado em unidades de comportamento especificável e verificável da ferramenta MC/DC.

Cada unidade terá identificador, gabarito independente, critérios de anotação e evidência documental.

O gabarito deve conter condições, entradas, resultados esperados, origem documental e evidências independentes da implementação.

Não deve ser derivado dos oráculos do LLM.

Classificação:

- TP: comportamento esperado corretamente identificado e especificado;
- FP: comportamento afirmado que não corresponde ao gabarito;
- FN: comportamento esperado omitido ou incorretamente especificado;
- Não avaliável: a unidade não possui referência suficiente ou é ambígua.

Fórmulas:

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision+Recall}
\]

Os resultados serão reportados por execução e agregados por média e dispersão quando houver amostra suficiente.

Serão apresentados também resultados por categoria da ferramenta e variações em pontos percentuais entre condições.

Casos não avaliáveis permanecerão fora de TP/FP/FN.

## Comparabilidade

Para comparar condições documentais:

- mesmo modelo;
- mesmo prompt estrutural;
- mesmos parâmetros;
- mesmos comportamentos selecionados;
- mesma implementação;
- mesma suíte de validação;
- múltiplas execuções.
