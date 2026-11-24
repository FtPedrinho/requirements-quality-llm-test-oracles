import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class CasosC4 {
    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            throw new IllegalArgumentException("Uso: CasosC4 casos.json z3.exe resultados.jsonl");
        }
        ObjectMapper json = new ObjectMapper();
        JsonNode cases = json.readTree(Path.of(args[0]).toFile());
        int failures = 0;
        try (BufferedWriter output = Files.newBufferedWriter(Path.of(args[2]), StandardCharsets.UTF_8)) {
            for (JsonNode c : cases) {
                Map<String, Object> result = new LinkedHashMap<>();
                result.put("id", c.required("id").asText());
                result.put("oraculo", "CONFORME À DOCUMENTAÇÃO — AUTOAVALIAÇÃO");
                result.put("entrada", c);
                String expected = c.required("viabilidade_documental").asText();
                result.put("esperado", expected);
                try {
                    Expr expression = ExpressionParser.parse("speed > 100 or (speed > 50 and rain)");
                    List<String> inputs = expression.inputs();
                    Map<String, Boolean> desired = Map.of(
                            "speed > 100", c.required("p").booleanValue(),
                            "speed > 50", c.required("q").booleanValue(),
                            "rain", c.required("rain").booleanValue());
                    if (inputs.size() != desired.size() || !desired.keySet().containsAll(inputs)) {
                        throw new IllegalStateException("Entradas do SUT inesperadas: " + inputs);
                    }
                    int index = 0;
                    for (String input : inputs) {
                        index = (index << 1) | (desired.get(input) ? 0 : 1);
                    }
                    TestVector row = new TestVector(index, inputs, false, true, null);
                    Z3FeasibilityChecker checker = new Z3FeasibilityChecker(
                            List.of(new InputVariable("speed", "int", List.of()),
                                    new InputVariable("rain", "bool", List.of())),
                            args[1]);
                    var observations = checker.solve(expression, List.of(row));
                    if (observations.size() != 1) {
                        throw new IllegalStateException("Quantidade de respostas inesperada: " + observations.size());
                    }
                    String observed = observations.get(0).isPresent() ? "mantida" : "descartada";
                    result.put("observado", observed);
                    if (!expected.equals(observed)) {
                        throw new AssertionError("Esperado " + expected + ", observado " + observed);
                    }
                    result.put("execucao", "PASSOU");
                } catch (AssertionError e) {
                    failures++;
                    result.put("execucao", "FALHOU — DIVERGÊNCIA DOCUMENTAÇÃO/SUT");
                    result.put("erro", e.toString());
                } catch (RuntimeException e) {
                    failures++;
                    result.put("execucao", "ERRO DE EXECUÇÃO");
                    result.put("erro", e.toString());
                    e.printStackTrace(System.err);
                }
                output.write(json.writeValueAsString(result));
                output.newLine();
                output.flush();
            }
        }
        if (failures != 0) {
            System.exit(1);
        }
    }
}
