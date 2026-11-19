# Avaliação da documentação — EXP1

## Documentação adicionada

A cópia independente foi organizada em `documentation/`:

- cópia original do README;
- cópia da especificação técnica;
- versão C1 estruturada da documentação da ferramenta.

## Melhorias

- separação entre sistema sob teste e dados de entrada;
- explicitação dos três comandos;
- definição das fontes;
- definição dos formatos de saída;
- descrição dos limites;
- separação de Z3 como dependência externa;
- esclarecimento de comportamentos não implementados;
- registro de códigos de saída;
- rastreabilidade dos comandos aos módulos Java.

## Avaliação

| Dimensão | Avaliação EXP1 |
|---|---|
| Clareza | Alta |
| Completude | Alta para comportamentos implementados selecionados |
| Precisão | Alta com base no código |
| Consistência | Alta dentro do novo documento |
| Especificidade | Alta |
| Testabilidade | Alta |

## Limitações

- não substitui revisão independente por especialista;
- não declara formalmente o PDF como implementação;
- não define gabaritos TP/FP/FN;
- não fornece geração automática por LLM externo.
