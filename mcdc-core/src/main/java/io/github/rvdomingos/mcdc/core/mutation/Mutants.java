package io.github.rvdomingos.mcdc.core.mutation;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.UnaryOperator;

/** Gera as versões com uma falha de uma expressão (mutantes), uma por posição e tipo de falha. */
public final class Mutants {

    /** Uma versão da expressão com exatamente uma falha. */
    public record Mutant(FaultClass fault, Expr expression) {
    }

    private Mutants() {
    }

    public static List<Mutant> of(Expr expr) {
        List<Expr> nodes = new ArrayList<>();
        preorder(expr, nodes);
        Map<String, Cond> inputs = new LinkedHashMap<>();
        for (Expr node : nodes) {
            if (node instanceof Cond c) {
                inputs.putIfAbsent(c.id(), c);
            }
        }

        Set<Mutant> mutants = new LinkedHashSet<>(); // o mesmo mutante pode surgir de posições diferentes
        for (int i = 0; i < nodes.size(); i++) {
            Expr node = nodes.get(i);
            int at = i;
            switch (node) {
                case And(var left, var right) -> {
                    mutants.add(new Mutant(FaultClass.ORF, replace(expr, at, n -> new Or(left, right))));
                    mutants.add(new Mutant(FaultClass.ENF, replace(expr, at, Not::new)));
                    missingVariable(expr, at, left, right, mutants);
                    // parênteses deslocados: F1 and (F2 or F3) vira (F1 and F2) or F3
                    if (right instanceof Or(var y, var z)) {
                        mutants.add(new Mutant(FaultClass.ASF, replace(expr, at, n -> new Or(new And(left, y), z))));
                    }
                    if (left instanceof Or(var y, var z)) {
                        mutants.add(new Mutant(FaultClass.ASF, replace(expr, at, n -> new Or(y, new And(z, right)))));
                    }
                }
                case Or(var left, var right) -> {
                    mutants.add(new Mutant(FaultClass.ORF, replace(expr, at, n -> new And(left, right))));
                    mutants.add(new Mutant(FaultClass.ENF, replace(expr, at, Not::new)));
                    missingVariable(expr, at, left, right, mutants);
                }
                case Cond c -> {
                    mutants.add(new Mutant(FaultClass.VNF, replace(expr, at, Not::new)));
                    for (Cond other : inputs.values()) {
                        if (!other.id().equals(c.id())) {
                            mutants.add(new Mutant(FaultClass.VRF, replace(expr, at, n -> other)));
                        }
                    }
                }
                case Not n -> {
                    // a negação de uma condição é tratada pelo VNF da própria condição
                }
            }
        }
        return List.copyOf(mutants);
    }

    /** Tira uma folha que é filha direta de and/or: o nó vira o irmão dela. */
    private static void missingVariable(Expr expr, int at, Expr left, Expr right, Set<Mutant> mutants) {
        if (isLeaf(left)) {
            mutants.add(new Mutant(FaultClass.MVF, replace(expr, at, n -> right)));
        }
        if (isLeaf(right)) {
            mutants.add(new Mutant(FaultClass.MVF, replace(expr, at, n -> left)));
        }
    }

    private static boolean isLeaf(Expr expr) {
        return expr instanceof Cond || (expr instanceof Not(var operand) && operand instanceof Cond);
    }

    private static void preorder(Expr expr, List<Expr> nodes) {
        nodes.add(expr);
        switch (expr) {
            case Cond c -> {
            }
            case And(var left, var right) -> {
                preorder(left, nodes);
                preorder(right, nodes);
            }
            case Or(var left, var right) -> {
                preorder(left, nodes);
                preorder(right, nodes);
            }
            case Not(var operand) -> preorder(operand, nodes);
        }
    }

    /** Copia a expressão trocando o nó {@code target} (em pré-ordem) pelo resultado de {@code change}. */
    private static Expr replace(Expr root, int target, UnaryOperator<Expr> change) {
        return replace(root, target, change, new int[] {0});
    }

    private static Expr replace(Expr expr, int target, UnaryOperator<Expr> change, int[] next) {
        if (next[0]++ == target) {
            return change.apply(expr);
        }
        return switch (expr) {
            case Cond c -> c;
            case And(var left, var right) -> new And(replace(left, target, change, next), replace(right, target, change, next));
            case Or(var left, var right) -> new Or(replace(left, target, change, next), replace(right, target, change, next));
            case Not(var operand) -> new Not(replace(operand, target, change, next));
        };
    }
}
