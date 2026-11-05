package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import org.junit.jupiter.api.Test;

class GherkinReportTest {

    @Test
    void writesOneScenarioPerTestInPortuguese() {
        String text = "(A and B) or C";
        Decision decision = new Decision("d1", "REQ-001", text, ExpressionParser.parse(text), List.of("liga o alarme"));
        String gherkin = GherkinReport.format("sistema", List.of(Mcdc.analyze(decision, McdcOptions.defaults())));

        assertTrue(gherkin.startsWith("# language: pt\n"));
        assertEquals(4, gherkin.lines().filter(l -> l.strip().startsWith("Cenário:")).count());
        assertTrue(gherkin.contains("  Cenário: REQ-001 V2 demonstra A, B\n"
                + "    Dado que a condição \"A\" é verdadeira\n"
                + "    E a condição \"B\" é verdadeira\n"
                + "    E a condição \"C\" é falsa\n"
                + "    Quando a guarda \"(A and B) or C\" é avaliada\n"
                + "    Então ela é verdadeira\n"
                + "    E o sistema executa \"liga o alarme\"\n"), gherkin);
    }
}
