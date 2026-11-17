package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
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
            List<IndependencePair> pairs = new ArrayList<>();
            for (TestVector row : table.rows()) {
                if (!row.feasible() || (row.index() & mask) != 0) {
                    continue;
                }
                // a mesma linha com só esta entrada falsa
                TestVector flipped = table.rows().get(row.index() | mask);
                if (flipped.feasible()
                        && row.outcome() != flipped.outcome()
                        && condition.decides(table.expression(), row)
                        && condition.decides(table.expression(), flipped)) {
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
            List<TestVector> whenTrue = new ArrayList<>();
            List<TestVector> whenFalse = new ArrayList<>();
            for (TestVector row : table.rows()) {
                // "decide" é uma propriedade da fórmula: vale mesmo que a linha com a condição invertida seja impossível
                if (!row.feasible() || !condition.decides(table.expression(), row)) {
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
}
