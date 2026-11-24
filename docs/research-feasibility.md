# Viabilidade da metodologia revisada

## Sistema sob teste

O SUT é a ferramenta MC/DC implementada nos módulos Java `mcdc-core`, `mcdc-requirements`, `mcdc-z3` e `mcdc-cli`. VM, TIS e NPP são entradas de exemplo; não há implementações de domínio correspondentes neste repositório.

## Desenho experimental

As condições C0-C4 e o protocolo estão descritos em [experimentacao-pesquisa/](../experimentacao-pesquisa/). C0 é a documentação original e não recebe nível alto/baixo por suposição. C1-C4 são as células fatoriais pretendidas. Documentos originais e manipulados são fontes congeladas que não devem ser alteradas.

## Métricas e viabilidade

- **Branch Coverage:** única métrica de cobertura da pesquisa; disponível por instrumentação como JaCoCo, desde que coletada sobre os testes gerados e um escopo do SUT definido em comum.
- **Quantidades:** contar testes aprovados, falhos e indeterminados, sem
  confundir erros técnicos com falhas semânticas.
- **Z3:** o uso independente é obrigatório para formalizar e verificar as
  restrições do oráculo; o resultado não verifica sozinho a fidelidade da
  tradução documental.

## Limitações e validade

A ausência de implementação de domínio para VM/TIS/NPP impede usá-los como sistemas de aplicação sob teste, mas não impede testar a ferramenta MC/DC. Diferenças de modelos, prompts, contexto, ambiente, harness e instrumentação podem confundir comparações. Conformidade é medida contra a documentação normativa, não equivale a verdade objetiva do documento ou à correção geral do SUT. C0 não é parte do fatorial.

## Escopo excluído

As únicas métricas são Branch Coverage e quantidades de testes aprovados,
falhos e indeterminados. As verificações internas do produto são distintas
dos experimentos; consulte o [protocolo](../experimentacao-pesquisa/protocolo/metodologia.md).
