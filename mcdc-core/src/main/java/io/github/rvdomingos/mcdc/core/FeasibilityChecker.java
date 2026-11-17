package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Diz quais linhas da tabela são possíveis a partir dos predicados e dá valores concretos (implementação com Z3 no mcdc-z3). */
public interface FeasibilityChecker {

    /** Para cada linha, na mesma ordem: os valores que a realizam, ou vazio se ela é impossível. */
    List<Optional<Map<String, String>>> solve(Expr expression, List<TestVector> rows);
}
