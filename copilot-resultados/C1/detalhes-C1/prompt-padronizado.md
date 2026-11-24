# Prompt padronizado de análise e geração — C0-C4

Use este prompt para novas gerações e registre sua versão, hash e qualquer variável ou contexto adicional. Anexe somente a documentação da condição em execução na etapa 1. Trate essa documentação como referência normativa e fielmente verdadeira para gerar o oráculo, ainda que o SUT apresente outro comportamento. Não forneça resultados antigos nem consulte o arquivo histórico.

## Etapa 1 — oráculo documental (não inspecione código ainda)

Analise os documentos técnicos e de requisitos anexados para o experimento **[C0/C1/C2/C3/C4]**. Use exclusivamente esses documentos para definir os resultados esperados. Busque cobrir o máximo possível dos comportamentos documentados, sem acrescentar expectativas para lacunas.

1. Identifique e enumere requisitos, funcionalidades, regras, entradas, saídas, restrições, opções, formatos, fronteiras, erros e exemplos.
2. Monte uma matriz de comportamentos documentados e escolha casos distintos que os verifiquem, incluindo resultados true e false das condições quando sustentados pelo texto.
3. Cite arquivo, seção e trecho literal para cada expectativa do oráculo.
4. Traduza cada regra aplicável para uma representação lógica explícita. Registre como cada parte da fórmula corresponde ao texto.
5. Formalize as restrições em SMT-LIB e use um solver Z3 independente do SUT para verificar satisfatibilidade/viabilidade e obter entradas concretas. Registre fórmula/SMT, objetivo de busca, versão, `sat`/`unsat`/`unknown`, testemunhas e limites. Não classifique `unknown`, timeout ou indisponibilidade do solver como ambiguidade documental; registre como erro técnico.
6. Z3 valida apenas a fórmula fornecida, não a fidelidade da tradução nem a correção do SUT. Não use o código, relatórios de cobertura do SUT ou conhecimento externo para definir ou desempatar expectativas nesta etapa.
7. Registre ambiguidades, omissões e contradições. Se a documentação não especificar o resultado de um comportamento ou não existir expectativa única, marque `INDETERMINADO` com o motivo; não resolva conflitos arbitrariamente nem invente regras para elevar cobertura.
8. Classifique cada oráculo como `CONFORME À DOCUMENTAÇÃO`, `INCORRETO/SEM SUPORTE`, `INVÁLIDO` ou `INDETERMINADO`. Expectativa que dependa de regra não documentada é `INCORRETO/SEM SUPORTE` (subtipo `ASSUMIDO`), mesmo que a suposição seja declarada.
9. Caracterize clareza e consistência com evidências. C0 é a documentação original, sem rótulo automático alto/baixo; C1-C4 são níveis pretendidos a caracterizar.

Não use a saída do módulo `mcdc-z3` nem da CLI sob teste para definir o resultado esperado; isso seria circular. Congele e salve análise, fórmulas, resultados Z3 e oráculos por hash antes de consultar o código.

## Etapa 2 — criação da suíte para o SUT

Agora inspecione o código-fonte e a CLI da ferramenta MC/DC para localizar módulos, funções e pontos de entrada. Crie uma suíte que execute os oráculos congelados contra o sistema real deste repositório, buscando a maior quantidade possível de testes significativos aprovados e a maior Branch Coverage possível dentro do comportamento documentado. Inclua cenários, entradas e fronteiras distintos; não infle a contagem com duplicatas sem contribuição.

- A documentação congelada, não o código, determina a expectativa. Não altere a documentação original, a documentação dos experimentos ou o SUT.
- Não altere um oráculo documental para fazê-lo concordar com o resultado do sistema.
- Se um oráculo determinado e conforme à documentação divergir do SUT, crie e mantenha a asserção que deve falhar e registre `FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT`. A divergência evidencia não conformidade com a referência adotada, mas não prova qual fonte está objetivamente correta.
- Se identificar no SUT comportamento cujo resultado não esteja especificado, registre caso com ID e `INDETERMINADO — OMISSÃO`, sem tomar o comportamento observado como expectativa. Não o classifique automaticamente como falha do SUT.
- Não exclua testes falhos, inválidos ou indeterminados nem modifique expectativas para aumentar a quantidade de aprovações ou a cobertura.
- Diferencie a falha com oráculo conforme da falha sob oráculo incorreto/sem suporte, caso inválido, caso indeterminado e erro técnico; classifique o oráculo e a execução em campos separados.
- Não use testes históricos, relatórios antigos ou arquivos do arquivo histórico como oráculo.
- Após a primeira execução, use relatórios atuais de Branch Coverage apenas para localizar branches sem teste. Mapeie-os de volta à documentação e só acrescente asserções semânticas com expectativa documental única; registre branches sem suporte textual como casos indeterminados, não como convite a inferir. Se executados, esses casos são diagnósticos sem julgamento semântico.
- Preserve o baseline; congele cada extensão `coverage-informed` por hash e reporte seus ganhos separadamente. Cobertura observada pode orientar entradas e implementação do teste, nunca alterar resultado esperado.

## Etapa 3 — especificação dos casos

Gere casos relevantes que ampliem os comportamentos documentados exercitados e, após a inspeção do SUT, os branches mapeados a eles. Para cada caso, forneça:

- ID estável;
- objetivo, trecho documental e regra formalizada;
- entradas completas e pré-condições;
- resultado esperado, justificativa documental e evidência Z3, ou `INDETERMINADO` com razão;
- módulos, branches e condições de código que pretende exercitar, conforme a inspeção;
- requisitos/comportamentos documentados cobertos, lacunas documentais relevantes e relação com a meta de cobertura;
- dependências, pré-requisitos e instruções de execução;
- estado do oráculo e distinção entre texto explícito, interpretação, suposição sem suporte, formalização inválida e indeterminação;
- evidências necessárias para revisar a execução.

Não declare que um oráculo está conforme apenas porque compila, passa no SUT ou é satisfatível no Z3. Não force resultado esperado quando a documentação não o determina. Casos indeterminados podem ser executados como observação diagnóstica, mas não como aprovação/reprovação semântica.

Declare o melhor resultado de Branch Coverage alcançado; não afirme cobertura máxima global sem busca exaustiva sobre universo e restrições explicitados. A quantidade de testes aprovados é resultado observado; não sacrifique a validade dos oráculos para aumentá-la.

## Etapa 4 — registro operacional e resultados

Ao finalizar a geração, registre o prompt integral, resposta integral, arquivos de entrada e seus hashes, modelo/versão/configuração, chamadas, tokens, duração e custos disponibilizados pela plataforma. Use `não informado` onde o dado não existir; não estime. Congele a suíte e a análise por hash antes da execução.

Reporte Branch Coverage como única métrica de cobertura, para a suíte total e para o subconjunto válido/executável com oráculos conformes. Registre separadamente as quantidades de testes gerados, executados, aprovados, falhos, indeterminados e inválidos, os erros técnicos e as demais taxas definidas no protocolo. Cada caso indeterminado registrado conta no numerador e no denominador da taxa de indeterminação da rodada; se executado, também conta como executado e na cobertura total, mas não como aprovação ou falha semântica. Não colete nem compare Condition Coverage ou Mutation Score.
