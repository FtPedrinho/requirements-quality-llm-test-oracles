package io.github.rvdomingos.mcdc.requirements;

import io.github.rvdomingos.mcdc.core.TestCase;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Testes existentes em CSV, uma linha por (teste, entrada): colunas test, input e value, mais decision e
 * expected_outcome opcionais. Em input vai uma condição (value T/F) ou uma variável (valor concreto).
 */
public final class TestCasesFile {

    /** Valores de um teste como vieram do arquivo. */
    public record RawTest(Map<String, String> values, Boolean expected) {
    }

    /** Testes por decisão; a chave é "" quando o arquivo não tem a coluna decision. */
    public record Contents(Map<String, Map<String, RawTest>> byDecision) {

        public boolean hasDecisionColumn() {
            return !byDecision.containsKey("");
        }
    }

    private TestCasesFile() {
    }

    public static Contents read(Path path) throws IOException {
        return parse(Files.readAllLines(path), path.toString());
    }

    static Contents parse(List<String> lines, String source) {
        List<String> header = null;
        Map<String, Map<String, Map<String, String>>> values = new LinkedHashMap<>();
        Map<String, Map<String, Boolean>> expected = new LinkedHashMap<>();
        int lineNumber = 0;
        for (String line : lines) {
            lineNumber++;
            if (line.isBlank() || line.startsWith("#")) {
                continue;
            }
            List<String> cells = cells(line);
            if (header == null) {
                header = cells;
                for (String required : List.of("test", "input", "value")) {
                    if (!header.contains(required)) {
                        throw new IllegalArgumentException(source + ": falta a coluna \"" + required + "\" no cabeçalho");
                    }
                }
                continue;
            }
            String decision = column(header, cells, "decision");
            decision = decision == null ? "" : decision;
            String test = column(header, cells, "test");
            String input = column(header, cells, "input");
            String value = column(header, cells, "value");
            if (test == null || input == null || value == null) {
                throw new IllegalArgumentException(source + ", linha " + lineNumber + ": faltam test, input ou value");
            }
            values.computeIfAbsent(decision, k -> new LinkedHashMap<>())
                    .computeIfAbsent(test, k -> new LinkedHashMap<>())
                    .put(input, value);
            String outcome = column(header, cells, "expected_outcome");
            if (outcome != null) {
                expected.computeIfAbsent(decision, k -> new LinkedHashMap<>())
                        .put(test, TestCase.parseBoolean(outcome, source + ", linha " + lineNumber));
            }
        }
        if (values.isEmpty()) {
            throw new IllegalArgumentException("Nenhum teste em " + source);
        }

        Map<String, Map<String, RawTest>> byDecision = new LinkedHashMap<>();
        values.forEach((decision, tests) -> {
            Map<String, RawTest> raw = new LinkedHashMap<>();
            tests.forEach((test, v) -> raw.put(test,
                    new RawTest(v, expected.getOrDefault(decision, Map.of()).get(test))));
            byDecision.put(decision, raw);
        });
        return new Contents(byDecision);
    }

    private static String column(List<String> header, List<String> cells, String name) {
        int i = header.indexOf(name);
        if (i < 0 || i >= cells.size() || cells.get(i).isBlank()) {
            return null;
        }
        return cells.get(i).strip();
    }

    /** Divide uma linha CSV respeitando aspas ("a, b" e "" dentro de aspas). */
    static List<String> cells(String line) {
        List<String> cells = new ArrayList<>();
        var cell = new StringBuilder();
        boolean quoted = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (quoted) {
                if (c == '"' && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    cell.append('"');
                    i++;
                } else if (c == '"') {
                    quoted = false;
                } else {
                    cell.append(c);
                }
            } else if (c == '"') {
                quoted = true;
            } else if (c == ',') {
                cells.add(cell.toString());
                cell.setLength(0);
            } else {
                cell.append(c);
            }
        }
        cells.add(cell.toString());
        return cells;
    }
}
