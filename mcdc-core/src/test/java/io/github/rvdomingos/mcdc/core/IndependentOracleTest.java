package io.github.rvdomingos.mcdc.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;

/**
 * Confere o motor contra um oráculo escrito direto da definição de MC/DC, em milhares de expressões
 * geradas ao acaso. O oráculo não usa a tabela verdade, os pares nem a função "decide" do motor: monta as
 * combinações sozinho e decide pela derivada booleana (a saída muda entre a folha valer T e valer F).
 */
class IndependentOracleTest {

    private static final long SEED = 20261117L;
    private static final int EXPRESSIONS = 3000;
    private static final List<String> NAMES = List.of("A", "B", "C", "D", "E", "F");

    // ---------- oráculo ----------

    /** Todas as 2ⁿ combinações das entradas, montadas sem a tabela do motor. */
    private static List<Map<String, Boolean>> combinations(List<String> inputs) {
        List<Map<String, Boolean>> all = new ArrayList<>();
        for (int mask = 0; mask < (1 << inputs.size()); mask++) {
            Map<String, Boolean> values = new HashMap<>();
            for (int i = 0; i < inputs.size(); i++) {
                values.put(inputs.get(i), (mask & (1 << i)) != 0);
            }
            all.add(values);
        }
        return all;
    }

    /** A expressão com a folha {@code target} trocada por uma constante. */
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

    /** Derivada booleana: a folha decide quando a saída com ela T é diferente da saída com ela F. */
    private static boolean decides(Expr expr, int leaf, Map<String, Boolean> values) {
        return eval(withLeaf(expr, leaf, true, new int[] {0}), values)
                != eval(withLeaf(expr, leaf, false, new int[] {0}), values);
    }

    private static boolean differOnlyIn(Map<String, Boolean> a, Map<String, Boolean> b, String input) {
        for (String key : a.keySet()) {
            if (!key.equals(input) && !a.get(key).equals(b.get(key))) {
                return false;
            }
        }
        return !a.get(input).equals(b.get(input));
    }

    /** Definição do par (RN01, RN02): T num, F no outro, a saída muda e a folha decide nos dois. */
    private static boolean validPair(Expr expr, int leaf, String input, Map<String, Boolean> t,
            Map<String, Boolean> f, McdcVariant variant) {
        return t.get(input) && !f.get(input)
                && eval(expr, t) != eval(expr, f)
                && decides(expr, leaf, t) && decides(expr, leaf, f)
                && (variant == McdcVariant.MASKING || differOnlyIn(t, f, input));
    }

    /** Quantos pares a folha tem entre as combinações aceitas. */
    private static int countPairs(Expr expr, int leaf, String input, List<Map<String, Boolean>> rows,
            McdcVariant variant) {
        int count = 0;
        for (Map<String, Boolean> t : rows) {
            for (Map<String, Boolean> f : rows) {
                if (validPair(expr, leaf, input, t, f, variant)) {
                    count++;
                }
            }
        }
        return count;
    }

    // ---------- gerador ----------

    private static Expr random(Random rnd, List<String> pool, int leaves) {
        if (leaves == 1) {
            Expr c = new Cond(pool.get(rnd.nextInt(pool.size())));
            return rnd.nextInt(4) == 0 ? new Not(c) : c;
        }
        int left = 1 + rnd.nextInt(leaves - 1);
        Expr l = random(rnd, pool, left);
        Expr r = random(rnd, pool, leaves - left);
        Expr e = rnd.nextBoolean() ? new And(l, r) : new Or(l, r);
        return rnd.nextInt(6) == 0 ? new Not(e) : e;
    }

    private record Case(Expr expr, Expr constraint) {
    }

