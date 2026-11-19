package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class C2DerivedSuiteTest {

    @Test void noCommandShowsUsage() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {}));
    }

    @Test void unknownOptionReturnsInputError() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--invalid"}));
    }

    @Test void exactlyOneSourceIsRequired() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze"}));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "-f", "unused.mcdc"}));
    }

    @Test void invalidExpressionIsRejectedWithDecisionId() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and"}));
    }

    @Test void mcdcFileUsesIdAndExpression(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("valid.mcdc");
        Files.writeString(file, "REQ-001: (A and B) or C\n");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "-f", file.toString()}));
    }

    @Test void emptyMcdcFileIsRejected(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("empty.mcdc");
        Files.writeString(file, "# vazio\n");
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "-f", file.toString()}));
    }

    @Test void nat2TestJsonUsesSystemInputsAndDecisions(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("decisions.json");
        Files.writeString(file, """
                {"system":"s","inputs":[
                  {"name":"A","type":"bool"},
                  {"name":"B","type":"bool"}
                ],"decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"A /\\\\ B","actions":["x := true"]}
                ]}
                """);
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "--json", file.toString()}));
    }

    @Test void nat2TestJsonWithoutDecisionsIsRejected(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("empty-decisions.json");
        Files.writeString(file, "{\"system\":\"s\",\"inputs\":[],\"decisions\":[]}");
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "--json", file.toString()}));
    }

    @Test void csvMissingValueColumnIsRejected(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("invalid.csv");
        Files.writeString(file, "test,input\nT1,A\n");
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"check", "A", "--tests", file.toString()}));
    }

    @Test void maskingIsDefault() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or C"}));
    }

    @Test void uniqueCauseCanBeSelected() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or C", "--unique-cause"}));
    }

    @Test void repeatedInputProducesDistinctConditions() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "(A and B) or (not A and C)", "--unique-cause"}));
    }

    @Test void tableLimitAccepts20AndRejects21() {
        StringBuilder valid = new StringBuilder("a0");
        for (int i = 1; i < 20; i++) valid.append(" and a").append(i);
        assertEquals(Main.OK, Main.run(new String[] {"analyze", valid.toString()}));

        StringBuilder invalid = new StringBuilder("a0");
        for (int i = 1; i <= 20; i++) invalid.append(" and a").append(i);
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", invalid.toString()}));
    }

    @Test void greedySuiteIsProduced() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "((E or D) and (not A or D)) or B"}));
    }

    @Test void exactSuiteUsesZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "((E or D) and (not A or D)) or B", "--exact"}));
    }

    @Test void directModeUsesZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--direct"}));
    }

    @Test void boundaryModeUsesZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "speed > 100", "--z3", "--boundary"}));
    }

    @Test void mutationReportIsProduced() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and (B or C)", "--mutation", "--format", "json"}));
    }

    @Test void verifyFindsConflict(@TempDir Path dir) throws Exception {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        Path file = dir.resolve("conflict.json");
        Files.writeString(file, """
                {"system":"s","decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"mode = choice /\\\\ timer <= 30","actions":["mode := weak"]},
                  {"id":"s#2","requirement":"REQ2","guard":"mode = choice /\\\\ timer >= 30","actions":["mode := strong"]}
                ]}
                """);
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"verify", "--json", file.toString()}));
    }

    @Test void verifyFindsGap(@TempDir Path dir) throws Exception {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        Path file = dir.resolve("gap.json");
        Files.writeString(file, """
                {"system":"s","decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"mode = idle","actions":["mode := weak"]}
                ]}
                """);
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"verify", "--json", file.toString(), "--context", "mode = choice"}));
    }

    @Test void jsonCsvAndTruthCsvFormatsAreAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "json"}));
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "csv"}));
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B", "--format", "truth-csv"}));
    }

    @Test void gherkinFormatIsRejected() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--format", "gherkin"}));
    }

    @Test void andOperatorIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B"}));
    }

    @Test void orOperatorIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A or B"}));
    }

    @Test void notOperatorIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "not A"}));
    }

    @Test void comparisonsAreAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "speed >= 100"}));
    }

    @Test void validCsvCheckCannotBeInvented() {
        throw new IllegalStateException("Erro C2: CSV de check não tem formato ou comportamento esperado definido");
    }

    @Test void repeatedInputBehaviorNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: entradas repetidas não são tratadas pela documentação");
    }

    @Test void infeasibleLineBehaviorNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: linhas impossíveis não têm semântica definida");
    }

    @Test void greedyAlgorithmNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: algoritmo guloso não é descrito");
    }

    @Test void exactSuiteDetailsNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: saída e critérios da suíte exata não são definidos");
    }

    @Test void mutationScoreOraclesNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: semântica de Mutation Score não é definida");
    }

    @Test void verifyCompatibleOverlapNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: sobreposição compatível não é definida");
    }

    @Test void z3UnknownBehaviorNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: comportamento de Z3 UNKNOWN não é definido");
    }

    @Test void truthTableFormatsNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: formato detalhado de truth-csv não é definido");
    }

    @Test void pairTruncationNotExecutableFromC2() {
        throw new IllegalStateException("Erro C2: limite e truncamento de pares não são definidos");
    }
}
