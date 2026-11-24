# Modelo de relatório da execução

Preencher para uma condição e execução, sem usar resultados de outra.

## Identificação e fontes

- Condição, fonte normativa e SHA-256.
- Prompt, modelo/configuração disponíveis, contexto e limites de isolamento.
- Commit de referência, ambiente, ferramentas e versões.

## Oráculos e Z3

- Inventário, citações, fórmulas SMT-LIB, versão e respostas Z3, testemunhas.
- Casos, entradas, expectativas ou motivos de indeterminação.
- Hashes do oráculo, suíte e entradas; revisão independente ou autorrevisão.

## Métricas

| Métrica | Resultado |
|---|---|
| Branch Coverage | branches cobertos / total e percentual; ou não coletado |
| Testes aprovados | quantidade |
| Testes falhos | quantidade |
| Testes indeterminados | quantidade |

Identificar a unidade de contagem, ferramenta, escopo de produção e exclusões.
Apresentar baseline, extensões e acumulado separadamente, quando houver.

## Evidências e limitações

Registrar resultados por caso, divergências, casos inválidos, erros técnicos,
comandos, dados brutos, limitações e eventuais perdas de isolamento. Dados
ausentes são `não informado`; não estimar. Preservar resultados e suíte fora
da pasta metodológica, sem sobrescrever outras execuções.
