package io.github.rvdomingos.mcdc.core.model;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import org.junit.jupiter.api.Test;

class ExprTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void evaluatesAndOr() {
        assertTrue(decision.eval(Map.of("A", true, "B", true, "C", false)));
        assertFalse(decision.eval(Map.of("A", true, "B", false, "C", false)));
        assertTrue(decision.eval(Map.of("A", false, "B", false, "C", true)));
    }

    @Test
    void evaluatesNot() {
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        assertTrue(expr.eval(Map.of("A", true, "B", false)));
        assertFalse(expr.eval(Map.of("A", true, "B", true)));
    }

    @Test
    void rejectsMissingCondition() {
        assertThrows(IllegalArgumentException.class, () -> decision.eval(Map.of("A", true, "B", true)));
    }
}
