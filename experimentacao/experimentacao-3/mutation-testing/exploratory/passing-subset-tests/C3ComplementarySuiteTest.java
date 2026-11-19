package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class C3ComplementarySuiteTest {

    @Disabled("Indeterminado: C3 não especifica o comportamento sem comando")
    @Test
    void noCommandBehaviorFromGold() {
        throw new AssertionError("C3 does not define the no-command behavior");
    }

    @Disabled("Indeterminado: ignorar linhas vazias não define o resultado de um arquivo sem decisões")
    @Test
    void emptyMcdcFromGold(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("empty.mcdc");
        Files.writeString(source, "# comment\n\n");
        throw new AssertionError("C3 does not define the result for an empty .mcdc source");
    }

    @Test
    void emptyDecisionsJsonFromGold(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("empty-decisions.json");
        Files.writeString(source, "{\"system\":\"s\",\"inputs\":[],\"decisions\":[]}");
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "--json", source.toString()}));
    }

    @Disabled("Indeterminado: C3 não define as colunas obrigatórias do CSV")
    @Test
    void missingCsvHeaderFromGold(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("missing-header.csv");
        Files.writeString(source, "test,input\nT1,A\n");
        throw new AssertionError("C3 does not define the required CSV header");
    }

    @Disabled("Indeterminado: C3 não define o algoritmo guloso nem o desempate")
    @Test
    void defaultGreedySuiteFromGold() {
        throw new AssertionError("C3 does not define the selected greedy suite");
    }
}
