package io.github.rvdomingos.mcdc.core.model;

import java.util.List;

/** Decisões de um sistema, como chegam de um arquivo de requisitos ou da NAT2TEST. */
public record DecisionSet(String system, List<InputVariable> inputs, List<Decision> decisions) {

    public DecisionSet {
        inputs = inputs == null ? List.of() : List.copyOf(inputs);
        decisions = List.copyOf(decisions);
    }
}
