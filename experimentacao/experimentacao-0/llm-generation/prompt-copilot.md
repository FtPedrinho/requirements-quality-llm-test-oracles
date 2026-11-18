# Prompt integral da geração independente

Você receberá um requisito original por vez ou um conjunto pequeno de requisitos originais.

Sua tarefa é produzir um oráculo estruturado sem consultar código-fonte, testes JUnit, CSV de testes, resultados históricos, implementação do domínio ou resultados formais produzidos pelo Z3.

Use somente o texto original, a guarda original, as ações explícitas, o identificador e o arquivo de origem.

Não invente estados, saídas, regras ou relações não documentadas.
Não interprete ausência de informação como comportamento falso.
Registre comportamentos não determináveis.
Apresente interpretações alternativas quando existirem.
Não resolva contradições silenciosamente.
Diferencie redundância, ambiguidade e inconsistência.
Não declare formalmente validado.

Produza para cada requisito:

| Campo | Conteúdo |
|---|---|
| Oracle ID | Identificador novo |
| Requirement ID | Identificador original |
| Preconditions | Condições necessárias explicitamente suportadas |
| Initial State | Estado inicial, se especificado |
| Inputs | Entradas relevantes |
| Conditions | Condições lógicas |
| Trigger/Event | Evento ou operação |
| Expected Decision | Resultado da decisão |
| Expected Action | Ação esperada |
| Expected Output | Saída esperada |
| Expected State | Estado final esperado |
| Rationale | Justificativa documental |
| Source Reference | Arquivo e localização |
| Uncertainties | Informações insuficientes |

Os dados formais Z3 não devem ser fornecidos nesta etapa.
