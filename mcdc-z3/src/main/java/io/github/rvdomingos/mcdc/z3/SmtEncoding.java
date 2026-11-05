package io.github.rvdomingos.mcdc.z3;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.math.BigDecimal;
import java.math.MathContext;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * Tradução de uma expressão para SMT-LIB: declara as variáveis e escreve, para cada entrada,
 * a fórmula que ela afirma. Enumerações viram inteiros de 0 a k-1.
 */
final class SmtEncoding {

    /** Valor extra das enumerações não declaradas: "qualquer outro valor". */
    static final String OTHER = "_outro";

    private static final Pattern INTEGER = Pattern.compile("-?\\d+");
    private static final Pattern NUMBER = Pattern.compile("-?\\d+(\\.\\d+)?");

    enum Sort { BOOL, INT, REAL, ENUM }

    record Variable(String name, Sort sort, List<String> values) {
    }

    /** Um ponto de fronteira: o texto para o relatório e a igualdade em SMT-LIB. */
    record Boundary(String text, String smt) {
    }

    /** Passo usado para "logo acima" e "logo abaixo" de um limite real. */
    static final BigDecimal REAL_STEP = new BigDecimal("0.01");

    private final Map<String, Variable> variables = new LinkedHashMap<>();
    private final Map<String, Cond> inputs = new LinkedHashMap<>();

    SmtEncoding(Expr expr, List<InputVariable> declared) {
        collect(expr);
        Map<String, InputVariable> byName = new LinkedHashMap<>();
        declared.forEach(input -> byName.put(input.name(), input));

        // variáveis comparadas nos predicados
        Map<String, List<String>> literals = new LinkedHashMap<>();
        for (Cond cond : inputs.values()) {
            if (cond.predicate() != null) {
                literals.computeIfAbsent(cond.predicate().variable(), k -> new ArrayList<>());
            }
        }
        for (Cond cond : inputs.values()) {
            Predicate p = cond.predicate();
            if (p != null && !literals.containsKey(p.value()) && !byName.containsKey(p.value())) {
                literals.get(p.variable()).add(p.value());
            }
        }
        literals.forEach((name, values) -> variables.put(name, variable(name, values, byName.get(name))));
        // variáveis declaradas que só aparecem do lado do valor, como "limite" em x < limite
        for (Cond cond : inputs.values()) {
            Predicate p = cond.predicate();
            if (p != null && byName.containsKey(p.value()) && !variables.containsKey(p.value())) {
                variables.put(p.value(), variable(p.value(), List.of(), byName.get(p.value())));
            }
        }

        // condições sem predicado: a própria condição é uma variável booleana
        for (Cond cond : inputs.values()) {
            if (cond.predicate() == null && !variables.containsKey(cond.id())) {
                variables.put(cond.id(), new Variable(cond.id(), Sort.BOOL, List.of()));
            }
        }
        variables.keySet().forEach(SmtEncoding::checkName);
    }

    Iterable<Variable> variables() {
        return variables.values();
    }

    /** Declarações e restrições de domínio das enumerações. */
    String declarations() {
        var sb = new StringBuilder();
        for (Variable v : variables.values()) {
            String sort = switch (v.sort()) {
                case BOOL -> "Bool";
                case INT, ENUM -> "Int";
                case REAL -> "Real";
            };
            sb.append("(declare-const ").append(symbol(v.name())).append(' ').append(sort).append(")\n");
            if (v.sort() == Sort.ENUM) {
                sb.append("(assert (and (>= ").append(symbol(v.name())).append(" 0) (< ")
                        .append(symbol(v.name())).append(' ').append(v.values().size()).append(")))\n");
            }
        }
        return sb.toString();
    }

    /** Fórmula que diz que a entrada tem o valor dado na linha. */
    String literal(String input, boolean value) {
        String formula = formula(inputs.get(input));
        return value ? formula : "(not " + formula + ")";
    }

    /**
     * Pontos de fronteira de uma entrada com o valor que ela tem na linha. Só para comparações de uma
     * variável numérica com uma constante; as outras não têm fronteira.
     */
    List<Boundary> boundaries(String input, boolean value) {
        Predicate p = inputs.get(input).predicate();
        if (p == null || variables.containsKey(p.value())) {
            return List.of();
        }
        Variable v = variables.get(p.variable());
        if (v.sort() != Sort.INT && v.sort() != Sort.REAL) {
            return List.of();
        }
        BigDecimal limit = new BigDecimal(p.value());
        BigDecimal step = v.sort() == Sort.INT ? BigDecimal.ONE : REAL_STEP;
        // com a condição falsa, vale a comparação oposta: não (x > c) é x <= c
        String operator = value ? p.operator() : switch (p.operator()) {
            case "=" -> "!=";
            case "!=" -> "=";
            case "<" -> ">=";
            case "<=" -> ">";
            case ">" -> "<=";
            case ">=" -> "<";
            default -> throw new IllegalArgumentException("Operador desconhecido: " + p.operator());
        };
        List<BigDecimal> points = switch (operator) {
            case ">=", "<=", "=" -> List.of(limit);
            case ">" -> List.of(limit.add(step));
            case "<" -> List.of(limit.subtract(step));
            case "!=" -> List.of(limit.subtract(step), limit.add(step));
            default -> List.of();
        };
        List<Boundary> boundaries = new ArrayList<>();
        for (BigDecimal point : points) {
            String text = v.sort() == Sort.INT ? point.toBigInteger().toString() : point.toPlainString();
            boundaries.add(new Boundary(v.name() + " = " + text,
                    "(= " + symbol(v.name()) + " " + constant(v, text) + ")"));
        }
        return boundaries;
    }

