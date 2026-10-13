package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

public record Or(Expr left, Expr right) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        return left.eval(values) | right.eval(values);
    }
}
