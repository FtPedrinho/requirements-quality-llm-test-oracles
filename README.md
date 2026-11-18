# Impacto da qualidade dos requisitos na geração de oráculos de teste por LLMs

Este repositório é o ambiente de pesquisa de uma investigação experimental sobre como a qualidade documental de requisitos influencia os oráculos de teste gerados por Large Language Models (LLMs).

A proposta combina um desenho experimental controlado, Controlled Natural Language (CNL), verificação lógica com Z3 e avaliação semântica por métricas e avaliadores humanos.

## Pergunta central

> Em que medida a clareza e a consistência da documentação de requisitos influenciam a correção semântica e a cobertura dos oráculos de teste gerados por LLMs?

## Objetivo

Investigar experimentalmente a influência de dois fatores documentais:

- **clareza:** precisão com que os requisitos descrevem condições, estados e comportamentos esperados;
- **consistência:** ausência de contradições entre requisitos relacionados.

A qualidade dos oráculos será comparada com uma especificação de referência independente, construída e validada a partir dos requisitos originais.

## Motivação

Os oráculos determinam se o comportamento observado em um teste corresponde ao resultado esperado. LLMs podem gerar oráculos a partir de requisitos em linguagem natural, mas dependem diretamente das informações recebidas.

Ambiguidade, vaguidade, contradições e imprecisão podem produzir oráculos aparentemente plausíveis, porém incorretos, incompletos ou apoiados em suposições não documentadas.

A pesquisa busca evidências empíricas sobre a contribuição de requisitos mais claros e consistentes para oráculos mais corretos e completos.

## Perguntas específicas

- **RQ1:** Como a clareza dos requisitos influencia a correção semântica dos oráculos gerados por LLMs?
- **RQ2:** Como a inconsistência entre requisitos influencia a correção semântica dos oráculos?
- **RQ3:** Existe interação entre clareza e consistência na qualidade dos oráculos?

## Desenho experimental

O estudo utiliza um desenho fatorial 2 × 2. A documentação canônica será manipulada para criar quatro condições:

| Condição | Clareza | Consistência |
|---|---|---|
| C1 | Alta | Alta |
| C2 | Baixa | Alta |
| C3 | Alta | Baixa |
| C4 | Baixa | Baixa |

Todas as condições derivam da mesma documentação de referência. As manipulações são controladas:

- **clareza baixa:** introdução de ambiguidades e vaguidade;
- **consistência baixa:** introdução de contradições entre requisitos, preservando, tanto quanto possível, a clareza individual das regras.

As manipulações deverão ser validadas para confirmar que os fatores foram alterados de maneira independente.

## Metodologia

### 1. Seleção dos requisitos

Pretende-se utilizar o dataset PURE (PUblic REquirements dataset), composto por 79 documentos e aproximadamente 34.268 sentenças. Serão selecionados documentos ou grupos de requisitos com comportamentos funcionais, condições e resultados identificáveis.

A seleção deve evitar requisitos cujo comportamento esperado não possa ser determinado com confiabilidade.

### 2. Construção do Gold Standard

O comportamento esperado será decomposto em afirmações verificáveis:

- condições de entrada;
- estado anterior, quando aplicável;
- evento ou condição de disparo;
- resultado esperado;
- casos-limite documentados;
- comportamentos não especificados.

O Gold Standard será uma referência independente construída a partir das especificações originais e validada por avaliadores humanos. Divergências devem ser resolvidas antes da avaliação dos oráculos.

### 3. Formalização com CNL e Z3

Os requisitos selecionados serão representados em Controlled Natural Language e convertidos em estruturas lógicas processadas pelo Z3.

```text
Requisitos em linguagem natural
             ↓
Controlled Natural Language
             ↓
Formalização lógica
             ↓
Z3 — verificação formal
```

Serão investigadas:

| Propriedade | Finalidade |
|---|---|
| Consistência | Identificar regras que podem produzir resultados incompatíveis |
| Completude | Identificar estados relevantes sem regra aplicável |
| Alcançabilidade | Verificar se as condições podem ser satisfeitas |
| Redundância | Identificar regras que não acrescentam comportamento novo |

O Z3 poderá fornecer modelos de contraexemplo e unsat cores. A formalização não substitui a validação humana da tradução da linguagem natural.

### 4. Geração dos oráculos

Um LLM receberá as documentações experimentais e deverá gerar oráculos sem inventar comportamentos não documentados. Serão controlados:

- modelo e versão;
- prompt;
- temperatura e demais parâmetros;
- formato de entrada e saída;
- contexto fornecido.

Serão realizadas múltiplas execuções por condição para medir a variabilidade do modelo.

### 5. Avaliação dos oráculos

Cada oráculo será comparado com o Gold Standard.

**Correção semântica**

