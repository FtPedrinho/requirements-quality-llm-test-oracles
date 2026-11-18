# Avaliação da viabilidade da pesquisa

## 1. Adequação para clareza dos requisitos

**Avaliação: adequada com limitações.**

Há guardas curtas e longas, texto natural, identificadores e ações. O formato permite comparar documentos claros e ambíguos em experimentos futuros, mas não existe um corpus homogêneo de requisitos original.

Há candidatos a vaguidade e incompletude, como:

- limites temporais que não especificam unidades ou comportamento fora da fronteira em alguns textos auxiliares;
- termos de estado como “idle”, “choice”, “preparing weak” e “preparing strong” cuja definição operacional aparece apenas pelas ações;
- nomes `_antes` que precisam ser interpretados como transições de estado;
- exceções e comportamentos inválidos não documentados em várias decisões.

Essas observações são preliminares e não representam rótulos definitivos.

## 2. Adequação para consistência dos requisitos

**Avaliação: adequada com limitações.**

O `Z3RequirementsVerifier` é capaz de encontrar duas guardas simultaneamente verdadeiras que escrevem valores diferentes em uma mesma variável. Os JSON têm ações e estados partilhados, especialmente em VM, TIS e NPP, permitindo uma análise real de consistência.

O código é um verificador sobre a representação extraída em JSON, não uma prova da consistência do documento natural original. Antes de usar resultados automáticos como verdade, é necessário validar:

- fidelidade do parsing;
- correspondência entre `text`, `guard` e `actions`;
- significado de estados anteriores;
- restrições de domínio;
- contexto temporal.

## 3. Viabilidade do Gold Standard

**Avaliação: parcialmente viável.**

Os JSON fornecem entradas, guardas, ações e alguns limites, então é possível construir casos esperados para decisões isoladas. Em particular:

- VM fornece limites 30.0, 10.0 e 50.0;
- NPP fornece limites 9 e 10;
- TIS fornece limites 80, 220 e 340;
- `_antes` fornece eventos necessários para a transição.

Porém, um Gold Standard independente não pode ser derivado automaticamente só das guardas sem decisão humana sobre:

- domínio real das variáveis;
- combinações inválidas;
- relações temporais;
- resultados fora das ações listadas;
- comportamento inicial;
- output não mencionado;
- divergências entre texto natural e ação.

Exemplos com comportamento não determinável de forma segura:

- ações referem `the_safety_injection_mode` em NPP, mas o JSON não declara esse valor em `inputs`;
- várias decisões dependem de estados anteriores não presentes em todas as descrições;
- no [exemplos/testes.csv](../exemplos/testes.csv), `T4` é declarado incorreto no próprio comentário;
- não há implementação de domínio que confirme o significado das ações.

## 4. Viabilidade de Mutation Testing

**Avaliação tecnicamente viável, mas o experimento ainda não está definido.**

O projeto já usa PIT para produzir mutantes no código Java da ferramenta. Isso é diferente de Mutation Testing experimental dos sistemas descritos nos requisitos. Os artefatos já existentes em `relatorios/pit/` não são mutantes de VM, TIS ou NPP.

A implementação Java é compatível com PIT, JUnit 5 e Maven. Os componentes adequados a um eventual estudo são:

- expressão e parsing;
- tabela verdade;
- pares de independência;
- seleção de suíte;
- verificador Z3;
- CLI.

Obstáculos:

- não existe implementação de VM, TIS ou NPP para receber casos mutados;
- mutantes do motor medem qualidade dos testes da ferramenta, não defeitos nos oráculos gerados;
- os requisitos têm muitas variáveis e estados;
- a correspondência entre mutante de guardas e defeito de domínio precisa ser definida;
- Z3 pode ser externo e ausente.

Nenhum mutante novo ou experimento foi executado nesta etapa.

## 5. Unidades experimentais recomendadas

Recomendações:

1. **Decisões VM REQ001 a REQ005**: pequeno conjunto de estados e limites, com implementação de referência potencialmente verificável pelos exemplos.
2. **Transições NPP REQ001 a REQ008**: limites claros e estados anteriores; útil para consistência de transições.
3. **Ações NPP REQ009 a REQ011**: resultado de saída dependente de modo e override.
4. **Decisões TIS selecionadas**: `tis#1`, `tis#6` a `tis#9` e `tis#10` a `tis#17` podem representar eventos, timers e estados, mas o conjunto inteiro é grande.
5. **Expressão redundante `REQ-003`**: útil para investigar clareza e detecção de redundância, não consistência contraditória.

O conjunto total deve ser limitado por decisão, tamanho da expressão e disponibilidade de texto natural. Conjuntos maiores não garantem maior qualidade metodológica.

## 6. Obstáculos técnicos

- JDK 21 e Maven são obrigatórios;
- Z3 é necessário para recursos específicos;
- os testes Z3 podem ser ignorados sem o executável;
- o script `mcdc` exige compilação prévia;
- o PDF não foi extraído;
- os requisitos dos exemplos não têm implementação de domínio;
- não existe rastreabilidade oficial;
- há diferença entre contagens históricas e contagens obtidas nesta análise.

## 7. Ameaças à validade

Observadas:

- representatividade limitada a quatro exemplos;
- possíveis diferenças entre texto natural e guardas;
- ausência de implementação independente;
- bases históricas de cobertura e mutação não reproduzidas;
- exemplos gerados pela mesma ferramenta podem ter circularidade como referência.

Riscos potenciais:

- generalização inadequada para requisitos industriais;
- viés de seleção dos casos mais lógicos;
- variação de complexidade por sistema;
- incompletude do Gold Standard;
- dependência de Z3 e seu timeout;
- mutação artificial pouco representativa de defeitos reais.

## 8. Próximas etapas

Antes da implementação experimental:

1. obter ou confirmar o significado completo do PDF técnico;
2. definir a fonte canônica de cada requisito;
3. validar os JSON contra textos naturais por avaliadores humanos;
4. selecionar unidades experimentais independentes;
5. construir um esquema de Gold Standard aprovado;
6. estabelecer critérios de clareza e consistência;
7. verificar manualmente candidatos a ambiguidade e contradição;
8. decidir como Mutation Testing será aplicado: requisitos mutados, código mutado ou ambos;
9. reproduzir os testes básicos sem alterar o repositório;
10. confirmar dependências Z3 e ambiente JDK/Maven;
11. resolver o versionamento de `docs/`, atualmente excluído pelo `.gitignore`.
