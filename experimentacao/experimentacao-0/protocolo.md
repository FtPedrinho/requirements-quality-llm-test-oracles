# Protocolo da Experimentação 0

## Fontes utilizadas

Fontes normativas prioritárias:

- `exemplos/requisitos.mcdc`;
- `exemplos/maquina-cafe.mcdc`;
- `exemplos/vm-requisitos.mcdc`;
- `exemplos/vm-decisoes.json`;
- `exemplos/tis-decisoes.json`;
- `exemplos/npp-decisoes.json`.

O PDF técnico da ferramenta é tratado como documentação arquitetural, não como requisito normativo dos sistemas VM, TIS ou NPP.

## Exclusões desta etapa

Não foram consultados:

- código-fonte da implementação;
- testes JUnit;
- CSVs de casos de teste externos;
- relatórios JaCoCo ou PIT;
- resultados interpretativos históricos da ferramenta;
- implementações dos sistemas de domínio.

## Sequência

1. Registrar identificador, origem, texto e expressão de cada requisito.
2. Formalizar guardas compatíveis com Z3 e registrar interpretações inferidas.
3. Executar satisfatibilidade, redundância, equivalência, implicação, incompatibilidade e MC/DC.
4. Registrar os resultados formais antes da geração dos oráculos.
5. Gerar os oráculos apenas a partir dos documentos normativos.
6. Comparar os oráculos com as formalizações.
7. Derivar casos de teste simbólicos e identificar limites de verificabilidade.
8. Preparar material para validação humana.

## Critérios

- SAT exige pelo menos um modelo.
- UNSAT exige demonstração da inexistência de modelo.
- UNKNOWN é registrado sem converter em falha ou contradição.
- Redundância lógica não é automaticamente incompatibilidade.
- Expressões equivalentes não são automaticamente correção semântica.
- Contraexemplos são evidências formais da formalização, não da intenção original.
- Casos MC/DC são classificados como simbólicos ou concretos conforme o domínio disponível.

Nenhuma expressão inferida é apresentada como texto original.
