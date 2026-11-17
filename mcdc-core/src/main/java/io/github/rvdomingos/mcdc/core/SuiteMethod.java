package io.github.rvdomingos.mcdc.core;

/** Como a suíte foi escolhida. */
public enum SuiteMethod {
    /** Escolha gulosa sobre a tabela verdade: rápida, nem sempre a menor. */
    GREEDY,
    /** Menor suíte possível, pela otimização do Z3. */
    EXACT,
    /** Pares pedidos direto ao Z3, sem montar a tabela. */
    DIRECT
}
