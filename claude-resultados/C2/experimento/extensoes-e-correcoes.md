# Correções e extensões — C2

## Correções

Nenhuma correção de oráculo, de suíte ou de rodada. Nenhuma expectativa foi alterada
depois do congelamento.

Ajuste feito **antes** do congelamento do oráculo (registrado por transparência):
a consulta Z3 `Q14-fronteira-*` da primeira geração tinha um erro de ordem (a asserção de
unicidade de `x` deixava o contexto `unsat` antes do bloco de `y`). O script
`scripts/gerar_z3.py` foi corrigido (push/pop por bloco) e todas as consultas foram
regeradas do zero antes do congelamento de 11:07:01. Os arquivos congelados são os da
geração corrigida.

## Extensão r2 (`extensao-r2/`)

- **Motivo:** a cobertura do baseline r1 (83,02%, medida com os indeterminados) apenas localizou áreas pouco exercitadas:
  codificação SMT de comparações `<`, `<=`, `>=`, `!=`, reais, enumerações e negativos;
  modo direto em sistemas e em arquivo `.mcdc`; CSV da suíte com valores concretos e
  fronteira; `check` e `verify` com `--format json` e `-o`; relatório em texto do VM com
  fronteira e mutação; `truth-csv` na causa única.
- **Suporte documental:** cada caso X01–X12 reusa uma leitura já registrada em
  `analise-oraculo.md` (L41/L463 valores concretos; L417 comparações acopladas; L153 tipos
  do JSON; L419 modo direto com o mesmo diagnóstico; L241 REQ-003; L121/L123 formatos e
  `-o`; L471/L475 números de VM e NPP; L205/L207/L485 formatos CSV). Nenhuma expectativa
  vem do comportamento observado nem da cobertura.
- **Z3:** `extensao-r2/z3/` (X01–X03: viabilidade das combinações e pares de causa única;
  tipos declarados explicitamente porque a expressão direta não declara tipos: inteiros
  para variáveis numéricas, inclusive `y <= x`, e domínio textual aberto para `m`).
  Nenhuma resposta `unknown`.
- **Congelamento:** `congelamento/extensao-r2.sha256` às 2026-11-24 11:17:14 -0300,
  antes da execução (oráculo de extensão, entradas, consultas/saídas Z3, runner r2).
- **Runner r2:** mesma lógica de asserções do r1; só acrescenta as opções `--oraculo`,
  `--manifesto` e `--entradas` (diferença em `suite/versoes/`).
- **Resultado:** 12 PASSOU, 0 FALHOU. Branch Coverage acumulada oficial (só casos determinados, r3+r4): 1091/1296 (84,18%); r1+r2 com indeterminados: 1099/1296 (84,80%).
