package io.github.rvdomingos.mcdc.core.model;

import java.util.List;

/**
 * Conjunto de decisões de um sistema, como chega de um arquivo de requisitos ou da NAT2TEST.
 *
 * @param system    nome do sistema; null quando não informado
 * @param inputs    variáveis de entrada declaradas; vazio quando não informadas
 * @param decisions decisões a analisar
 */
public record DecisionSet(String system, List<InputVariable> inputs, List<Decision> decisions) {

    public DecisionSet {
        inputs = inputs == null ? List.of() : List.copyOf(inputs);
        decisions = List.copyOf(decisions);
    }
}
