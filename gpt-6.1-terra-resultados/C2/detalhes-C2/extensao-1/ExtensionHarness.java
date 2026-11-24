package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestCase;
import io.github.rvdomingos.mcdc.core.TestSetEvaluation;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ExtensionHarness {
    private static final ObjectMapper JSON = new ObjectMapper();

    public static void main(String[] args) throws IOException {
        JsonNode cases = JSON.readTree(Files.readString(Path.of(args[0]), StandardCharsets.UTF_8));
        Path evidence = Path.of(args[1]);
        Path resultsPath = Path.of(args[2]);
        Files.createDirectory(evidence);
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
            result.put("entrada", c);
            String status;
            String observed = "";
            String error = "";
            try {
                switch (c.path("tipo").asText()) {
                    case "avaliacao" -> {
                        Expr expr = ExpressionParser.parse(c.path("expressao").asText());
                        List<TestCase> tests = new ArrayList<>();
                        for (JsonNode row : c.path("linhas")) {
                            Map<String, String> raw = new LinkedHashMap<>();
                            row.path("entradas").fields().forEachRemaining(e -> raw.put(e.getKey(), e.getValue().asBoolean() ? "T" : "F"));
                            tests.add(TestCase.resolve(expr, row.path("id_oraculo").asText(), raw, row.path("esperado").asBoolean()));
                        }
                        McdcVariant variant = c.path("variante").asText().equals("unique") ? McdcVariant.UNIQUE_CAUSE : McdcVariant.MASKING;
                        TestSetEvaluation evaluation = Mcdc.evaluate(expr, McdcOptions.defaults().withVariant(variant), tests);
                        int matches = 0;
                        for (TestCase test : tests) {
                            TestVector row = evaluation.vectorOfTest().get(test.name());
                            if (row != null && row.outcome() == test.expected()) matches++;
                        }
                        observed = matches + "/" + tests.size() + " decisões correspondem";
                        status = matches == tests.size() ? "PASSOU" : "FALHOU";
                    }
                    case "numeric" -> {
                        Expr expr = ExpressionParser.parse(c.path("expressao").asText());
                        Map<String, String> raw = new LinkedHashMap<>();
                        c.path("entradas").fields().forEachRemaining(e -> raw.put(e.getKey(), e.getValue().asText()));
                        TestCase test = TestCase.resolve(expr, id, raw, null);
                        if (test.values().size() != 1) {
                            observed = "valores resolvidos: " + test.values();
                            status = "ERRO DE EXECUÇÃO";
                            error = "Não foi possível identificar a comparação única";
                        } else {
                            boolean actual = test.values().values().iterator().next();
                            observed = Boolean.toString(actual);
                            status = actual == c.path("esperado").asBoolean() ? "PASSOU" : "FALHOU";
                        }
                    }
                    case "truth_csv" -> {
                        Captured captured = runCli(new String[]{"analyze", c.path("expressao").asText(), "--format", "truth-csv"});
                        Files.writeString(evidence.resolve(id + ".stdout.csv"), captured.out(), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
                        Files.writeString(evidence.resolve(id + ".stderr.txt"), captured.err(), StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
                        result.put("stdout", evidence.resolve(id + ".stdout.csv").toString());
                        result.put("stderr", evidence.resolve(id + ".stderr.txt").toString());
                        if (captured.exit() != 0 && captured.exit() != 2) {
                            observed = "exit=" + captured.exit();
                            status = "FALHOU";
                        } else {
                            CsvCheck check = checkTable(captured.out(), c.path("linhas"));
                            observed = "exit=" + captured.exit() + "; " + check.message();
                            status = check.adapterError() ? "ERRO DE EXECUÇÃO" : check.matches() ? "PASSOU" : "FALHOU";
                            if (check.adapterError()) error = check.message();
                        }
                    }
                    default -> {
                        status = "NÃO EXECUTADO — INVÁLIDO";
                        error = "Tipo desconhecido";
                    }
                }
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
        Files.writeString(resultsPath, JSON.writerWithDefaultPrettyPrinter().writeValueAsString(results) + "\n",
            StandardCharsets.UTF_8, StandardOpenOption.CREATE_NEW);
        if (errors > 0) System.exit(2);
        if (failures > 0) System.exit(1);
    }

    private record Captured(int exit, String out, String err) {}
    private record CsvCheck(boolean matches, boolean adapterError, String message) {}

    private static Captured runCli(String[] args) {
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayOutputStream err = new ByteArrayOutputStream();
        int exit;
        try (PrintStream capturedOut = new PrintStream(out, true, StandardCharsets.UTF_8);
             PrintStream capturedErr = new PrintStream(err, true, StandardCharsets.UTF_8)) {
            System.setOut(capturedOut);
            System.setErr(capturedErr);
            exit = Main.run(args);
        } finally {
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        return new Captured(exit, out.toString(StandardCharsets.UTF_8), err.toString(StandardCharsets.UTF_8));
    }

    private static CsvCheck checkTable(String text, JsonNode expectedRows) {
        List<String> lines = text.lines().filter(line -> !line.isBlank()).toList();
        if (lines.isEmpty()) return new CsvCheck(false, false, "tabela vazia");
        List<String> header = Arrays.asList(lines.get(0).split(",", -1));
        int outcome = header.indexOf("outcome");
        if (outcome < 0) return new CsvCheck(false, true, "adaptador não identificou coluna de decisão");
        int matches = 0;
        for (JsonNode expected : expectedRows) {
            int found = 0;
            for (int i = 1; i < lines.size(); i++) {
                String[] cells = lines.get(i).split(",", -1);
                boolean same = true;
                var fields = expected.path("entradas").fields();
                while (fields.hasNext()) {
                    var field = fields.next();
                    int column = header.indexOf(field.getKey());
                    if (column < 0 || column >= cells.length) return new CsvCheck(false, true, "adaptador não identificou coluna de entrada");
                    if (!cells[column].equals(field.getValue().asBoolean() ? "T" : "F")) same = false;
                }
                if (same) {
                    if (outcome >= cells.length) return new CsvCheck(false, true, "linha não contém a coluna de decisão");
                    found++;
                    if (!cells[outcome].equals(expected.path("esperado").asBoolean() ? "T" : "F")) {
                        return new CsvCheck(false, false, "decisão divergente para " + expected.path("entradas"));
                    }
                }
            }
            if (found != 1) return new CsvCheck(false, false, "vetor aparece " + found + " vezes");
            matches++;
        }
        if (lines.size() - 1 != expectedRows.size()) return new CsvCheck(false, false, "número de linhas divergente");
        return new CsvCheck(true, false, matches + "/" + expectedRows.size() + " vetores correspondem");
    }
}
