# Decisões de revisão

## Regras adotadas

As revisões aplicadas às cópias foram limitadas a:

- padronização de pontuação;
- padronização de palavras `shall`, `assign` e `reset`;
- remoção de espaçamento ou uso de dois-pontos entre a cláusula e a ação;
- manutenção integral das guardas;
- manutenção integral das ações;
- manutenção integral dos domínios e tipos;
- manutenção das lacunas sem preenchimento por suposição.

Nenhuma condição, limite, estado, ação ou comportamento foi alterado.

## Decisões por documento

### `vm-decisoes.json`

Os cinco textos foram padronizados para uma forma declarativa uniforme. Os limites 30.0, 10.0 e 50.0 foram preservados.

**Decisão:** manter separadamente os requisitos de café fraco e café forte. Não foi alterada a regra que usa `<= 30.0` em VM REQ002 e `> 30.0` em VM REQ003.

**Clareza revisada:** alta.

**Pendências:** nenhuma pendência crítica encontrada nesta revisão.

### `tis-decisoes.json`

Os dezessete textos foram padronizados. Nenhuma regra foi removida ou corrigida.

Os pares formais seguintes permanecem pendentes:

- TIS REQ002 versus REQ006;
- TIS REQ003 versus REQ006;
- TIS REQ004 versus REQ006.

Cada par pode satisfazer suas guardas simultaneamente e atribuir valores diferentes a `the_indication_lights`. Como não há evidência documental suficiente sobre prioridade ou impossibilidade temporal, não foi escolhida uma interpretação.

**Clareza revisada:** alta.

**Consistência revisada:** não confirmada até resolução humana.

### `npp-decisoes.json`

Os textos foram padronizados sem alterar guardas ou ações.

Permanece pendente:

- NPP REQ005 versus REQ008: ambas as guardas podem ser satisfeitas, enquanto uma atribui `true` e outra `false` a `the_overridden_mode`.
- NPP REQ009: define a ação sobre `the_safety_injection_mode`, mas o JSON não declara essa variável em `inputs`.

Não foi adicionada uma variável, domínio ou prioridade inexistente.

**Clareza revisada:** alta.

**Consistência revisada:** não confirmada até resolução humana.

### Arquivos `.mcdc`

- `requisitos.mcdc`: três expressões mantidas sem alteração.
- `vm-requisitos.mcdc`: cinco guardas mantidas sem alteração.
- `maquina-cafe.mcdc`: decisão auxiliar mantida sem alteração.

Os arquivos não foram usados para criar novas regras ou resolver ambiguidades.
