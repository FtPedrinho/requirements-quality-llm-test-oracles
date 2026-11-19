# Protocolo do Experimento 1

## Objetivo

Avaliar oráculos gerados a partir da condição documental C1: alta clareza e consistência documental registrada, com limitações semânticas não resolvidas.

## Fonte

A fonte normativa foi exclusivamente `requirements/experimental/`. Os arquivos originais foram utilizados apenas para rastreabilidade. O PDF arquitetural não foi usado para definir comportamentos dos sistemas.

## Ferramentas

- Python 3.13.5;
- Z3 Python 5.4.1;
- documentos JSON NAT2TEST;
- scripts reproduzíveis criados dentro do Experimento 1;
- mecanismo de mutação reutilizado do Experimento 0.

## Ordem executada

1. inspeção dos artefatos do Experimento 0;
2. formalização das guardas C1;
3. análise Z3;
4. geração independente dos oráculos;
5. geração dos casos de teste;
6. Mutation Testing;
7. auditoria das métricas;
8. análise de sensibilidade;
9. comparação com o Experimento 0.

## Independência

Os oráculos foram gerados antes do uso interpretativo dos resultados Z3 como gabarito. O Z3 foi usado posteriormente para formalização, conflitos e evidências.

Não foram consultados código-fonte, testes JUnit ou relatórios históricos durante a geração inicial.

## Unidade de análise

O mutante agregado é a unidade para Precision, Recall e F1:

- TP: mutante não equivalente morto;
- TN: mutante equivalente não morto;
- FP: mutante equivalente morto ou rejeição incorreta do comportamento original;
- FN: mutante não equivalente sobrevivente.

Casos não avaliáveis e mutantes UNKNOWN não entram na matriz.

## Operadores

Os mesmos operadores do Experimento 0 foram reutilizados:

- AND/OR;
- negação;
- remoção de condições;
- substituição relacional;
- alteração de constantes;
- negação integral da guarda.

## Exclusões

- mutantes equivalentes foram excluídos do denominador MS;
- mutantes UNKNOWN não foram mortos ou classificados como equivalentes;
- casos não concretizáveis não foram aprovados ou reprovados;
- a variável NPP não declarada não foi adicionada aos documentos.

## Auditoria

Os arquivos brutos são preservados em `mutation-testing/`. A auditoria recalcula totais por IDs únicos e pares mutante/caso.

## Avaliação de qualidade dos oráculos por Precision, Recall e F1

### Unidade de avaliação

Cada unidade será um comportamento especificável e verificável da ferramenta MC/DC, identificado independentemente da apresentação textual do oráculo.

Uma unidade pode ser decomposta em propriedades menores, como:

- entrada ou pré-condição;
- condição lógica;
- ação ou resultado esperado;
- saída observável;
- código de retorno;
- formato de relatório.

O gabarito deverá exigir correspondência semântica, não apenas menção ao nome do comportamento.

### Gabarito independente

Será criado um catálogo separado contendo:

- identificador do comportamento;
- descrição esperada;
- condições aplicáveis;
- entradas relevantes;
- resultados esperados;
- critérios de correção;
- origem documental;
- evidência independente da implementação.

O gabarito não será derivado dos oráculos gerados pelo LLM.

### Classificação

- TP: comportamento esperado corretamente identificado e especificado;
- FP: comportamento afirmado que não corresponde ao gabarito;
- FN: comportamento esperado omitido ou incorretamente especificado;
- Não avaliável: ambiguidade ou ausência de referência suficiente.

Um erro pode gerar FP e FN simultaneamente quando as regras permitirem contar a afirmação incorreta e a ausência da especificação correta.

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

Os valores serão calculados por execução e agregados por média, desvio-padrão e intervalo de confiança quando aplicável.

Serão apresentadas também contagens por categoria e por sistema funcional da ferramenta.

### Separação das métricas

Precision, Recall e F1 avaliam correspondência semântica dos oráculos.

Mutation Score, cobertura e aprovação dos testes avaliam a eficácia das suítes contra o SUT real.

Não serão usados os Mutation Scores históricos de especificações VM, TIS e NPP como substitutos das métricas dos oráculos.

### Limitação atual

Os oráculos C1 históricos deste experimento não são oráculos da ferramenta MC/DC e não possuem gabarito independente adequado.

Consequentemente, TP, FP, FN, Precision, Recall e F1 não podem ser apresentados como resultados válidos deste protocolo atual.
