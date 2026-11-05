package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import org.junit.jupiter.api.Test;

class CsvReportTest {

    @Test
    void writesOneLinePerTestAndInput() {
        String text = "(A and B) or C";
        Decision decision = new Decision("d1", "REQ-001", text, ExpressionParser.parse(text), List.of());
        String csv = CsvReport.format(List.of(Mcdc.analyze(decision, McdcOptions.defaults())));

        List<String> lines = csv.lines().toList();
        assertEquals(CsvReport.HEADER, lines.get(0));
        assertEquals(1 + 4 * 3, lines.size()); // 4 testes x 3 entradas
        assertEquals("d1,REQ-001,V2,A,T,T,A; B,", lines.get(1)); // V2 participa dos pares de A e de B
    }

    @Test
    void quotesCellsWithCommas() {
        Decision decision = new Decision("d1, parte 2", null, "A", ExpressionParser.parse("A"), List.of());
        String csv = CsvReport.format(List.of(Mcdc.analyze(decision, McdcOptions.defaults())));

        assertTrue(csv.lines().skip(1).allMatch(line -> line.startsWith("\"d1, parte 2\",,")));
    }
}
