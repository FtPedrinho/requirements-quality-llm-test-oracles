# Inventário das expressões formalizadas

## Fontes normativas

| Fonte | Quantidade | Uso |
|---|---:|---|
| `exemplos/vm-decisoes.json` | 5 | Máquina de café |
| `exemplos/tis-decisoes.json` | 17 | Turn Indicator System |
| `exemplos/npp-decisoes.json` | 11 | Safety Injection System |
| `exemplos/requisitos.mcdc` | 3 | Expressões gerais |
| **Total** | **36** | **36 expressões carregadas** |

Arquivos `.mcdc` derivados de VM e da máquina de café auxiliar não foram tratados como novas decisões independentes; eles repetem ou simplificam guardas já presentes em fontes JSON ou expressões auxiliares.

O PDF técnico foi registrado como arquitetura da ferramenta e não utilizado como fonte normativa dos sistemas.

## Representação

- Variáveis booleanas: Z3 `Bool`.
- Inteiros: Z3 `Int`.
- Reais: Z3 `Real`.
- Enumerações: Z3 `Int` com restrição de domínio pelo índice de cada valor.
- Operadores originais `and`/`or` também são aceitos após tradução das formas `/\` e `\/`.
- Comparações `=`, `!=`, `<`, `<=`, `>`, `>=` são formalizadas.

## Origem das interpretações

- Variáveis com sufixo `_antes` foram formalizadas como variáveis distintas.
- Enumerações foram representadas por índices restritos aos valores documentados.
- Valores não declarados em `inputs` não foram inventados.
- Formalizações inferidas são separadas do texto original em `metadata.md` e no protocolo.

## Limitações

- Relações temporais de estado não foram expandidas além das variáveis `_antes`.
- Expressões abstratas não representam toda a semântica de domínio.
- Não foi criada implementação dos sistemas para validar modelos concretos.
- Repetições da mesma variável não foram concretizadas em todos os vetores.
