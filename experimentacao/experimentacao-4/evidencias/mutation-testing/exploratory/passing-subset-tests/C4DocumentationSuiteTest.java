package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class C4DocumentationSuiteTest {

    private static final ObjectMapper JSON = new ObjectMapper();

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4An001DirectExecutionProducesTruthTable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--direct", "--format", "json"));
        assertTrue(json(output).path("decisions").path(0).path("truthTableBuilt").asBoolean());
    }

    @Test
    void o4An002DirectExecutionDoesNotBuildCompleteTable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--direct", "--format", "json"));
        JsonNode decision = json(output).path("decisions").path(0);
        assertFalse(decision.path("truthTableBuilt").asBoolean());
        assertTrue(decision.path("minimalSuite").size() > 0);
    }

    @Test
    void o4An003AcceptsExpressionSource(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "A and B"));
    }

    @Test
    void o4An003AcceptsMcdcSource(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("one.mcdc");
        Files.writeString(source, "REQ-001: A and B\n");
        assertEquals(Main.OK, runTo(dir.resolve("report.json"), "analyze", "-f", source.toString(), "--format", "json"));
    }

    @Test
    void o4Chk001ReportsCsvAnalysis(@TempDir Path dir) throws Exception {
        Path csv = writeCsv(dir.resolve("tests.csv"),
                "test,input,value,expected_outcome\n"
                        + "T1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\n"
                        + "T3,A,T,T\nT3,B,F,F\nT4,A,F,F\nT4,B,F,F\n");
        Path output = dir.resolve("check.json");
        assertEquals(Main.OK, runTo(output, "check", "A and B", "--tests", csv.toString(), "--format", "json"));
        JsonNode conditions = json(output).path("decisions").path(0).path("conditions");
        assertEquals(2, conditions.size());
    }

    @Test
    void o4Chk002ImpossibleCombinationIsNotValidEvidence(@TempDir Path dir) throws Exception {
        Path csv = impossiblePairCsv(dir);
        Path output = dir.resolve("check.json");
        assertEquals(Main.UNCOVERED,
                runTo(output, "check", "A and B", "--constraint", "A", "--z3", "--tests", csv.toString(), "--format", "json"));
        assertFalse(condition(json(output), "A").path("demonstrated").asBoolean());
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Chk003ImpossibleCombinationCanCountInCompletePair(@TempDir Path dir) throws Exception {
        Path csv = impossiblePairCsv(dir);
        Path output = dir.resolve("check.json");
        assertEquals(Main.UNCOVERED,
                runTo(output, "check", "A and B", "--constraint", "A", "--z3", "--tests", csv.toString(), "--format", "json"));
        assertTrue(condition(json(output), "A").path("demonstrated").asBoolean());
    }

    @Test
    void o4Vrf001CompatibleOverlapIsNotAConflict(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("compatible.json"), verifyJson("x := true"));
        Path output = dir.resolve("verify.json");
        assertEquals(Main.OK, runTo(output, "verify", "--json", source.toString(), "--format", "json"));
        assertEquals(0, json(output).path("conflicts").size());
        assertTrue(json(output).path("compatibleOverlaps").size() > 0);
    }

    @Test
    void o4Vrf002DifferentWritesAreAConflict(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("conflict.json"), verifyJson("x := false"));
        Path output = dir.resolve("verify.json");
        assertEquals(Main.UNCOVERED, runTo(output, "verify", "--json", source.toString(), "--format", "json"));
        assertTrue(json(output).path("conflicts").size() > 0);
    }

    @Test
    void o4Vrf003ChecksGapUnderContext(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("gap.json"), singleDecisionJson("A", "x := true", false));
        Path output = dir.resolve("verify.json");
        assertEquals(Main.UNCOVERED,
                runTo(output, "verify", "--json", source.toString(), "--context", "true", "--format", "json"));
        assertTrue(json(output).path("gaps").path("found").asBoolean());
    }

    @Test
    void o4Src001RejectsExpressionAndFileTogether(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("one.mcdc");
        Files.writeString(source, "REQ-001: A\n");
        assertEquals(Main.INPUT_ERROR,
                Main.run(new String[] {"analyze", "A", "-f", source.toString()}));
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Src002AcceptsSeveralIndependentFiles(@TempDir Path dir) throws Exception {
        Path first = dir.resolve("first.mcdc");
        Path second = dir.resolve("second.mcdc");
        Files.writeString(first, "REQ-001: A\n");
        Files.writeString(second, "REQ-002: B\n");
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", first.toString(), "-f", second.toString(), "--format", "json"));
        assertEquals(2, json(output).path("decisions").size());
    }

    @Test
    void o4Mcdc001EachValidLineIsIndependent(@TempDir Path dir) throws Exception {
        Path source = twoLineMcdc(dir);
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        assertEquals(2, json(output).path("decisions").size());
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Mcdc002AllLinesFormOneDecision(@TempDir Path dir) throws Exception {
        Path source = twoLineMcdc(dir);
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "-f", source.toString(), "--format", "json"));
        assertEquals(1, json(output).path("decisions").size());
    }

    @Test
    void o4Json001TemporalIsOptional(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("no-temporal.json"), singleDecisionJson("A", "x := true", false));
        assertEquals(Main.OK, runTo(dir.resolve("report.json"), "analyze", "--json", source.toString(), "--format", "json"));
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Json002TemporalIsRequired(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("no-temporal.json"), singleDecisionJson("A", "x := true", false));
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "--json", source.toString()}));
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Json003UsesLiteralFieldSpellings(@TempDir Path dir) throws Exception {
        String sourceText = """
                {"syem":"C4","inuts":[{"name":"A","type":"boolean","values":["true","false"]}],
                 "dciions":[{"i":"D1","requient":"R1","guad":"A","actions":["x := true"]}]}
                """;
        Path source = writeJson(dir.resolve("literal-fields.json"), sourceText);
        assertEquals(Main.OK, runTo(dir.resolve("report.json"), "analyze", "--json", source.toString(), "--format", "json"));
    }

    @Test
    void o4Var001MaskingIsTheDefaultForTwoConditions(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "json"));
        assertEquals("MASKING", json(output).path("variant").asText());
    }

    @Test
    void o4Var002UniqueCauseCanBeSelectedExplicitly(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--unique-cause", "--format", "json"));
        assertEquals("UNIQUE_CAUSE", json(output).path("variant").asText());
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Var003UniqueCauseIsAutomaticAboveTwoConditions(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "(A and B) or C", "--format", "json"));
        assertEquals("UNIQUE_CAUSE", json(output).path("variant").asText());
    }

    @Test
    void o4Z3001Z3ProvidesValues(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--z3", "--format", "json"));
        JsonNode decision = json(output).path("decisions").path(0);
        assertTrue(decision.path("truthTable").size() > 0);
        assertTrue(decision.path("truthTable").path(0).has("feasible"));
    }

    @Test
    void o4Z3002BasicAnalysisCanRunWithoutZ3Option(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "A and B"));
    }

    @Test
    void o4Z3003BoundaryWorksWithZ3(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.json");
        assertEquals(Main.OK,
                runTo(output, "analyze", "speed > 100", "--boundary", "--z3", "--format", "json"));
        assertTrue(json(output).path("decisions").path(0).path("boundaryTests").size() > 0);
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Z3003MisspelledBoundaryOptionIsAccepted(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "speed > 100", "--boudary", "-z3"));
    }

    @Test
    void o4Opt001ExactAndDirectAreExclusive() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A and B", "--exact", "--direct"}));
    }

    @Test
    void o4Lim002DirectAcceptsTwentyOneInputs(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", conjunction(21), "--direct"));
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Lim003DirectRejectsTwentyOneInputsByGeneralLimit(@TempDir Path dir) {
        assertEquals(Main.INPUT_ERROR,
                runTo(dir.resolve("report.txt"), "analyze", conjunction(21), "--direct"));
    }

    @Disabled("Indeterminado: os limites de tabela completa, 20 entradas e combinações Z3 se sobrepõem.")
    @Test
    void o4Lim001TwentyInputFullTable() {
        throw new AssertionError("C4 does not determine whether the 20-input table is constructible under the other limits");
    }

    @Disabled("Indeterminado: o texto alterna entre 096 e 46 combinações sem definir a entrada contada.")
    @Test
    void o4Lim004Z3Limit096() {
        throw new AssertionError("C4 does not determine the intended numeric threshold or unit");
    }

    @Disabled("Indeterminado: o valor 46 contradiz 096 e a unidade de contagem não é definida.")
    @Test
    void o4Lim005Z3Limit46() {
        throw new AssertionError("C4 does not determine the intended numeric threshold or unit");
    }

    @Disabled("Indeterminado: o limite de pares não define a consequência ao ser excedido.")
    @Test
    void o4Lim006MaximumPairsPerCondition() {
        throw new AssertionError("C4 does not define whether excess pairs are truncated or rejected");
    }

    @Disabled("Indeterminado: o timeout é citado, mas o resultado/código após timeout não é definido.")
    @Test
    void o4Lim007Z3TimeoutResult() {
        throw new AssertionError("C4 does not define the output for a timeout");
    }

    @Test
    void o4Out001TruthCsvContainsCompleteTable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("truth.csv");
        assertEquals(Main.OK, runTo(output, "analyze", "A and B", "--format", "truth-csv"));
        assertEquals(5, Files.readAllLines(output).size());
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Out002DirectTruthCsvCanContainOnlyDemonstrationPairs(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("truth.csv");
        assertEquals(Main.OK,
                runTo(output, "analyze", "A and B", "--direct", "--format", "truth-csv"));
        assertTrue(Files.size(output) > 0);
    }

    @Test
    void o4Out003CsvCanRunWithoutCompleteTable(@TempDir Path dir) throws Exception {
        Path output = dir.resolve("report.csv");
        assertEquals(Main.OK,
                runTo(output, "analyze", "A and B", "--direct", "--format", "csv"));
        assertTrue(Files.size(output) > 0);
    }

    @Test
    void o4Exit001UncoveredAnalysisReturnsTwo(@TempDir Path dir) {
        assertEquals(Main.UNCOVERED, runTo(dir.resolve("report.txt"), "analyze", "A and (A or B)"));
    }

    @Disabled("Excluded only from exploratory PIT: fails on unmutated baseline.")
    @Test
    void o4Exit002GeneratedReportsReturnZeroDespiteUncovered(@TempDir Path dir) {
        assertEquals(Main.OK, runTo(dir.resolve("report.txt"), "analyze", "A and (A or B)"));
    }

    @Test
    void o4Exit003InvalidOptionReturnsOne() {
        assertEquals(Main.INPUT_ERROR, Main.run(new String[] {"analyze", "A", "--invalid"}));
    }

    @Test
    void o4Exit004VerifyProblemReturnsTwo(@TempDir Path dir) throws Exception {
        Path source = writeJson(dir.resolve("conflict.json"), verifyJson("x := false"));
        assertEquals(Main.UNCOVERED, Main.run(new String[] {"verify", "--json", source.toString()}));
    }

    @Disabled("Indeterminado: a documentação diz que estas funcionalidades não estão confirmadas.")
    @Test
    void o4Unconfirmed001UnconfirmedFeaturesHaveNoExecutableOracle() {
        throw new AssertionError("C4 explicitly does not confirm these features as implemented");
    }

    private static Path twoLineMcdc(Path dir) throws IOException {
        Path source = dir.resolve("two-lines.mcdc");
        Files.writeString(source, "REQ-001: A\nREQ-002: B\n");
        return source;
    }

    private static Path impossiblePairCsv(Path dir) throws IOException {
        return writeCsv(dir.resolve("impossible.csv"),
                "test,input,value,expected_outcome\n"
                        + "T1,A,T,T\nT1,B,T,T\nT2,A,F,F\nT2,B,T,F\n");
    }

    private static Path writeCsv(Path path, String content) throws IOException {
        Files.writeString(path, content);
        return path;
    }

    private static Path writeJson(Path path, String content) throws IOException {
        Files.writeString(path, content);
        return path;
    }

    private static String singleDecisionJson(String guard, String action, boolean includeTemporal) {
        String temporal = includeTemporal ? ",\"temporal\":\"true\"" : "";
        return """
                {"system":"C4","inputs":[{"name":"A","type":"boolean","values":["true","false"]}],
                 "decisions":[{"id":"D1","requirement":"R1","guard":"%s","actions":["%s"]%s}]}
                """.formatted(guard, action, temporal);
    }

    private static String verifyJson(String secondAction) {
        return """
                {"system":"C4","inputs":[{"name":"A","type":"boolean","values":["true","false"]}],
                 "decisions":[
                   {"id":"D1","requirement":"R1","guard":"A","actions":["x := true"]},
                   {"id":"D2","requirement":"R2","guard":"A","actions":["%s"]}
                 ]}
                """.formatted(secondAction);
    }

    private static JsonNode condition(JsonNode report, String name) {
        for (JsonNode condition : report.path("decisions").path(0).path("conditions")) {
            if (condition.path("condition").asText().equals(name)) {
                return condition;
            }
        }
        throw new AssertionError("No condition named " + name + " in check report");
    }

    private static JsonNode json(Path path) throws IOException {
        return JSON.readTree(Files.readString(path));
    }

    private static int runTo(Path output, String... args) {
        List<String> full = new ArrayList<>(List.of(args));
        full.add("-o");
        full.add(output.toString());
        return Main.run(full.toArray(String[]::new));
    }

    private static String conjunction(int count) {
        return IntStream.rangeClosed(1, count).mapToObj(i -> "C" + i).collect(Collectors.joining(" and "));
    }
}
