package io.github.rvdomingos.mcdc.core.mutation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

/** A lista exata de mutantes: se um tipo de falha deixar de ser gerado, a nota de mutação mentiria. */
class MutantsTest {

    private static final Cond A = new Cond("A");
    private static final Cond B = new Cond("B");
    private static final Cond C = new Cond("C");

    private static Set<Expr> of(Expr expr, FaultClass fault) {
        return Mutants.of(expr).stream().filter(m -> m.fault() == fault).map(Mutants.Mutant::expression)
                .collect(Collectors.toSet());
    }

    @Test
    void everyMutantOfAAndBOrC() {
        Expr expr = new And(A, new Or(B, C));

        assertEquals(17, Mutants.of(expr).size());
        assertEquals(Set.of(new Or(A, new Or(B, C)), new And(A, new And(B, C))), of(expr, FaultClass.ORF));
        assertEquals(Set.of(new Not(expr), new And(A, new Not(new Or(B, C)))), of(expr, FaultClass.ENF));
        assertEquals(Set.of(new Or(B, C), new And(A, C), new And(A, B)), of(expr, FaultClass.MVF));
        assertEquals(Set.of(new Or(new And(A, B), C)), of(expr, FaultClass.ASF));
        assertEquals(Set.of(new And(new Not(A), new Or(B, C)), new And(A, new Or(new Not(B), C)),
                new And(A, new Or(B, new Not(C)))), of(expr, FaultClass.VNF));
        assertEquals(Set.of(
                new And(B, new Or(B, C)), new And(C, new Or(B, C)),
                new And(A, new Or(A, C)), new And(A, new Or(C, C)),
                new And(A, new Or(B, A)), new And(A, new Or(B, B))), of(expr, FaultClass.VRF));
    }

    @Test
    void parenthesesShiftAlsoWhenTheOrIsOnTheLeft() {
        // (A or B) and C vira A or (B and C)
        assertEquals(Set.of(new Or(A, new And(B, C))), of(new And(new Or(A, B), C), FaultClass.ASF));
    }

    @Test
    void aNegatedConditionCountsAsALeafButANegatedSubexpressionDoesNot() {
        assertEquals(Set.of(new Not(B), A), of(new And(A, new Not(B)), FaultClass.MVF));
        // tirar ¬(B and C) inteiro não é MVF; só as folhas: A, e B ou C dentro da negação
        assertEquals(Set.of(new Not(new And(B, C)), new And(A, new Not(C)), new And(A, new Not(B))),
                of(new And(A, new Not(new And(B, C))), FaultClass.MVF));
    }

    @Test
    void summaryAndScoreMatchTheResults() {
        // o deslocamento de parênteses em A and (B or C) é o único que escapa da suíte
        McdcReport report = Mcdc.analyze(new And(A, new Or(B, C)), McdcOptions.defaults());
        MutationReport mutation = MutationReport.of(report);

        Map<FaultClass, Integer> totals = new EnumMap<>(FaultClass.class);
        mutation.results().forEach(r -> totals.merge(r.mutant().fault(), 1, Integer::sum));
        mutation.byFault().forEach((fault, summary) -> {
            assertEquals(totals.get(fault), summary.total(), fault.name());
            assertEquals(summary.total() - summary.equivalent(), summary.detectable(), fault.name());
        });

        long detectable = mutation.results().stream().filter(r -> !r.equivalent()).count();
        long killed = mutation.results().stream().filter(r -> r.killedBy() != null).count();
        assertEquals(100.0 * killed / detectable, mutation.score(), 1e-9);
        List<FaultClass> escaped = mutation.survivors().stream().map(r -> r.mutant().fault()).toList();
        assertEquals(escaped.size(), detectable - killed);
        assertEquals(detectable - killed, mutation.byFault().values().stream()
                .mapToInt(s -> s.detectable() - s.killed()).sum());
    }

    @Test
    void equivalentMutantsLeaveTheScore() {
        // A or (A and B): tirar ou trocar a parte redundante não muda nada
        MutationReport mutation = MutationReport.of(Mcdc.analyze(new Or(A, new And(A, B)), McdcOptions.defaults()));
        long equivalent = mutation.results().stream().filter(MutationReport.Result::equivalent).count();
        long killed = mutation.results().stream().filter(r -> r.killedBy() != null).count();
        long total = mutation.results().size();
        assertEquals(true, equivalent > 0);
        assertEquals(100.0 * killed / (total - equivalent), mutation.score(), 1e-9);
        int detectable = mutation.byFault().values().stream().mapToInt(MutationReport.Summary::detectable).sum();
        assertEquals(total - equivalent, detectable);
    }

    @Test
    void scoreIsFullWhenNothingCanBeDetected() {
        assertEquals(100.0, new MutationReport(List.of()).score());
    }
}
