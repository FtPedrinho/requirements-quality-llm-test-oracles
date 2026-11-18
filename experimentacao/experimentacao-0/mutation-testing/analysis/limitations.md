# Limitações

- Não existe implementação independente dos sistemas VM, TIS e NPP neste repositório.
- Os mutantes representam alterações nas expressões formalizadas, não defeitos reais confirmados das aplicações.
- Os 152 casos são simbólicos na origem e somente 140 receberam dois ou um modelo concreto válido.
- Doze pares MC/DC não puderam ser concretizados com os domínios disponíveis.
- Os domínios numéricos não foram integralmente enumerados.
- Algumas relações temporais são representadas por variáveis `_antes`, mas não por uma máquina de estados completa.
- Os enumerações foram formalizadas por índices restritos aos valores existentes.
- Os mutantes não cobrem defeitos de implementação, integração ou saída não documentada.
- O Z3 não valida a semântica humana da tradução das guardas.
- A precisão por mutante é limitada pela ausência de falsos positivos encontrados; isso não demonstra correção semântica completa.
