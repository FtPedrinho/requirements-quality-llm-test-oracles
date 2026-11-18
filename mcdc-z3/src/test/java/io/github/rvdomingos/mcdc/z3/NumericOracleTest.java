package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.Condition;
import io.github.rvdomingos.mcdc.core.IndependencePair;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.UncoveredCondition;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * Oráculo independente com predicados numéricos e de enumeração, conferindo o motor junto com o Z3. As
 * combinações possíveis são descobertas por busca exaustiva de valores concretos (x e y inteiros de -3 a 9,
 * mode em idle/busy/off), com uma avaliação própria das comparações, sem o Z3 e sem o código do motor.
 * Com constantes de 0 a 6, esse intervalo alcança toda combinação que os inteiros alcançam.
 */
class NumericOracleTest {

    private static final long SEED = 20261118L;
    private static final int EXPRESSIONS = 150;
    private static final List<String> MODES = List.of("idle", "busy", "off");
    private static final List<InputVariable> DECLARED = List.of(
            new InputVariable("x", "int", List.of()),
            new InputVariable("y", "int", List.of()),
            new InputVariable("mode", "enum", MODES));
    private static final List<String> OPERATORS = List.of("=", "!=", "<", "<=", ">", ">=");

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    // ---------- oráculo ----------

    /** Todos os valores concretos do domínio de busca. */
    private static List<Map<String, String>> domain() {
        List<Map<String, String>> all = new ArrayList<>();
        for (int x = -3; x <= 9; x++) {
            for (int y = -3; y <= 9; y++) {
                for (String mode : MODES) {
                    all.add(Map.of("x", String.valueOf(x), "y", String.valueOf(y), "mode", mode));
                }
            }
        }
        return all;
    }

    /** Avaliação própria de uma comparação, sem o código do motor. */
    private static boolean holds(Predicate p, Map<String, String> values) {
        String left = values.get(p.variable());
        String right = values.getOrDefault(p.value(), p.value());
        if (p.variable().equals("mode")) {
            boolean equal = left.equals(right);
            return p.operator().equals("=") == equal;
        }
        int c = Integer.compare(Integer.parseInt(left), Integer.parseInt(right));
        return switch (p.operator()) {
            case "=" -> c == 0;
            case "!=" -> c != 0;
            case "<" -> c < 0;
            case "<=" -> c <= 0;
            case ">" -> c > 0;
            default -> c >= 0;
        };
    }

    private static Map<String, Boolean> row(Map<String, Predicate> atoms, Map<String, String> values) {
        Map<String, Boolean> row = new HashMap<>();
        atoms.forEach((id, p) -> row.put(id, holds(p, values)));
        return row;
    }

    private static Expr withLeaf(Expr expr, int target, boolean constant, int[] next) {
        return switch (expr) {
            case Cond c -> next[0]++ == target ? new Cond(constant ? "__T" : "__F") : c;
            case And(var l, var r) -> new And(withLeaf(l, target, constant, next), withLeaf(r, target, constant, next));
            case Or(var l, var r) -> new Or(withLeaf(l, target, constant, next), withLeaf(r, target, constant, next));
            case Not(var o) -> new Not(withLeaf(o, target, constant, next));
        };
    }

    private static boolean eval(Expr expr, Map<String, Boolean> values) {
        Map<String, Boolean> v = new HashMap<>(values);
        v.put("__T", true);
        v.put("__F", false);
        return expr.eval(v);
    }

    private static boolean decides(Expr expr, int leaf, Map<String, Boolean> values) {
        return eval(withLeaf(expr, leaf, true, new int[] {0}), values)
                != eval(withLeaf(expr, leaf, false, new int[] {0}), values);
    }

    private static boolean validPair(Expr expr, int leaf, String input, Map<String, Boolean> t,
            Map<String, Boolean> f, McdcVariant variant) {
        boolean onlyInput = t.keySet().stream().allMatch(k -> k.equals(input) || t.get(k).equals(f.get(k)));
        return t.get(input) && !f.get(input)
                && eval(expr, t) != eval(expr, f)
                && decides(expr, leaf, t) && decides(expr, leaf, f)
                && (variant == McdcVariant.MASKING || onlyInput);
    }

    private static int countPairs(Expr expr, int leaf, String input, Set<Map<String, Boolean>> rows,
            McdcVariant variant) {
        int count = 0;
        for (Map<String, Boolean> t : rows) {
            for (Map<String, Boolean> f : rows) {
                count += validPair(expr, leaf, input, t, f, variant) ? 1 : 0;
            }
        }
        return count;
    }

