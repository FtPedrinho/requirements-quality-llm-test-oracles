package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.TestCase;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** O que os relatórios dizem bate com o que foi calculado: nenhum relatório afirma algo que não é verdade. */
class ReportsContentTest {

    private static final ObjectMapper JSON = new ObjectMapper();

    private static String run(Path dir, String... args) throws IOException {
        Path out = dir.resolve("saida-" + System.nanoTime());
        String[] all = java.util.Arrays.copyOf(args, args.length + 2);
        all[args.length] = "-o";
        all[args.length + 1] = out.toString();
        int code = Main.run(all);
        assertTrue(code == Main.OK || code == Main.UNCOVERED, "código de saída " + code);
        return Files.readString(out);
    }

    private static Path tests(Path dir) throws IOException {
        Path csv = dir.resolve("testes.csv");
        Files.writeString(csv, "test,input,value,expected\nT1,A,T,T\nT1,B,T,T\nT3,A,T,F\nT3,B,F,F\n");
        return csv;
    }

    // ---------- modo avaliação ----------

    @Test
    void checkJsonMatchesTheEvaluation(@TempDir Path dir) throws IOException {
        JsonNode report = JSON.readTree(run(dir, "check", "A and B", "--tests", tests(dir).toString(), "--format", "json"));
        JsonNode d = report.get("decisions").get(0);

        assertEquals("check", report.get("mode").asText());
        assertFalse(report.get("complete").asBoolean());
        assertEquals(1, d.get("conditionsDemonstrated").asInt());
        assertEquals(2, d.get("conditionsTotal").asInt());
        assertEquals(3, d.get("outcomesCovered").asInt());
        assertEquals(4, d.get("outcomesTotal").asInt());
        assertEquals(75.0, d.get("outcomePercentage").asDouble());
        assertEquals("V2", d.get("tests").get(1).get("vector").asText());

        JsonNode a = d.get("conditions").get(0);
        assertFalse(a.get("demonstrated").asBoolean());
        assertEquals("V3", a.get("addVectors").get(0).get("vector").asText());
        assertFalse(a.get("addVectors").get(0).get("values").get("A").asBoolean());
        assertFalse(a.get("addVectors").get(0).get("outcome").asBoolean());

        JsonNode b = d.get("conditions").get(1);
        assertTrue(b.get("demonstrated").asBoolean());
        assertEquals("T1", b.get("whenTrue").get(0).asText());
        assertEquals("T3", b.get("whenFalse").get(0).asText());
        assertEquals(0, d.get("problems").size());
    }

    @Test
    void checkTextSaysWhatIsMissing(@TempDir Path dir) throws IOException {
        String text = run(dir, "check", "A and B", "--tests", tests(dir).toString());
        assertTrue(text.contains("A: falta; acrescente V3 (FT -> F)"), text);
        assertTrue(text.contains("B: demonstrada por T1 (T) e T3 (F)"), text);
        assertTrue(text.contains("3 de 4 (75,0%)"), text);
        assertTrue(text.contains("incompleta, 1 de 2 condições demonstradas"), text);
    }

    // ---------- verificação entre requisitos ----------

    @Test
    void verifyTextShowsTheConflictAndTheGap(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        Path decisions = dir.resolve("decisoes.json");
        Files.writeString(decisions, """
                {"system": "s", "decisions": [
                  {"id": "s#1", "requirement": "REQ1", "guard": "mode = choice /\\\\ timer <= 30", "actions": ["mode := weak"]},
                  {"id": "s#2", "requirement": "REQ2", "guard": "mode = choice /\\\\ timer >= 30", "actions": ["mode := strong"]}
                ]}
                """);
        String text = run(dir, "verify", "--json", decisions.toString(), "--context", "mode = choice");
        assertTrue(text.contains("Conflitos: 1"), text);
        assertTrue(text.contains("REQ1 × REQ2"), text);
        assertTrue(text.contains("mode: weak (REQ1) × strong (REQ2)"), text);
        assertTrue(text.contains("exemplo: mode = choice, timer = 30"), text);
        assertTrue(text.contains("Lacunas: nenhuma"), text);

        Files.writeString(decisions, Files.readString(decisions).replace("timer >= 30", "timer > 40"));
        String gap = run(dir, "verify", "--json", decisions.toString(), "--context", "mode = choice");
        assertTrue(gap.contains("Conflitos: nenhum"), gap);
        assertTrue(gap.contains("Lacunas: encontrada"), gap);
        assertTrue(gap.contains("timer = "), gap);
    }

    // ---------- análise ----------

