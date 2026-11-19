# Análise da documentação C2

## Documento analisado

- Arquivo: `experimentacao/experimentacao-2/documentation/tool-readme-C2.md`
- Hash SHA-256: `3cb561f8ed827c65f9495accd2fb54af66abd41720a468f1b99fc88a0b717e2c`

Nenhuma correção ou consulta à documentação C1 foi usada nesta análise.

## Requisitos interpretáveis diretamente

Os trechos seguintes são suficientemente específicos para um oráculo parcial:

| Trecho literal | Interpretação possível |
|---|---|
| `comando tem analyze check verify` | Existem três comandos. |
| `se tiver opçao errada da erro` | Opções inválidas devem produzir erro. |
| `mascaramento e o normal que vem primeiro` | Mascaramento é o modo padrão. |
| `causa unica tambem existe mas escolhe ela` | Causa única pode ser selecionada. |
| `duas decisao na mesma variavel com valor diferente pode ser conflito` | Ações conflitantes em variável compartilhada podem gerar conflito. |
| `quando nenhuma serve pode ter lacuna` | Nenhuma decisão aplicável pode representar lacuna. |
| `expressao sozinha e direta` | Expressão direta é uma fonte. |
| `arquivo mcdc tem linha identificaçao e expressao` | `.mcdc` usa identificador e expressão por linha. |
| `json tem sistema entrada decisao` | JSON contém sistema, entradas e decisões. |
| `AND`, `OR`, `NOT` e operadores | Existem operadores lógicos e comparações. |
| `tabela 20 entrada` | O limite indicado é 20. |
| `linha 4096` | O limite indicado é 4096. |
| `direto 30` | O modo direto indica limite 30. |
| `condiçao 1000 par` | O limite indicado é 1000 pares. |
| `z3 60 segundo` | O timeout indicado é 60 segundos. |
| `zero sem problema`, `um entrada ou opçao ruim`, `dois...` | Códigos 0, 1 e 2. |

## Ambiguidades

### Comandos e ausência de comando

Trecho: `se nao coloca comando pode mostra instruçao ou nao depende`

Não determina claramente se a CLI sempre mostrará uso ou se alguma alternativa implícita existe.

### `analyze` e `check`

Trecho: `manda o que quer analisa e ela faz a analise`, `manda os teste e compara com o que foi informado`

Não especifica formatos completos, campos do resultado, condições de sucesso ou conteúdo exato.

### Check

Trecho: `os par pode ser conhecido ou nao conhecido`

Não determina como pares ausentes são reportados, nem como o resultado esperado é representado.

### Verify

Trecho: `olha as decisao junto`

Não especifica quais decisões são comparadas, qual informação de entrada é usada ou quando uma sobreposição é compatível.

### Saídas

Trecho: `cada um mostra de um jeito pode nao mostra tudo igual`

Não permite determinar quais campos, colunas ou estruturas são garantidos.

## Informações incompletas

- Não define o formato completo do CSV de testes.
- Não define todos os campos do JSON.
- Não define quais informações aparecem em cada saída.
- Não define o formato exato da tabela ou dos vetores.
- Não informa como uma combinação impossível é marcada em todos os formatos.
- Não define o comportamento exato quando Z3 retorna UNKNOWN.
- Não define o comportamento exato de arquivos vazios ou campos ausentes.
- Não define como pares máximos são truncados.

## Possíveis interpretações

- `check` pode aceitar resultados booleanos ou valores concretos, mas o texto não distingue.
- `verify` pode comparar todas as decisões ou apenas decisões que compartilham ações, sem especificação suficiente.
- “não terminou” pode significar código de saída, ausência de resultado ou exceção.
- “linha 4096” pode referir-se a combinações, mas a palavra não declara explicitamente a unidade.

## Conclusão

A documentação permite oráculos determinados apenas para aspectos explícitos e isolados. Comandos, fontes, operadores, limites e códigos podem ser parcialmente formalizados. Relações como conteúdos de relatório, exatamente como check trata pares e a semântica completa de verify permanecem ambíguas ou indeterminadas.