    /**
     * Fronteiras esperadas, calculadas sem o Z3: para cada teste e cada comparação com constante, o ponto no
     * limite da comparação que vale no teste (a própria, se verdadeira; a oposta, se falsa), quando algum valor
     * do domínio com a variável nesse ponto mantém a combinação do teste.
     */
    private static Set<String> expectedBoundaries(List<TestVector> suite, Map<String, Predicate> atoms,
            List<Map<String, String>> domain) {
        Set<String> expected = new HashSet<>();
        for (TestVector test : suite) {
            for (Map.Entry<String, Predicate> e : atoms.entrySet()) {
                Predicate p = e.getValue();
                if (p.variable().equals("mode") || !p.value().matches("-?\\d+")) {
                    continue;
                }
                int c = Integer.parseInt(p.value());
                boolean value = test.value(e.getKey());
                String op = value ? p.operator() : switch (p.operator()) {
                    case "=" -> "!=";
                    case "!=" -> "=";
                    case "<" -> ">=";
                    case "<=" -> ">";
                    case ">" -> "<=";
                    default -> "<";
                };
                List<Integer> points = switch (op) {
                    case ">=", "<=", "=" -> List.of(c);
                    case ">" -> List.of(c + 1);
                    case "<" -> List.of(c - 1);
                    default -> List.of(c - 1, c + 1);
                };
                for (int point : points) {
                    String at = String.valueOf(point);
                    boolean realizable = domain.stream().anyMatch(values -> values.get(p.variable()).equals(at)
                            && row(atoms, values).equals(test.values()));
                    if (realizable) {
                        expected.add(test.name() + " | " + e.getKey() + " | " + p.variable() + " = " + point);
                    }
                }
            }
        }
        return expected;
    }

    // ---------- gerador ----------

    private static Predicate atom(Random rnd) {
        int kind = rnd.nextInt(10);
        if (kind < 2) {
            return new Predicate("mode", rnd.nextBoolean() ? "=" : "!=", MODES.get(rnd.nextInt(MODES.size())));
        }
        String variable = rnd.nextBoolean() ? "x" : "y";
        String operator = OPERATORS.get(rnd.nextInt(OPERATORS.size()));
        if (kind == 2) {
            return new Predicate(variable, operator, variable.equals("x") ? "y" : "x");
        }
        return new Predicate(variable, operator, String.valueOf(rnd.nextInt(7)));
    }

    private static Expr random(Random rnd, List<Predicate> pool, int leaves) {
        if (leaves == 1) {
            Expr c = new Cond(pool.get(rnd.nextInt(pool.size())));
            return rnd.nextInt(5) == 0 ? new Not(c) : c;
        }
        int left = 1 + rnd.nextInt(leaves - 1);
        Expr e = rnd.nextBoolean()
                ? new And(random(rnd, pool, left), random(rnd, pool, leaves - left))
                : new Or(random(rnd, pool, left), random(rnd, pool, leaves - left));
        return rnd.nextInt(6) == 0 ? new Not(e) : e;
    }

    private static void collect(Expr expr, Map<String, Predicate> atoms) {
        switch (expr) {
            case Cond c -> atoms.putIfAbsent(c.id(), c.predicate());
            case And(var l, var r) -> {
                collect(l, atoms);
                collect(r, atoms);
            }
            case Or(var l, var r) -> {
                collect(l, atoms);
                collect(r, atoms);
            }
            case Not(var o) -> collect(o, atoms);
        }
    }

    // ---------- propriedades ----------

