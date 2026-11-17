package io.github.rvdomingos.mcdc.core;

import java.util.Map;

/**
 * Teste da suíte com uma comparação numérica levada ao limite: "speed > 100" verdadeira vira
 * speed = 101; falsa, speed = 100. As outras condições continuam com o mesmo valor.
 *
 * @param baseVector teste da suíte de origem, ex.: "V5"
 * @param boundary   o ponto de fronteira, ex.: "speed = 100"
 */
public record BoundaryTest(String baseVector, String condition, String boundary, Map<String, String> assignment) {
}
