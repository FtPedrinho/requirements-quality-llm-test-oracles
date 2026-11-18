package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

/** Leitura das respostas do Z3: espaços, quebras de linha, símbolos entre barras e erros. */
class SExprTest {

    @Test
    void readsAnswersWithSpacesAndLineBreaks() {
        assertEquals(List.of("sat", List.of(List.of("x", "1"), List.of("|r 1|", "true")), "unsat"),
                SExpr.parseAll("  sat\n(  (x 1)\n   ( |r 1| true) )\n unsat \n"));
    }

    @Test
    void readsNegativeNumbersAndStrings() {
        assertEquals(List.of(List.of(List.of("t", List.of("-", "5"))), List.of("error", "\"line 2: x\"")),
                SExpr.parseAll("((t (- 5)))(error \"line 2: x\")"));
    }

    @Test
    void emptyOutputHasNoAnswers() {
        assertEquals(List.of(), SExpr.parseAll(" \n "));
    }

    @Test
    void errorsInsideValueListsAreNotIgnored() {
        assertThrows(IllegalStateException.class,
                () -> Z3Process.valueLists("((x 1))\n(error \"model is not available\")"));
        assertThrows(IllegalStateException.class, () -> Z3Process.all("sat\n(error \"x\")"));
    }
}
