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
import org.junit.jupiter.api.Test;

class ConditionTest {

    // (A and B) or (not A and C)
    private final Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C")));

    @Test
    void numbersOnlyRepeatedInputs() {
        List<String> labels = Condition.of(expr).stream().map(Condition::label).toList();
        assertEquals(List.of("A#1", "B", "A#2", "C"), labels);
    }

    @Test
    void decidesFlipsOnlyThatOccurrence() {
        TruthTable table = TruthTable.of(expr);
        Condition first = table.conditions().get(0);  // A em (A and B)
        Condition second = table.conditions().get(2); // A em (not A and C)
        TestVector ttf = table.rows().get(1);         // V2: A=T, B=T, C=F

        assertTrue(first.decides(expr, ttf));
        assertFalse(second.decides(expr, ttf));
    }
}
