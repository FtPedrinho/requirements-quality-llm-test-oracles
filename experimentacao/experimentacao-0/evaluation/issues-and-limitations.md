# Questões e limitações

## Questões técnicas

- Z3 estava ausente no início e foi instalado como pacote Python.
- Z3 executável não estava disponível no `PATH`.
- A versão usada do modelo Copilot não foi disponível no ambiente.
- Os scripts dependem da estrutura DFRS/NAT2TEST encontrada no dataset.
- Expressões fora dos padrões JSON podem exigir expansão manual.

## Questões metodológicas

- Os requisitos originais não possuem implementação independente conhecida para este exercício.
- As ações não estão separadas em um modelo executável.
- Os estados anteriores são formalizados como variáveis distintas, mas suas relações temporais não são validadas por alcance.
- A análise de ação conflitante considera apenas a escrita simultânea da mesma variável com valores diferentes.
- A análise simbólica MC/DC não valida alcançabilidade concreta no domínio.

## Próximos passos

1. Realizar validação humana das formalizações.
2. Resolver os conflitos formais TIS e NPP.
3. Confirmar enumerações e limites numéricos.
4. Definir casos concretos com uma implementação ou modelo independente.
5. Executar a suíte de oráculos em uma implementação antes de declarar Mutation Score.
6. Fechar ambiguidades antes do experimento fatorial.
