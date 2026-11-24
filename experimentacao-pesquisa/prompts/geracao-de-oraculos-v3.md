# Prompt comum — geração de oráculos e testes Cx

Execute uma condição Cx de modo independente. Use apenas a documentação
técnica e de requisitos indicada para Cx como fonte de comportamento. Para
este experimento, ela é verdade absoluta e não deve ser corrigida pelo código
ou pela saída do sistema. Não use resultados, suítes ou oráculos de outras
execuções. Não altere a documentação nem o sistema sob nenhuma circunstância.

## 1. Oráculo documental, antes de ler o sistema

1. Leia integralmente a fonte Cx após verificar seu SHA-256.
2. Inventarie comportamentos, regras, entradas, saídas, limites, erros e
   exemplos. Para cada caso registre ID, entrada, pré-condição, trecho literal,
   regra, expectativa e justificativa.
3. Registre `INDETERMINADO` quando omissão, ambiguidade ou conflito não
   resolvido pelo texto impedir uma expectativa única. Não use suposições,
   conhecimento do sistema, resultados ou cobertura para desempatar.
4. Formalize as restrições em SMT-LIB e execute obrigatoriamente Z3
   independente do SUT. Registre versão, consultas, respostas, testemunhas e
   limites. A satisfatibilidade não prova fidelidade da tradução. `unknown`,
   timeout e indisponibilidade são erros técnicos, não indeterminações.
5. Revise e congele por SHA-256 a análise, as fórmulas, os casos, os
   resultados Z3 e os oráculos antes de consultar o código ou saída do SUT.
   Se não houver revisão independente, declare a autorrevisão.

## 2. Suíte e execução

Inspecione o SUT somente após o congelamento e crie uma suíte nova contra a
ferramenta MC/DC real. Busque a maior Branch Coverage possível com testes
significativos e expectativas documentais. Não altere expectativas para
concordar com o sistema; preserve as asserções falhas.

Congele a suíte e entradas antes de executá-las. Registre cada caso como
`PASSOU`, `FALHOU` ou `INDETERMINADO`, conforme a documentação e a
observação. Registre falhas técnicas, casos inválidos e casos não avaliados
separadamente; não os transforme em falhas semânticas ou indeterminações.
Casos indeterminados podem ser observados sem julgamento semântico.

Extensões podem exercitar situações documentadas ainda não testadas; a
cobertura pode localizar branches, mas nunca definir resultados esperados.
Congele cada extensão antes da execução e preserve o baseline.

## 3. Relatório

Reporte as quatro métricas: Branch Coverage e quantidades de testes
aprovados, falhos e indeterminados. Inclua escopo, numerador e denominador da
cobertura, resultados por caso, evidências, limitações, ferramentas, hashes e
erros técnicos. Inclua todas as classes de produção dos quatro módulos no
denominador, inclusive classes de mutação não executadas; exclua harness e
bibliotecas externas. Não execute análise de mutação.

Registre qualquer dado indisponível como `não informado` e preserve todos os
artefatos da execução fora da pasta metodológica. Não alegue cobertura máxima
global ou ausência de influência sem demonstração.
