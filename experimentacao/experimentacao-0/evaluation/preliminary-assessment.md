# Avaliação preliminar

## Possibilidades observadas

- Os 36 requisitos carregados têm expressões formalizáveis em Z3.
- Todas as expressões individuais tiveram pelo menos um modelo SAT.
- Foram encontrados pares simbólicos para todas as 119 folhas das decisões NAT2TEST.
- O catálogo gerou 36 oráculos e 152 casos simbólicos.
- Foram detectadas implicações formais no NPP e incompatibilidades potenciais em TIS e NPP.

## Limitações

- Não foi consultada implementação de domínio.
- Não foi realizada validação humana nesta etapa.
- Não foram produzidos valores concretos completos para todas as combinações.
- Não foi demonstrada cobertura MC/DC executável.
- Nenhum Mutation Score foi calculado.
- A ausência de UNSAT não significa correção textual.
- Os resultados dependem da tradução das guardas e enumerações.

## Conclusão exploratória

Os requisitos originais permitem uma linha de base formal parcial e uma geração inicial de oráculos estruturados. A utilidade das formalizações é limitada por informações temporais, de domínio e de implementação não explicitadas nos documentos consultados.
