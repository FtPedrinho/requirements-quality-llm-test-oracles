package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class MainTest {

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
        assertEquals(1 + 4, Files.readString(table).lines().count()); // cabeçalho + 4 linhas da tabela
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
    void mutationAndGherkinOutputs(@TempDir Path dir) throws IOException {
        Path json = dir.resolve("relatorio.json");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and (B or C)", "--mutation", "--format", "json", "-o", json.toString()}));
        String report = Files.readString(json);
        assertTrue(report.contains("\"mutation\""));
        assertTrue(report.contains("ASF: A and B or C")); // o exemplo de Hayhurst e Veerhusen

        Path feature = dir.resolve("suite.feature");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "gherkin", "-o", feature.toString()}));
        assertTrue(Files.readString(feature).startsWith("# language: pt"));

        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"check", "A", "--tests", "t.csv", "--mutation"}));
    }
}
