package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

/**
 * Trava os resultados dos 33 requisitos dos três sistemas de exemplo da NAT2TEST (VM, TIS e NPP),
 * rodando pelo mesmo caminho da linha de comando. Se uma mudança no motor alterar algum número, este teste falha.
 */
class RequirementsRegressionTest {

    private static final Path EXAMPLES = Path.of("..", "exemplos");
    private static final ObjectMapper JSON = new ObjectMapper();

    @BeforeAll
    static void requiresZ3AndExamples() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
        assumeTrue(Files.isDirectory(EXAMPLES), "pasta exemplos não encontrada");
    }

    private static JsonNode run(Path dir, String name, String... options) throws IOException {
        Path out = dir.resolve(name + "-" + options.length + ".json");
        List<String> args = new ArrayList<>(List.of(options));
        args.addAll(List.of("--json", EXAMPLES.resolve(name + "-decisoes.json").toString(),
                "--format", "json", "-o", out.toString()));
        int code = Main.run(args.toArray(String[]::new));
        assertEquals(true, code == Main.OK || code == Main.UNCOVERED, "código de saída " + code);
        return JSON.readTree(out.toFile());
    }

    private static int sum(JsonNode report, java.util.function.ToIntFunction<JsonNode> f) {
        int total = 0;
        for (JsonNode decision : report.get("decisions")) {
            total += f.applyAsInt(decision);
        }
        return total;
    }

    private static int suiteSize(JsonNode report) {
        return sum(report, d -> d.get("minimalSuite").size());
    }

    private static int mutation(JsonNode report, String field) {
        return sum(report, d -> {
            int t = 0;
            for (JsonNode fault : d.get("mutation").get("faults")) {
                t += fault.get(field).asInt();
            }
            return t;
        });
    }

    @ParameterizedTest(name = "{0}")
    @CsvSource({
        // sistema, requisitos, completos, condições, sem par, combinações, impossíveis, testes, mutantes, equivalentes, pegos, conflitos
        "vm,   5,  5, 21, 0, 152, 4, 26, 152,  0, 152, 0",
        "tis, 17, 14, 69, 6, 268, 4, 80, 450, 21, 428, 3",
        "npp, 11, 11, 29, 0,  76, 1, 40, 146,  0, 146, 1",
    })
    void resultsOfEachSystem(String system, int requirements, int complete, int conditions, int uncovered,
            int rows, int infeasible, int tests, int mutants, int equivalent, int killed, int conflicts,
            @TempDir Path dir) throws IOException {
        JsonNode greedy = run(dir, system, "analyze", "--z3", "--mutation");

        assertEquals(requirements, greedy.get("decisions").size(), "requisitos");
        assertEquals(complete, sum(greedy, d -> d.get("complete").asBoolean() ? 1 : 0), "completos");
        assertEquals(conditions, sum(greedy, d -> d.get("conditions").size()), "condições");
        assertEquals(uncovered, sum(greedy, d -> d.get("uncoveredConditions").size()), "condições sem par");
        assertEquals(rows, sum(greedy, d -> d.get("truthTableRows").asInt()), "combinações");
        assertEquals(infeasible, sum(greedy, d -> {
            int n = 0;
            for (JsonNode row : d.get("truthTable")) {
                n += row.get("feasible").asBoolean() ? 0 : 1;
            }
            return n;
        }), "combinações impossíveis");
        assertEquals(tests, suiteSize(greedy), "testes");
        assertEquals(mutants, mutation(greedy, "total"), "mutantes");
        assertEquals(equivalent, mutation(greedy, "equivalent"), "mutantes equivalentes");
        assertEquals(killed, mutation(greedy, "killed"), "mutantes pegos");

        // nos completos, a suíte tem condições + 1 testes
        for (JsonNode d : greedy.get("decisions")) {
            if (d.get("complete").asBoolean()) {
                assertEquals(d.get("conditions").size() + 1, d.get("minimalSuite").size(), d.get("requirement").asText());
            }
        }

        // a busca exata e a causa única chegam ao mesmo número de testes
        assertEquals(tests, suiteSize(run(dir, system, "analyze", "--z3", "--exact")), "testes com a busca exata");
        assertEquals(tests, suiteSize(run(dir, system, "analyze", "--z3", "--unique-cause", "--exact", "--mutation")),
                "testes em causa única");

        JsonNode verify = run(dir, system, "verify");
        assertEquals(conflicts, verify.get("conflicts").size(), "conflitos entre requisitos");
    }
}
