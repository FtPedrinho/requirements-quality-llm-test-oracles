# Documentação e geração de testes por LLMs

Esta pesquisa estuda como clareza e consistência da documentação técnica influenciam a geração de testes e oráculos por modelos de linguagem para a ferramenta Java MC/DC deste repositório.

- **Protocolo e condições:** [experimentacao-pesquisa/](experimentacao-pesquisa/)
- **Relatórios e suítes do Copilot:** [copilot-resultados/](copilot-resultados/)
- **Evidências complementares do C0 oficial:** [resultados-llm/](resultados-llm/)
- **Documentos de contexto e inventários:** [research/](research/)
- **Fontes experimentais C0-C4:** [protocolo e fontes](experimentacao-pesquisa/protocolo/metodologia.md)

O conjunto de resultados do Copilot é adotado como a primeira coleta da
pesquisa. Essa decisão não elimina as limitações registradas em cada relatório.

## Objetivo e questões de pesquisa

Investigar como diferentes níveis de clareza e consistência da documentação técnica influenciam a geração de oráculos e suítes de testes por LLMs, observando Branch Coverage e quantidades de testes aprovados, falhos e indeterminados.

- **RQ1:** Como a redução da clareza documental influencia a cobertura estrutural dos testes gerados?
- **RQ2:** Como a redução da consistência documental influencia a cobertura estrutural dos testes gerados?
- **RQ3:** Como a combinação de baixa clareza e baixa consistência influencia a geração de testes?
- **RQ4:** Como os atributos documentais influenciam as quantidades de testes aprovados, falhos e indeterminados?
- **RQ5:** Quais limitações documentais e operacionais afetam a interpretação desses resultados?

## Experimentos

| C | Clareza | Consistência | Papel |
|---|---|---|---|
| C0 | Documentação original, caracterizar sem atribuir alto/baixo por suposição | Documentação original, caracterizar sem atribuir alto/baixo por suposição | Condição natural, reportada separadamente |
| C1 | Alta pretendida | Alta pretendida | Fatorial 2×2 |
| C2 | Baixa pretendida | Alta pretendida | Fatorial 2×2 |
| C3 | Alta pretendida | Baixa pretendida | Fatorial 2×2 |
| C4 | Baixa pretendida | Baixa pretendida | Fatorial 2×2 |

As fontes C0-C4 devem ser preservadas sem edição. Os rótulos C1-C4 representam manipulações pretendidas, não uma validação independente já concluída.

## Metodologia e métricas

A geração ocorre em duas etapas: primeiro, a IA deriva e formaliza o oráculo a partir da documentação congelada, usando obrigatoriamente Z3 independente; depois, inspeciona o código para criar e executar a suíte contra o SUT real. A documentação é tratada como verdade absoluta para o experimento: se o SUT divergir de uma expectativa documental determinada, o teste deve falhar sem adaptar o oráculo ao código. Cada condição segue o mesmo protocolo e não depende de outra execução.

Métricas quantitativas atuais:

1. **Branch Coverage:** branches executados / branches totais × 100.
2. **Quantidade de testes aprovados.**
3. **Quantidade de testes falhos.**
4. **Quantidade de testes indeterminados.**

Registrar erros técnicos e casos inválidos separadamente, sem confundi-los com falhas semânticas ou indeterminações. A suíte busca a maior Branch Coverage possível sem modificar o SUT ou as expectativas documentais.

A classificação dos oráculos mede fidelidade à documentação congelada, não a verdade objetiva da documentação ou a correção geral do sistema. Contradições e ambiguidades sem expectativa única são indeterminadas; pressupostos sem suporte não são conformes. Não usar o gabarito legado de 19 itens, o catálogo candidato de 20 itens, Mutation Score, Precision, Recall ou F1 como método atual.

O procedimento detalhado, as fontes e as limitações estão no [protocolo](experimentacao-pesquisa/protocolo/metodologia.md).

## Preservação e escopo

O sistema Java e as documentações técnicas e de requisitos C0-C4 devem permanecer inalterados. Evidências preservadas ficam fora da pasta metodológica e não são entrada para novas gerações. C0 é uma condição natural; as comparações fatoriais são entre C1-C4. Diferenças só permitem inferência causal se os controles forem suficientes.
