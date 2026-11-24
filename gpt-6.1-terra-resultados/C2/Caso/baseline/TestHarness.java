package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class TestHarness {
    private static final ObjectMapper JSON = new ObjectMapper();

    public static void main(String[] args) throws IOException {
        Path caseFile = Path.of(args[0]);
        Path fixtureRoot = Path.of(args[1]);
        Path evidence = Path.of(args[2]);
        Path resultFile = Path.of(args[3]);
        boolean conformOnly = args[4].equals("conformes");
        Files.createDirectory(evidence);
        JsonNode cases = JSON.readTree(Files.readString(caseFile, StandardCharsets.UTF_8));
        List<Map<String, Object>> results = new ArrayList<>();
        int failures = 0;
        int errors = 0;
        for (JsonNode c : cases) {
            String classification = c.path("classificacao").asText();
            if (conformOnly && !classification.equals("CONFORME À DOCUMENTAÇÃO")) continue;
            Map<String, Object> result = execute(c, fixtureRoot, evidence);
            results.add(result);
            String status = (String) result.get("status");
            if (status.equals("FALHOU")) failures++;
            if (status.equals("ERRO DE EXECUÇÃO")) errors++;
            System.out.printf("%s\t%s%n", c.path("id").asText(), status);
        }
        Files.writeString(resultFile, JSON.writerWithDefaultPrettyPrinter().writeValueAsString(results) + "\n",
            StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
        if (errors > 0) System.exit(2);
        if (failures > 0) System.exit(1);
    }

    private static Map<String, Object> execute(JsonNode c, Path fixtureRoot, Path evidence) throws IOException {
        String id = c.path("id").asText();
        String type = c.path("tipo").asText();
        boolean diagnostic = type.equals("diagnostico");
        long start = System.nanoTime();
        Map<String, Object> record = new LinkedHashMap<>();
        record.put("id", id);
        record.put("tipo", type);
        record.put("classificacao", c.path("classificacao").asText());
        record.put("entrada", type.equals("truth") ? c.path("expressao").asText() + " " + c.path("entradas") : c.path("argumentos"));
        record.put("esperado", c.path("esperado"));
        record.put("evidencia_z3", c.path("evidencia_z3").asText());
        String status;
        Object observed = null;
        String error = "";
        try {
            if (type.equals("truth")) {
                TruthTable table = TruthTable.of(ExpressionParser.parse(c.path("expressao").asText()));
                Map<String, Boolean> values = new LinkedHashMap<>();
                c.path("entradas").fields().forEachRemaining(e -> values.put(e.getKey(), e.getValue().asBoolean()));
                List<TestVector> rows = table.rows().stream().filter(row -> row.values().equals(values)).toList();
                if (rows.size() != 1) {
                    observed = "Linhas correspondentes: " + rows.size();
                    status = "FALHOU";
                } else {
                    observed = rows.get(0).outcome();
                    status = ((Boolean) observed) == c.path("esperado").asBoolean() ? "PASSOU" : "FALHOU";
                }
            } else if (type.equals("cli") || diagnostic) {
                List<String> call = new ArrayList<>();
                for (JsonNode arg : c.path("argumentos")) {
                    String value = arg.asText();
                    call.add(value.startsWith("@") ? fixture(fixtureRoot, value) : value);
                }
                Captured captured = runCli(call.toArray(String[]::new));
                Files.writeString(evidence.resolve(id + ".stdout.txt"), captured.stdout(), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
                Files.writeString(evidence.resolve(id + ".stderr.txt"), captured.stderr(), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
                record.put("stdout", evidence.resolve(id + ".stdout.txt").toString());
                record.put("stderr", evidence.resolve(id + ".stderr.txt").toString());
                observed = "exit=" + captured.exit();
                if (technicalFailure(captured)) {
                    status = "ERRO DE EXECUÇÃO";
                    error = captured.stderr();
                } else if (diagnostic) {
                    status = "SEM JULGAMENTO";
                } else {
                    String validation = c.path("validacao").asText();
                    int expectedExit = validation.equals("exact_size") || validation.equals("boundary") ? 0 : c.path("esperado").asInt();
                    boolean matches = captured.exit() == expectedExit;
                    if (matches && validation.equals("nonempty")) {
                        boolean nonempty = !captured.stdout().isBlank();
                        observed += "; saída não vazia=" + nonempty;
                        matches = nonempty;
                    } else if (matches && validation.equals("json")) {
                        boolean valid = parseJson(captured.stdout()) != null;
                        observed += "; JSON válido=" + valid;
                        matches = valid;
                    } else if (matches && validation.equals("exact_size")) {
                        JsonNode root = parseJson(captured.stdout());
                        JsonNode suite = root == null ? null : root.path("decisions").path(0).path("minimalSuite");
                        int size = suite != null && suite.isArray() ? suite.size() : -1;
                        observed += "; tamanho=" + size;
                        matches = size == c.path("esperado").asInt();
                    } else if (matches && validation.equals("boundary")) {
                        JsonNode root = parseJson(captured.stdout());
                        JsonNode tests = root == null ? null : root.path("decisions").path(0).path("boundaryTests");
                        List<String> numbers = new ArrayList<>();
                        if (tests != null && tests.isArray()) {
                            for (JsonNode test : tests) {
                                JsonNode speed = test.path("assignment").path("speed");
                                if (!speed.isMissingNode()) numbers.add(speed.asText());
                            }
                        }
                        observed += "; valores de speed=" + numbers;
                        matches = containsNumber(numbers, 100) && containsNumber(numbers, 101);
                    }
                    status = matches ? "PASSOU" : "FALHOU";
                }
            } else {
                status = "NÃO EXECUTADO — INVÁLIDO";
                error = "Tipo de caso desconhecido: " + type;
            }
        } catch (RuntimeException e) {
            status = "ERRO DE EXECUÇÃO";
            error = e.toString();
        }
        record.put("observado", observed);
        record.put("status", status);
        record.put("erro", error);
        record.put("duracao_ms", (System.nanoTime() - start) / 1_000_000.0);
        return record;
    }

    private static String fixture(Path root, String marker) {
        String name = switch (marker) {
            case "@simples" -> "simples.mcdc";
            case "@complementar" -> "complementar.mcdc";
            case "@csv-vlue" -> "csv-vlue.csv";
            case "@csv-value" -> "csv-value.csv";
            case "@json-literal" -> "json-literal.json";
            default -> throw new IllegalArgumentException("Fixture desconhecida: " + marker);
        };
        return root.resolve(name).toString();
    }

    private record Captured(int exit, String stdout, String stderr) {}

    private static Captured runCli(String[] arguments) {
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayOutputStream err = new ByteArrayOutputStream();
        int exit;
        try (PrintStream capturedOut = new PrintStream(new FilteredOutput(out), true, StandardCharsets.UTF_8);
             PrintStream capturedErr = new PrintStream(err, true, StandardCharsets.UTF_8)) {
            System.setOut(capturedOut);
            System.setErr(capturedErr);
            exit = Main.run(arguments);
        } finally {
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        return new Captured(exit, out.toString(StandardCharsets.UTF_8), err.toString(StandardCharsets.UTF_8));
    }

    private static final class FilteredOutput extends OutputStream {
        private final ByteArrayOutputStream target;
        private final ByteArrayOutputStream line = new ByteArrayOutputStream();

        private FilteredOutput(ByteArrayOutputStream target) {
            this.target = target;
        }

        @Override
        public void write(int value) throws IOException {
            line.write(value);
            if (value == '\n') flushLine();
        }

        @Override
        public void close() throws IOException {
            flushLine();
        }

        private void flushLine() throws IOException {
            String text = line.toString(StandardCharsets.UTF_8);
            if (!text.startsWith("Resultados de condição demonstrados:") && !text.startsWith("Cobertura MC/DC:")) {
                line.writeTo(target);
            }
            line.reset();
        }
    }

    private static boolean technicalFailure(Captured result) {
        String text = result.stderr();
        return text.contains("Z3 não encontrado") || text.contains("Z3 não respondeu")
            || text.contains("Falha ao conversar com o Z3") || text.contains("Interrompido esperando o Z3")
            || text.contains("Erro do Z3:");
    }

    private static JsonNode parseJson(String text) {
        try {
            return JSON.readTree(text);
        } catch (JsonProcessingException e) {
            return null;
        }
    }

    private static boolean containsNumber(List<String> values, int expected) {
        for (String value : values) {
            try {
                if (new BigDecimal(value).compareTo(BigDecimal.valueOf(expected)) == 0) return true;
            } catch (NumberFormatException e) {
                // A representação foi preservada como evidência e não corresponde ao número esperado.
            }
        }
        return false;
    }
}
