# Experimento C1 — alta clareza e consistência pretendida

## Objetivo, condição e metodologia

Avaliar uma cópia documental reestruturada para maior clareza, sem alterar guardas ou ações. C1 representa a condição de alta clareza/alta consistência pretendida, mas a consistência semântica integral não foi confirmada: persistem quatro pares de ações potencialmente incompatíveis e uma variável de saída não declarada.

A documentação foi organizada e os 36 requisitos centrais foram formalizados. Há duas trilhas de resultados: análise formal das expressões e suíte Java/PIT da ferramenta; elas não medem o mesmo objeto.

## Métricas do experimento

Clareza e consistência foram avaliadas em escala de 1 a 5. A auditoria registra clareza média de 4,06 para o original e 4,97 para C1; a consistência ficou em 4,67 em ambos. Também foram registrados casos Z3, testes JUnit, mutantes mortos/sobreviventes/equivalentes/não avaliáveis. Precision/Recall/F1 da qualidade de oráculos não foram calculados com uma execução independente de LLM.

## Artefatos essenciais

- Resultados: [results.md](results.md).
- Documento C1 adaptado: [documentation/tool-readme-C1.md](documentation/tool-readme-C1.md).
- Suíte JUnit da ferramenta: [test-suites/exp1/](test-suites/exp1/).
- Casos e oráculos formais: [oracles/](oracles/) e [test-suites/](test-suites/).
- Instruções para uso de outra IA: não há execução independente de LLM registrada para a geração de oráculos C1.

## Integridade

A versão C1 é uma cópia experimental; a documentação e o código do sistema principal permanecem inalterados.