    /** Expressões de 1 a 5 entradas e 1 a 7 folhas, com repetição; um terço com restrição entre as entradas. */
    private static List<Case> cases(long seed, int count, boolean withConstraints) {
        Random rnd = new Random(seed);
        List<Case> cases = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            List<String> pool = NAMES.subList(0, 1 + rnd.nextInt(5));
            Expr expr = random(rnd, pool, 1 + rnd.nextInt(7));
            Expr constraint = null;
            if (withConstraints && rnd.nextInt(3) == 0) {
                constraint = random(rnd, expr.inputs(), 1 + rnd.nextInt(3));
            }
            cases.add(new Case(expr, constraint));
        }
        return cases;
    }

    // ---------- propriedades ----------

    @Test
    void engineAgreesWithTheDefinition() {
        int checked = 0;
        for (Case c : cases(SEED, EXPRESSIONS, true)) {
            for (McdcVariant variant : McdcVariant.values()) {
                check(c.expr(), c.constraint(), variant);
                checked++;
            }
        }
        assertEquals(2 * EXPRESSIONS, checked);
    }

    private static void check(Expr expr, Expr constraint, McdcVariant variant) {
        String where = expr + (constraint == null ? "" : " | restrição " + constraint) + " | " + variant;
        McdcReport report = Mcdc.analyze(expr,
                McdcOptions.defaults().withVariant(variant).withConstraint(constraint));

        List<String> inputs = expr.inputs();
        List<Map<String, Boolean>> all = combinations(inputs);
        List<Map<String, Boolean>> feasible = all.stream()
                .filter(v -> constraint == null || constraint.eval(v)).toList();

        // tabela: uma linha por combinação, com a saída e a viabilidade certas
        assertEquals(all.size(), report.table().rows().size(), where);
        Set<Map<String, Boolean>> seen = new HashSet<>();
        for (TestVector row : report.table().rows()) {
            Map<String, Boolean> v = row.values();
            assertTrue(seen.add(v), "linha repetida em " + where);
            assertEquals(expr.eval(v), row.outcome(), "saída errada em " + where);
            assertEquals(constraint == null || constraint.eval(v), row.feasible(), "viabilidade errada em " + where);
        }

        List<String> leaves = expr.leaves();
        List<Condition> conditions = Condition.of(expr);
        Set<Map<String, Boolean>> suite = new HashSet<>();
        for (TestVector test : report.minimalSuite()) {
            assertTrue(test.feasible(), "teste impossível na suíte em " + where);
            suite.add(test.values());
        }

        int covered = 0;
        for (int leaf = 0; leaf < leaves.size(); leaf++) {
            String input = leaves.get(leaf);
            String label = conditions.get(leaf).label();
            List<IndependencePair> listed = report.pairs().get(label);

            // todo par listado é válido e usa só linhas possíveis
            for (IndependencePair p : listed) {
                assertTrue(p.whenTrue().feasible() && p.whenFalse().feasible(), "par com linha impossível em " + where);
                assertTrue(validPair(expr, leaf, input, p.whenTrue().values(), p.whenFalse().values(), variant),
                        "par inválido " + p + " para " + label + " em " + where);
            }
            // e nenhum par válido ficou de fora
            int expected = countPairs(expr, leaf, input, feasible, variant);
            assertEquals(Math.min(expected, IndependencePairs.MAX_PAIRS_PER_CONDITION), listed.size(),
                    "número de pares de " + label + " em " + where);

            boolean uncovered = report.uncoveredConditions().contains(label);
            assertEquals(expected == 0, uncovered, "cobertura de " + label + " em " + where);

            if (expected > 0) {
                covered++;
                // a suíte contém um par válido da condição, conferido sem olhar a escolha do motor
                boolean inSuite = false;
                for (Map<String, Boolean> t : suite) {
                    for (Map<String, Boolean> f : suite) {
                        inSuite |= validPair(expr, leaf, input, t, f, variant);
                    }
                }
                assertTrue(inSuite, "a suíte não demonstra " + label + " em " + where);
                IndependencePair chosen = report.chosenPairs().get(label);
                assertTrue(suite.contains(chosen.whenTrue().values()) && suite.contains(chosen.whenFalse().values()),
                        "par escolhido fora da suíte em " + where);
            } else {
                // diagnóstico (RN05): redundante só se não há par nem com todas as combinações
                UncoveredCondition u = report.uncovered().stream()
                        .filter(x -> x.condition().equals(label)).findFirst().orElseThrow();
                boolean pairWithoutConstraint = countPairs(expr, leaf, input, all, variant) > 0;
                assertEquals(pairWithoutConstraint ? UncoveredCondition.Reason.INFEASIBLE
                        : UncoveredCondition.Reason.REDUNDANT, u.reason(), "diagnóstico de " + label + " em " + where);
            }
        }

        // tamanho: nada na suíte se não há o que demonstrar; no máximo dois testes por condição coberta
        if (covered == 0) {
            assertTrue(report.minimalSuite().isEmpty(), "suíte sem motivo em " + where);
        } else {
            assertTrue(report.minimalSuite().size() >= 2, where);
            assertTrue(report.minimalSuite().size() <= 2 * covered, "suíte grande demais em " + where);
        }
        assertEquals(report.isComplete(), covered == leaves.size(), where);

        // o modo avaliação reconhece a suíte gerada como completa quando ela é
        List<TestCase> tests = new ArrayList<>();
        for (TestVector test : report.minimalSuite()) {
            tests.add(new TestCase(test.name(), test.values(), test.outcome()));
        }
        TestSetEvaluation evaluation = Mcdc.evaluate(expr,
                McdcOptions.defaults().withVariant(variant).withConstraint(constraint), tests);
        assertEquals(report.isComplete(), evaluation.isComplete(), "avaliação da própria suíte em " + where);
        assertTrue(evaluation.problems().isEmpty(), "problemas na própria suíte em " + where);
    }

    @Test
    void maskingCoversAtLeastWhatUniqueCauseCovers() {
        for (Case c : cases(SEED + 1, EXPRESSIONS, true)) {
            McdcOptions options = McdcOptions.defaults().withConstraint(c.constraint());
            Set<String> uc = new HashSet<>(Mcdc.analyze(c.expr(), options.withVariant(McdcVariant.UNIQUE_CAUSE))
                    .uncoveredConditions());
            Set<String> masking = new HashSet<>(Mcdc.analyze(c.expr(), options.withVariant(McdcVariant.MASKING))
                    .uncoveredConditions());
            assertTrue(uc.containsAll(masking), "mascaramento cobre menos que causa única em " + c.expr());
        }
    }

    @Test
    void mutationVerdictsAreTrue() {
        for (Case c : cases(SEED + 2, EXPRESSIONS, false)) {
            McdcReport report = Mcdc.analyze(c.expr(), McdcOptions.defaults());
            List<Map<String, Boolean>> all = combinations(c.expr().inputs());
            Map<String, Map<String, Boolean>> suiteByName = new HashMap<>();
            report.minimalSuite().forEach(t -> suiteByName.put(t.name(), t.values()));

            for (MutationReport.Result r : MutationReport.of(report).results()) {
                Expr mutant = r.mutant().expression();
                boolean sameEverywhere = all.stream().allMatch(v -> mutant.eval(v) == c.expr().eval(v));
                assertEquals(sameEverywhere, r.equivalent(), "equivalência de " + mutant + " de " + c.expr());
                boolean someTestKills = suiteByName.values().stream()
                        .anyMatch(v -> mutant.eval(v) != c.expr().eval(v));
                if (r.killedBy() != null) {
                    Map<String, Boolean> killer = suiteByName.get(r.killedBy());
                    if (killer == null || mutant.eval(killer) == c.expr().eval(killer)) {
                        fail(r.killedBy() + " não pega " + mutant + " de " + c.expr());
                    }
                } else if (!r.equivalent()) {
                    assertFalse(someTestKills, "mutante dado como vivo, mas um teste o pega: " + mutant);
                }
            }
        }
    }

    @Test
    void sameInputGivesTheSameResult() {
        for (Case c : cases(SEED + 3, 500, true)) {
            McdcOptions options = McdcOptions.defaults().withConstraint(c.constraint());
            McdcReport a = Mcdc.analyze(c.expr(), options);
            McdcReport b = Mcdc.analyze(c.expr(), options);
            assertEquals(a.minimalSuite().stream().map(TestVector::index).toList(),
                    b.minimalSuite().stream().map(TestVector::index).toList(), "suíte diferente em " + c.expr());
            assertEquals(a.chosenPairs().toString(), b.chosenPairs().toString(), c.expr().toString());
        }
    }
}
