package io.github.rvdomingos.mcdc.core.mutation;

import io.github.rvdomingos.mcdc.core.McdcReport;
import io.github.rvdomingos.mcdc.core.TestVector;
import io.github.rvdomingos.mcdc.core.model.Expr;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/**
 * Validação por mutação: para cada versão com uma falha, se ela é equivalente à original e, se não for,
 * qual teste da suíte a detecta.
 */
public record MutationReport(List<Result> results) {

    /**
     * @param equivalent dá o mesmo resultado que a original em toda linha possível
     * @param killedBy   teste da suíte que detecta a falha; null se nenhum detecta
     */
    public record Result(Mutants.Mutant mutant, boolean equivalent, String killedBy) {

        public boolean survived() {
            return !equivalent && killedBy == null;
        }
    }

    /** Totais de um tipo de falha. */
    public record Summary(int total, int equivalent, int killed) {

        public int detectable() {
            return total - equivalent;
        }
    }

    /** Gera os mutantes da expressão e os confronta com a suíte do relatório. */
    public static MutationReport of(McdcReport report) {
        Expr original = report.expression();
        List<Result> results = new ArrayList<>();
        for (Mutants.Mutant mutant : Mutants.of(original)) {
            boolean equivalent = report.table().rows().stream()
                    .filter(TestVector::feasible)
                    .allMatch(row -> mutant.expression().eval(row.values()) == row.outcome());
            String killedBy = null;
            if (!equivalent) {
                killedBy = report.minimalSuite().stream()
                        .filter(test -> mutant.expression().eval(test.values()) != test.outcome())
                        .map(TestVector::name)
                        .findFirst().orElse(null);
            }
            results.add(new Result(mutant, equivalent, killedBy));
        }
        return new MutationReport(List.copyOf(results));
    }

    public Map<FaultClass, Summary> byFault() {
        Map<FaultClass, Summary> summaries = new EnumMap<>(FaultClass.class);
        for (FaultClass fault : FaultClass.values()) {
            List<Result> of = results.stream().filter(r -> r.mutant().fault() == fault).toList();
            if (!of.isEmpty()) {
                summaries.put(fault, new Summary(of.size(),
                        (int) of.stream().filter(Result::equivalent).count(),
                        (int) of.stream().filter(r -> r.killedBy() != null).count()));
            }
        }
        return summaries;
    }

    public List<Result> survivors() {
        return results.stream().filter(Result::survived).toList();
    }

    /** Detectados / detectáveis, em porcentagem. */
    public double score() {
        long detectable = results.stream().filter(r -> !r.equivalent()).count();
        long killed = results.stream().filter(r -> r.killedBy() != null).count();
        return detectable == 0 ? 100.0 : 100.0 * killed / detectable;
    }
}
