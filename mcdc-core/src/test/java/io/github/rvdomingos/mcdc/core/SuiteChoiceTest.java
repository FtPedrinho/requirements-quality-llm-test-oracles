package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Test;

/** Escolha exata pela interface SuiteOptimizer, tabela parcial do modo direto e o check além do teto de pares. */
class SuiteChoiceTest {

    // (A and B) or C
    private final Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void anOptimizerDecidesTheRows() {
        // V2 (TTF), V3 (TFT), V4 (TFF), V6 (FTF): a suíte de 4 testes
        SuiteOptimizer fixed = pairs -> Set.of(1, 2, 3, 5);
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults().withOptimizer(fixed));

        assertEquals(SuiteMethod.EXACT, report.suiteMethod());
        assertEquals(List.of("V2", "V3", "V4", "V6"), report.minimalSuite().stream().map(TestVector::name).toList());
        assertTrue(report.isComplete());
        assertEquals(SuiteMethod.GREEDY, Mcdc.analyze(expr, McdcOptions.defaults()).suiteMethod());
    }

    @Test
    void rowsWithoutAPairOfSomeConditionAreRejected() {
        SuiteOptimizer wrong = pairs -> Set.of(0);
        assertThrows(IllegalArgumentException.class,
                () -> Mcdc.analyze(expr, McdcOptions.defaults().withOptimizer(wrong)));
    }

    @Test
    void fromRowsPrefersUniqueCause() {
        TruthTable table = TruthTable.of(expr);
        Map<String, List<IndependencePair>> pairs = IndependencePairs.masking(table);
        // todas as linhas disponíveis: cada condição fica com um par de causa única
        Set<Integer> all = Set.of(0, 1, 2, 3, 4, 5, 6, 7);
        MinimalSuite.Selection selection = MinimalSuite.fromRows(pairs, all);

        assertTrue(selection.chosen().values().stream().allMatch(IndependencePair::isUniqueCause));
    }

    @Test
    void partialTableKeepsTheSizeOfTheFullOne() {
        TruthTable full = TruthTable.of(expr);
        TruthTable partial = TruthTable.partial(expr, List.of(full.rows().get(1), full.rows().get(5)));

        assertTrue(full.isFull());
        assertFalse(partial.isFull());
        assertEquals(8, partial.combinations());
        assertEquals(2, partial.rows().size());
    }

    @Test
    void checkFindsPairsBeyondTheCapOfThePairList() {
        // A and (B1 or ... or B11): A passa do teto de 1000 pares; o par usado (só B11 verdadeira) fica fora da lista
        Expr or = new Cond("B1");
        for (int i = 2; i <= 11; i++) {
            or = new Or(or, new Cond("B" + i));
        }
        Expr big = new And(new Cond("A"), or);
        assertTrue(IndependencePairs.masking(TruthTable.of(big)).get("A").size()
                >= IndependencePairs.MAX_PAIRS_PER_CONDITION);

        List<TestCase> tests = new ArrayList<>();
        for (boolean a : new boolean[] {true, false}) {
            Map<String, Boolean> values = new HashMap<>();
            values.put("A", a);
            for (int i = 1; i <= 11; i++) {
                values.put("B" + i, i == 11);
            }
            tests.add(new TestCase(a ? "T1" : "T2", values, null));
        }
        TestSetEvaluation evaluation = Mcdc.evaluate(big, McdcOptions.defaults(), tests);

        assertTrue(evaluation.demonstrated().containsKey("A"), evaluation.demonstrated().toString());
        assertTrue(evaluation.demonstrated().get("A").isUniqueCause());
    }
}
