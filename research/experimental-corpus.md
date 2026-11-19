# Proposta de corpus experimental

## Objetivo do corpus

Fornecer ao LLM documentação da ferramenta MC/DC, não documentação dos sistemas usados como entradas.

## Corpus recomendado

1. [README da ferramenta](../docs/README.md);
2. seção de uso da `Main` em Java;
3. Javadocs relevantes de:
   - `RequirementsFile`;
   - `Nat2TestJsonReader`;
   - `ExpressionParser`;
   - `TruthTable`;
   - `IndependencePairs`;
   - `MinimalSuite`;
   - `Z3FeasibilityChecker`;
   - `Z3RequirementsVerifier`;
   - formato de saída da CLI.

4. Exemplos sintéticos curtos criados apenas a partir da documentação já existente, sem introduzir comportamento novo.

## Conteúdo reservado para validação independente

Não fornecer ao gerador inicial:

- código-fonte da implementação;
- testes JUnit existentes;
- Mutation Reports;
- resultados históricos;
- saídas já geradas;
- scripts de validação.

## Documentação auxiliar e referência arquitetural

- PDF técnico como especificação de referência da tarefa, com seções não implementadas marcadas como propostas não confirmadas;
- relatórios JaCoCo/PIT;
- análise histórica em `docs/`;
- arquivos VM, TIS e NPP;
- arquivos de saída dos exemplos.

## Funcionalidades sem especificação suficiente

Até decidir-se uma fonte normativa adicional, não gerar oráculos para:

- plugin Eclipse;
- execução sobre AST Java;
- instrumentação de bytecode;
- geração Gherkin;
- cobertura dinâmica de código;
- integração Eclipse.

Esses itens aparecem no PDF, mas não estão implementados no repositório atual.
