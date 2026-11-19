# Limitações e validade - Experimento 1

## Ressalvas documentais

Quatro pares apresentam sobreposição formal de guardas e ações potencialmente conflitantes:

- TIS REQ002 x REQ006;
- TIS REQ003 x REQ006;
- TIS REQ004 x REQ006;
- NPP REQ005 x REQ008.

Os pares não foram classificados como conflitos semânticos confirmados.

## Alcançabilidade

As conjunções são SAT sob a formalização recebida. Não foi demonstrada alcançabilidade em uma máquina de estados ou implementação independente.

## Prioridade

Nenhum documento disponibilizado estabelece prioridade ou precedência entre os requisitos conflitantes potenciais.

## Variável NPP

`the_safety_injection_mode` não está declarado em `inputs` e não possui tipo, domínio ou classificação explícita. Sua menção em REQ009, REQ010 e REQ011 foi mantida como ação textual; nenhuma representação temporária foi adicionada aos documentos.

## Ausência de implementação

Não existe implementação independente dos sistemas VM, TIS e NPP. Os resultados medem discriminação em modelos expressos pelas guardas, não defeitos reais detectados em sistema.

## Mutation Testing

- os mutantes são sintéticos;
- mutantes equivalentes são excluídos;
- UNKNOWN não é usado como equivalente;
- um Mutation Score alto não prova correção semântica.

## Comparação

O Experimento 1 preservou integralmente guardas e ações do Experimento 0. Mudanças principais estão na clareza do texto natural C1 e no rastreamento das ressalvas. Diferenças numéricas só são interpretáveis como efeitos indiretos da documentação revisada, não como efeitos causais isolados.
