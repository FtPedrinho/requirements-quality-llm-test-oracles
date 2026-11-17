package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * Um teste já existente, a ser avaliado pelo modo avaliação.
 *
 * @param expected resultado esperado da decisão; null quando não informado
 */
public record TestCase(String name, Map<String, Boolean> values, Boolean expected) {

    /**
     * Monta o teste a partir do arquivo: cada entrada vem direto com T/F ou é calculada pelo predicado
     * a partir dos valores concretos (speed = 101).
     */
    public static TestCase resolve(Expr expr, String name, Map<String, String> raw, Boolean expected) {
        Map<String, Cond> conds = new LinkedHashMap<>();
        collect(expr, conds);
        Map<String, Boolean> values = new LinkedHashMap<>();
        for (Cond cond : conds.values()) {
            String direct = raw.get(cond.id());
            if (direct != null) {
                values.put(cond.id(), parseBoolean(direct, name));
            } else if (cond.predicate() != null) {
                try {
                    values.put(cond.id(), cond.predicate().holds(raw));
                } catch (IllegalArgumentException e) {
                    throw new IllegalArgumentException(name + ": " + e.getMessage());
                }
            } else {
                throw new IllegalArgumentException(name + ": sem valor para " + cond.id());
            }
        }
        return new TestCase(name, values, expected);
    }

    /** Aceita T/F, true/false, V/F e 1/0. */
    public static boolean parseBoolean(String text, String context) {
        return switch (text.strip().toLowerCase(Locale.ROOT)) {
            case "t", "true", "v", "verdadeiro", "1" -> true;
            case "f", "false", "falso", "0" -> false;
            default -> throw new IllegalArgumentException(context + ": valor lógico inválido: " + text);
        };
    }

    private static void collect(Expr expr, Map<String, Cond> conds) {
        switch (expr) {
            case Cond c -> conds.putIfAbsent(c.id(), c);
            case And(var left, var right) -> {
                collect(left, conds);
                collect(right, conds);
            }
            case Or(var left, var right) -> {
                collect(left, conds);
                collect(right, conds);
            }
            case Not(var operand) -> collect(operand, conds);
        }
    }
}
