package io.github.rvdomingos.mcdc.core;

import java.util.Map;

/**
 * Variante de um teste da suíte com uma comparação numérica exatamente no limite, como na análise de
 * valores de fronteira de Sun et al.: "speed > 100" verdadeira vira speed = 101; falsa vira speed = 100.
 * As outras condições do teste continuam com o mesmo valor.
 *
 * @param baseVector teste da suíte de origem, ex.: "V5"
 * @param condition  condição levada ao limite, ex.: "speed > 100"
 * @param boundary   o ponto de fronteira, ex.: "speed = 100"
 * @param assignment valores concretos de todas as variáveis
 */
public record BoundaryTest(String baseVector, String condition, String boundary, Map<String, String> assignment) {
}
