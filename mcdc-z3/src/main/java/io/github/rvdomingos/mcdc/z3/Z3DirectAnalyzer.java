package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.Condition;
import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.SuiteMethod;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

/**
 * Modo direto: pede ao Z3 um par de independência por condição, sem montar a tabela verdade, para
 * decisões grandes demais para a verificação linha a linha. Cada consulta fala dos dois testes do par
 * ao mesmo tempo, com duas cópias das variáveis do sistema. Restrições flexíveis fazem o Z3
 * reaproveitar testes já escolhidos, para a suíte ficar pequena.
 */
public final class Z3DirectAnalyzer {

    /** Peso de reaproveitar um teste já escolhido; maior que o de preferir causa única. */
    private static final int REUSE_WEIGHT = 10;

    private final List<InputVariable> declared;
    private final String command;

    public Z3DirectAnalyzer(List<InputVariable> declared) {
        this(declared, "z3");
    }

    public Z3DirectAnalyzer(List<InputVariable> declared, String command) {
        this.declared = List.copyOf(declared);
        this.command = command;
    }

    /** Um par encontrado pelo Z3. */
    private record Found(TestVector whenTrue, TestVector whenFalse) {
    }

    public McdcReport analyze(Expr expression, McdcOptions options) {
        List<String> inputs = expression.inputs();
        if (inputs.size() > TruthTable.MAX_DIRECT_INPUTS) {
            throw new IllegalArgumentException("Decisão com " + inputs.size()
                    + " entradas; o limite do modo direto é " + TruthTable.MAX_DIRECT_INPUTS);
        }
        if (options.constraint() != null) {
            for (String id : options.constraint().inputs()) {
                if (!inputs.contains(id)) {
                    throw new IllegalArgumentException("A restrição usa uma entrada que não está na decisão: " + id);
                }
            }
        }
        SmtEncoding encoding = new SmtEncoding(expression, declared);

        Map<Integer, TestVector> suite = new TreeMap<>();
        Map<String, List<IndependencePair>> pairs = new LinkedHashMap<>();
        Map<String, IndependencePair> chosen = new LinkedHashMap<>();
        List<UncoveredCondition> uncovered = new ArrayList<>();

        for (Condition condition : Condition.of(expression)) {
            Optional<Found> found = search(expression, encoding, inputs, condition, options, suite.values(), true);
            if (found.isPresent()) {
                // um teste igual a outro já escolhido é o mesmo teste: fica com o primeiro
                TestVector t = suite.computeIfAbsent(found.get().whenTrue().index(), k -> found.get().whenTrue());
                TestVector f = suite.computeIfAbsent(found.get().whenFalse().index(), k -> found.get().whenFalse());
                IndependencePair pair = new IndependencePair(condition.label(), t, f);
                pairs.put(condition.label(), List.of(pair));
                chosen.put(condition.label(), pair);
            } else {
                pairs.put(condition.label(), List.of());
                // sem as restrições: se ainda não há par, a condição é redundante; se há, as restrições bloquearam
                Optional<Found> relaxed = search(expression, encoding, inputs, condition, options, List.of(), false);
                uncovered.add(new UncoveredCondition(condition.label(),
                        relaxed.isEmpty() ? UncoveredCondition.Reason.REDUNDANT : UncoveredCondition.Reason.INFEASIBLE,
                        relaxed.map(r -> List.of(new IndependencePair(condition.label(), r.whenTrue(), r.whenFalse())))
                                .orElse(List.of())));
            }
        }

        List<TestVector> tests = List.copyOf(suite.values());
        return new McdcReport(expression, options, TruthTable.partial(expression, tests), pairs, tests, chosen,
                List.copyOf(uncovered), SuiteMethod.DIRECT);
    }

