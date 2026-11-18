package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.Action;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import org.junit.jupiter.api.Test;

/** Detalhes do motor que a mutação do código mostrou sem teste: ordem da escolha, avaliação, comparações e limites. */
class EngineDetailsTest {

    private static final List<String> AB = List.of("A", "B");
    private static final Expr A_AND_B = new And(new Cond("A"), new Cond("B"));

    private static TestVector row(int index) {
        return new TestVector(index, AB, index == 0, true, null);
    }

    private static IndependencePair pair(String condition, int whenTrue, int whenFalse) {
        return new IndependencePair(condition, row(whenTrue), row(whenFalse));
    }

    // ---------- escolha da suíte ----------

    @Test
    void conditionsWithFewerPairsChooseFirst() {
        // se X escolhesse primeiro, pegaria (0, 1) e Y obrigaria a acrescentar (2, 3): 4 testes em vez de 2
        Map<String, List<IndependencePair>> pairs = new LinkedHashMap<>();
        pairs.put("X", List.of(pair("X", 0, 1), pair("X", 2, 3)));
        pairs.put("Y", List.of(pair("Y", 2, 3)));

        MinimalSuite.Selection selection = MinimalSuite.select(pairs);

        assertEquals(List.of(2, 3), selection.tests().stream().map(TestVector::index).toList());
        assertEquals(List.of("X", "Y"), List.copyOf(selection.chosen().keySet()));
    }

    @Test
    void fromRowsKeepsAUniqueCausePairAndSwapsANonUniqueOne() {
        Map<String, List<IndependencePair>> uniqueFirst = Map.of("X", List.of(pair("X", 0, 1), pair("X", 0, 3)));
        assertEquals(1, MinimalSuite.fromRows(uniqueFirst, Set.of(0, 1, 3)).chosen().get("X").whenFalse().index());

        Map<String, List<IndependencePair>> maskingFirst = Map.of("X", List.of(pair("X", 0, 3), pair("X", 0, 1)));
        assertEquals(1, MinimalSuite.fromRows(maskingFirst, Set.of(0, 1, 3)).chosen().get("X").whenFalse().index());

        Map<String, List<IndependencePair>> onlyMasking = Map.of("X", List.of(pair("X", 0, 3)));
        assertEquals(3, MinimalSuite.fromRows(onlyMasking, Set.of(0, 3)).chosen().get("X").whenFalse().index());
    }

    // ---------- modo avaliação ----------

    @Test
    void evaluationSuggestsOnlyTheMissingTestAndCountsOutcomes() {
        // só V1 (A = T, B = T): cada condição mostra o lado T; falta V3 para A e V2 para B
        TestSetEvaluation evaluation = Mcdc.evaluate(A_AND_B, McdcOptions.defaults(),
                List.of(new TestCase("t1", Map.of("A", true, "B", true), true)));

        assertTrue(evaluation.demonstrated().isEmpty());
        assertEquals(List.of(2), evaluation.suggestions().get("A").stream().map(TestVector::index).toList());
        assertEquals(List.of(1), evaluation.suggestions().get("B").stream().map(TestVector::index).toList());
        assertEquals(2, evaluation.outcomesCovered());
        assertEquals(4, evaluation.outcomesTotal());
        assertEquals(50.0, evaluation.outcomePercentage());
        assertTrue(evaluation.problems().isEmpty());
        assertFalse(evaluation.isComplete());
    }

    @Test
    void evaluationFlagsAWrongExpectedOutcomeOnlyWhenItIsWrong() {
        TestSetEvaluation wrong = Mcdc.evaluate(A_AND_B, McdcOptions.defaults(),
                List.of(new TestCase("t1", Map.of("A", true, "B", true), false)));
        assertEquals(1, wrong.problems().size());
        assertTrue(wrong.problems().get(0).contains("resultado esperado F, mas a guarda dá T"), wrong.problems().get(0));

        TestSetEvaluation unknown = Mcdc.evaluate(A_AND_B, McdcOptions.defaults(),
                List.of(new TestCase("t1", Map.of("A", true, "B", true), null)));
        assertTrue(unknown.problems().isEmpty());
    }

    @Test
    void evaluationSuggestsTheCheapestPairPreferringUniqueCause() {
        // A and (B or C) com só V2 (TTF): para A, (V2, V6) custa um teste e é de causa única; (V2, V5) também custa um
        Expr expr = new And(new Cond("A"), new Or(new Cond("B"), new Cond("C")));
        TestSetEvaluation evaluation = Mcdc.evaluate(expr, McdcOptions.defaults(),
                List.of(new TestCase("t", Map.of("A", true, "B", true, "C", false), true)));

        assertEquals(List.of(5), evaluation.suggestions().get("A").stream().map(TestVector::index).toList());
    }

