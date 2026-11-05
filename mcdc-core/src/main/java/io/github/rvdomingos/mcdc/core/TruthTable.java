package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Tabela verdade completa de uma expressão, montada sobre as entradas. A linha 0 tem todas as entradas verdadeiras.
 *
 * @param expression expressão analisada
 * @param inputs     entradas, uma coluna cada
 * @param conditions condições: cada ocorrência de uma entrada na expressão
 * @param rows       todas as combinações das entradas
 */
public record TruthTable(Expr expression, List<String> inputs, List<Condition> conditions, List<TestVector> rows) {

    public static final int MAX_INPUTS = 20;

    public static TruthTable of(Expr expr) {
        return of(expr, null, null);
    }

    public static TruthTable of(Expr expr, Expr constraint) {
        return of(expr, constraint, null);
    }

    /**
     * @param constraint  expressão que toda linha possível satisfaz, sobre as mesmas entradas
     *                    da decisão; null quando não há restrição
     * @param feasibility verificação das linhas a partir dos predicados (ex.: Z3); null para não verificar
     */
    public static TruthTable of(Expr expr, Expr constraint, FeasibilityChecker feasibility) {
        List<String> inputs = expr.inputs();
        int n = inputs.size();
        if (n > MAX_INPUTS) {
            throw new IllegalArgumentException(
                    "Decisão com " + n + " entradas; o limite é " + MAX_INPUTS);
        }
        if (constraint != null) {
            for (String id : constraint.inputs()) {
                if (!inputs.contains(id)) {
                    throw new IllegalArgumentException("A restrição usa uma entrada que não está na decisão: " + id);
                }
            }
        }

        Map<String, Integer> bits = new HashMap<>();
        for (int i = 0; i < n; i++) {
            bits.put(inputs.get(i), bit(n, i));
        }
        List<TestVector> rows = new ArrayList<>(1 << n);
        // cada linha é um número de n bits: bit 0 = entrada verdadeira, bit 1 = falsa
        for (int row = 0; row < (1 << n); row++) {
            boolean feasible = constraint == null || eval(constraint, row, bits);
            rows.add(new TestVector(row, inputs, eval(expr, row, bits), feasible, null));
        }
        if (feasibility != null) {
            rows = checkFeasibility(expr, rows, feasibility);
        }
        return new TruthTable(expr, inputs, Condition.of(expr), List.copyOf(rows));
    }

    /** Avalia direto sobre os bits da linha, sem montar mapas. */
    private static boolean eval(Expr expr, int row, Map<String, Integer> bits) {
        return switch (expr) {
            case Cond c -> (row & bits.get(c.id())) == 0;
            case And(var left, var right) -> eval(left, row, bits) && eval(right, row, bits);
            case Or(var left, var right) -> eval(left, row, bits) || eval(right, row, bits);
            case Not(var operand) -> !eval(operand, row, bits);
        };
    }

    /** Pergunta ao verificador só pelas linhas que a restrição manual já aceitou. */
    private static List<TestVector> checkFeasibility(Expr expr, List<TestVector> rows, FeasibilityChecker feasibility) {
        List<TestVector> candidates = rows.stream().filter(TestVector::feasible).toList();
        List<Optional<Map<String, String>>> answers = feasibility.solve(expr, candidates);

        Map<Integer, Optional<Map<String, String>>> byIndex = new HashMap<>();
        for (int i = 0; i < candidates.size(); i++) {
            byIndex.put(candidates.get(i).index(), answers.get(i));
        }
        List<TestVector> checked = new ArrayList<>();
        for (TestVector row : rows) {
            Optional<Map<String, String>> answer = byIndex.getOrDefault(row.index(), Optional.empty());
            checked.add(new TestVector(row.index(), row.inputs(), row.outcome(), answer.isPresent(), answer.orElse(null)));
        }
        return checked;
    }

    /** A mesma tabela com todas as linhas possíveis: serve para saber se uma condição sem par é redundante. */
    public TruthTable withoutConstraints() {
        List<TestVector> all = rows.stream()
                .map(r -> new TestVector(r.index(), r.inputs(), r.outcome(), true, r.assignment()))
                .toList();
        return new TruthTable(expression, inputs, conditions, all);
    }

    /** Máscara do bit da entrada i. A primeira entrada é o bit mais significativo. */
    static int bit(int n, int i) {
        return 1 << (n - 1 - i);
    }

    public String format() {
        var sb = new StringBuilder();
        sb.append(String.format("%-6s", "Vetor"));
        for (String input : inputs) {
            sb.append(column(input, input));
        }
        sb.append("| D\n");
        for (TestVector row : rows) {
            sb.append(String.format("%-6s", row.name()));
            for (String input : inputs) {
                sb.append(column(row.values().get(input) ? "T" : "F", input));
            }
            sb.append("| ").append(row.outcome() ? "T" : "F");
            if (!row.feasible()) {
                sb.append("  (impossível)");
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    /** Alinha o texto na largura da coluna, que acompanha o tamanho do nome da entrada. */
    private static String column(String text, String input) {
        return String.format("%-" + (input.length() + 3) + "s", text);
    }
}
