package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class IndependencePairsTest {

    // (A and B) or C
    private final Expr andOr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void findsPairsForAndOr() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        assertEquals("[(V3, V4), (V5, V6), (V7, V8)]", pairs.get("C").toString());
    }

    @Test
    void findsPairsWithNegation() {
        // A and not B
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals("[(V2, V4)]", pairs.get("A").toString());
        assertEquals("[(V1, V2)]", pairs.get("B").toString());
    }

    @Test
    void conditionWithoutEffectHasNoPair() {
        // A or (A and B): B nunca muda o resultado sozinha
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals(List.of(), pairs.get("B"));
    }

    @Test
    void maskingAcceptsPairsWhereMaskedConditionsChange() {
        Map<String, List<IndependencePair>> pairs = IndependencePairs.masking(TruthTable.of(andOr));

        assertEquals("[(V2, V6)]", pairs.get("A").toString());
        assertEquals("[(V2, V4)]", pairs.get("B").toString());
        // V7 (FFT) e V4 (TFF): A também muda, mas (A and B) é falso nos dois, então A está mascarada
        assertEquals(9, pairs.get("C").size());
        assertTrue(pairs.get("C").toString().contains("(V7, V4)"));
    }

    @Test
    void everyUniqueCausePairIsAlsoAMaskingPair() {
        List<Expr> expressions = List.of(
                andOr,
                new And(new Cond("A"), new Not(new Cond("B"))),
                new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C"))));

        for (Expr expr : expressions) {
            TruthTable table = TruthTable.of(expr);
            Map<String, List<IndependencePair>> unique = IndependencePairs.uniqueCause(table);
            Map<String, List<IndependencePair>> masking = IndependencePairs.masking(table);
            for (String condition : masking.keySet()) {
                assertTrue(masking.get(condition).containsAll(unique.get(condition)), condition);
            }
        }
    }

    @Test
    void ignoresImpossibleRows() {
        // A or (B and C), com A = speed > 100 e B = speed > 50: A verdadeira exige B verdadeira
        Expr expr = new Or(new Cond("A"), new And(new Cond("B"), new Cond("C")));
        Expr constraint = new Or(new Not(new Cond("A")), new Cond("B"));
        TruthTable table = TruthTable.of(expr, constraint);

        Map<String, List<IndependencePair>> unique = IndependencePairs.uniqueCause(table);
        assertEquals("[(V2, V6)]", unique.get("A").toString());
        assertEquals("[(V5, V7)]", unique.get("B").toString());
        assertEquals("[(V5, V6)]", unique.get("C").toString());

        Map<String, List<IndependencePair>> masking = IndependencePairs.masking(table);
        assertEquals("[(V2, V6), (V2, V7), (V2, V8)]", masking.get("A").toString());
    }

    @Test
    void eachOccurrenceOfARepeatedInputHasItsOwnPairs() {
        // (A and B) or (not A and C)
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.uniqueCause(TruthTable.of(expr));

        assertEquals(List.of("A#1", "B", "A#2", "C"), List.copyOf(pairs.keySet()));
        assertEquals("[(V2, V6)]", pairs.get("A#1").toString());
        assertEquals("[(V3, V7)]", pairs.get("A#2").toString());
        assertEquals("[(V1, V3), (V2, V4)]", pairs.get("B").toString());
        assertEquals("[(V5, V6), (V7, V8)]", pairs.get("C").toString());
    }

    @Test
    void maskingAlsoWorksPerOccurrence() {
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C")));
        Map<String, List<IndependencePair>> pairs = IndependencePairs.masking(TruthTable.of(expr));

        // A#1 decide quando B = T e (not A and C) é falso
        assertEquals("[(V1, V6), (V2, V6)]", pairs.get("A#1").toString());
        assertTrue(pairs.get("A#2").toString().contains("(V3, V7)"));
    }
}
