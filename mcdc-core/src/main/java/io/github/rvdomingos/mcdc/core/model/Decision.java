package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

/**
 * Decisão extraída de um requisito.
 *
 * @param id             identificador do requisito, ex.: "REQ-001"
 * @param expression     antecedente do requisito
 * @param labels         id da condição para texto legível
 * @param expectedAction consequente do requisito
 */
public record Decision(String id, Expr expression, Map<String, String> labels, String expectedAction) {
}
