package io.github.rvdomingos.mcdc.core.model;

import java.util.Map;

/** Expressão booleana de uma decisão. As folhas são condições atômicas. */
public sealed interface Expr permits Cond, And, Or, Not {

    /** Avalia a expressão para os valores dados, indexados pelo id da condição. */
    boolean eval(Map<String, Boolean> values);
}