    @Test
    void analysisTextShowsImpossibleRowsBoundaryAndMutation(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        String text = run(dir, "analyze", "speed > 100 or (speed > 50 and rain)", "--z3", "--boundary", "--mutation");
        assertEquals(2, text.lines().filter(l -> l.endsWith("(impossível)")).count(), text);
        assertTrue(text.contains("Suíte mínima (4 testes)"), text);
        assertTrue(text.contains("Testes de fronteira (6)"), text);
        assertTrue(text.contains("Validação por mutação: 100,0%"), text);
        assertTrue(text.contains("Cobertura MC/DC: completa"), text);
        assertTrue(text.contains("Variante:  mascaramento"), text);
        assertTrue(text.contains("speed > 100: (V2, V6), (V2, V7), (V2, V8)"), text);
        assertTrue(text.contains("speed > 50: (V5, V7)"), text);
        assertTrue(text.contains("rain: V5 (T) e V6 (F), só ela muda"), text);
        assertTrue(text.contains("troca de operador (ORF): 2 de 2"), text);
        assertTrue(text.contains("troca de variável (VRF): 6 de 6"), text);
    }

    @Test
    void jsonDescribesEveryInputAndTheMutationScore(@TempDir Path dir) throws IOException {
        JsonNode d = JSON.readTree(run(dir, "analyze", "not (x > 1 and (y < 2 or mode = idle)) or A",
                "--mutation", "--format", "json")).get("decisions").get(0);
        Map<String, String> inputs = new LinkedHashMap<>();
        for (JsonNode input : d.get("inputs")) {
            inputs.put(input.get("name").asText(), input.has("variable")
                    ? input.get("variable").asText() + "|" + input.get("operator").asText() + "|" + input.get("value").asText()
                    : "-");
        }
        assertEquals(Map.of("x > 1", "x|>|1", "y < 2", "y|<|2", "mode = idle", "mode|=|idle", "A", "-"), inputs);
        assertEquals(16, d.get("truthTable").size());

        // A and (B or C): 17 mutantes, só o deslocamento de parênteses escapa -> 16 de 17 = 94,1%
        JsonNode m = JSON.readTree(run(dir, "analyze", "A and (B or C)", "--mutation", "--format", "json"))
                .get("decisions").get(0).get("mutation");
        assertEquals(94.1, m.get("score").asDouble());
        assertEquals(1, m.get("survivors").size());
        assertEquals(1, m.get("faults").get("ASF").get("total").asInt());
        assertEquals(0, m.get("faults").get("ASF").get("killed").asInt());
    }

    /**
     * Os valores concretos de cada teste (suíte e fronteiras) realizam a combinação declarada, e o resultado
     * esperado é o que a guarda dá para esses valores. Conferido no exemplo e nos requisitos dos três sistemas.
     */
    @Test
    void concreteValuesRealizeEveryTest(@TempDir Path dir) throws IOException {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado");
        String guard = "speed > 100 or (speed > 50 and rain)";
        int rows = checkCsv(run(dir, "analyze", guard, "--z3", "--boundary", "--format", "csv"), Map.of("REQ", guard));
        assertEquals(30, rows);

        Path examples = Path.of("..", "exemplos");
        assumeTrue(Files.isDirectory(examples), "pasta exemplos não encontrada");
        for (String system : List.of("vm", "tis", "npp")) {
            String source = examples.resolve(system + "-decisoes.json").toString();
            Map<String, String> guards = new HashMap<>();
            for (JsonNode d : JSON.readTree(run(dir, "analyze", "--json", source, "--format", "json")).get("decisions")) {
                guards.put(d.get("id").asText(), d.get("guard").asText());
            }
            assertTrue(checkCsv(run(dir, "analyze", "--json", source, "--z3", "--boundary", "--format", "csv"), guards) > 0);
        }
    }

    /** Confere cada linha do CSV e devolve quantas foram conferidas. */
    private static int checkCsv(String csv, Map<String, String> guards) {
        List<String> lines = csv.lines().toList();
        assertEquals("decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values", lines.get(0));
        int checked = 0;
        for (String line : lines.subList(1, lines.size())) {
            String[] cells = line.split(",", -1);
            String where = line;
            Expr expr = ExpressionParser.parse(guards.get(cells[0]));
            Map<String, Cond> conds = new LinkedHashMap<>();
            collect(expr, conds);
            Map<String, String> concrete = new HashMap<>();
            for (String part : cells[7].split("; ")) {
                String[] kv = part.split(" = ", 2);
                concrete.put(kv[0], kv[1]);
            }

            Map<String, Boolean> values = new HashMap<>();
            conds.forEach((id, c) -> values.put(id, c.predicate() != null
                    ? c.predicate().holds(concrete)
                    : TestCase.parseBoolean(concrete.get(id), where)));
            assertEquals(TestCase.parseBoolean(cells[4], where), values.get(cells[3]), "valor da entrada em " + where);
            assertEquals(TestCase.parseBoolean(cells[5], where), expr.eval(values), "resultado esperado em " + where);
            checked++;
        }
        return checked;
    }

    private static void collect(Expr expr, Map<String, Cond> conds) {
        switch (expr) {
            case Cond c -> conds.putIfAbsent(c.id(), c);
            case And(var l, var r) -> {
                collect(l, conds);
                collect(r, conds);
            }
            case Or(var l, var r) -> {
                collect(l, conds);
                collect(r, conds);
            }
            case Not(var o) -> collect(o, conds);
        }
    }
}
