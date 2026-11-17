package io.github.rvdomingos.mcdc.core;

import io.github.rvdomingos.mcdc.core.model.Expr;

/**
 * Opções da análise.
 *
 * @param constraint  restrição entre as condições escrita à mão; null quando não há
 * @param feasibility verificação das linhas pelos predicados (ex.: Z3); null para não verificar
 * @param optimizer   escolha exata da suíte; null para a escolha gulosa
 */
public record McdcOptions(McdcVariant variant, Expr constraint, FeasibilityChecker feasibility,
        SuiteOptimizer optimizer) {

    /** Mascaramento, sem restrição, sem verificação de viabilidade e com a escolha gulosa. */
    public static McdcOptions defaults() {
        return new McdcOptions(McdcVariant.MASKING, null, null, null);
    }

    public McdcOptions withVariant(McdcVariant variant) {
        return new McdcOptions(variant, constraint, feasibility, optimizer);
    }

    public McdcOptions withConstraint(Expr constraint) {
        return new McdcOptions(variant, constraint, feasibility, optimizer);
    }

    public McdcOptions withFeasibility(FeasibilityChecker feasibility) {
        return new McdcOptions(variant, constraint, feasibility, optimizer);
    }

    public McdcOptions withOptimizer(SuiteOptimizer optimizer) {
        return new McdcOptions(variant, constraint, feasibility, optimizer);
    }
}
