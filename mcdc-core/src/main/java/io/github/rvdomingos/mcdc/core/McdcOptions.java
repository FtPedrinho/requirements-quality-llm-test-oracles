package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;

/**
 * Opções da análise.
 *
 * @param variant     variante de MC/DC
 * @param constraint  restrição entre as condições escrita à mão; null quando não há
 * @param feasibility verificação das linhas a partir dos predicados (ex.: Z3); null para não verificar
 */
public record McdcOptions(McdcVariant variant, Expr constraint, FeasibilityChecker feasibility) {

    /** Mascaramento, sem restrição e sem verificação de viabilidade. */
    public static McdcOptions defaults() {
        return new McdcOptions(McdcVariant.MASKING, null, null);
    }

    public McdcOptions withVariant(McdcVariant variant) {
        return new McdcOptions(variant, constraint, feasibility);
    }

    public McdcOptions withConstraint(Expr constraint) {
        return new McdcOptions(variant, constraint, feasibility);
    }

    public McdcOptions withFeasibility(FeasibilityChecker feasibility) {
        return new McdcOptions(variant, constraint, feasibility);
    }
}
