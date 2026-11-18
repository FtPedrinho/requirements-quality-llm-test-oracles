package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Pares de independência de cada condição (cada ocorrência de uma entrada). Condição sem par fica com
 * lista vazia; linhas impossíveis ficam de fora.
 */
public final class IndependencePairs {

    /** Teto de pares por condição: no mascaramento eles crescem como o produto de duas listas. */
    public static final int MAX_PAIRS_PER_CONDITION = 1000;

    private IndependencePairs() {
    }

    public static Map<String, List<IndependencePair>> of(TruthTable table, McdcVariant variant) {
        return switch (variant) {
            case UNIQUE_CAUSE -> uniqueCause(table);
            case MASKING -> masking(table);
        };
    }

    /**
     * Causa única: só a entrada da condição muda, o resultado muda e a ocorrência decide nos dois
     * vetores (UCMS quando a entrada se repete).
     */
    public static Map<String, List<IndependencePair>> uniqueCause(TruthTable table) {
        int n = table.inputs().size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (Condition condition : table.conditions()) {
            int mask = TruthTable.bit(n, table.inputs().indexOf(condition.input()));
            boolean single = appearsOnce(table, condition);
            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if (!row.feasible() || (row.index() & mask) != 0) {
                    continue;
                }
                // a mesma linha com só esta entrada falsa
                TestVector flipped = table.rows().get(row.index() | mask);
                if (flipped.feasible()
                        && row.outcome() != flipped.outcome()
                        && decides(table, condition, row, mask, single)
                        && decides(table, condition, flipped, mask, single)) {
                    pairs.add(new IndependencePair(condition.label(), row, flipped));
                    if (pairs.size() == MAX_PAIRS_PER_CONDITION) {
                        break;
                    }
                }
            }
            result.put(condition.label(), List.copyOf(pairs));
        }
        return result;
    }

    /** Mascaramento: as outras condições podem mudar, desde que estejam mascaradas. */
    public static Map<String, List<IndependencePair>> masking(TruthTable table) {
        int n = table.inputs().size();
        Map<String, List<IndependencePair>> result = new LinkedHashMap<>();

        for (Condition condition : table.conditions()) {
            int mask = TruthTable.bit(n, table.inputs().indexOf(condition.input()));
            boolean single = appearsOnce(table, condition);
            List<TestVector> whenTrue = new ArrayList<>();
            List<TestVector> whenFalse = new ArrayList<>();
            for (TestVector row : table.rows()) {
                // "decide" é uma propriedade da fórmula: vale mesmo que a linha com a condição invertida seja impossível
                if (!row.feasible() || !decides(table, condition, row, mask, single)) {
                    continue;
                }
                if ((row.index() & mask) == 0) {
                    whenTrue.add(row);
                } else {
                    whenFalse.add(row);
                }
            }

            List<IndependencePair> pairs = new ArrayList<>();
            search:
            for (TestVector t : whenTrue) {
                for (TestVector f : whenFalse) {
                    if (t.outcome() != f.outcome()) {
                        pairs.add(new IndependencePair(condition.label(), t, f));
                        if (pairs.size() == MAX_PAIRS_PER_CONDITION) {
                            break search;
                        }
                    }
                }
            }
            result.put(condition.label(), List.copyOf(pairs));
        }
        return result;
    }

    /** Se a entrada aparece uma vez só e a tabela tem todas as linhas, na posição do índice. */
    private static boolean appearsOnce(TruthTable table, Condition condition) {
        return table.isFull() && Collections.frequency(table.expression().leaves(), condition.input()) == 1;
    }

    /**
     * Se a condição decide a saída na linha. Quando a entrada aparece uma vez só, trocar a aparição é trocar
     * o bit da entrada: basta olhar a saída da linha vizinha, sem reavaliar a fórmula (20 entradas em
     * fração de segundo em vez de segundos). Com a entrada repetida, reavalia trocando só aquela aparição.
     */
    private static boolean decides(TruthTable table, Condition condition, TestVector row, int mask, boolean single) {
        if (single) {
            return row.outcome() != table.rows().get(row.index() ^ mask).outcome();
        }
        return condition.decides(table.expression(), row);
    }
}
