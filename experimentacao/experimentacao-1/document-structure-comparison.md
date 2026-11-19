# Comparação estrutural da documentação — Experimento 0 versus Experimento 1

## Experimento 0

Os JSON NAT2TEST continham os textos originais em `text`, guardas em `guard`, tipos em `inputs` e ações em `actions`.

Arquivos `.mcdc` continham identificador e expressão.

## Experimento 1

Os textos naturais em `text` foram padronizados:

- remoção de dois-pontos após `shall`;
- padronização de `Assign` e `Reset`;
- uniformização de espaçamento e pontuação.

As estruturas semânticas permaneceram iguais:

| Elemento | Mudança |
|---|---|
| Guardas | Nenhuma |
| Ações | Nenhuma |
| Tipos | Nenhum |
| Valores numéricos | Nenhum |
| Enumerações | Nenhuma |
| Condições temporais | Nenhuma |
| Arquivos `.mcdc` | Nenhuma |
| IDs e requisitos | Nenhum |

## Efeitos esperados

Uma LLM pode interpretar melhor os textos naturais do Experimento 1, mas o motor MC/DC histórico não usa `text` como entrada semântica. Ele analisa `guard` e não os textos naturais.

Por isso, os resultados históricos iguais não são prova de que a documentação não influencia oráculos em geral. Eles mostram que a transformação C1 anterior não alterou as estruturas consumidas pelo pipeline do Experimento 0/1.

## Limitação

Penderam conflitos semânticos e lacunas do JSON. A clareza aumentou, mas consistência semântica não foi confirmada.
