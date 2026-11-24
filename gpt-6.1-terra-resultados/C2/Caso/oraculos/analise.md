# Resposta de geração e planejamento de busca

Os registros individuais estão em `casos.json`: cada entrada contém ID, objetivo, citação, referência ao inventário, regra, vínculo textual, entrada e pré-condição, expectativa ou estado indeterminado, classificação e referência à evidência SMT. A classificação é autoavaliação. Nenhuma saída de execução atual do SUT foi usada para definir as expectativas.

## Objetivo e restrições

Buscou-se ampliar comportamentos documentados: tabela e operadores booleanos com combinações completas, causas única e mascaramento para guardas simples, condições sem par, restrições, seleção exata, modo direto, formatos, viabilidade e fronteira numérica, arquivo `.mcdc`, lacunas e códigos de saída. São excluídos todos os testes de mutação. Esquemas de `check` e JSON de entrada com grafia problemática são diagnósticos indeterminados: sua saída não se torna gabarito.

Para cada forma booleana escolhida foram geradas todas as combinações; o solver independente gera a testemunha e verifica que o resultado oposto é impossível. Para pares simples, são exigidas mudanças de decisão e de uma entrada com as outras fixas. Para seleção exata em causa única, o solver testa o limite inferior e uma solução com o tamanho previsto. A implicação numérica é verificada sobre reais, e portanto também vale sobre inteiros. Limite de 60 s por consulta; `unknown`, timeout e falha do solver são erros técnicos, não indeterminação.

Critério de parada efetivamente aplicado: esgotar as combinações das expressões selecionadas, as variantes explicitadas na lista de casos e os problemas SMT correspondentes; não há prova de exaustão sobre a documentação completa. A busca não realizou otimização global da suíte. O gerador e os resultados íntegros permitem revisar o universo realmente escolhido; o Z3 não prova fidelidade da tradução.

## Evidências e ressalvas

`resultado-z3.json` registra consultas, SMT-LIB, resultados e testemunhas. `formulas.smt2` conserva as consultas reproduzíveis. `entradas/` contém fixtures congeláveis criadas para esta rodada; não foram copiados testes históricos. Dependências de implementação e módulos específicos serão mapeados na suíte posteriormente. Fórmulas sintáticas (por exemplo, uma string incompleta não é expressão válida) e de formato não são artificialmente apresentadas como prova SMT. A decisão de considerar essas entradas inválidas é uma interpretação autoavaliada, não uma certeza independente.

O documento completo foi lido, mas traz exemplos, nomes de testes e resultados históricos. Embora não tenham sido usados conscientemente como gabarito, o contexto também continha informação prévia de código e resultados; não há garantia de cegamento nem de ausência de influência. O texto de C2 contém grafia degradada; os níveis pretendidos de clareza e consistência não são tomados como atingidos.

Antes do congelamento, C115 foi mudado de expectativa determinada para indeterminação: o texto lista operadores aceitos, mas não afirma que sejam os únicos. A alteração ocorreu por revisão documental, sem execução do SUT.
