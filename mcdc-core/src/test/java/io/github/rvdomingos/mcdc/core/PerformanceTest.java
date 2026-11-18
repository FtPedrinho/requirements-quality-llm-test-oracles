package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import java.util.List;
import java.util.function.Supplier;
import org.junit.jupiter.api.Test;

/**
 * Desempenho do motor sem o Z3 (RNF09). Os limites têm folga de cerca de 10 vezes sobre o tempo medido, para
 * não falhar numa máquina mais lenta; o tempo de cada caso aparece na saída do teste.
 */
class PerformanceTest {

    /** Tabela inteira no limite de 20 entradas (cerca de 1 milhão de combinações). */
    private static final double MAX_SECONDS_20_INPUTS = 5.0;
    /** Entradas repetidas: cada aparição é reavaliada, o caminho mais caro. */
    private static final double MAX_SECONDS_REPEATED = 5.0;

    private static <T> T timed(String label, double maxSeconds, Supplier<T> work) {
        long start = System.nanoTime();
        T result = work.get();
        double seconds = (System.nanoTime() - start) / 1e9;
        System.out.printf("desempenho: %s em %.2f s (limite %.1f s)%n", label, seconds, maxSeconds);
        assertTrue(seconds < maxSeconds, label + " levou " + seconds + " s");
        return result;
    }

    private static Expr chain(int n, boolean withOr) {
        Expr expr = new Cond("x0");
        for (int i = 1; i < n; i++) {
            Cond next = new Cond("x" + i);
            expr = withOr && i % 3 == 0 ? new Or(expr, next) : new And(expr, next);
        }
        return expr;
    }

    @Test
    void twentyInputsInBothVariants() {
        for (boolean withOr : new boolean[] {false, true}) {
            for (McdcVariant variant : McdcVariant.values()) {
                Expr expr = chain(TruthTable.MAX_INPUTS, withOr);
                McdcReport report = timed("20 entradas, " + (withOr ? "e/ou" : "só e") + ", " + variant,
                        MAX_SECONDS_20_INPUTS, () -> Mcdc.analyze(expr, McdcOptions.defaults().withVariant(variant)));
                assertEquals(1 << 20, report.table().rows().size());
                assertTrue(report.isComplete());
                if (!withOr) {
                    assertEquals(21, report.minimalSuite().size()); // N + 1
                }
            }
        }
    }

    @Test
    void repeatedInputsTakeTheSlowPathInTime() {
        // 12 entradas, cada uma em duas aparições: 24 condições reavaliadas linha a linha
        Expr expr = null;
        for (int i = 0; i < 12; i++) {
            Expr term = new Or(new And(new Cond("x" + i), new Cond("x" + ((i + 1) % 12))), new Not(new Cond("x" + i)));
            expr = expr == null ? term : new And(expr, term);
        }
        Expr decision = expr;
        McdcReport report = timed("12 entradas repetidas, mascaramento", MAX_SECONDS_REPEATED,
                () -> Mcdc.analyze(decision, McdcOptions.defaults()));
        assertEquals(36, report.table().conditions().size());
    }

    @Test
    void mutationOfALargeDecision() {
        Expr expr = chain(16, true);
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());
        MutationReport mutation = timed("mutação, 16 entradas", MAX_SECONDS_20_INPUTS, () -> MutationReport.of(report));
        assertTrue(mutation.results().size() > 100);
    }

    @Test
    void evaluationOfExistingTestsOnTwentyInputs() {
        Expr expr = chain(TruthTable.MAX_INPUTS, false);
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE));
        List<TestCase> tests = report.minimalSuite().stream()
                .map(v -> new TestCase(v.name(), v.values(), v.outcome())).toList();
        TestSetEvaluation evaluation = timed("avaliação de 21 testes, 20 entradas", MAX_SECONDS_20_INPUTS,
                () -> Mcdc.evaluate(expr, McdcOptions.defaults(), tests));
        assertTrue(evaluation.isComplete());
    }
}
