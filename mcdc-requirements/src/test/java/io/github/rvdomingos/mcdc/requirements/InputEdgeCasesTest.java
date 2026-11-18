package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Entradas no limite: aspas no fim da linha, sinal de menos no fim, número da linha com erro. */
class InputEdgeCasesTest {

    @Test
    void csvCellsWithQuotes() {
        assertEquals(List.of("a", "b, c", "d \"e\""), TestCasesFile.cells("a,\"b, c\",\"d \"\"e\"\"\""));
        assertEquals(List.of("a", "b"), TestCasesFile.cells("a,\"b\""));
        assertEquals(List.of("a", "b\""), TestCasesFile.cells("a,\"b\"\"\""));
        assertEquals(List.of("a", ""), TestCasesFile.cells("a,"));
    }

    @Test
    void csvErrorsPointToTheRightLine() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () -> TestCasesFile.parse(
                List.of("test,input,value", "# comentário", "T1,A,T", "T2,,T"), "t.csv"));
        assertTrue(e.getMessage().contains("linha 4"), e.getMessage());
    }

    @Test
    void requirementErrorsPointToTheRightLine() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () -> RequirementsFile.parse(
                List.of("R1: A and B", "", ": C"), "r.mcdc"));
        assertTrue(e.getMessage().contains("Linha 3"), e.getMessage());
        // um id de um caractere é válido
        assertEquals("X", RequirementsFile.parse(List.of("X: A"), "r.mcdc").decisions().get(0).id());
    }

    @Test
    void minusSignOnlyStartsANumber() {
        assertEquals(new Cond(new Predicate("x", ">", "-5")), ExpressionParser.parse("x > -5"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("x > -"));
        assertThrows(IllegalArgumentException.class, () -> ExpressionParser.parse("x - 5"));
    }
}
