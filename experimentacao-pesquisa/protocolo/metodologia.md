# Protocolo comum dos experimentos C0–C4

## 1. Objetivo e independência

Avaliar a geração por LLM de oráculos e suítes para a ferramenta Java MC/DC
sob diferentes documentações. Cada experimento usa este mesmo protocolo e o
mesmo prompt-base; apenas a documentação da condição muda. Nenhuma condição
depende da execução, suíte, oráculo ou resultado de outra. Não fornecer
resultados anteriores ao modelo nem usá-los como gabarito ou meta.

O documento da condição é a **verdade absoluta para o experimento**: somente
ele define as expectativas do oráculo, independentemente do comportamento do
sistema. Isso é uma regra metodológica, não prova de que o documento descreve
objetivamente o produto. Não alterar, corrigir, substituir ou reescrever a
documentação técnica/de requisitos nem o sistema sob qualquer circunstância.

## 2. Fontes das condições

Antes de ler a fonte, verificar o SHA-256 completo; se estiver ausente ou não
coincidir, interromper e registrar o bloqueio. Não substituir a fonte por
outra sem decisão explícita do pesquisador.

| Condição | Fonte normativa exclusiva | SHA-256 |
|---|---|---|
| C0 | [tool-readme-original.md](../documentacao-original/tool-readme-original.md) | `72B827BDEE6CE859527765CFF574A473519C00A1AF9AA9F3AACCE4236A4995F8` |
| C1 | [tool-readme-C1.md](../experimentacao-1/documentation/tool-readme-C1.md) | `91981FA0181E5CC1BC5A67DAAFC965BB82D6F8EB0A6D47EB58CE291A3EF5D33B` |
| C2 | [tool-readme-C2.md](../experimentacao-2/documentation/tool-readme-C2.md) | `61C4062B5FC6B4F364F40465B0E017C80E0FA0C5433412EB2E925C545F6EFBE1` |
| C3 | [tool-readme-C3.md](../experimentacao-3/documentation/tool-readme-C3.md) | `F18B0821D79C7315486C13D5260FA2F6D6E9418EF03B86CDE58E66B91B7B87A3` |
| C4 | [tool-readme-C4.md](../experimentacao-4/tool-readme-C4.md) | `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2` |

C0 é a documentação original, sem atribuição automática de nível. Para
C1–C4, alta/alta, baixa/alta, alta/baixa e baixa/baixa são níveis de
clareza/consistência pretendidos, não resultados presumidos. Outras cópias
documentais não substituem a fonte da condição.

## 3. Procedimento de cada experimento

### 3.1 Preparação independente

Identificar a condição, a fonte, seu hash, o prompt, o modelo e a configuração
disponíveis. Usar o [prompt comum](../prompts/geracao-de-oraculos-v3.md).
Registrar o contexto recebido e qualquer perda de isolamento. Não afirmar
cegamento ou ausência de influência que não possam ser demonstrados. Cada
geração deve poder começar sem consultar ou executar outro experimento.

### 3.2 Oráculo documental e Z3

Antes de ler código ou saída do SUT:

1. Ler integralmente a fonte da condição e inventariar requisitos,
   comportamentos, entradas, saídas, erros, fronteiras e exemplos aplicáveis.
2. Para cada caso, registrar ID, entrada, pré-condições, trecho literal,
   regra, expectativa e justificativa. Não acrescentar semântica a lacunas.
3. Registrar como **INDETERMINADO** o caso sem expectativa única por
   omissão, ambiguidade ou conflito que o próprio texto não resolva. Não
   decidir pelo código, por resultados, por cobertura ou por suposições.
4. Formalizar em SMT-LIB as restrições pertinentes e executar
   **obrigatoriamente Z3 independente do SUT**. Preservar versão, fórmulas,
   consultas, `sat`/`unsat`/`unknown`, testemunhas e limites. Não usar a
   saída do módulo `mcdc-z3` ou da CLI avaliada como oráculo.
