package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class C3DocumentationSuiteTest {

    private static final ObjectMapper JSON = new ObjectMapper();

    @Test
    void unknownOptionUsesCodeOne() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--invalid"}));
    }

    @Test
    void expressionSourceIsAccepted(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "A and B"));
    }

    @Test
    void multipleSourcesAreRejected(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("one.mcdc");
        Files.writeString(source, "REQ1: A\n");
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "-f", source.toString()}));
    }

    @Test
    void invalidExpressionUsesCodeOne() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and"}));
    }

    @Test
    void mcdcValidLineIsAccepted(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("valid.mcdc");
        Files.writeString(source, "REQ-001: (A and B) or C\n");
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        JsonNode decision = json(output).path("decisions").get(0);
        assertEquals("REQ-001", decision.path("id").asText());
        assertFalse(decision.path("guard").asText().isBlank());
    }

    @Test
    void mcdcIgnoresEmptyAndCommentLines(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("comments.mcdc");
        Files.writeString(source, "# note\n\nREQ-001: A\n");
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        JsonNode decisions = json(output).path("decisions");
        assertEquals(1, decisions.size());
        assertEquals("REQ-001", decisions.get(0).path("id").asText());
    }

    @Test
    void mcdcMultipleLinesAreIndependent(@TempDir Path dir) throws Exception {
        Path source = twoLineMcdc(dir);
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        assertEquals(2, json(output).path("decisions").size());
    }

    @Test
    void mcdcMultipleLinesBelongToOneDecision(@TempDir Path dir) throws Exception {
        Path source = twoLineMcdc(dir);
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        assertEquals(1, json(output).path("decisions").size());
    }

    @Test
    void jsonTemporalIsOptional(@TempDir Path dir) throws Exception {
        Path source = jsonSource(dir, jsonDecision("A and B", null, "x := true"));
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "--json", source.toString(), "--format", "json"));
        assertEquals("s#1", json(output).path("decisions").get(0).path("id").asText());
    }

    @Test
    void jsonTemporalIsRequired(@TempDir Path dir) throws Exception {
        Path source = jsonSource(dir, jsonDecision("A and B", null, "x := true"));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "--json", source.toString()}));
    }

    @Test
    void jsonTemporalStringIsAccepted(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        Path source = jsonSource(dir, jsonDecision("A and B", "A", "x := true"));
        assertEquals(Main.UNCOVERED, runTo(output, "analyze", "--json", source.toString(), "--format", "json"));
        assertEquals("s#1", json(output).path("decisions").get(0).path("id").asText());
    }

    @Test
    void maskingDefaultForTwoConditions(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "json"));
        assertEquals("MASKING", json(output).path("variant").asText());
    }

    @Test
    void maskingDefaultForThreeConditions(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "(A and B) or C", "--format", "json"));
        assertEquals("MASKING", json(output).path("variant").asText());
    }

    @Test
    void uniqueCauseAutomaticForThreeConditions(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "(A and B) or C", "--format", "json"));
        assertEquals("UNIQUE_CAUSE", json(output).path("variant").asText());
    }

    @Test
    void uniqueCauseCanBeExplicit(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "(A and B) or C", "--unique-cause", "--format", "json"));
        JsonNode decision = json(output).path("decisions").get(0);
        assertEquals("UNIQUE_CAUSE", json(output).path("variant").asText());
        assertTrue(decision.path("chosenPairs").size() > 0);
        decision.path("chosenPairs").elements().forEachRemaining(pair ->
                assertTrue(pair.path("uniqueCause").asBoolean()));
    }

    @Test
    void basicAnalysisNeedsNoZ3Flag(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "A and B"));
    }

    @Test
    void directDoesNotBuildCompleteTable(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--direct", "--format", "json"));
        JsonNode decision = json(output).path("decisions").get(0);
        assertFalse(decision.path("truthTableBuilt").asBoolean());
        assertTrue(decision.path("minimalSuite").size() > 0);
    }

    @Test
    void directAlwaysBuildsTruthTable(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--direct", "--format", "json"));
        assertTrue(json(output).path("decisions").get(0).path("truthTableBuilt").asBoolean());
    }

    @Test
    void boundaryRequiresZ3Option() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "speed > 100", "--boundary"}));
    }

    @Test
    void relationalBoundaryIsProducedWithZ3(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK,
                runTo(output, "analyze", "speed > 100", "--z3", "--boundary", "--format", "json"));
        JsonNode boundaryTests = json(output).path("decisions").get(0).path("boundaryTests");
        assertTrue(boundaryTests.size() > 0);
        assertTrue(containsBoundary(boundaryTests, "speed = 100"));
        assertTrue(containsBoundary(boundaryTests, "speed = 101"));
    }

    @Test
    void exactAndDirectAreExclusive() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--exact", "--direct"}));
    }

    @Test
    void directAllowsTwentyOneInputs(@TempDir Path dir) {
        assumeZ3();
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", conjunction(21), "--direct"));
    }

    @Test
    void directRejectsTwentyOneInputsByGeneralLimit(@TempDir Path dir) {
        assumeZ3();
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", conjunction(21), "--direct", "-o", dir.resolve("report.txt").toString()}));
    }

    @Test
    void truthCsvFullTableHasFourCombinations(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("truth.csv");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "truth-csv"));
        assertEquals(5, Files.readAllLines(output).size());
    }

    @Test
    void truthCsvCanBeUsedInDirectMode(@TempDir Path dir) {
        assumeZ3();
        assertEquals(Main.OK,
                runTo(dir.resolve("truth.csv"), "analyze", "A and B", "--direct", "--format", "truth-csv"));
    }

    @Test
    void truthCsvDirectRequiresCompleteTable(@TempDir Path dir) {
        assumeZ3();
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and B", "--direct", "--format", "truth-csv",
                        "-o", dir.resolve("truth.csv").toString()}));
    }

    @Test
    void uncoveredAnalysisReturnsTwo(@TempDir Path dir) {
        assertEquals(Main.UNCOVERED,
                runTo(dir.resolve("report.json"), "analyze", "A and (A or B)", "--format", "json"));
    }

    @Test
    void uncoveredAnalysisReturnsZeroWhenReportsWritten(@TempDir Path dir) {
        assertEquals(Main.OK,
                runTo(dir.resolve("report.json"), "analyze", "A and (A or B)", "--format", "json"));
    }

    @Test
    void mutationReportIsAvailable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and (B or C)", "--mutation", "--format", "json"));
        JsonNode mutation = json(output).path("decisions").get(0).path("mutation");
        assertTrue(mutation.has("score"));
        assertTrue(mutation.has("survivors"));
    }

    @Test
    void mutationNeedsCompleteTable(@TempDir Path dir) {
        assumeZ3();
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and B", "--direct", "--mutation",
                        "-o", dir.resolve("report.json").toString()}));
    }

    @Test
    void jsonFormatIsAvailable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "json"));
        assertFalse(Files.readString(output).isBlank());
    }

    @Test
    void csvFormatIsAvailable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.csv");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "csv"));
        assertFalse(Files.readString(output).isBlank());
    }

    @Test
    void truthCsvFormatIsAvailable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("truth.csv");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "truth-csv"));
        assertFalse(Files.readString(output).isBlank());
    }

    @Test
    void verifyFindsDifferentActionConflict(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path source = verificationSource(dir, "x := weak", "x := strong");
        Path output = dir.resolve("verify-report.json");
        assertEquals(Main.UNCOVERED, runTo(output, "verify", "--json", source.toString(), "--format", "json"));
        JsonNode conflicts = json(output).path("conflicts");
        assertTrue(conflicts.size() > 0);
        assertTrue(conflicts.get(0).path("conflicts").size() > 0);
        assertTrue(conflicts.get(0).path("witness").size() > 0);
    }

    @Test
    void verifyCompatibleActionsAreNotConflict(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path source = verificationSource(dir, "x := weak", "x := weak");
        Path output = dir.resolve("verify-report.json");
        assertEquals(Main.OK, runTo(output, "verify", "--json", source.toString(), "--format", "json"));
        assertTrue(json(output).path("compatibleOverlaps").size() > 0);
    }

    @Test
    void verifyFindsGapUnderContext(@TempDir Path dir) throws Exception {
        assumeZ3();
        Path source = jsonSource(dir, jsonDecision("A", "A", "x := true"));
        Path output = dir.resolve("verify-report.json");
        assertEquals(Main.UNCOVERED, Main.run(new String[] {
                "verify", "--json", source.toString(), "--context", "not A", "--format", "json",
                "-o", output.toString()
        }));
        JsonNode gaps = json(output).path("gaps");
        assertTrue(gaps.path("found").asBoolean());
        assertTrue(gaps.path("witness").size() > 0);
    }

    @Test
    void andKeywordIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A and B"}));
    }

    @Test
    void andSymbolicAliasIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A && B"}));
    }

    @Test
    void orKeywordIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A or B"}));
    }

    @Test
    void orSymbolicAliasIsAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "A || B"}));
    }

    @Test
    void notKeywordAndSymbolAreAccepted() {
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "not A"}));
        assertEquals(Main.OK, Main.run(new String[] {"analyze", "!A"}));
    }

    @Test
    void equalityOperatorsAreEquivalent(@TempDir Path dir) throws Exception {
        Path equalsOutput = dir.resolve("equals.json");
        Path doubleEqualsOutput = dir.resolve("double-equals.json");
        assertEquals(Main.OK, runTo(equalsOutput, "analyze", "speed = 100", "--format", "json"));
        assertEquals(Main.OK, runTo(doubleEqualsOutput, "analyze", "speed == 100", "--format", "json"));
        assertEquals(outcomes(json(equalsOutput)), outcomes(json(doubleEqualsOutput)));
    }

    @Test
    void operatorPrecedenceUsesAndBeforeOr(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A or B and C", "--format", "json"));
        JsonNode rows = json(output).path("decisions").get(0).path("truthTable");
        for (JsonNode row : rows) {
            JsonNode values = row.path("values");
            if (values.path("A").asBoolean() && !values.path("B").asBoolean() && !values.path("C").asBoolean()) {
                assertTrue(row.path("outcome").asBoolean());
                return;
            }
        }
        throw new AssertionError("Expected truth-table row A=true, B=false, C=false");
    }

    @Test
    void gherkinFormatIsRejected() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--format", "gherkin"}));
    }

    @Disabled("Indeterminado: C3 não define como múltiplas fontes de decisão são codificadas")
    @Test
    void multipleDecisionSourceSyntaxCanBeObserved() {
        throw new AssertionError("No defensible source syntax or expected result is specified by C3");
    }

    @Disabled("Indeterminado: C3 não define o CSV nem o marcador de combinação impossível")
    @Test
    void checkImpossibleCombinationCanBeBuilt() {
        throw new AssertionError("No defensible CSV fixture or expected result is specified by C3");
    }

    @Disabled("Indeterminado: não é possível isolar Z3 ausente sem alterar o ambiente; C3 também conflita")
    @Test
    void analyzeWithoutZ3ExecutableCanBeObserved() {
        throw new AssertionError("No isolated solver-absence environment or precedence rule is specified by C3");
    }

    @Disabled("Indeterminado: C3 não define enumeração de pares para produzir entrada reprodutível")
    @Test
    void pairLimitCanBeTriggered() {
        throw new AssertionError("No defensible expression is specified to exceed the pair cap");
    }

    @Disabled("Indeterminado: C3 não define entrada determinística nem saída para timeout")
    @Test
    void z3TimeoutCanBeTriggered() {
        throw new AssertionError("No defensible timeout input or expected result is specified by C3");
    }

    private static int runTo(Path output, String... args) {
        List<String> command = new ArrayList<>(List.of(args));
        command.add("-o");
        command.add(output.toString());
        return Main.run(command.toArray(String[]::new));
    }

    private static void assumeZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
    }

    private static Path twoLineMcdc(Path dir) throws Exception {
        Path source = dir.resolve("two.mcdc");
        Files.writeString(source, "REQ1: A and B\nREQ2: A or B\n");
        return source;
    }

    private static Path jsonSource(Path dir, String decision) throws Exception {
        Path source = dir.resolve("source.json");
        Files.writeString(source, """
                {"system":"s","inputs":[{"name":"A","type":"bool"},{"name":"B","type":"bool"}],
                 "decisions":[%s]}
                """.formatted(decision));
        return source;
    }

    private static String jsonDecision(String guard, String temporal, String action) {
        String temporalField = temporal == null ? "" : ",\"temporal\":\"%s\"".formatted(temporal);
        return """
                {"id":"s#1","requirement":"REQ1","guard":"%s"%s,"actions":["%s"]}
                """.formatted(guard, temporalField, action).trim();
    }

    private static Path verificationSource(Path dir, String firstAction, String secondAction) throws Exception {
        Path source = dir.resolve("verify.json");
        Files.writeString(source, """
                {"system":"s","inputs":[{"name":"A","type":"bool"}],"decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"A","temporal":"A","actions":["%s"]},
                  {"id":"s#2","requirement":"REQ2","guard":"A","temporal":"A","actions":["%s"]}
                ]}
                """.formatted(firstAction, secondAction));
        return source;
    }

    private static String conjunction(int count) {
        List<String> variables = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            variables.add("a" + i);
        }
        return String.join(" and ", variables);
    }

    private static JsonNode json(Path path) throws Exception {
        return JSON.readTree(Files.readString(path));
    }

    private static List<JsonNode> outcomes(JsonNode root) {
        List<JsonNode> values = new ArrayList<>();
        root.path("decisions").get(0).path("truthTable").forEach(row -> values.add(row.path("outcome")));
        return values;
    }

    private static boolean containsBoundary(JsonNode tests, String value) {
        for (JsonNode test : tests) {
            if (value.equals(test.path("boundary").asText())) {
                return true;
            }
        }
        return false;
    }
}
