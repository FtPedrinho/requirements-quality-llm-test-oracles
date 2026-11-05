package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.FeasibilityChecker;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.TimeUnit;

/**
 * Viabilidade das linhas com o Z3: cada linha vira uma consulta em que cada entrada verdadeira entra
 * como o predicado e cada falsa como a negação. "unsat" marca a linha como impossível; "sat" traz os
 * valores concretos. São duas chamadas ao executável por decisão: uma verifica todas as linhas, outra
 * pede os valores das possíveis.
 */
public final class Z3FeasibilityChecker implements FeasibilityChecker {

    private static final long TIMEOUT_SECONDS = 60;

    /** Cada linha é uma consulta; acima disso (12 entradas) o tempo deixa de ser razoável. */
    public static final int MAX_ROWS = 4096;

    private final List<InputVariable> declared;
    private final String command;

    /** @param declared variáveis com tipo declarado (ex.: "inputs" do JSON da NAT2TEST); as outras têm o tipo inferido */
    public Z3FeasibilityChecker(List<InputVariable> declared) {
        this(declared, "z3");
    }

    public Z3FeasibilityChecker(List<InputVariable> declared, String command) {
        this.declared = List.copyOf(declared);
        this.command = command;
    }

    @Override
    public List<Optional<Map<String, String>>> solve(Expr expression, List<TestVector> rows) {
        if (rows.isEmpty()) {
            return List.of();
        }
        if (rows.size() > MAX_ROWS) {
            throw new IllegalArgumentException("O Z3 verifica linha a linha e aceita até " + MAX_ROWS
                    + " linhas (12 entradas); esta decisão tem " + rows.size());
        }
        SmtEncoding encoding = new SmtEncoding(expression, declared);
        return solveAll(encoding, rows.stream().map(row -> assertRow(encoding, row)).toList());
    }

    /**
     * Variantes de fronteira dos testes da suíte: para cada teste e cada comparação numérica, o mesmo
     * teste com a variável no limite, quando as outras condições continuam valendo.
     */
    public List<BoundaryTest> boundaryTests(Expr expression, List<TestVector> suite) {
        SmtEncoding encoding = new SmtEncoding(expression, declared);
        record Candidate(TestVector base, String condition, SmtEncoding.Boundary boundary) {
        }
        List<Candidate> candidates = new ArrayList<>();
        for (TestVector test : suite) {
            for (String input : test.inputs()) {
                for (SmtEncoding.Boundary boundary : encoding.boundaries(input, test.value(input))) {
                    candidates.add(new Candidate(test, input, boundary));
                }
            }
        }
        List<Optional<Map<String, String>>> answers = solveAll(encoding, candidates.stream()
                .map(c -> assertRow(encoding, c.base()) + "(assert " + c.boundary().smt() + ")\n")
                .toList());

        List<BoundaryTest> tests = new ArrayList<>();
        for (int i = 0; i < candidates.size(); i++) {
            Candidate c = candidates.get(i);
            answers.get(i).filter(values -> !values.isEmpty()).ifPresent(values -> tests.add(
                    new BoundaryTest(c.base().name(), c.condition(), c.boundary().text(), values)));
        }
        return tests;
    }

