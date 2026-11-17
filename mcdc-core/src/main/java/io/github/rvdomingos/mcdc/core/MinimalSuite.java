package io.github.rvdomingos.mcdc.core;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

public final class MinimalSuite {

    /**
     * Resultado da escolha.
     *
     * @param chosen par escolhido para cada condição com par, na ordem das condições
     */
    public record Selection(List<TestVector> tests, Map<String, IndependencePair> chosen) {

        /** Condições que um vetor da suíte ajuda a demonstrar. */
        public List<String> demonstratedBy(TestVector vector) {
            return chosen.entrySet().stream()
                    .filter(e -> e.getValue().whenTrue().index() == vector.index()
                            || e.getValue().whenFalse().index() == vector.index())
                    .map(Map.Entry::getKey)
                    .toList();
        }
    }

    private MinimalSuite() {
    }

    public static List<TestVector> greedy(Map<String, List<IndependencePair>> pairsByCondition) {
        return select(pairsByCondition).tests();
    }

    /**
     * Escolha gulosa: trata primeiro as condições com menos pares e pega o par que acrescenta menos
     * vetores novos; no empate, prefere causa única. Rápida, mas nem sempre ótima.
     */
    public static Selection select(Map<String, List<IndependencePair>> pairsByCondition) {
        Map<Integer, TestVector> selected = new TreeMap<>();
        Map<String, IndependencePair> chosen = new LinkedHashMap<>();

        List<Map.Entry<String, List<IndependencePair>>> byFewestPairs = new ArrayList<>(pairsByCondition.entrySet());
        byFewestPairs.sort(Comparator.comparingInt(e -> e.getValue().size()));

        for (Map.Entry<String, List<IndependencePair>> entry : byFewestPairs) {
            IndependencePair best = null;
            int bestCost = Integer.MAX_VALUE;
            for (IndependencePair pair : entry.getValue()) {
                int cost = (selected.containsKey(pair.whenTrue().index()) ? 0 : 1)
                        + (selected.containsKey(pair.whenFalse().index()) ? 0 : 1);
                if (cost < bestCost || (cost == bestCost && pair.isUniqueCause() && !best.isUniqueCause())) {
                    best = pair;
                    bestCost = cost;
                }
            }
            if (best != null) {
                selected.put(best.whenTrue().index(), best.whenTrue());
                selected.put(best.whenFalse().index(), best.whenFalse());
                chosen.put(entry.getKey(), best);
            }
        }

        return new Selection(List.copyOf(selected.values()), inConditionOrder(pairsByCondition, chosen));
    }

    /**
     * Seleção a partir de linhas já escolhidas (ex.: pela busca exata), preferindo causa única.
     *
     * @throws IllegalArgumentException se alguma condição com pares ficar sem par no conjunto
     */
    public static Selection fromRows(Map<String, List<IndependencePair>> pairsByCondition, Set<Integer> rows) {
        Map<Integer, TestVector> selected = new TreeMap<>();
        Map<String, IndependencePair> chosen = new LinkedHashMap<>();
        for (Map.Entry<String, List<IndependencePair>> entry : pairsByCondition.entrySet()) {
            IndependencePair best = null;
            for (IndependencePair pair : entry.getValue()) {
                if (rows.contains(pair.whenTrue().index()) && rows.contains(pair.whenFalse().index())
                        && (best == null || (pair.isUniqueCause() && !best.isUniqueCause()))) {
                    best = pair;
                }
            }
            if (best == null && !entry.getValue().isEmpty()) {
                throw new IllegalArgumentException("As linhas escolhidas não contêm um par de " + entry.getKey());
            }
            if (best != null) {
                selected.put(best.whenTrue().index(), best.whenTrue());
                selected.put(best.whenFalse().index(), best.whenFalse());
                chosen.put(entry.getKey(), best);
            }
        }
        return new Selection(List.copyOf(selected.values()), chosen);
    }

    /** Devolve na ordem das condições, não na ordem em que foram tratadas. */
    private static Map<String, IndependencePair> inConditionOrder(Map<String, List<IndependencePair>> pairsByCondition,
            Map<String, IndependencePair> chosen) {
        Map<String, IndependencePair> ordered = new LinkedHashMap<>();
        for (String condition : pairsByCondition.keySet()) {
            if (chosen.containsKey(condition)) {
                ordered.put(condition, chosen.get(condition));
            }
        }
        return ordered;
    }
}
