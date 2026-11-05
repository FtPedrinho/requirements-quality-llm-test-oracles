package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.core.BoundaryTest;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.TruthTable;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class Z3FeasibilityCheckerTest {

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private static Cond cond(String variable, String operator, String value) {
        return new Cond(new Predicate(variable, operator, value));
    }

    private static String feasibility(TruthTable table) {
        return table.rows().stream().map(row -> row.feasible() ? "1" : "0").collect(Collectors.joining());
    }

    @Test
    void findsImpossibleRowsFromPredicates() {
        // speed > 100 or (speed > 50 and rain): speed > 100 exige speed > 50
        Expr expr = new Or(cond("speed", ">", "100"), new And(cond("speed", ">", "50"), new Cond("rain")));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of()));

        assertEquals("11001111", feasibility(table));
    }

    @Test
    void givesConcreteValuesThatRealizeEachRow() {
        Expr expr = new Or(cond("speed", ">", "100"), new And(cond("speed", ">", "50"), new Cond("rain")));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of()));

        TestVector ftt = table.rows().get(4); // speed > 100 falsa, speed > 50 verdadeira, rain verdadeira
        int speed = Integer.parseInt(ftt.assignment().get("speed"));
        assertTrue(speed > 50 && speed <= 100, ftt.assignment().toString());
        assertEquals("true", ftt.assignment().get("rain"));
    }

    @Test
    void sameResultAsTheHandWrittenConstraint() {
        Expr expr = new Or(cond("speed", ">", "100"), new And(cond("speed", ">", "50"), new Cond("rain")));
        McdcOptions z3 = McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE)
                .withFeasibility(new Z3FeasibilityChecker(List.of()));
        McdcOptions manual = McdcOptions.defaults().withVariant(McdcVariant.UNIQUE_CAUSE)
                .withConstraint(new Or(new Not(new Cond("speed > 100")), new Cond("speed > 50")));

        assertEquals(suite(Mcdc.analyze(expr, manual)), suite(Mcdc.analyze(expr, z3)));
    }

    @Test
    void declaredEnumValuesExcludeEachOther() {
        // mode = idle and mode = choice nunca são verdadeiras juntas
        Expr expr = new Or(cond("mode", "=", "idle"), cond("mode", "=", "choice"));
        List<InputVariable> declared = List.of(new InputVariable("mode", "enum", List.of("idle", "choice", "off")));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(declared));

        assertEquals("0111", feasibility(table));
        assertEquals("off", table.rows().get(3).assignment().get("mode"));
    }

    @Test
    void undeclaredEnumGetsAnOtherValue() {
        Expr expr = new Or(cond("mode", "=", "idle"), cond("mode", "=", "choice"));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of()));

        assertEquals("0111", feasibility(table));
        assertEquals(SmtEncoding.OTHER, table.rows().get(3).assignment().get("mode"));
    }

    @Test
    void declaredBooleanCannotBeTrueAndFalse() {
        Expr expr = new And(cond("coin", "=", "true"), cond("coin", "=", "false"));
        TruthTable table = TruthTable.of(expr, null,
                new Z3FeasibilityChecker(List.of(new InputVariable("coin", "bool", null))));

        assertFalse(table.rows().get(0).feasible());
    }

    @Test
    void handlesRealsAndNegativeNumbers() {
        Expr expr = new And(cond("x", "<=", "-2.5"), cond("x", ">", "-10"));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of()));

        double x = Double.parseDouble(table.rows().get(0).assignment().get("x"));
        assertTrue(x <= -2.5 && x > -10, String.valueOf(x));
        assertFalse(table.rows().get(3).feasible()); // x > -2.5 e x <= -10 ao mesmo tempo
    }

    @Test
    void comparesTwoVariables() {
        Expr expr = new And(cond("x", "<", "limit"), cond("limit", "<", "x"));
        List<InputVariable> declared = List.of(new InputVariable("x", "int", null), new InputVariable("limit", "int", null));
        TruthTable table = TruthTable.of(expr, null, new Z3FeasibilityChecker(declared));

        assertFalse(table.rows().get(0).feasible());
    }

    @Test
    void rejectsValuesThatDoNotMatchTheType() {
        Expr expr = cond("mode", "=", "turbo");
        List<InputVariable> declared = List.of(new InputVariable("mode", "enum", List.of("idle", "choice")));

        assertThrows(IllegalArgumentException.class,
                () -> TruthTable.of(expr, null, new Z3FeasibilityChecker(declared)));
    }

    @Test
    void explainsWhenZ3IsMissing() {
        Expr expr = cond("x", ">", "1");
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> TruthTable.of(expr, null, new Z3FeasibilityChecker(List.of(), "z3-que-nao-existe")));
        assertTrue(e.getMessage().contains("brew install z3"));
    }

    private static String suite(McdcReport report) {
        return report.minimalSuite().stream().map(TestVector::name).collect(Collectors.joining(", "));
    }

    @Test
    void generatesBoundaryVariantsOfTheSuite() {
        // suíte de causa única: V2 (TTF), V5 (FTT), V6 (FTF), V7 (FFT)
        Expr expr = new Or(cond("speed", ">", "100"), new And(cond("speed", ">", "50"), new Cond("rain")));
        Z3FeasibilityChecker z3 = new Z3FeasibilityChecker(List.of());
        McdcReport report = Mcdc.analyze(expr, McdcOptions.defaults()
                .withVariant(McdcVariant.UNIQUE_CAUSE).withFeasibility(z3));

        List<String> boundaries = z3.boundaryTests(expr, report.minimalSuite()).stream()
                .map(b -> b.baseVector() + ": " + b.boundary()).toList();

        // V2 não admite speed = 51 (contradiz speed > 100); V7 não admite speed = 100 (contradiz speed <= 50)
        assertEquals(List.of("V2: speed = 101", "V5: speed = 100", "V5: speed = 51",
                "V6: speed = 100", "V6: speed = 51", "V7: speed = 50"), boundaries);
    }

    @Test
    void realBoundariesUseASmallStep() {
        Expr expr = new And(cond("x", "<=", "-2.5"), cond("y", "!=", "0"));
        Z3FeasibilityChecker z3 = new Z3FeasibilityChecker(List.of(new InputVariable("x", "real", null)));
        TruthTable table = TruthTable.of(expr, null, z3);

        List<BoundaryTest> tests = z3.boundaryTests(expr, List.of(table.rows().get(0), table.rows().get(2)));
        List<String> texts = tests.stream().map(BoundaryTest::boundary).toList();
        // V1 (x <= -2.5 e y != 0): x = -2.5, y = -1, y = 1; V3 (x > -2.5): x = -2.49
        assertEquals(List.of("x = -2.5", "y = -1", "y = 1", "x = -2.49", "y = -1", "y = 1"), texts);
        assertEquals("-2.49", tests.get(3).assignment().get("x"));
    }
}
