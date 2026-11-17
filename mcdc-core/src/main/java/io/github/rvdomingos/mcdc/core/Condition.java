package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Uma ocorrência de uma entrada na expressão: em {@code (A and B) or (not A and C)} há 3 entradas
 * e 4 condições (A#1, B, A#2 e C).
 *
 * @param leaf  posição da folha na expressão, da esquerda para a direita, a partir de 0
 * @param label nome nos relatórios: a entrada, ou "entrada#n" quando ela se repete
 */
public record Condition(int leaf, String input, int occurrence, String label) {

    /** As condições de uma expressão, na ordem das folhas. */
    public static List<Condition> of(Expr expr) {
        List<String> leaves = expr.leaves();
        List<Condition> conditions = new ArrayList<>();
        for (int leaf = 0; leaf < leaves.size(); leaf++) {
            String input = leaves.get(leaf);
            int occurrence = Collections.frequency(leaves.subList(0, leaf + 1), input);
            boolean repeated = Collections.frequency(leaves, input) > 1;
            conditions.add(new Condition(leaf, input, occurrence, repeated ? input + "#" + occurrence : input));
        }
        return List.copyOf(conditions);
    }

    /** Se inverter só esta ocorrência, mantendo as outras da mesma entrada, inverte o resultado da linha. */
    public boolean decides(Expr expr, TestVector row) {
        return row.outcome() != evalFlipping(expr, row, leaf, new int[] {0});
    }

    /** Avalia a expressão com a folha {@code flipped} invertida. Avalia os dois lados de and/or para manter a contagem das folhas. */
    private static boolean evalFlipping(Expr expr, TestVector row, int flipped, int[] next) {
        return switch (expr) {
            case Cond c -> {
                boolean value = row.value(c.id());
                yield next[0]++ == flipped ? !value : value;
            }
            case And(var left, var right) -> evalFlipping(left, row, flipped, next) & evalFlipping(right, row, flipped, next);
            case Or(var left, var right) -> evalFlipping(left, row, flipped, next) | evalFlipping(right, row, flipped, next);
            case Not(var operand) -> !evalFlipping(operand, row, flipped, next);
        };
    }
}
