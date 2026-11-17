package io.github.rvdomingos.mcdc.core.model;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

/** Expressão booleana de uma decisão. As folhas são condições atômicas. */
public sealed interface Expr permits Cond, And, Or, Not {

    /** Avalia a expressão; os valores são indexados pelo id da condição. */
    boolean eval(Map<String, Boolean> values);

    /** Ids das condições sem repetição, na ordem da primeira aparição. */
    default List<String> inputs() {
        return List.copyOf(new LinkedHashSet<>(leaves()));
    }

    /** Ids das folhas da esquerda para a direita, com repetição: cada uma é uma condição. */
    default List<String> leaves() {
        List<String> ids = new ArrayList<>();
        collect(this, ids);
        return List.copyOf(ids);
    }

    private static void collect(Expr expr, List<String> ids) {
        switch (expr) {
            case Cond c -> ids.add(c.id());
            case And(var left, var right) -> {
                collect(left, ids);
                collect(right, ids);
            }
            case Or(var left, var right) -> {
                collect(left, ids);
                collect(right, ids);
            }
            case Not(var operand) -> collect(operand, ids);
        }
    }
}
