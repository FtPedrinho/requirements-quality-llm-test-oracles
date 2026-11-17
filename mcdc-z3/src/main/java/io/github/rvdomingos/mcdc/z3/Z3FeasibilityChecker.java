package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.FeasibilityChecker;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Viabilidade das linhas com o Z3: "unsat" marca a linha como impossível e "sat" traz os valores
 * concretos. Faz duas chamadas por decisão: uma decide todas as linhas, outra pede os valores das possíveis.
 */
public final class Z3FeasibilityChecker implements FeasibilityChecker {

    /** Cada linha é uma consulta; acima disso (12 entradas) o tempo deixa de ser razoável. */
    public static final int MAX_ROWS = 4096;

    private final List<InputVariable> declared;
    private final String command;

    /** @param declared variáveis com tipo declarado; as outras têm o tipo inferido */
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
        return solveAll(command, encoding, rows.stream().map(row -> assertRow(encoding, row)).toList());
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
        List<Optional<Map<String, String>>> answers = solveAll(command, encoding, candidates.stream()
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

    /**
     * Cada consulta numa pilha própria (push/pop) sobre as mesmas declarações. Para cada uma, na mesma
     * ordem: vazio se impossível, os valores se possível, mapa vazio se o Z3 não decidiu.
     */
    static List<Optional<Map<String, String>>> solveAll(String command, SmtEncoding encoding, List<String> queries) {
        if (queries.isEmpty()) {
            return List.of();
        }
        // 1ª chamada: sat / unsat / unknown de cada consulta
        var check = new StringBuilder(encoding.declarations());
        for (String query : queries) {
            check.append("(push 1)\n").append(query).append("(check-sat)\n(pop 1)\n");
        }
        List<String> answers = Z3Process.atoms(Z3Process.run(command, check.toString()));
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
        List<List<Object>> values = answers.contains("sat") ? Z3Process.valueLists(Z3Process.run(command, models.toString())) : List.of();

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
    static Map<String, String> assignment(SmtEncoding encoding, List<Object> pairs) {
        Map<String, String> assignment = new LinkedHashMap<>();
        for (Object pair : pairs) {
            List<Object> p = (List<Object>) pair;
            String symbol = (String) p.get(0);
            String name = symbol.substring(1, symbol.length() - 1);
            assignment.put(name, encoding.decode(name, p.get(1)));
        }
        return Collections.unmodifiableMap(assignment);
    }

    /** Se o executável responde; usado pelos testes para pular quando o Z3 não está instalado. */
    public static boolean isAvailable(String command) {
        return Z3Process.isAvailable(command);
    }
}
