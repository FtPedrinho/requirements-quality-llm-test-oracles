package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class MinimalSuiteTest {

    private static String suiteOf(Expr expr) {
        List<TestVector> suite = MinimalSuite.greedy(IndependencePairs.uniqueCause(TruthTable.of(expr)));
        return suite.stream().map(TestVector::name).collect(Collectors.joining(", "));
    }

    @Test
    void andOrNeedsFourTests() {
        // (A and B) or C
        assertEquals("V2, V3, V4, V6", suiteOf(new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"))));
    }

    @Test
    void andNotNeedsThreeTests() {
        // A and not B
        assertEquals("V1, V2, V4", suiteOf(new And(new Cond("A"), new Not(new Cond("B")))));
    }

    @Test
    void recordsWhichPairDemonstratesEachCondition() {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));
        MinimalSuite.Selection selection = MinimalSuite.select(IndependencePairs.uniqueCause(TruthTable.of(expr)));

        assertEquals("{A=(V2, V6), B=(V2, V4), C=(V3, V4)}", selection.chosen().toString());
        TestVector v2 = selection.tests().get(0);
        assertEquals(List.of("A", "B"), selection.demonstratedBy(v2));
    }

    @Test
    void prefersUniqueCausePairsOnTies() {
        // A or (B and C), mascaramento: (V2, V7) e (V3, V7) custam o mesmo, mas só (V3, V7) muda apenas A
        Expr expr = new Or(new Cond("A"), new And(new Cond("B"), new Cond("C")));
        List<IndependencePair> pairsOfA = IndependencePairs.masking(TruthTable.of(expr)).get("A");
        IndependencePair masked = pairsOfA.stream().filter(p -> p.toString().equals("(V2, V7)")).findFirst().orElseThrow();
        IndependencePair unique = pairsOfA.stream().filter(p -> p.toString().equals("(V3, V7)")).findFirst().orElseThrow();
        assertFalse(masked.isUniqueCause());
        assertTrue(unique.isUniqueCause());

        MinimalSuite.Selection selection = MinimalSuite.select(Map.of("A", List.of(masked, unique)));
        assertEquals(unique, selection.chosen().get("A"));
    }
}