\[
\text{Correção}
= \frac{\text{Expectativas corretas}}
{\text{Expectativas avaliáveis}}
\times 100
\]

**Cobertura de requisitos**

\[
\text{Cobertura}
= \frac{\text{Requisitos verificados validamente}}
{\text{Requisitos aplicáveis}}
\times 100
\]

Métricas complementares:

- precisão;
- recall;
- F1-score;
- especificidade dos oráculos;
- taxa de reconhecimento de ambiguidades e contradições.

A avaliação poderá ser realizada por avaliadores humanos independentes, com critérios previamente definidos e concordância medida por Cohen's Kappa ou Krippendorff's Alpha.

### 6. Análise dos resultados

Os resultados devem considerar:

- efeito principal da clareza;
- efeito principal da consistência;
- interação entre clareza e consistência;
- estrutura de medidas repetidas por documento e por execução.

Hipóteses prévias:

- **H1:** maior clareza tende a produzir oráculos mais corretos;
- **H2:** inconsistências tendem a reduzir a correção ou aumentar interpretações incompatíveis;
- **H3:** baixa clareza combinada com baixa consistência pode produzir efeito negativo adicional.

Resultados nulos ou contrários às hipóteses também serão considerados válidos.

## Variáveis do estudo

| Categoria | Variáveis |
|---|---|
| Independentes | Clareza documental e consistência documental |
| Dependentes principais | Correção semântica e cobertura dos oráculos |
| Dependentes complementares | Precisão, recall, F1, especificidade e reconhecimento de problemas |
| Controles | Modelo, versão, prompt, parâmetros, contexto e dados de entrada |

## Fork para o experimento

Em uma etapa posterior, este repositório poderá receber forks de projetos que contenham, no mesmo snapshot:

- documentação de requisitos;
- implementação do sistema;
- suíte de testes existente;
- configuração reproduzível do build;
- metadados necessários para rastreabilidade.

Os forks deverão ser usados para análises comparáveis de oráculos gerados por LLMs. Os resultados podem incluir:

- correção semântica dos oráculos;
- cobertura dos requisitos;
- precisão, recall e F1;
- reconhecimento de ambiguidades e inconsistências;
- mutation score obtido pela execução dos oráculos ou testes associados.

As versões usadas, prompts, parâmetros dos modelos, commits dos forks e resultados brutos devem ser preservados para garantir reprodutibilidade.

## Proposta de Mutation Testing

A Mutation Testing será definida antes da execução do experimento. Duas possibilidades independentes são possíveis:

1. mutar requisitos ou guardas para verificar se os oráculos detectam a alteração;
2. mutar o código do sistema e verificar se os oráculos produzem testes ou expectativas capazes de detectar os defeitos.

Os artefatos existentes deste repositório original não devem ser tratados automaticamente como o sistema experimental:

- PIT mede mutantes da própria ferramenta MC/DC;
- os exemplos VM, TIS e NPP não possuem, neste snapshot, implementação de domínio correspondente;
- Mutation Testing dos sistemas exige uma versão mutável do sistema e um critério independente de sucesso.

## Escopo e limitações

O estudo concentra-se em qualidade semântica e não demonstra, por si só, a capacidade dos oráculos de detectar defeitos reais em implementações.

O dataset PURE não fornece geralmente suítes completas de testes associadas aos requisitos. Assim, a pesquisa precisa construir uma referência independente.

Os resultados do Z3 serão limitados à formalização recebida. O Z3 não verifica a intenção original do cliente, a clareza linguística ou a correção de uma tradução equivocada.

Outras limitações previstas:

- representatividade limitada dos documentos selecionados;
- subjetividade da clareza e da consistência;
- custo de avaliação humana;
- incompletude possível do Gold Standard;
- variabilidade dos LLMs;
- generalização limitada a outros domínios e modelos;
- dependência da qualidade da tradução para CNL.

## Contribuições esperadas

1. evidências empíricas sobre o efeito da clareza e da consistência na geração de oráculos;
2. uma metodologia controlada para comparar versões documentais;
3. integração entre CNL, Z3 e avaliação semântica;
4. caracterização dos erros dos modelos diante de requisitos ambíguos ou contraditórios;
5. recomendações para documentação usada como entrada em ferramentas automáticas de teste;
6. dados reprodutíveis sobre correção, cobertura e Mutation Testing.

## Estado atual

Este repositório iniciou pela caracterização do projeto MC/DC como candidato ao estudo. A execução experimental ainda não foi realizada.

Documentação desta etapa:

- [documentação do repositório base](docs/README.md)
- [análise técnica](docs/repository-analysis.md)
- [caracterização como dataset](docs/dataset-characterization.md)
- [avaliação da viabilidade](docs/research-feasibility.md)
- [matriz de rastreabilidade](docs/traceability-matrix.md)
