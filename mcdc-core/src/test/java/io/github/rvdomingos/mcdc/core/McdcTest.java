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
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class McdcTest {

    @Test
    void analyzesWithDefaults() {
        // (A and B) or C
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());

        assertEquals(McdcVariant.MASKING, report.options().variant());
        assertEquals(4, report.minimalSuite().size());
        assertTrue(report.isComplete());
    }

    @Test
    void reportsRedundantCondition() {
        // A or (A and B): o segundo A também fica sem par, porque cada ocorrência é uma condição
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());

        assertEquals(List.of("A#2", "B"), report.uncoveredConditions());
        assertFalse(report.isComplete());
    }

    @Test
    void appliesConstraintAndVariant() {
        // A or (B and C), com restrição not A or B
        Expr expr = new Or(new Cond("A"), new And(new Cond("B"), new Cond("C")));
        McdcOptions options = McdcOptions.defaults()
                .withVariant(McdcVariant.UNIQUE_CAUSE)
                .withConstraint(new Or(new Not(new Cond("A")), new Cond("B")));

        McdcReport report = Mcdc.analyze(expr, options);
        String suite = report.minimalSuite().stream().map(TestVector::name).collect(Collectors.joining(", "));
        assertEquals("V2, V5, V6, V7", suite);
    }

    @Test
    void repeatedInputNeedsOnePairPerOccurrence() {
        // (A and B) or (not A and C): 3 entradas e 4 condições; A#1 só tem o par (V2, V6) e A#2 só (V3, V7)
        Expr expr = new Or(new And(new Cond("A"), new Cond("B")), new And(new Not(new Cond("A")), new Cond("C")));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE));

        assertTrue(report.isComplete());
        List<String> suite = report.minimalSuite().stream().map(TestVector::name).toList();
        assertTrue(suite.containsAll(List.of("V2", "V6", "V3", "V7")), suite.toString());
    }

    @Test
    void redundantConditionsAreDiagnosedAsSuch() {
        // A or (A and B): o segundo A e B não mudam o resultado em nenhuma combinação
        Expr expr = new Or(new Cond("A"), new And(new Cond("A"), new Cond("B")));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults());

        assertEquals(2, report.uncovered().size());
        assertTrue(report.uncovered().stream().allMatch(u -> u.reason() == UncoveredCondition.Reason.REDUNDANT));
    }

    @Test
    void conditionsBlockedByConstraintsAreDiagnosedAsInfeasible() {
        // A or B, com a restrição "A or B": a linha FF é impossível, e era ela que dava os pares
        Expr expr = new Or(new Cond("A"), new Cond("B"));
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults()
                .withVariant(McdcVariant.UNIQUE_CAUSE)
                .withConstraint(new Or(new Cond("A"), new Cond("B"))));

        assertEquals(List.of("A", "B"), report.uncoveredConditions());
        UncoveredCondition a = report.uncovered().get(0);
        assertEquals(UncoveredCondition.Reason.INFEASIBLE, a.reason());
        assertEquals("[(V2, V4)]", a.blockedPairs().toString());
    }
}
