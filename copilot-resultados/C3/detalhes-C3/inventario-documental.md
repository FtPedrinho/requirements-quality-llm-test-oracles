# Inventário documental preliminar

Referência única: `tool-readme-C3.md`, SHA-256 informado em `estado-inicial.md`. Citações abaixo são literais; seções qualificam sua localização. Resultados históricos e números de testes descritos no próprio documento não são usados como expectativas, metas ou fundamentos.

## Comportamentos

| ID | Seção | Trecho | Escopo |
|---|---|---|---|
| D01 | O que a ferramenta faz | “Tabela verdade, pares de independência, suíte de testes e o par que demonstra cada condição” | analyze |
| D02 | Como funciona | “para as entradas distintas da expressão, são consideradas as 2ⁿ combinações e calculado o resultado da guarda em cada uma” | tabela e avaliação |
| D03 | Uso | “`and`, `&&`, `/\`”; “`or`, `\|\|`, `\/`”; “`not`, `!`” | operadores lógicos aceitos |
| D04 | Uso | “`=`, `==`, `!=`, `<`, `<=`, `>`, `>=`” | comparações aceitas |
| D05 | Formatos de entrada | “um requisito por linha, `ID: expressão`. Linhas com `#` são comentários” | arquivo |
| D06 | Formatos de entrada | “cada linha associa um teste a uma entrada e ao valor atribuído a essa entrada” | CSV de check |
| D07 | O que a ferramenta faz | “Conflitos (dois requisitos valem juntos e escrevem valores diferentes) e lacunas (nenhum requisito vale)” | verify |
| D08 | Uso | “No `verify`: confere se, nessa situação, sempre alguma guarda vale” | contexto |
| D09 | Formatos de entrada | “contém as variáveis e seus tipos, além das decisões, cada uma com sua guarda e suas ações” | JSON NAT2TEST |
| D10 | Formatos de entrada | “esse valor é identificado pelo sufixo `_antes`” | valor anterior |
| D11 | Uso | “`--boundary` | Com `--z3`, acrescenta variantes de fronteira” | fronteiras |
| D12 | O que a ferramenta faz | “`speed > 100` → 100 e 101” | exemplo fronteira |
| D13 | Uso | “`-o <arquivo>` | Grava o relatório no arquivo em vez de mostrar na tela” | destino |
| D14 | Como funciona | “a estratégia gulosa considera primeiro as condições com menos pares e escolhe pares que acrescentem menos testes à suíte; em caso de empate, prioriza causa única” | escolha gulosa |
| D15 | Limites conhecidos | “até 1000 pares guardados por condição” | limite de pares |
| D16 | Limites conhecidos | “a ferramenta analisa um passo isolado” | guardas temporais |
| D17 | Uso | “`check` e `verify` aceitam `text` e `json`” | formatos |
| D18 | Uso | “Restrição entre condições escrita à mão (só com expressão direta)” | constraint |
| D19 | Uso | “Causa única em vez de mascaramento” | seleção de variante |

O significado preciso dos operadores lógicos é tomado das designações “e”, “ou” e “não” na própria tabela de operadores, sem adotar resultados de testes históricos. Aceitação de uma forma sintática não implica que mensagens, ordem de linhas, ordem de pares ou estrutura interna de objetos tenham sido especificadas.

## Conflitos e indeterminações

| ID | Seção | Alternativas documentais | Consequência |
|---|---|---|---|
| I01 | O que a ferramenta faz | “condição é cada ocorrência” versus “cada variável distinta como uma única condição” | contagem de condições repetidas indeterminada |
| I02 | Instalação | “Sem o Z3, continuam disponíveis os recursos que não dependem dele” versus “Sem o Z3, nenhum comando pode ser iniciado” | execução sem Z3 indeterminada |
| I03 | Uso | troca automática para modo direto acima de 12 versus permanência obrigatória na tabela a partir da 13ª entrada | comportamento acima de 12 indeterminado |
| I04 | Uso | direto “sem montar a tabela (até 30 entradas)” versus “só funciona até 12 entradas e exige que a tabela-verdade já tenha sido construída” | limites e pré-condição do direto indeterminados |
| I05 | Uso | códigos 0/1/2 para sucesso/entrada inválida/problema funcional versus 0/1/2 para entrada inválida/sucesso/falha de instalação | códigos indeterminados |
| I06 | Formatos de entrada | colunas `decision` e `expected_outcome` “opcionais” versus “deve conter” ambas | aceitação de CSV sem colunas indeterminada |
| I07 | Saídas | `truth-csv` tabela inteira e `csv` suíte versus `truth-csv` somente pares e `csv` somente tabela | conteúdo desses formatos indeterminado |
| I08 | Como funciona | `unsat` impossível e descartado versus `unsat` possível e mantido; `sat` também invertido | tratamento de viabilidade indeterminado |
| I09 | Como funciona | par exige mudança do resultado versus resultado pode permanecer igual | pares e cobertura MC/DC indeterminados onde as alternativas diferem |
| I10 | Como funciona | `--exact` tamanho mínimo versus heurística aproximada sem garantia; gulosa aproximada versus sempre mínima | garantias de minimização indeterminadas |
| I11 | Como funciona | sem par em todas combinações é redundante versus bloqueada; perda por impossibilidade é bloqueada versus redundante | rótulos de diagnóstico indeterminados |
| I12 | Arquitetura | Z3 processo externo com limite de 60 s versus biblioteca interna sem limite | arquitetura e timeout indeterminados |
| I13 | Qualidade e testes | cobertura total ponderada por contagens e métricas distintas versus média simples e cobertura de linhas igual a desvios | interpretação documental do relatório histórico indeterminada; não usar números históricos |
| I14 | Qualidade e testes | JaCoCo por módulo versus apenas agregação global | aprovação do build indeterminada |
| I15 | Limites conhecidos | MC/DC não garante defeitos de parênteses versus garante qualquer alteração | garantia indeterminada; mutação não será executada |

O documento não determina, entre outros aspectos, o esquema exato de todos os campos de saída, ordenação de linhas ou pares, nem mensagens detalhadas de erro. Ausência de expectativa única não pode ser preenchida pela observação do SUT.

## Clareza e revisão

As opções e os exemplos dão formas concretas de entrada, porém afirmações opostas no mesmo documento atingem conceitos fundamentais e não são resolvidas consistentemente. Assim, há clareza local em vários trechos e inconsistência demonstrada pelos pares acima; não se presume o nível pretendido. A revisão é autorrevisão da própria IA, não revisão independente. A tradução lógica precisa de revisão humana e o solver não demonstra fidelidade documental.
