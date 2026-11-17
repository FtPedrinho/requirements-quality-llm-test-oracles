package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier.Overlap;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier.Result;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class Z3RequirementsVerifierTest {

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private final Z3RequirementsVerifier verifier = new Z3RequirementsVerifier();

    private static Cond p(String variable, String operator, String value) {
        return new Cond(new Predicate(variable, operator, value));
    }

    private static Expr and(Expr... parts) {
        Expr expr = parts[0];
        for (int i = 1; i < parts.length; i++) {
            expr = new And(expr, parts[i]);
        }
        return expr;
    }

    private static Decision decision(String requirement, Expr guard, String... actions) {
        return new Decision(requirement, requirement, guard.toString(), guard, List.of(actions));
    }

    private static DecisionSet set(Decision... decisions) {
        return new DecisionSet("sistema", List.of(), List.of(decisions));
    }

    @Test
    void findsContradictoryRequirementsThatFireTogether() {
        // NPP REQ005 e REQ008: o bloqueio liga o override; o modo saindo de high o desliga
        Decision req005 = decision("REQ005", and(p("blockage_antes", "!=", "pressed"), p("blockage", "=", "pressed"),
                p("reset", "!=", "pressed"), p("mode", "!=", "high")), "overridden := true");
        Decision req008 = decision("REQ008", and(p("mode_antes", "=", "high"), p("mode", "!=", "high")),
                "overridden := false");
        Decision req009 = decision("REQ009", and(p("mode", "=", "low"), p("overridden", "=", "true")),
                "injection := off");

        Result result = verifier.verify(set(req005, req008, req009), null);

        assertEquals(1, result.pairsChecked());
        assertEquals(1, result.conflicts().size());
        Overlap conflict = result.conflicts().get(0);
        assertEquals("overridden", conflict.conflicts().get(0).variable());
        assertTrue(holds(req005.expression(), conflict) && holds(req008.expression(), conflict), conflict.witness().toString());
        assertTrue(result.hasProblems());
        assertFalse(result.gapChecked());
    }

    private static boolean holds(Expr expr, Overlap overlap) {
        return switch (expr) {
            case Cond c -> c.predicate().holds(overlap.witness());
            case And(var l, var r) -> holds(l, overlap) && holds(r, overlap);
            default -> throw new IllegalArgumentException(expr.toString());
        };
    }

    @Test
    void disjointGuardsDoNotOverlap() {
        // VM REQ004 e REQ005: o timer 30 é comum, mas o modo é diferente
        Decision weak = decision("REQ004", and(p("mode", "=", "weak"), p("timer", ">=", "10"), p("timer", "<=", "30")),
                "mode := idle", "output := weak");
        Decision strong = decision("REQ005", and(p("mode", "=", "strong"), p("timer", ">=", "30"), p("timer", "<=", "50")),
                "mode := idle", "output := strong");

        Result result = verifier.verify(set(weak, strong), null);

        assertEquals(1, result.pairsChecked());
        assertTrue(result.overlaps().isEmpty());
        assertFalse(result.hasProblems());
    }

    @Test
    void sameValueIsACompatibleOverlap() {
        Decision a = decision("A", p("voltage", ">", "80"), "timer := 0");
        Decision b = decision("B", p("lever", "=", "left"), "timer := 0.0");

        Result result = verifier.verify(set(a, b), null);

        assertEquals(1, result.compatible().size());
        assertTrue(result.conflicts().isEmpty());
        assertFalse(result.hasProblems());
    }

    @Test
    void findsGapsOnlyUnderAContext() {
        // VM REQ002 e REQ003: com a escolha feita, o timer decide entre fraco e forte
        Decision weak = decision("REQ002", and(p("mode", "=", "choice"), p("timer", "<=", "30")), "mode := weak");
        Decision strong = decision("REQ003", and(p("mode", "=", "choice"), p("timer", ">", "30")), "mode := strong");
        DecisionSet set = set(weak, strong);

        Result covered = verifier.verify(set, p("mode", "=", "choice"));
        assertTrue(covered.gapChecked());
        assertNull(covered.gap());

        Result gap = verifier.verify(set(weak), p("mode", "=", "choice"));
        assertNotNull(gap.gap());
        assertTrue(Double.parseDouble(gap.gap().get("timer")) > 30, gap.gap().toString());
        assertTrue(gap.hasProblems());
    }
}
