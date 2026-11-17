package io.github.rvdomingos.mcdc.core;

import java.util.List;
import java.util.Map;
import java.util.Set;

/** Escolha exata da suíte: o menor conjunto de linhas com um par de cada condição (implementação com Z3 no mcdc-z3). */
public interface SuiteOptimizer {

    /** Índices das linhas escolhidas; condições sem par são ignoradas. */
    Set<Integer> minimumRows(Map<String, List<IndependencePair>> pairsByCondition);
}
