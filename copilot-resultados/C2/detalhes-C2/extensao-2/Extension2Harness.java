package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class Extension2Harness {
    private static final ObjectMapper JSON = new ObjectMapper();

    public static void main(String[] args) throws IOException {
        JsonNode cases = JSON.readTree(Files.readString(Path.of(args[0]), StandardCharsets.UTF_8));
        List<Map<String, Object>> results = new ArrayList<>();
        int failures = 0;
        int errors = 0;
        for (JsonNode c : cases) {
            long start = System.nanoTime();
            Map<String, Object> result = new LinkedHashMap<>();
            String id = c.path("id").asText();
            result.put("id", id);
            result.put("tipo", c.path("tipo").asText());
            result.put("classificacao", c.path("classificacao").asText());
            result.put("entrada", c.path("entrada"));
            result.put("esperado", c.path("esperado"));
            result.put("evidencia_z3", c.path("evidencia_z3").asText());
            Object observed = null;
            String error = "";
            String status;
            try {
                boolean actual;
                JsonNode input = c.path("entrada");
                switch (c.path("tipo").asText()) {
                    case "conflict" -> {
                        List<Decision> decisions = decisions(input.path("guards"), input.path("actions"));
                        DecisionSet set = new DecisionSet(null, List.of(new InputVariable("A", "bool", List.of())), decisions);
                        actual = !new Z3RequirementsVerifier().verify(set, null).conflicts().isEmpty();
                    }
                    case "gap" -> {
                        List<Decision> decisions = decisions(input.path("guards"), null);
                        DecisionSet set = new DecisionSet(null, List.of(new InputVariable("A", "bool", List.of())), decisions);
                        Expr context = ExpressionParser.parse(input.path("context").asText());
                        actual = new Z3RequirementsVerifier().verify(set, context).gap() != null;
                    }
                    case "feasibility" -> {
                        Expr expr = ExpressionParser.parse(input.path("expression").asText());
                        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of()));
                        String first = ExpressionParser.parse("speed > 100").inputs().get(0);
                        String second = ExpressionParser.parse("speed > 50").inputs().get(0);
                        List<TestVector> selected = table.rows().stream()
                            .filter(row -> row.value(first) == input.path("first").asBoolean()
                                && row.value(second) == input.path("second").asBoolean())
                            .toList();
                        if (selected.size() != 1) throw new IllegalStateException("Quantidade de linhas correspondentes: " + selected.size());
                        actual = selected.get(0).feasible();
                    }
                    default -> throw new IllegalArgumentException("Tipo desconhecido: " + c.path("tipo").asText());
                }
                observed = actual;
                status = actual == c.path("esperado").asBoolean() ? "PASSOU" : "FALHOU";
            } catch (RuntimeException e) {
                status = "ERRO DE EXECUÇÃO";
                error = e.toString();
            }
            result.put("observado", observed);
            result.put("status", status);
            result.put("erro", error);
            result.put("duracao_ms", (System.nanoTime() - start) / 1_000_000.0);
            results.add(result);
            System.out.printf("%s\t%s%n", id, status);
            if (status.equals("FALHOU")) failures++;
            if (status.equals("ERRO DE EXECUÇÃO")) errors++;
        }
        Files.writeString(Path.of(args[1]), JSON.writerWithDefaultPrettyPrinter().writeValueAsString(results) + "\n",
            StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
        if (errors > 0) System.exit(2);
        if (failures > 0) System.exit(1);
    }

    private static List<Decision> decisions(JsonNode guards, JsonNode actions) {
        List<Decision> decisions = new ArrayList<>();
        for (int i = 0; i < guards.size(); i++) {
            String guard = guards.get(i).asText();
            List<String> assigned = actions == null ? List.of() : List.of(actions.get(i).asText());
            decisions.add(new Decision("R" + i, null, guard, ExpressionParser.parse(guard), assigned));
        }
        return decisions;
    }
}
