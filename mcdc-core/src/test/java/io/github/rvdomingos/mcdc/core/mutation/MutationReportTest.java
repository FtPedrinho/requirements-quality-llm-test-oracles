package io.github.rvdomingos.mcdc.core.mutation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.ExprText;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class MutationReportTest {

    private static final Cond A = new Cond("A");
    private static final Cond B = new Cond("B");
    private static final Cond C = new Cond("C");
    private static final Cond D = new Cond("D");

    /** Expressões sem entradas repetidas e sem entradas redundantes, como exige o teorema. */
    private static final List<Expr> EXPRESSIONS = List.of(
            new Or(new And(A, B), C),
            new And(A, new Or(B, C)),
            new And(new Or(A, B), new Or(C, D)),
            new And(A, new Not(B)),
            new Or(new And(A, B), new And(C, D)),
            new Or(A, new And(B, new Or(C, D))));

    /** Kapoor e Bowen (Corolário 3): suítes de causa única detectam toda falha ENF, VNF, MVF, VRF e ORF; ASF não tem garantia. */
    @Test
    void uniqueCauseSuitesDetectEveryGuaranteedFault() {
        Set<FaultClass> guaranteed = Set.of(FaultClass.ORF, FaultClass.ENF, FaultClass.VNF, FaultClass.MVF, FaultClass.VRF);
        for (Expr expr : EXPRESSIONS) {
            McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE));
            MutationReport mutation = MutationReport.of(report);

            List<String> missed = mutation.survivors().stream()
                    .filter(r -> guaranteed.contains(r.mutant().fault()))
                    .map(r -> r.mutant().fault() + ": " + ExprText.format(r.mutant().expression()))
                    .toList();
            assertEquals(List.of(), missed, ExprText.format(expr));
        }
    }

    @Test
    void generatesEveryFaultClass() {
        // A and (B or C) tem todas as formas: and, or, condições e o padrão de parênteses deslocados
        Set<FaultClass> faults = new java.util.HashSet<>();
        Mutants.of(new And(A, new Or(B, C))).forEach(m -> faults.add(m.fault()));
        assertEquals(Set.of(FaultClass.values()), faults);
    }

    @Test
    void associativeShiftIsTheClassicExample() {
        // A and (B or C) escrito sem parênteses: A and B or C, que significa (A and B) or C
        List<Mutants.Mutant> shifts = Mutants.of(new And(A, new Or(B, C))).stream()
                .filter(m -> m.fault() == FaultClass.ASF).toList();
        assertEquals("A and B or C", ExprText.format(shifts.get(0).expression()));
    }

    @Test
    void equivalentMutantsAreNotCountedAsMissed() {
        // em A or (A and B), trocar o B por A dá A or (A and A), que é igual a A or (A and B): equivalente
        McdcReport report = Mcdc.analyze(new Or(A, new And(A, B)), McdcOptions.defaults());
        MutationReport mutation = MutationReport.of(report);

        assertTrue(mutation.results().stream().anyMatch(MutationReport.Result::equivalent));
        assertTrue(mutation.results().stream().filter(MutationReport.Result::equivalent)
                .noneMatch(MutationReport.Result::survived));
    }

    @Test
    void formatsExpressionsWithMinimalParentheses() {
        assertEquals("(A or B) and not C", ExprText.format(new And(new Or(A, B), new Not(C))));
        assertEquals("A and B or C", ExprText.format(new Or(new And(A, B), C)));
        assertEquals("not (A and B)", ExprText.format(new Not(new And(A, B))));
    }
}
