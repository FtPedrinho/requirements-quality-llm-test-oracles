package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import org.junit.jupiter.api.Test;

class TruthTableCsvReportTest {

    private static Decision decision(String id, String requirement, String text) {
        return new Decision(id, requirement, text, ExpressionParser.parse(text), List.of());
    }

    @Test
    void writesEveryRowWithOneColumnPerCondition() {
        String csv = TruthTableCsvReport.format(List.of(
                Mcdc.analyze(decision("d1", "REQ-001", "(A and B) or C"), McdcOptions.defaults())));

        List<String> lines = csv.lines().toList();
        assertEquals("decision,requirement,row,A,B,C,outcome,feasible,in_suite,demonstrates,concrete_values", lines.get(0));
        assertEquals(1 + 8, lines.size());
        assertEquals("d1,REQ-001,V1,T,T,T,T,T,F,,", lines.get(1)); // fora da suíte
        assertEquals("d1,REQ-001,V2,T,T,F,T,T,T,A; B,", lines.get(2)); // na suíte, demonstra A e B
    }

    @Test
    void marksImpossibleRows() {
        // A implica B: a linha com A verdadeira e B falsa é impossível
        McdcOptions options = McdcOptions.defaults().withConstraint(ExpressionParser.parse("not A or B"));
        String csv = TruthTableCsvReport.format(List.of(Mcdc.analyze(decision("d1", null, "A and B"), options)));

        assertEquals("d1,,V2,T,F,F,F,F,,", csv.lines().toList().get(2));
    }

    @Test
    void givesEachDecisionItsOwnHeader() {
        String csv = TruthTableCsvReport.format(List.of(
                Mcdc.analyze(decision("d1", null, "A and B"), McdcOptions.defaults()),
                Mcdc.analyze(decision("d2", null, "speed > 100 or rain"), McdcOptions.defaults())));

        assertTrue(csv.contains("\n\ndecision,requirement,row,speed > 100,rain,outcome,"));
        assertEquals(2, csv.lines().filter(line -> line.startsWith("decision,")).count());
    }
}
