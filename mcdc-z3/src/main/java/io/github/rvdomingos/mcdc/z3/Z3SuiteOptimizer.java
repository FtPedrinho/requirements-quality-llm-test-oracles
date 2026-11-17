package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.SuiteOptimizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/**
 * Suíte exata com o otimizador do Z3. Cada linha que aparece em algum par vira uma variável booleana
 * ("a linha entra na suíte"); cada condição exige que algum par dela tenha as duas linhas dentro;
 * o objetivo é o menor número de linhas. No empate, prefere o conjunto em que mais condições têm um
 * par de causa única.
 */
public final class Z3SuiteOptimizer implements SuiteOptimizer {

    private final String command;

    public Z3SuiteOptimizer() {
        this("z3");
    }

    public Z3SuiteOptimizer(String command) {
        this.command = command;
    }

    @Override
    public Set<Integer> minimumRows(Map<String, List<IndependencePair>> pairsByCondition) {
        Set<Integer> rows = new TreeSet<>();
        pairsByCondition.values().forEach(pairs -> pairs.forEach(p -> {
            rows.add(p.whenTrue().index());
            rows.add(p.whenFalse().index());
        }));
        if (rows.isEmpty()) {
            return Set.of();
        }

        var script = new StringBuilder("(set-option :produce-models true)\n");
        for (int row : rows) {
            script.append("(declare-const ").append(row(row)).append(" Bool)\n");
        }
        // toda condição com par precisa de um par inteiro na suíte
        for (List<IndependencePair> pairs : pairsByCondition.values()) {
            if (!pairs.isEmpty()) {
                script.append("(assert ").append(any(pairs)).append(")\n");
            }
        }
        // 1º objetivo: menos linhas
        script.append("(minimize (+ 0");
        rows.forEach(row -> script.append(" (ite ").append(row(row)).append(" 1 0)"));
        script.append("))\n");
        // 2º objetivo, no empate: condições demonstradas por um par de causa única
        for (List<IndependencePair> pairs : pairsByCondition.values()) {
            List<IndependencePair> unique = pairs.stream().filter(IndependencePair::isUniqueCause).toList();
            if (!unique.isEmpty()) {
                script.append("(assert-soft ").append(any(unique)).append(" :id causa_unica)\n");
            }
        }
        script.append("(check-sat)\n(get-value (");
        rows.forEach(row -> script.append(row(row)).append(' '));
        script.append("))\n");

        List<Object> answer = Z3Process.all(Z3Process.run(command, script.toString()));
        if (answer.isEmpty() || !"sat".equals(answer.get(0))) {
            throw new IllegalStateException("O Z3 não encontrou a suíte exata: " + answer);
        }
        Set<Integer> chosen = new TreeSet<>();
        for (Object item : answer) {
            if (item instanceof List<?> values) {
                for (Object value : values) {
                    List<?> pair = (List<?>) value;
                    if ("true".equals(pair.get(1))) {
                        // o Z3 pode devolver |r12| ou r12
                        String symbol = ((String) pair.get(0)).replace("|", "");
                        chosen.add(Integer.parseInt(symbol.substring(1)));
                    }
                }
            }
        }
        return chosen;
    }

    /** "Algum destes pares está inteiro na suíte." */
    private static String any(List<IndependencePair> pairs) {
        List<String> options = new ArrayList<>();
        for (IndependencePair p : pairs) {
            options.add("(and " + row(p.whenTrue().index()) + " " + row(p.whenFalse().index()) + ")");
        }
        return options.size() == 1 ? options.get(0) : "(or " + String.join(" ", options) + ")";
    }

    private static String row(int index) {
        return "|r" + index + "|";
    }
}
