package io.github.rvdomingos.mcdc.core;

import java.util.List;

/**
 * Condição que ficou sem par de independência, e o motivo.
 *
 * @param blockedPairs pares que existiriam sem as linhas impossíveis; vazio quando redundante
 */
public record UncoveredCondition(String condition, Reason reason, List<IndependencePair> blockedPairs) {

    public enum Reason {
        /** Não há par nem na tabela completa: a condição não muda o resultado e pode ser simplificada. */
        REDUNDANT,
        /** Havia pares, mas todos usam linhas impossíveis pelas restrições ou pelo Z3. */
        INFEASIBLE
    }
}