5. `sat` e `unsat` dizem respeito à fórmula, não provam fidelidade da
   tradução documental. `unknown`, timeout ou indisponibilidade de Z3 são
   erros técnicos, não indeterminação documental; interromper ou registrar
   os casos afetados como não avaliados até resolver o bloqueio.
6. Revisar a relação texto–fórmula e congelar análise, regras, casos,
   entradas, expectativas e evidências Z3 por SHA-256 antes de ler o SUT.
   Se não houver revisor independente, registrar que a revisão é própria.

### 3.3 Suíte e execução

Após o congelamento, inspecionar o código apenas para compreender como
invocar o MC/DC real e alcançar comportamentos documentados. Criar uma suíte
nova a partir dos oráculos congelados, buscando a maior Branch Coverage
possível e casos significativos, sem duplicatas sem contribuição. A cobertura
ou o comportamento observado nunca definem ou alteram expectativas.

Congelar a suíte e suas entradas por SHA-256 antes da execução. Executar sem
modificar o SUT, qualquer documentação de requisitos/técnica ou os oráculos
congelados. Preservar asserções falhas: se o resultado observado contrariar
uma expectativa documental determinada e sustentada pelo texto, registrar
**FALHOU** como divergência em relação à referência adotada.

Um caso indeterminado não recebe aprovação nem falha semântica. Pode ser
executado apenas como diagnóstico sem expectativa inventada. Uma falha de
infraestrutura, compilação ou solver deve ser registrada separadamente;
não é falha semântica nem indeterminação documental.

Se a documentação sustentar uma expectativa única para uma situação ainda
não testada, uma extensão pode acrescentar casos. Cobertura pode localizar
branches não exercitados, nunca fornecer a expectativa. Congelar a extensão e
suas entradas antes de executá-la e preservar o baseline e os resultados por
rodada. Sem suporte documental, registrar a lacuna como indeterminada.

## 4. Métricas

As métricas da pesquisa são exclusivamente:

1. **Branch Coverage:** branches executados / branches totais × 100.
2. **Quantidade de testes que passaram:** casos determinados cuja observação
   satisfez a expectativa documental.
3. **Quantidade de testes que falharam:** casos determinados cuja
   observação contrariou a expectativa documental.
4. **Quantidade de testes indeterminados:** casos registrados sem expectativa
   documental única, executados ou não como diagnóstico.

Usar uma unidade de contagem explícita e IDs estáveis; não contar uma
repetição do mesmo caso como novo teste. Não incluir erros técnicos,
testes inválidos ou casos não avaliados como aprovação ou falha. Registrá-los
separadamente como informação operacional, sem criar métricas adicionais.
Preservar resultados por caso e diferenças entre rodadas.

Instrumentar o SUT real com a suíte gerada. O denominador de Branch Coverage
inclui todas as classes de produção dos quatro módulos, inclusive classes
não carregadas e classes de mutação; excluir harness e bibliotecas externas.
Não executar análises de mutação para esta pesquisa. Registrar ferramenta,
versão, escopo, branches cobertos e total. Se o denominador for zero, informar
`não calculável`; se não for possível medir, informar `não coletado` e a
razão. Não alegar máximo global sem busca exaustiva demonstrada.

## 5. Registro e preservação

Guardar cada execução e suas evidências **fora desta pasta metodológica**:
fonte/hash, prompt, contexto, fórmulas e resultados Z3, oráculos, suíte,
comandos, ambiente, commit de referência, hashes, resultados por caso e
relatório. Usar o [modelo de relatório](modelo-relatorio.md). Registrar
dados não disponíveis como `não informado`, sem estimativas; não sobrescrever
uma execução anterior. Compilar e gravar saídas em local de trabalho
separado, sem modificar fontes ou documentos.

Ao comparar resultados, informar diferenças de modelo, prompt, ambiente,
escopo e unidade de teste; não inferir causalidade ou equivalência sem
controles suficientes. Relatar limitações sem ocultar resultados baixos.
