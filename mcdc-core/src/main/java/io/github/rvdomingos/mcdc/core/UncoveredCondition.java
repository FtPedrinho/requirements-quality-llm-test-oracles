package io.github.rvdomingos.mcdc.core;

import java.util.List;

/**
 * Condição que ficou sem par de independência, e o motivo.
 *
 * @param condition    rótulo da condição
 * @param reason       por que não há par
 * @param blockedPairs pares que existiriam se as linhas impossíveis fossem possíveis; vazio quando redundante
 */
public record UncoveredCondition(String condition, Reason reason, List<IndependencePair> blockedPairs) {

    public enum Reason {
        /** Não há par nem na tabela completa: a condição não influencia o resultado; o requisito pode ser simplificado. */
        REDUNDANT,
        /** Havia pares, mas todos usam linhas impossíveis pelas restrições ou pelo Z3. */
        INFEASIBLE
    }
}