    @Test
    void engineWithZ3AgreesWithExhaustiveSearch() {
        Random rnd = new Random(SEED);
        List<Map<String, String>> domain = domain();
        Z3FeasibilityChecker checker = new Z3FeasibilityChecker(DECLARED);
        int infeasibleRows = 0;
        int boundaryTests = 0;

        for (int i = 0; i < EXPRESSIONS; i++) {
            List<Predicate> pool = new ArrayList<>();
            for (int k = 0; k < 2 + rnd.nextInt(3); k++) {
                pool.add(atom(rnd));
            }
            Expr expr = random(rnd, pool, 1 + rnd.nextInt(6));
            Map<String, Predicate> atoms = new LinkedHashMap<>();
            collect(expr, atoms);

            // combinações possíveis, pela busca exaustiva
            Set<Map<String, Boolean>> reachable = new HashSet<>();
            domain.forEach(values -> reachable.add(row(atoms, values)));

            for (McdcVariant variant : McdcVariant.values()) {
                String where = expr + " | " + variant;
                McdcReport report = Mcdc.analyze(expr,
                        McdcOptions.defaults().withVariant(variant).withFeasibility(checker));

                // viabilidade de cada linha e valores concretos que a realizam
                for (TestVector row : report.table().rows()) {
                    assertEquals(reachable.contains(row.values()), row.feasible(), "viabilidade de " + row.bits() + " em " + where);
                    if (row.feasible()) {
                        Map<String, String> assignment = new HashMap<>(row.assignment());
                        assignment.putIfAbsent("x", "0");
                        assignment.putIfAbsent("y", "0");
                        assignment.putIfAbsent("mode", "idle");
                        assertTrue(MODES.contains(assignment.get("mode")), "valor fora da enumeração em " + where);
                        assertEquals(row.values(), row(atoms, assignment), "valores do Z3 não realizam " + row.bits() + " em " + where);
                    } else if (variant == McdcVariant.MASKING) {
                        infeasibleRows++;
                    }
                }

                // pares, cobertura e diagnóstico, contra as combinações possíveis
                Set<Map<String, Boolean>> feasible = new HashSet<>(reachable);
                Set<Map<String, Boolean>> all = new HashSet<>();
                report.table().rows().forEach(r -> all.add(r.values()));
                List<String> leaves = expr.leaves();
                List<Condition> conditions = Condition.of(expr);
                Set<Map<String, Boolean>> suite = new HashSet<>();
                report.minimalSuite().forEach(t -> suite.add(t.values()));

                for (int leaf = 0; leaf < leaves.size(); leaf++) {
                    String input = leaves.get(leaf);
                    String label = conditions.get(leaf).label();
                    for (IndependencePair p : report.pairs().get(label)) {
                        assertTrue(validPair(expr, leaf, input, p.whenTrue().values(), p.whenFalse().values(), variant)
                                && feasible.contains(p.whenTrue().values()) && feasible.contains(p.whenFalse().values()),
                                "par inválido " + p + " para " + label + " em " + where);
                    }
                    int expected = countPairs(expr, leaf, input, feasible, variant);
                    assertEquals(expected, report.pairs().get(label).size(), "pares de " + label + " em " + where);
                    if (expected > 0) {
                        boolean inSuite = false;
                        for (Map<String, Boolean> t : suite) {
                            for (Map<String, Boolean> f : suite) {
                                inSuite |= validPair(expr, leaf, input, t, f, variant);
                            }
                        }
                        assertTrue(inSuite, "a suíte não demonstra " + label + " em " + where);
                    } else {
                        UncoveredCondition u = report.uncovered().stream()
                                .filter(x -> x.condition().equals(label)).findFirst().orElseThrow();
                        boolean blocked = countPairs(expr, leaf, input, all, variant) > 0;
                        assertEquals(blocked ? UncoveredCondition.Reason.INFEASIBLE : UncoveredCondition.Reason.REDUNDANT,
                                u.reason(), "diagnóstico de " + label + " em " + where);
                    }
                }

                // testes de fronteira: mesma combinação do teste de origem, no limite de uma comparação
                if (variant == McdcVariant.MASKING) {
                    Map<String, TestVector> byName = new HashMap<>();
                    report.minimalSuite().forEach(t -> byName.put(t.name(), t));
                    List<BoundaryTest> produced = checker.boundaryTests(expr, report.minimalSuite());
                    Set<String> got = new HashSet<>();
                    produced.forEach(b -> got.add(b.baseVector() + " | " + b.condition() + " | " + b.boundary()));
                    assertEquals(expectedBoundaries(report.minimalSuite(), atoms, domain), got,
                            "testes de fronteira em " + where);
                    for (BoundaryTest b : produced) {
                        Map<String, String> assignment = new HashMap<>(b.assignment());
                        assignment.putIfAbsent("x", "0");
                        assignment.putIfAbsent("y", "0");
                        assignment.putIfAbsent("mode", "idle");
                        assertEquals(byName.get(b.baseVector()).values(), row(atoms, assignment),
                                "fronteira " + b.boundary() + " muda a combinação de " + b.baseVector() + " em " + where);
                        String[] kv = b.boundary().split(" = ");
                        int value = Integer.parseInt(kv[1]);
                        boolean nextToAConstant = atoms.values().stream().anyMatch(p -> p.variable().equals(kv[0])
                                && p.value().matches("-?\\d+") && Math.abs(Integer.parseInt(p.value()) - value) <= 1);
                        assertTrue(nextToAConstant, "fronteira longe das constantes: " + b.boundary() + " em " + where);
                        boundaryTests++;
                    }
                }
            }
        }
        System.out.printf("oráculo numérico: %d expressões, %d combinações impossíveis, %d testes de fronteira%n",
                EXPRESSIONS, infeasibleRows, boundaryTests);
        assertTrue(infeasibleRows > 0, "o gerador precisa produzir combinações impossíveis");
        assertTrue(boundaryTests > 0, "o gerador precisa produzir testes de fronteira");
    }
}
