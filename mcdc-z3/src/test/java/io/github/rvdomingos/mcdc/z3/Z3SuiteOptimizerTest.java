package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.SuiteMethod;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class Z3SuiteOptimizerTest {

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private static Cond c(String id) {
        return new Cond(id);
    }

    private static final McdcOptions GREEDY = McdcOptions.defaults();
    private static final McdcOptions EXACT = McdcOptions.defaults().withOptimizer(new Z3SuiteOptimizer());

    @Test
    void beatsTheGreedyChoiceWhenItIsNotMinimal() {
        // ((E or D) and (not A or D)) or B: a gulosa escolhe 6 testes; o mínimo é 5
        Expr expr = new Or(new And(new Or(c("E"), c("D")), new Or(new Not(c("A")), c("D"))), c("B"));
        McdcReport greedy = Mcdc.analyze(expr, GREEDY);
        McdcReport exact = Mcdc.analyze(expr, EXACT);

        assertEquals(6, greedy.minimalSuite().size());
        assertEquals(5, exact.minimalSuite().size());
        assertEquals(SuiteMethod.EXACT, exact.suiteMethod());
        assertTrue(exact.isComplete());
        assertEquals(exact.table().conditions().size(), exact.chosenPairs().size());
    }

    @Test
    void neverWorseThanGreedy() {
        List<Expr> expressions = List.of(
                new Or(new And(c("A"), c("B")), c("C")),
                new Or(new And(c("A"), c("B")), new And(new Not(c("A")), c("C"))),
                new And(c("A"), new Or(c("B"), new And(c("C"), c("D")))),
                new Or(new And(c("B"), c("C")), new And(c("B"), new Or(new Or(new Not(c("C")), c("A")), c("A")))));
        for (McdcVariant variant : McdcVariant.values()) {
            for (Expr expr : expressions) {
                McdcReport greedy = Mcdc.analyze(expr, GREEDY.withVariant(variant));
                McdcReport exact = Mcdc.analyze(expr, EXACT.withVariant(variant));
                assertTrue(exact.minimalSuite().size() <= greedy.minimalSuite().size(), expr + " " + variant);
                assertEquals(greedy.uncoveredConditions(), exact.uncoveredConditions());
            }
        }
    }
}
