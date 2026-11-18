package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/** Confere a busca exata e o modo direto em expressões geradas ao acaso, contra a força bruta e a tabela inteira. */
class Z3RandomizedTest {

    private static final long SEED = 20261117L;
    private static final List<String> NAMES = List.of("A", "B", "C", "D", "E");

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private static Expr random(Random rnd, List<String> pool, int leaves) {
        if (leaves == 1) {
            Expr c = new Cond(pool.get(rnd.nextInt(pool.size())));
            return rnd.nextInt(4) == 0 ? new Not(c) : c;
        }
        int left = 1 + rnd.nextInt(leaves - 1);
        Expr e = rnd.nextBoolean()
                ? new And(random(rnd, pool, left), random(rnd, pool, leaves - left))
                : new Or(random(rnd, pool, left), random(rnd, pool, leaves - left));
        return rnd.nextInt(6) == 0 ? new Not(e) : e;
    }

    private static List<Expr> expressions(long seed, int count, int maxInputs, int maxLeaves) {
        Random rnd = new Random(seed);
        List<Expr> list = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            list.add(random(rnd, NAMES.subList(0, 1 + rnd.nextInt(maxInputs)), 1 + rnd.nextInt(maxLeaves)));
        }
        return list;
    }

    /** Menor número de linhas com um par inteiro de cada condição que tem par, por força bruta. */
    private static int bruteForceMinimum(Map<String, List<IndependencePair>> pairs) {
        List<List<IndependencePair>> needed = pairs.values().stream().filter(p -> !p.isEmpty()).toList();
        if (needed.isEmpty()) {
            return 0;
        }
        List<Integer> rows = new ArrayList<>(needed.stream().flatMap(List::stream)
                .flatMap(p -> java.util.stream.Stream.of(p.whenTrue().index(), p.whenFalse().index()))
                .collect(Collectors.toCollection(TreeSet::new)));
        int best = Integer.MAX_VALUE;
        for (long subset = 1; subset < (1L << rows.size()); subset++) {
            int size = Long.bitCount(subset);
            if (size >= best) {
                continue;
            }
            Set<Integer> chosen = new TreeSet<>();
            for (int i = 0; i < rows.size(); i++) {
                if ((subset & (1L << i)) != 0) {
                    chosen.add(rows.get(i));
                }
            }
            boolean all = needed.stream().allMatch(list -> list.stream().anyMatch(p ->
                    chosen.contains(p.whenTrue().index()) && chosen.contains(p.whenFalse().index())));
            if (all) {
                best = size;
            }
        }
        return best;
    }

    @Test
    void exactSuiteIsTheTrueMinimum() {
        McdcOptions exact = McdcOptions.defaults().withOptimizer(new Z3SuiteOptimizer());
        int greedyAboveMinimum = 0;
        int checked = 0;
        for (Expr expr : expressions(SEED, 300, 4, 6)) {
            for (McdcVariant variant : McdcVariant.values()) {
                McdcReport greedy = Mcdc.analyze(expr, McdcOptions.defaults().withVariant(variant));
                McdcReport best = Mcdc.analyze(expr, exact.withVariant(variant));
                int minimum = bruteForceMinimum(greedy.pairs());
                String where = expr + " " + variant;

                assertEquals(minimum, best.minimalSuite().size(), "a busca exata não é mínima em " + where);
                assertTrue(greedy.minimalSuite().size() >= minimum, where);
                assertEquals(greedy.uncoveredConditions(), best.uncoveredConditions(), where);
                Set<Integer> suite = best.minimalSuite().stream().map(TestVector::index)
                        .collect(Collectors.toSet());
                best.chosenPairs().forEach((condition, pair) -> {
                    assertTrue(greedy.pairs().get(condition).stream().anyMatch(q ->
                            q.whenTrue().index() == pair.whenTrue().index()
                                    && q.whenFalse().index() == pair.whenFalse().index()), where);
                    assertTrue(suite.contains(pair.whenTrue().index()) && suite.contains(pair.whenFalse().index()), where);
                });
                if (greedy.minimalSuite().size() > minimum) {
                    greedyAboveMinimum++;
                }
                checked++;
            }
        }
        System.out.printf("busca exata: %d casos; a gulosa passou do mínimo em %d%n", checked, greedyAboveMinimum);
    }

    @Test
    void directModeAgreesWithTheFullTable() {
        Z3DirectAnalyzer direct = new Z3DirectAnalyzer(List.of());
        for (Expr expr : expressions(SEED + 1, 120, 5, 7)) {
            for (McdcVariant variant : McdcVariant.values()) {
                McdcOptions options = McdcOptions.defaults().withVariant(variant);
                McdcReport table = Mcdc.analyze(expr, options);
                McdcReport report = direct.analyze(expr, options);
                String where = expr + " " + variant;

                assertEquals(reasons(table), reasons(report), "cobertura diferente em " + where);
                Set<Integer> suite = report.minimalSuite().stream().map(TestVector::index)
                        .collect(Collectors.toSet());
                report.chosenPairs().forEach((condition, pair) -> {
                    assertTrue(table.pairs().get(condition).stream().anyMatch(q ->
                            q.whenTrue().index() == pair.whenTrue().index()
                                    && q.whenFalse().index() == pair.whenFalse().index()),
                            "par inexistente " + pair + " para " + condition + " em " + where);
                    assertTrue(suite.contains(pair.whenTrue().index()) && suite.contains(pair.whenFalse().index()), where);
                });
            }
        }
    }

    private static Map<String, UncoveredCondition.Reason> reasons(McdcReport report) {
        Map<String, UncoveredCondition.Reason> reasons = new LinkedHashMap<>();
        report.uncovered().forEach(u -> reasons.put(u.condition(), u.reason()));
        return reasons;
    }
}