    /** Uma consulta por condição; com {@code feasible}, liga os predicados às variáveis e aplica a restrição. */
    private Optional<Found> search(Expr expr, SmtEncoding encoding, List<String> inputs, Condition condition,
            McdcOptions options, Collection<TestVector> reuse, boolean feasible) {
        int n = inputs.size();
        int c = inputs.indexOf(condition.input());
        var s = new StringBuilder("(set-option :produce-models true)\n");
        if (feasible) {
            s.append(encoding.declarations("t")).append(encoding.declarations("f"));
        }
        for (String k : List.of("t", "f")) {
            for (int i = 0; i < n; i++) {
                s.append("(declare-const ").append(b(k, i)).append(" Bool)\n");
            }
        }
        if (feasible) {
            for (String k : List.of("t", "f")) {
                for (int i = 0; i < n; i++) {
                    s.append("(assert (= ").append(b(k, i)).append(' ')
                            .append(encoding.literal(inputs.get(i), true, k)).append("))\n");
                }
                if (options.constraint() != null) {
                    s.append("(assert ").append(bool(options.constraint(), k, inputs, -1)).append(")\n");
                }
            }
        }

        // a condição verdadeira num teste e falsa no outro
        s.append("(assert ").append(b("t", c)).append(")\n");
        s.append("(assert (not ").append(b("f", c)).append("))\n");
        List<String> sameOthers = new ArrayList<>();
        for (int j = 0; j < n; j++) {
            if (j != c) {
                sameOthers.add("(= " + b("t", j) + " " + b("f", j) + ")");
            }
        }
        if (options.variant() == McdcVariant.UNIQUE_CAUSE) {
            sameOthers.forEach(eq -> s.append("(assert ").append(eq).append(")\n"));
        }

        // saídas diferentes, e a condição decide nos dois testes
        String outT = bool(expr, "t", inputs, -1);
        String outF = bool(expr, "f", inputs, -1);
        s.append("(assert (not (= ").append(outT).append(' ').append(outF).append(")))\n");
        s.append("(assert (not (= ").append(outT).append(' ')
                .append(bool(expr, "t", inputs, condition.leaf())).append(")))\n");
        s.append("(assert (not (= ").append(outF).append(' ')
                .append(bool(expr, "f", inputs, condition.leaf())).append(")))\n");

        // preferências: reaproveitar testes já escolhidos e, no mascaramento, ficar em causa única
        if (!reuse.isEmpty()) {
            for (String k : List.of("t", "f")) {
                List<String> matches = reuse.stream().map(v -> matches(k, v, inputs)).toList();
                s.append("(assert-soft ").append(or(matches)).append(" :weight ").append(REUSE_WEIGHT).append(")\n");
            }
        }
        if (options.variant() == McdcVariant.MASKING && !sameOthers.isEmpty()) {
            s.append("(assert-soft ").append(and(sameOthers)).append(" :weight 1)\n");
        }

        s.append("(check-sat)\n(get-value (");
        for (String k : List.of("t", "f")) {
            for (int i = 0; i < n; i++) {
                s.append(b(k, i)).append(' ');
            }
        }
        s.append("))\n");
        if (feasible) {
            s.append("(get-value (").append(String.join(" ", encoding.symbols("t"))).append("))\n");
            s.append("(get-value (").append(String.join(" ", encoding.symbols("f"))).append("))\n");
        }

        String output = Z3Process.run(command, s.toString());
        List<Object> items = SExpr.parseAll(output);
        Object answer = items.isEmpty() ? "" : items.get(0);
        if ("unsat".equals(answer)) {
            return Optional.empty();
        }
        if (!"sat".equals(answer)) {
            throw new IllegalStateException("O Z3 não decidiu o par de " + condition.label() + ": " + output.strip());
        }
        List<Object> lists = Z3Process.all(output).stream().filter(List.class::isInstance).toList();

        Map<String, Boolean> bits = new LinkedHashMap<>();
        for (Object item : (List<?>) lists.get(0)) {
            List<?> pair = (List<?>) item;
            bits.put(((String) pair.get(0)).replace("|", ""), "true".equals(pair.get(1)));
        }
        TestVector t = vector(expr, inputs, "t", bits, feasible ? values(encoding, lists.get(1)) : Map.of());
        TestVector f = vector(expr, inputs, "f", bits, feasible ? values(encoding, lists.get(2)) : Map.of());
        return Optional.of(new Found(t, f));
    }

    /** Monta o teste a partir dos valores booleanos de uma cópia; o índice segue a tabela (bit 1 = falsa). */
    private static TestVector vector(Expr expr, List<String> inputs, String k, Map<String, Boolean> bits,
            Map<String, String> assignment) {
        int n = inputs.size();
        int index = 0;
        Map<String, Boolean> values = new LinkedHashMap<>();
        for (int i = 0; i < n; i++) {
            boolean value = bits.get(b(k, i).replace("|", ""));
            values.put(inputs.get(i), value);
            if (!value) {
                index |= 1 << (n - 1 - i);
            }
        }
        return new TestVector(index, inputs, expr.eval(values), true, assignment);
    }

    private static Map<String, String> values(SmtEncoding encoding, Object list) {
        Map<String, String> assignment = new LinkedHashMap<>();
        for (Object item : (List<?>) list) {
            List<?> pair = (List<?>) item;
            String variable = SmtEncoding.variableOf((String) pair.get(0));
            assignment.put(variable, encoding.decode(variable, pair.get(1)));
        }
        return assignment;
    }

    /** "O teste k é igual ao teste v": as mesmas entradas verdadeiras e falsas. */
    private static String matches(String k, TestVector v, List<String> inputs) {
        List<String> literals = new ArrayList<>();
        for (int i = 0; i < inputs.size(); i++) {
            literals.add(v.value(inputs.get(i)) ? b(k, i) : "(not " + b(k, i) + ")");
        }
        return and(literals);
    }

    /** A expressão sobre as entradas booleanas de uma cópia, com a folha {@code flipped} invertida (-1: nenhuma). */
    private static String bool(Expr expr, String k, List<String> inputs, int flipped) {
        return bool(expr, k, inputs, flipped, new int[] {0});
    }

    private static String bool(Expr expr, String k, List<String> inputs, int flipped, int[] next) {
        return switch (expr) {
            case Cond cond -> {
                String literal = b(k, inputs.indexOf(cond.id()));
                yield next[0]++ == flipped ? "(not " + literal + ")" : literal;
            }
            case Not(var operand) -> "(not " + bool(operand, k, inputs, flipped, next) + ")";
            case And(var left, var right) -> {
                String l = bool(left, k, inputs, flipped, next);
                yield "(and " + l + " " + bool(right, k, inputs, flipped, next) + ")";
            }
            case Or(var left, var right) -> {
                String l = bool(left, k, inputs, flipped, next);
                yield "(or " + l + " " + bool(right, k, inputs, flipped, next) + ")";
            }
        };
    }

    /** Valor da entrada i no teste k; o @ evita colisão com os nomes das variáveis do sistema. */
    private static String b(String k, int i) {
        return "|@" + k + i + "|";
    }

    private static String and(List<String> terms) {
        return terms.size() == 1 ? terms.get(0) : "(and " + String.join(" ", terms) + ")";
    }

    private static String or(List<String> terms) {
        return terms.size() == 1 ? terms.get(0) : "(or " + String.join(" ", terms) + ")";
    }
}
