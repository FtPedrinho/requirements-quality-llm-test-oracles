package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Decide quais linhas da tabela verdade são possíveis, a partir do que as condições afirmam
 * (os predicados), e dá valores concretos para as possíveis. A implementação com Z3 fica no módulo mcdc-z3.
 */
public interface FeasibilityChecker {

    /**
     * Para cada linha, na mesma ordem, os valores concretos das variáveis que a realizam
     * (ex.: speed = 101), ou vazio se a linha for impossível.
     */
    List<Optional<Map<String, String>>> solve(Expr expression, List<TestVector> rows);
}
