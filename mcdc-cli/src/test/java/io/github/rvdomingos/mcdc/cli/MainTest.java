package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class MainTest {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Test
    void completeCoverageReturnsZero() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or C"}));
    }

    @Test
    void redundantConditionReturnsTwo() {
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"analyze", "A or (A and B)"}));
    }

    @Test
    void invalidInputReturnsOne() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--constraint"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--constraint", "Z"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--foo"}));
    }

    @Test
    void readsRequirementsFile(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("requisitos.mcdc");
        Files.writeString(file, "# comentário\nREQ-1: A and B\n\nREQ-2: A or not B\n");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "-f", file.toString()}));
    }

    @Test
    void readsNat2TestJson(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("decisoes.json");
        Files.writeString(file, """
                { "decisions": [
                    { "id": "d1", "requirement": "REQ-1", "guard": "(A = x /\\\\ B = y) \\\\/ C" },
                    { "id": "d2", "guard": "speed > 100 and mode = idle" }
                ] }
                """);
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "--json", file.toString()}));
    }

    @Test
    void acceptsOnlyOneInput(@TempDir Path dir) {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--json", "x.json"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "--json", dir.resolve("nao-existe.json").toString()}));
    }

    @Test
    void writesReportToFile(@TempDir Path dir) throws IOException {
        Path out = dir.resolve("relatorio.json");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or C", "--format", "json", "-o", out.toString()}));
        assertTrue(Files.readString(out).contains("\"decisions\""));

        Path csv = dir.resolve("suite.csv");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "csv", "-o", csv.toString()}));
        assertTrue(Files.readString(csv).startsWith(CsvReport.HEADER));

        Path table = dir.resolve("tabela.csv");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "truth-csv", "-o", table.toString()}));
        assertEquals(1 + 4, Files.readString(table).lines().count());
    }

    @Test
    void rejectsUnknownFormat() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--format", "xml"}));
    }

    @Test
    void checkMeasuresExistingTests(@TempDir Path dir) throws IOException {
        Path tests = dir.resolve("testes.csv");
        Files.writeString(tests, "test,input,value\nT1,A,T\nT1,B,T\nT2,A,F\nT2,B,T\nT3,A,T\nT3,B,F\n");
        assertEquals(Main.OK, Main.run(new String[] {"check", "A and B", "--tests", tests.toString()}));

        Files.writeString(tests, "test,input,value\nT1,A,T\nT1,B,T\n");
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"check", "A and B", "--tests", tests.toString()}));
    }

    @Test
    void checkNeedsTestsAndBoundaryNeedsZ3() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"check", "A and B"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "x > 1", "--boundary"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"check", "A", "--tests", "t.csv", "--format", "csv"}));
    }

    @Test
    void mutationOutputAndNoGherkin(@TempDir Path dir) throws IOException {
        Path json = dir.resolve("relatorio.json");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and (B or C)", "--mutation", "--format", "json", "-o", json.toString()}));
        String report = Files.readString(json);
        assertTrue(report.contains("\"mutation\""));
        assertTrue(report.contains("ASF: A and B or C")); // o exemplo de Hayhurst e Veerhusen

        // o Gherkin saiu da ferramenta
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--format", "gherkin"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"check", "A", "--tests", "t.csv", "--mutation"}));
    }

    @Test
    void exactSuiteIsSmallerWhenGreedyIsNotMinimal(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        String expr = "((E or D) and (not A or D)) or B";
        Path greedy = dir.resolve("gulosa.json");
        Path exact = dir.resolve("exata.json");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", expr, "--format", "json", "-o", greedy.toString()}));
        assertEquals(Main.OK, Main.run(new String[] {"analyze", expr, "--exact", "--format", "json", "-o", exact.toString()}));

        assertTrue(Files.readString(greedy).contains("\"suiteMethod\" : \"GREEDY\""));
        String report = Files.readString(exact);
        assertTrue(report.contains("\"suiteMethod\" : \"EXACT\""), report);
        assertEquals(6, MAPPER.readTree(greedy.toFile()).get("decisions").get(0).get("minimalSuite").size());
        assertEquals(5, MAPPER.readTree(exact.toFile()).get("decisions").get(0).get("minimalSuite").size());
    }

    @Test
    void largeDecisionsGoToTheDirectModeWithZ3(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        StringBuilder expr = new StringBuilder("a0 > 0");
        for (int i = 1; i < 14; i++) {
            expr.append(" /\\ a").append(i).append(" > ").append(i);
        }
        Path json = dir.resolve("grande.json");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", expr.toString(), "--z3", "--format", "json", "-o", json.toString()}));
        var decision = MAPPER.readTree(json.toFile()).get("decisions").get(0);
        assertEquals("DIRECT", decision.get("suiteMethod").asText());
        assertFalse(decision.get("truthTableBuilt").asBoolean());
        assertEquals(1L << 14, decision.get("truthTableRows").asLong());
        assertEquals(15, decision.get("minimalSuite").size());

        // a mutação e o truth-csv precisam da tabela inteira
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", expr.toString(), "--z3", "--mutation"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--direct", "--format", "truth-csv"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--direct", "--exact"}));
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--direct"}));
    }

    @Test
    void verifyFindsConflictsAndGaps(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        Path decisions = dir.resolve("decisoes.json");
        Files.writeString(decisions, """
                {"system": "s", "decisions": [
                  {"id": "s#1", "requirement": "REQ1", "guard": "mode = choice /\\\\ timer <= 30", "actions": ["mode := weak"]},
                  {"id": "s#2", "requirement": "REQ2", "guard": "mode = choice /\\\\ timer >= 30", "actions": ["mode := strong"]}
                ]}
                """);
        Path json = dir.resolve("verificacao.json");
        // timer = 30: as duas valem e escrevem valores diferentes
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"verify", "--json", decisions.toString(), "--format", "json", "-o", json.toString()}));
        var report = MAPPER.readTree(json.toFile());
        assertEquals(1, report.get("conflicts").size());
        assertEquals("30", report.get("conflicts").get(0).get("witness").get("timer").asText());
        assertFalse(report.get("gaps").get("checked").asBoolean());

        Files.writeString(decisions, Files.readString(decisions).replace("timer >= 30", "timer > 30"));
        assertEquals(Main.OK, Main.run(new String[] {"verify", "--json", decisions.toString(), "--context", "mode = choice"}));
        Files.writeString(decisions, Files.readString(decisions).replace("timer > 30", "timer > 40"));
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"verify", "--json", decisions.toString(), "--context", "mode = choice"}));

        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--context", "A"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"verify", "A", "--z3"}));
    }
}
