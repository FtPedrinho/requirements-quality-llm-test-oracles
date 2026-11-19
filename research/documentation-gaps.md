# Lacunas, ambiguidades e inconsistências documentais

## PDF técnico

O PDF declara um status explícito de proposta de arquitetura e descreve:

- plugin Eclipse;
- Eclipse JDT AST;
- integração Java bytecode/Javassist/ASM;
- modo caixa-branca;
- Gherkin;
- cobertura dinâmica;
- Rich Client Platform.

No snapshot atual:

- não há plugin Eclipse implementado;
- não há parser ANTLR implementado;
- não há integração Java AST/Javassist/ASM;
- não há execução JUnit do código-fonte do sistema;
- não há formato Gherkin aceito;
- o projeto é CLI Maven com módulos Java.

O PDF é usado como especificação de referência desta reconstrução, mas suas seções de Eclipse/plugin, AST, bytecode, Gherkin e cobertura dinâmica devem ser reconciliadas com o código antes de serem tratadas como comportamentos implementados.

## README da ferramenta

Fornece descrição externa útil, mas pode incluir valores históricos de testes e notas de qualidade que não foram reexecutadas nesta etapa.

Não substitui a especificação detalhada de todos os códigos de erro e formatos.

## Implementação

Limitações que podem exigir especificação adicional:

- comportamento exato de `unknown` do Z3 em cada operação;
- limites entre 12, 20 e 30 entradas em linguagem externa;
- limites do número de pares por condição;
- mensagens completas de erro;
- precedência de opções da CLI;
- quais fontes podem ser usadas com cada opção;
- diferenças entre mascaramento e causa única em entradas repetidas;
- comportamento com arquivos vazios ou campos JSON ausentes;
- comportamento sem Z3;
- timeout de Z3.

## Corpus não documentado

VM, TIS e NPP não são especificação da ferramenta. Eles são exemplos de dados de entrada e não devem ser usados como requisitos do SUT.
