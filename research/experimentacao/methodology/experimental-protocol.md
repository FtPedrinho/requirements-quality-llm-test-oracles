# Protocolo reconstruído dos Experimentos 0 e 1

## Sistema sob teste

O SUT é a implementação Java da ferramenta MC/DC neste repositório.

Os sistemas VM, TIS e NPP são entradas de demonstração do SUT e não são sistemas sob teste.

## Condição dos experimentos

- Experimento 0: cópias da documentação original da ferramenta.
- Experimento 1: cópias independentes com clareza, precisão, completude e consistência aprimoradas sem alteração funcional.

## Controle

- mesmo commit do SUT;
- mesma versão Java;
- mesmo Z3;
- mesma CLI;
- mesmo prompt-base;
- mesmas unidades de comportamento;
- mesma suíte de validação.

## Geração dos oráculos

O LLM recebe somente a documentação da condição. Código-fonte, testes existentes, Mutation Reports e resultados históricos ficam fora do contexto.

## Gabarito

O gabarito é construído independentemente com base na especificação original, revisão técnica e evidências executáveis da implementação.

## Unidade

A unidade principal é um comportamento especificável e verificável da ferramenta MC/DC.

## Métricas

- correction semântica;
- completeza;
- rastreabilidade;
- casos não avaliáveis;
- Precision, Recall e F1 por unidade de comportamento;
- Mutation Score sobre mutantes Java da implementação;
- aprovação da suíte real.

## Mutation Testing

Somente mutantes da implementação Java serão usados como resultados principais. PIT deve ser separado dos mutantes internos de expressões e dos antigos mutantes JSON.
