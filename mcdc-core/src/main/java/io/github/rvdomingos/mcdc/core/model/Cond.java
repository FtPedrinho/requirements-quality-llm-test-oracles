package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

public record Cond(String id) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        Boolean value = values.get(id);
        if (value == null) {
            throw new IllegalArgumentException("Condição sem valor: " + id);
        }
        return value;
    }
}