    @Test
    void evaluationOfACompleteSetIsComplete() {
        List<TestCase> tests = List.of(
                new TestCase("tt", Map.of("A", true, "B", true), true),
                new TestCase("tf", Map.of("A", true, "B", false), false),
                new TestCase("ft", Map.of("A", false, "B", true), false));
        TestSetEvaluation evaluation = Mcdc.evaluate(A_AND_B, McdcOptions.defaults(), tests);

        assertTrue(evaluation.isComplete());
        assertEquals(100.0, evaluation.outcomePercentage());
        assertTrue(evaluation.suggestions().isEmpty());
    }

    // ---------- comparações ----------

    @Test
    void comparisonsAtTheBoundary() {
        Map<String, String> at100 = Map.of("speed", "100");
        assertFalse(new Predicate("speed", "<", "100").holds(at100));
        assertTrue(new Predicate("speed", "<=", "100").holds(at100));
        assertFalse(new Predicate("speed", ">", "100").holds(at100));
        assertTrue(new Predicate("speed", ">=", "100").holds(at100));
        assertTrue(new Predicate("speed", "=", "100.0").holds(at100));
        assertFalse(new Predicate("speed", "!=", "100.0").holds(at100));
        assertTrue(new Predicate("speed", "<", "100").holds(Map.of("speed", "99.5")));
        assertTrue(new Predicate("speed", ">", "100").holds(Map.of("speed", "101")));
    }

    @Test
    void textComparisonsIgnoreCaseAndRejectOrderings() {
        Map<String, String> idle = Map.of("mode", "IDLE");
        assertTrue(new Predicate("mode", "=", "idle").holds(idle));
        assertFalse(new Predicate("mode", "!=", "idle").holds(idle));
        assertFalse(new Predicate("mode", "=", "busy").holds(idle));
        assertTrue(new Predicate("mode", "!=", "busy").holds(idle));
        assertThrows(IllegalArgumentException.class, () -> new Predicate("mode", "<", "idle").holds(idle));
        assertThrows(IllegalArgumentException.class, () -> new Predicate("speed", ">", "1").holds(idle));
        // o valor pode ser outra variável
        assertTrue(new Predicate("a", "=", "b").holds(Map.of("a", "5", "b", "5.0")));
    }

    @Test
    void actionsCompareNumbersAsNumbers() {
        assertTrue(new Action("t", "1").contradicts(new Action("t", "2")));
        assertFalse(new Action("t", "0").contradicts(new Action("t", "0.0")));
        assertFalse(new Action("t", "1").contradicts(new Action("u", "2")));
    }

    @Test
    void parsesLogicalValues() {
        for (String yes : List.of("T", "true", "V", "verdadeiro", "1")) {
            assertTrue(TestCase.parseBoolean(yes, "x"), yes);
        }
        for (String no : List.of("F", "false", "falso", "0")) {
            assertFalse(TestCase.parseBoolean(no, "x"), no);
        }
        assertThrows(IllegalArgumentException.class, () -> TestCase.parseBoolean("talvez", "x"));
    }

    // ---------- tabela ----------

    @Test
    void feasibilityIsAskedOnlyForRowsTheConstraintAccepts() {
        // restrição: A; o verificador falso diz que só a linha 0 é possível
        List<Integer> asked = new ArrayList<>();
        FeasibilityChecker checker = (expr, rows) -> {
            rows.forEach(r -> asked.add(r.index()));
            return rows.stream().map(r -> r.index() == 0
                    ? Optional.of(Map.of("A", "sim")) : Optional.<Map<String, String>>empty()).toList();
        };
        TruthTable table = TruthTable.of(A_AND_B, new Cond("A"), checker);

        assertEquals(List.of(0, 1), asked);
        assertEquals(List.of(true, false, false, false), table.rows().stream().map(TestVector::feasible).toList());
        assertEquals(Map.of("A", "sim"), table.rows().get(0).assignment());
        assertEquals(Map.of(), table.rows().get(1).assignment());
    }

    @Test
    void formatShowsEveryRowAndMarksImpossibleOnes() {
        assertEquals("""
                Vetor A   B   | D
                V1    T   T   | T
                V2    T   F   | F
                V3    F   T   | F  (impossível)
                V4    F   F   | F  (impossível)
                """, TruthTable.of(A_AND_B, new Cond("A")).format());
    }

    @Test
    void directModeAcceptsUpToThirtyInputs() {
        assertEquals(30, buildPartial(30).inputs().size());
        assertThrows(IllegalArgumentException.class, () -> buildPartial(31));
        assertEquals(1L << 30, buildPartial(30).combinations());
        assertFalse(buildPartial(30).isFull());
    }

    private static TruthTable buildPartial(int inputs) {
        Expr expr = new Cond("x0");
        for (int i = 1; i < inputs; i++) {
            expr = new And(expr, new Cond("x" + i));
        }
        return TruthTable.partial(expr, List.of());
    }

    @Test
    void vectorsWithoutValuesHaveAnEmptyAssignment() {
        assertEquals(Map.of(), new TestVector(0, AB, true, true, null).assignment());
    }
}
