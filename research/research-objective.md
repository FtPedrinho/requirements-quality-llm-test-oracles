# Objetivo e questões de pesquisa

## Problema

Uma suíte de testes gerada por LLM pode ser sintaticamente válida e executável sem que suas expectativas sigam a documentação. Documentação ambígua ou contraditória pode levar a casos omitidos, pressupostos, oráculos incompatíveis, inválidos ou indeterminados. A pesquisa assume a documentação congelada como referência normativa e separa conformidade documental, comportamento observado do SUT e cobertura estrutural.

## Motivação e justificativa

Cobertura de código e aprovação de testes informam, respectivamente, quais partes do SUT foram exercitadas e se a execução satisfez as expectativas codificadas. A documentação é assumida como normativa nesta pesquisa: a IA deve derivar dela o oráculo com apoio do Z3 antes de inspecionar o código. Assim é possível medir conformidade com o texto e, separadamente, falhas causadas por divergência entre documentação e implementação; isso não afirma que a documentação seja uma verdade objetiva sobre o produto.

## Objetivo geral

Investigar como diferentes níveis de clareza e consistência da documentação técnica influenciam a geração de testes por LLMs, observando Branch Coverage e quantidades de testes aprovados, falhos e indeterminados.

## Objetivos específicos

1. Caracterizar documentalmente as condições C0-C4 sem reclassificar C0 como alto/baixo por suposição.
2. Gerar suítes com procedimento e variáveis operacionais registrados.
3. Medir Branch Coverage no escopo de produção definido pelo protocolo.
4. Contar testes aprovados, falhos e indeterminados.
5. Registrar casos inválidos, erros técnicos e divergências sem confundi-los com as métricas.
6. Comparar as condições sem afirmar causalidade quando controles forem insuficientes.

## Questões de pesquisa

- **RQ1:** Como a redução da clareza documental influencia a cobertura estrutural dos testes gerados?
- **RQ2:** Como a redução da consistência documental influencia a cobertura estrutural dos testes gerados?
- **RQ3:** Como a combinação de baixa clareza e baixa consistência influencia a geração de testes?
- **RQ4:** Como os atributos documentais influenciam as quantidades de testes aprovados, falhos e indeterminados?
- **RQ5:** Quais limitações documentais e operacionais afetam a interpretação desses resultados?

## Contribuição esperada

Produzir um protocolo rastreável para derivar oráculos exclusivamente dos documentos, usando Z3 obrigatório, e executar testes independentes contra o SUT. As conclusões são relativas à referência documental adotada, não uma prova de correção geral do sistema.

## Sistema sob teste

O SUT é a ferramenta MC/DC implementada em Java neste repositório. VM, TIS e NPP são dados de entrada de exemplo, não implementações de domínio sob teste. Consulte [system-under-test.md](system-under-test.md).
