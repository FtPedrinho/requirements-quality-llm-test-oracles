# Formalizacao dos requisitos experimentais C1

## Fontes

As 36 unidades principais foram formalizadas a partir de `requirements/experimental/`:

- 5 requisitos VM;
- 17 requisitos TIS;
- 11 requisitos NPP;
- 3 expressões gerais.

## Representacao

- Booleanos: `Bool`;
- Inteiros: `Int`;
- Reais: `Real`;
- Enumerações: `Int` com restricao aos índices dos valores documentados;
- Guardas: reprodução das expressões estruturadas;
- Ações: registro de atribuicoes sem alteracao do JSON.

## Hypoteses e lacunas

`the_safety_injection_mode` aparece nas ações de NPP REQ009, REQ010 e REQ011, mas não possui declaração em `inputs`.

Nao foi criada declaracao no documento experimental. Esta lacuna nao foi formalizada como fato documental. Os resultados Z3 das guardas npp#9 a npp#11 permanecem independentes dessa representacao temporaria.

## Ressalvas semanticas

Os seguintes pares foram preservados como sobreposicoes formais:

- tis#2 x tis#6;
- tis#3 x tis#6;
- tis#4 x tis#6;
- npp#5 x npp#8.

Para os pares, Z3 encontrou SAT na conjuncao das guardas e encontrou atribuicoes diferentes na mesma variável de ação. Isso não demonstra alcançabilidade ou conflito semântico confirmado.
