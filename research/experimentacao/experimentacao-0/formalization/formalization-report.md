# Formalização Z3 - Experimento 0 reconstruído

Os oráculos serão formalizados a partir dos comportamentos da ferramenta MC/DC.

Propriedades verificáveis incluem:

- exatamente uma fonte fornecida;
- tabelas com 2^n combinações;
- incompletude por condições sem pares;
- conflito entre decisões que atribuem valores diferentes;
- lacuna sob contexto;
- Z3 indisponível como erro, não como sucesso;
- tamanho máximo de tabela direta.

Os resultados Z3 devem registrar SAT, UNSAT, UNKNOWN, modelos e limitações.

Satisfatibilidade não substitui avaliação semântica independente.
