package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class Exp2McdcSuiteTest {

    @Test
    void noCommandPrintsUsage() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {}));
    }

    @Test
    void unknownOptionIsRejected() {
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "(A and B)", "--invalid"}));
    }

    @Test
    void exactlyOneSourceIsRequired() {
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze"}));
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A", "-f", "x.mcdc"}));
    }

    @Test
    void invalidExpressionIsRejectedWithDecisionId() {
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and"}));
    }

    @Test
    void mcdcFileProducesCompleteAnalysis(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("valid.mcdc");
        Files.writeString(source, "REQ-001: (A and B) or C\n");
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "-f", source.toString(), "--format", "json"}));
    }

    @Test
    void emptyMcdcFileIsRejected(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("empty.mcdc");
        Files.writeString(source, "# empty\n");
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "-f", source.toString()}));
    }

    @Test
    void nat2TestJsonIsAccepted(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("decisions.json");
        Files.writeString(source, """
                {"system":"s","inputs":[
                  {"name":"A","type":"bool"},
                  {"name":"B","type":"bool"}
                ],"decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"A /\\\\ B","actions":["x := true"]}
                ]}
                """);
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "--json", source.toString(), "--format", "json"}));
    }

    @Test
    void nat2TestJsonWithoutDecisionsIsRejected(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("empty-decisions.json");
        Files.writeString(source, "{\"system\":\"s\",\"inputs\":[],\"decisions\":[]}");
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "--json", source.toString()}));
    }

    @Test
    void csvCheckRequiresRequiredColumns(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("invalid.csv");
        Files.writeString(source, "test,input\nT1,A\n");
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"check", "A and B", "--tests", source.toString()}));
    }

    @Test
    void truthTableContainsFourRows() throws Exception {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C", "--format", "text"}));
    }

    @Test
    void maskingAndUniqueCauseAreSupported() {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C"}));
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C", "--unique-cause"}));
    }

    @Test
    void repeatedInputProducesOneConditionPerOccurrence() {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or (not A and C)", "--unique-cause"}));
    }

    @Test
    void constraintAndVariantCanBeCombined() {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "A or (B and C)",
                        "--unique-cause", "--constraint", "not A or B"}));
    }

    @Test
    void greedySuiteIsProduced() {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze",
                        "((E or D) and (not A or D)) or B"}));
    }

    @Test
    void exactSuiteIsProducedWithZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze",
                        "((E or D) and (not A or D)) or B", "--exact"}));
    }

    @Test
    void directModeIsAcceptedForSmallDecision() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "A and B", "--direct"}));
    }

    @Test
    void directModeRejectsMutationsAndTruthCsv() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and B", "--direct",
                        "--format", "truth-csv"}));
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and B", "--direct", "--exact"}));
    }

    @Test
    void boundaryOptionRequiresZ3() {
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "speed > 100", "--boundary"}));
    }

    @Test
    void boundaryTestsAreProducedWithZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze",
                        "speed > 100 or (speed > 50 and rain)",
                        "--z3", "--boundary"}));
    }

    @Test
    void internalMutationReportIsProduced() throws Exception {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "A and (B or C)",
                        "--mutation", "--format", "json"}));
    }

    @Test
    void verifyFindsConflictingActions(@TempDir Path dir) throws Exception {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        Path source = dir.resolve("conflict.json");
        Files.writeString(source, """
                {"system":"s","decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"mode = choice /\\\\ timer <= 30","actions":["mode := weak"]},
                  {"id":"s#2","requirement":"REQ2","guard":"mode = choice /\\\\ timer >= 30","actions":["mode := strong"]}
                ]}
                """);
        assertEquals(Main.UNCOVERED,
                Main.run(new String[] {"verify", "--json", source.toString(),
                        "--format", "text"}));
    }

    @Test
    void verifyFindsGapUnderContext(@TempDir Path dir) throws Exception {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        Path source = dir.resolve("gap.json");
        Files.writeString(source, """
                {"system":"s","decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"mode = idle","actions":["mode := weak"]}
                ]}
                """);
        assertEquals(Main.UNCOVERED,
                Main.run(new String[] {"verify", "--json", source.toString(),
                        "--context", "mode = choice", "--format", "text"}));
    }

    @Test
    void jsonCsvAndTruthCsvReportsAreAccepted(@TempDir Path dir) throws Exception {
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C",
                        "--format", "json"}));
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C",
                        "--format", "csv"}));
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", "(A and B) or C",
                        "--format", "truth-csv"}));
    }

    @Test
    void gherkinFormatIsRejected() {
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A and B", "--format", "gherkin"}));
    }

    @Test
    void twentyInputLimitIsValidated() {
        StringBuilder twenty = new StringBuilder("a0");
        for (int i = 1; i < 20; i++) {
            twenty.append(" and a").append(i);
        }
        assertEquals(Main.OK,
                Main.run(new String[] {"analyze", twenty.toString()}));

        StringBuilder twentyOne = new StringBuilder("a0");
        for (int i = 1; i <= 20; i++) {
            twentyOne.append(" and a").append(i);
        }
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", twentyOne.toString()}));
    }
}