    /** Duas chamadas: check-sat de cada consulta e, só para as possíveis, os valores. */
    private List<Optional<Map<String, String>>> solveAll(SmtEncoding encoding, List<String> queries) {
        if (queries.isEmpty()) {
            return List.of();
        }
        // 1ª chamada: sat / unsat / unknown de cada consulta
        var check = new StringBuilder(encoding.declarations());
        for (String query : queries) {
            check.append("(push 1)\n").append(query).append("(check-sat)\n(pop 1)\n");
        }
        List<String> answers = atoms(run(check.toString()));
        if (answers.size() != queries.size()) {
            throw new IllegalStateException("Resposta inesperada do Z3: " + answers);
        }

        // 2ª chamada: valores das variáveis nas consultas possíveis
        List<String> names = new ArrayList<>();
        encoding.variables().forEach(v -> names.add(v.name()));
        String getValue = "(get-value (" + String.join(" ", names.stream().map(SmtEncoding::symbol).toList()) + "))\n";
        var models = new StringBuilder("(set-option :produce-models true)\n").append(encoding.declarations());
        for (int i = 0; i < queries.size(); i++) {
            if (answers.get(i).equals("sat")) {
                models.append("(push 1)\n").append(queries.get(i))
                        .append("(check-sat)\n").append(getValue).append("(pop 1)\n");
            }
        }
        List<List<Object>> values = answers.contains("sat") ? valueLists(run(models.toString())) : List.of();

        List<Optional<Map<String, String>>> result = new ArrayList<>();
        int next = 0;
        for (String answer : answers) {
            switch (answer) {
                case "unsat" -> result.add(Optional.empty());
                case "sat" -> result.add(Optional.of(assignment(encoding, values.get(next++))));
                // o Z3 não conseguiu decidir: a linha fica como possível, sem valores
                default -> result.add(Optional.of(Map.of()));
            }
        }
        return result;
    }

    private static String assertRow(SmtEncoding encoding, TestVector row) {
        var sb = new StringBuilder("(assert (and");
        row.values().forEach((input, value) -> sb.append(' ').append(encoding.literal(input, value)));
        return sb.append("))\n").toString();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, String> assignment(SmtEncoding encoding, List<Object> pairs) {
        Map<String, String> assignment = new LinkedHashMap<>();
        for (Object pair : pairs) {
            List<Object> p = (List<Object>) pair;
            String symbol = (String) p.get(0);
            String name = symbol.substring(1, symbol.length() - 1);
            assignment.put(name, encoding.decode(name, p.get(1)));
        }
        return Collections.unmodifiableMap(assignment);
    }

    /** Respostas de check-sat; qualquer (error ...) vira exceção. */
    private static List<String> atoms(String output) {
        List<String> atoms = new ArrayList<>();
        for (Object item : SExpr.parseAll(output)) {
            failOnError(item);
            if (item instanceof String atom) {
                atoms.add(atom);
            }
        }
        return atoms;
    }

    /** Listas de get-value, uma por linha possível. */
    @SuppressWarnings("unchecked")
    private static List<List<Object>> valueLists(String output) {
        List<List<Object>> lists = new ArrayList<>();
        for (Object item : SExpr.parseAll(output)) {
            failOnError(item);
            if (item instanceof List<?> list) {
                lists.add((List<Object>) list);
            }
        }
        return lists;
    }

    private static void failOnError(Object item) {
        if (item instanceof List<?> list && !list.isEmpty() && "error".equals(list.get(0))) {
            throw new IllegalStateException("Erro do Z3: " + list.get(1));
        }
    }

    private String run(String script) {
        Process process;
        try {
            process = new ProcessBuilder(command, "-in", "-smt2").redirectErrorStream(true).start();
        } catch (IOException e) {
            throw new IllegalStateException("Z3 não encontrado (" + command + "). Instale com: brew install z3");
        }
        try {
            try (OutputStream in = process.getOutputStream()) {
                in.write(script.getBytes(StandardCharsets.UTF_8));
            }
            String output = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
            if (!process.waitFor(TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
                process.destroyForcibly();
                throw new IllegalStateException("O Z3 não respondeu em " + TIMEOUT_SECONDS + " segundos");
            }
            return output;
        } catch (IOException e) {
            throw new IllegalStateException("Falha ao conversar com o Z3: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Interrompido esperando o Z3");
        }
    }

    /** Se o executável responde; usado pelos testes para pular quando o Z3 não está instalado. */
    public static boolean isAvailable(String command) {
        try {
            Process process = new ProcessBuilder(command, "--version").redirectErrorStream(true).start();
            process.getInputStream().readAllBytes();
            return process.waitFor(10, TimeUnit.SECONDS) && process.exitValue() == 0;
        } catch (IOException e) {
            return false;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
}