    /** Valor do modelo do Z3 em texto legível: enumerações voltam ao nome, frações viram decimais. */
    String decode(String variable, Object smtValue) {
        Variable v = variables.get(variable);
        String number = number(smtValue);
        if (v.sort() == Sort.ENUM) {
            return v.values().get(Integer.parseInt(number));
        }
        return number;
    }

    private String formula(Cond cond) {
        Predicate p = cond.predicate();
        if (p == null) {
            return symbol(cond.id());
        }
        Variable v = variables.get(p.variable());
        String right = variables.containsKey(p.value()) ? symbol(p.value()) : constant(v, p.value());
        String left = symbol(v.name());
        return switch (p.operator()) {
            case "=" -> "(= " + left + " " + right + ")";
            case "!=" -> "(not (= " + left + " " + right + "))";
            default -> {
                if (v.sort() == Sort.BOOL || v.sort() == Sort.ENUM) {
                    throw new IllegalArgumentException(
                            "Comparação " + p.operator() + " não se aplica a " + v.name() + ", que não é numérica");
                }
                yield "(" + p.operator() + " " + left + " " + right + ")";
            }
        };
    }

    private static String constant(Variable v, String value) {
        return switch (v.sort()) {
            case BOOL -> {
                if (!value.equals("true") && !value.equals("false")) {
                    throw new IllegalArgumentException(v.name() + " é booleana, mas foi comparada com " + value);
                }
                yield value;
            }
            case INT -> {
                if (!INTEGER.matcher(value).matches()) {
                    throw new IllegalArgumentException(v.name() + " é inteira, mas foi comparada com " + value);
                }
                yield value.startsWith("-") ? "(- " + value.substring(1) + ")" : value;
            }
            case REAL -> {
                if (!NUMBER.matcher(value).matches()) {
                    throw new IllegalArgumentException(v.name() + " é real, mas foi comparada com " + value);
                }
                String decimal = value.contains(".") ? value : value + ".0";
                yield decimal.startsWith("-") ? "(- " + decimal.substring(1) + ")" : decimal;
            }
            case ENUM -> {
                int index = v.values().indexOf(value);
                if (index < 0) {
                    throw new IllegalArgumentException(value + " não é um dos valores de " + v.name() + ": " + v.values());
                }
                yield String.valueOf(index);
            }
        };
    }

    /** Tipo declarado no JSON, ou inferido dos valores comparados. */
    private static Variable variable(String name, List<String> literals, InputVariable declared) {
        if (declared != null && declared.type() != null) {
            return switch (declared.type().toLowerCase(Locale.ROOT)) {
                case "bool", "boolean" -> new Variable(name, Sort.BOOL, List.of());
                case "int", "integer" -> new Variable(name, Sort.INT, List.of());
                case "real", "float", "double" -> new Variable(name, Sort.REAL, List.of());
                case "enum" -> new Variable(name, Sort.ENUM, declared.values());
                default -> throw new IllegalArgumentException("Tipo desconhecido para " + name + ": " + declared.type());
            };
        }
        if (!literals.isEmpty() && literals.stream().allMatch(v -> v.equals("true") || v.equals("false"))) {
            return new Variable(name, Sort.BOOL, List.of());
        }
        if (literals.stream().allMatch(v -> INTEGER.matcher(v).matches())) {
            return new Variable(name, Sort.INT, List.of());
        }
        if (literals.stream().allMatch(v -> NUMBER.matcher(v).matches())) {
            return new Variable(name, Sort.REAL, List.of());
        }
        Set<String> values = new LinkedHashSet<>(literals);
        values.add(OTHER);
        return new Variable(name, Sort.ENUM, List.copyOf(values));
    }

    private void collect(Expr expr) {
        switch (expr) {
            case Cond c -> inputs.putIfAbsent(c.id(), c);
            case And(var left, var right) -> {
                collect(left);
                collect(right);
            }
            case Or(var left, var right) -> {
                collect(left);
                collect(right);
            }
            case Not(var operand) -> collect(operand);
        }
    }

    /** Número do modelo: "101", "(- 5)", "2.5" ou "(/ 5.0 2.0)". */
    @SuppressWarnings("unchecked")
    private static String number(Object smtValue) {
        if (smtValue instanceof String atom) {
            return atom.endsWith(".0") ? atom.substring(0, atom.length() - 2) : atom;
        }
        List<Object> list = (List<Object>) smtValue;
        if (list.get(0).equals("-") && list.size() == 2) {
            return "-" + number(list.get(1));
        }
        if (list.get(0).equals("/")) {
            BigDecimal a = new BigDecimal(number(list.get(1)));
            BigDecimal b = new BigDecimal(number(list.get(2)));
            return a.divide(b, MathContext.DECIMAL64).stripTrailingZeros().toPlainString();
        }
        throw new IllegalStateException("Valor do Z3 não reconhecido: " + smtValue);
    }

    static String symbol(String name) {
        return "|" + name + "|";
    }

    private static void checkName(String name) {
        if (name.contains("|") || name.contains("\\")) {
            throw new IllegalArgumentException("Nome de variável não suportado pelo Z3: " + name);
        }
    }
}
