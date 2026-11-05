package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import org.junit.jupiter.api.Test;

class ExpressionParserTest {

    private static final Cond A = new Cond("A");
    private static final Cond B = new Cond("B");
    private static final Cond C = new Cond("C");

    @Test
    void parsesParentheses() {
        assertEquals(new Or(new And(A, B), C), ExpressionParser.parse("(A and B) or C"));
    }

    @Test
    void andBindsTighterThanOr() {
        assertEquals(new Or(A, new And(B, C)), ExpressionParser.parse("A or B and C"));
    }

    @Test
    void acceptsSymbolsAndUppercaseKeywords() {
        assertEquals(new And(new Not(A), B), ExpressionParser.parse("!A && B"));
        assertEquals(new Or(A, new Not(B)), ExpressionParser.parse("A OR NOT B"));
    }

    @Test
    void rejectsInvalidExpressions() {
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A and"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("(A or B"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A $ B"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A B"));
    }

    @Test
    void parsesComparisonsAsConditionsWithPredicate() {
        Cond speed = new Cond(new Predicate("speed", ">", "100"));
        Cond mode = new Cond(new Predicate("mode", "=", "idle"));
        assertEquals(new And(speed, mode), ExpressionParser.parse("speed > 100 and mode = idle"));
        assertEquals("speed > 100", speed.id());
    }

    @Test
    void acceptsAllComparisonOperators() {
        assertEquals(new Cond(new Predicate("x", "=", "1")), ExpressionParser.parse("x == 1"));
        assertEquals(new Cond(new Predicate("x", "!=", "1")), ExpressionParser.parse("x != 1"));
        assertEquals(new Cond(new Predicate("x", "<=", "-2.5")), ExpressionParser.parse("x <= -2.5"));
        assertEquals(new Cond(new Predicate("x", ">=", "0")), ExpressionParser.parse("x>=0"));
        assertEquals(new Cond(new Predicate("x", "<", "y")), ExpressionParser.parse("x < y"));
    }

    @Test
    void acceptsDfrsOperators() {
        Cond ax = new Cond(new Predicate("A", "=", "x"));
        Cond by = new Cond(new Predicate("B", "=", "y"));
        assertEquals(new Or(new And(ax, by), C), ExpressionParser.parse("(A = x /\\ B = y) \\/ C"));
    }

    @Test
    void notStillWorksNextToComparisons() {
        assertEquals(new Not(new Cond(new Predicate("door", "=", "open"))), ExpressionParser.parse("!door = open"));
    }

    @Test
    void rejectsIncompleteComparisons() {
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A ="));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("= x"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("A = and B"));
    }
}
