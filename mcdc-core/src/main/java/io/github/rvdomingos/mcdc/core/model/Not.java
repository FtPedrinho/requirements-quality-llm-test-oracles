package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

public record Not(Expr operand) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        return !operand.eval(values);
    }
}
