package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

/**
 * Condição atômica.
 *
 * @param id        nome da entrada; para comparações, o texto normalizado do predicado, ex.: "speed > 100"
 * @param predicate o que a condição afirma; null para condições puramente booleanas
 */
public record Cond(String id, Predicate predicate) implements Expr {

    public Cond(String id) {
        this(id, null);
    }

    public Cond(Predicate predicate) {
        this(predicate.toString(), predicate);
    }

    @Override
    public boolean eval(Map<String, Boolean> values) {
        Boolean value = values.get(id);
        if (value == null) {
            throw new IllegalArgumentException("Condição sem valor: " + id);
        }
        return value;
    }
}
