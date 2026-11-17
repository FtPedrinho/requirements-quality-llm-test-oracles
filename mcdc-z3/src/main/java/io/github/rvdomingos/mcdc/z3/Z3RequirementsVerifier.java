package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.model.Action;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/**
 * Verificação entre requisitos com o Z3. Aponta conflitos: duas guardas que valem no mesmo passo e
 * escrevem valores diferentes na mesma variável. Com um contexto, aponta lacunas: situações em que
 * nenhuma guarda vale.
 */
public final class Z3RequirementsVerifier {

    private final String command;

    public Z3RequirementsVerifier() {
        this("z3");
    }

    public Z3RequirementsVerifier(String command) {
        this.command = command;
    }

    /** Duas decisões escrevem valores diferentes na mesma variável. */
    public record Conflict(String variable, String firstValue, String secondValue) {
    }

    /**
     * Duas guardas que podem valer juntas, entre decisões que escrevem alguma variável em comum.
     *
     * @param shared    variáveis escritas pelas duas
     * @param conflicts variáveis com valores diferentes; vazio quando a sobreposição é compatível
     * @param witness   valores que fazem as duas guardas valerem; vazio se o Z3 não decidiu
     */
    public record Overlap(Decision first, Decision second, List<String> shared, List<Conflict> conflicts,
            Map<String, String> witness) {

        public boolean isConflict() {
            return !conflicts.isEmpty();
        }
    }

    /**
     * Resultado da verificação.
     *
     * @param pairsChecked pares de decisões comparados (os que escrevem alguma variável em comum)
     * @param context      contexto das lacunas; null quando não informado
     * @param gap          valores em que nenhuma guarda vale sob o contexto; null sem lacuna ou sem contexto
     */
    public record Result(int decisions, int pairsChecked, List<Overlap> overlaps, Expr context, Map<String, String> gap) {

        public List<Overlap> conflicts() {
            return overlaps.stream().filter(Overlap::isConflict).toList();
        }

        public List<Overlap> compatible() {
            return overlaps.stream().filter(o -> !o.isConflict()).toList();
        }

        public boolean gapChecked() {
            return context != null;
        }

        /** Algum conflito ou lacuna. */
        public boolean hasProblems() {
            return !conflicts().isEmpty() || gap != null;
        }
    }

    /** @param context contexto para as lacunas; null para conferir só as sobreposições */
    public Result verify(DecisionSet set, Expr context) {
        List<Decision> decisions = set.decisions();
        if (decisions.isEmpty()) {
            return new Result(0, 0, List.of(), context, null);
        }
        List<List<Action>> actions = decisions.stream()
                .map(d -> d.actions().stream().map(Action::parse).flatMap(Optional::stream).toList())
                .toList();

        // uma codificação para o conjunto todo: as variáveis e os tipos são os mesmos em todas as consultas
        Expr all = decisions.get(0).expression();
        for (int i = 1; i < decisions.size(); i++) {
            all = new Or(all, decisions.get(i).expression());
        }
        SmtEncoding encoding = new SmtEncoding(context == null ? all : new And(context, all), set.inputs());

        record Candidate(int first, int second, List<String> shared) {
        }
        List<Candidate> candidates = new ArrayList<>();
        List<String> queries = new ArrayList<>();
        for (int i = 0; i < decisions.size(); i++) {
            for (int j = i + 1; j < decisions.size(); j++) {
                List<String> shared = sharedVariables(actions.get(i), actions.get(j));
                if (!shared.isEmpty()) {
                    candidates.add(new Candidate(i, j, shared));
                    queries.add("(assert (and " + encoding.formula(decisions.get(i).expression(), "") + " "
                            + encoding.formula(decisions.get(j).expression(), "") + "))\n");
                }
            }
        }
        String gapQuery = context == null ? null
                : "(assert (and " + encoding.formula(context, "") + " "
                        + encoding.formula(new Not(all), "") + "))\n";
        if (gapQuery != null) {
            queries.add(gapQuery);
        }

        List<Optional<Map<String, String>>> answers = queries.isEmpty()
                ? List.of()
                : Z3FeasibilityChecker.solveAll(command, encoding, queries);

        List<Overlap> overlaps = new ArrayList<>();
        for (int q = 0; q < candidates.size(); q++) {
            Optional<Map<String, String>> answer = answers.get(q);
            if (answer.isEmpty()) {
                continue; // as duas guardas nunca valem juntas
            }
            Candidate c = candidates.get(q);
            List<Conflict> conflicts = new ArrayList<>();
            for (String variable : c.shared()) {
                Action a = first(actions.get(c.first()), variable);
                Action b = first(actions.get(c.second()), variable);
                if (a.contradicts(b)) {
                    conflicts.add(new Conflict(variable, a.value(), b.value()));
                }
            }
            Set<String> used = variablesOf(decisions.get(c.first()).expression());
            used.addAll(variablesOf(decisions.get(c.second()).expression()));
            overlaps.add(new Overlap(decisions.get(c.first()), decisions.get(c.second()), c.shared(),
                    List.copyOf(conflicts), only(answer.get(), used)));
        }
        Map<String, String> gap = gapQuery == null ? null : answers.get(answers.size() - 1).orElse(null);
        return new Result(decisions.size(), candidates.size(), List.copyOf(overlaps), context, gap);
    }

    /** Variáveis citadas numa expressão, dos dois lados das comparações. */
    private static Set<String> variablesOf(Expr expr) {
        Set<String> names = new LinkedHashSet<>();
        switch (expr) {
            case Cond c -> {
                if (c.predicate() == null) {
                    names.add(c.id());
                } else {
                    names.add(c.predicate().variable());
                    names.add(c.predicate().value());
                }
            }
            case Not(var operand) -> names.addAll(variablesOf(operand));
            case And(var left, var right) -> {
                names.addAll(variablesOf(left));
                names.addAll(variablesOf(right));
            }
            case Or(var left, var right) -> {
                names.addAll(variablesOf(left));
                names.addAll(variablesOf(right));
            }
        }
        return names;
    }

    /** Só os valores das variáveis que as duas guardas citam: o resto do exemplo é indiferente. */
    private static Map<String, String> only(Map<String, String> witness, Set<String> names) {
        Map<String, String> kept = new LinkedHashMap<>();
        witness.forEach((name, value) -> {
            if (names.contains(name)) {
                kept.put(name, value);
            }
        });
        return kept;
    }

    private static List<String> sharedVariables(List<Action> a, List<Action> b) {
        Set<String> written = new LinkedHashSet<>();
        a.forEach(action -> written.add(action.variable()));
        Set<String> shared = new LinkedHashSet<>();
        b.forEach(action -> {
            if (written.contains(action.variable())) {
                shared.add(action.variable());
            }
        });
        return List.copyOf(shared);
    }

    private static Action first(List<Action> actions, String variable) {
        return actions.stream().filter(a -> a.variable().equals(variable)).findFirst().orElseThrow();
    }
}
