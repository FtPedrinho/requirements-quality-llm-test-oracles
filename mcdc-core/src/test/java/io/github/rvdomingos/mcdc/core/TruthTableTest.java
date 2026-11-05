package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.stream.Collectors;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

class TruthTableTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void hasOneRowPerCombination() {
        TruthTable table = TruthTable.of(decision);
        assertEquals(8, table.rows().size());
    }

    @Test
    void firstRowIsAllTrueAndLastIsAllFalse() {
        TruthTable table = TruthTable.of(decision);
        assertEquals("TTT", table.rows().get(0).bits());
        assertEquals("FFF", table.rows().get(7).bits());
    }

    @Test
    void computesOutcomeOfEachRow() {
        TruthTable table = TruthTable.of(decision);
        String outcomes = table.rows().stream()
                .map(row -> row.outcome() ? "T" : "F")
                .collect(Collectors.joining());
        assertEquals("TTTFTFTF", outcomes);
    }

    @Test
    void rejectsTooManyConditions() {
        Expr expr = new Cond("C0");
        for (int i = 1; i <= TruthTable.MAX_INPUTS; i++) {
            expr = new Or(expr, new Cond("C" + i));
        }
        Expr tooBig = expr;
        assertThrows(IllegalArgumentException.class, () -> TruthTable.of(tooBig));
    }

    @Test
    void marksRowsThatViolateTheConstraint() {
        // not A or B: A verdadeira exige B verdadeira, então TFT e TFF são impossíveis
        TruthTable table = TruthTable.of(decision, new Or(new Not(new Cond("A")), new Cond("B")));
        String feasible = table.rows().stream()
                .map(row -> row.feasible() ? "1" : "0")
                .collect(Collectors.joining());
        assertEquals("11001111", feasible);
    }

    @Test
    void rejectsConstraintWithUnknownCondition() {
        assertThrows(IllegalArgumentException.class, () -> TruthTable.of(decision, new Cond("Z")));
    }

    @Test
    void valuesComeFromTheBitsOfTheIndex() {
        TestVector v2 = TruthTable.of(decision).rows().get(1); // 001: A=T, B=T, C=F
        assertEquals(Map.of("A", true, "B", true, "C", false), v2.values());
        assertEquals(false, v2.value("C"));
        assertEquals("TTF", v2.bits());
    }

    @Test
    @Timeout(value = 30, unit = TimeUnit.SECONDS)
    void handlesTwentyInputs() {
        // C0 or C1 or ... or C19: 1.048.576 linhas
        Expr expr = new Cond("C0");
        for (int i = 1; i < TruthTable.MAX_INPUTS; i++) {
            expr = new Or(expr, new Cond("C" + i));
        }
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE));

        assertEquals(1 << 20, report.table().rows().size());
        assertEquals(21, report.minimalSuite().size()); // N + 1
    }
}
