package io.github.rvdomingos.mcdc.cli;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier.Conflict;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier.Overlap;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier.Result;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/** Relatório do {@code mcdc verify}: conflitos, sobreposições compatíveis e lacunas. */
final class VerifyReport {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    /** Sobreposições compatíveis listadas no texto; o JSON traz todas. */
    static final int MAX_COMPATIBLE_SHOWN = 10;

    private VerifyReport() {
    }

    static String text(String system, String context, Result result) {
        var sb = new StringBuilder();
        sb.append("Verificação entre requisitos");
        if (system != null) {
            sb.append(": ").append(system);
        }
        sb.append('\n').append(result.decisions()).append(" decisões, ").append(result.pairsChecked())
                .append(" pares que escrevem alguma variável em comum\n\n");

        List<Overlap> conflicts = result.conflicts();
        sb.append("Conflitos: ").append(conflicts.isEmpty() ? "nenhum" : conflicts.size()).append('\n');
        for (Overlap o : conflicts) {
            sb.append("  ").append(name(o.first())).append(" × ").append(name(o.second()))
                    .append(": as duas guardas valem no mesmo passo\n");
            for (Conflict c : o.conflicts()) {
                sb.append("    ").append(c.variable()).append(": ").append(c.firstValue()).append(" (")
                        .append(name(o.first())).append(") × ").append(c.secondValue()).append(" (")
                        .append(name(o.second())).append(")\n");
            }
            if (!o.witness().isEmpty()) {
                sb.append("    exemplo: ").append(values(o.witness())).append('\n');
            }
        }

        List<Overlap> compatible = result.compatible();
        sb.append("\nSobreposições sem conflito: ").append(compatible.isEmpty() ? "nenhuma" : compatible.size()).append('\n');
        for (Overlap o : compatible.subList(0, Math.min(compatible.size(), MAX_COMPATIBLE_SHOWN))) {
            sb.append("  ").append(name(o.first())).append(" × ").append(name(o.second()))
                    .append(": mesmo valor em ").append(String.join(", ", o.shared())).append('\n');
        }
        if (compatible.size() > MAX_COMPATIBLE_SHOWN) {
            sb.append("  ... e mais ").append(compatible.size() - MAX_COMPATIBLE_SHOWN)
                    .append(" (lista completa com --format json)\n");
        }

        sb.append("\nLacunas: ");
        if (!result.gapChecked()) {
            sb.append("não conferidas (use --context \"<expressão>\" para dizer em que situação alguma guarda deve valer)\n");
        } else if (result.gap() == null) {
            sb.append("nenhuma: sob ").append(context).append(", sempre alguma guarda vale\n");
        } else {
            sb.append("encontrada: sob ").append(context).append(", nenhuma guarda vale em\n    ")
                    .append(result.gap().isEmpty() ? "(o Z3 não deu valores)" : values(result.gap())).append('\n');
        }
        return sb.toString();
    }

    static String json(String system, String context, Result result) {
        Map<String, Object> root = new LinkedHashMap<>();
        root.put("tool", "mcdc");
        root.put("check", "verify");
        root.put("system", system);
        root.put("decisions", result.decisions());
        root.put("pairsChecked", result.pairsChecked());
        root.put("conflicts", result.conflicts().stream().map(VerifyReport::overlap).toList());
        root.put("compatibleOverlaps", result.compatible().stream().map(VerifyReport::overlap).toList());
        Map<String, Object> gaps = new LinkedHashMap<>();
        gaps.put("checked", result.gapChecked());
        gaps.put("context", context);
        gaps.put("found", result.gap() != null);
        gaps.put("witness", result.gap());
        root.put("gaps", gaps);
        root.put("ok", !result.hasProblems());
        try {
            return MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(root) + "\n";
        } catch (JsonProcessingException e) {
            throw new IllegalStateException("Falha ao gerar o JSON", e);
        }
    }

    private static Map<String, Object> overlap(Overlap o) {
        Map<String, Object> node = new LinkedHashMap<>();
        node.put("first", o.first().id());
        node.put("firstRequirement", o.first().requirement());
        node.put("second", o.second().id());
        node.put("secondRequirement", o.second().requirement());
        node.put("sharedVariables", o.shared());
        node.put("conflicts", o.conflicts().stream().map(c -> {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("variable", c.variable());
            item.put("first", c.firstValue());
            item.put("second", c.secondValue());
            return item;
        }).toList());
        node.put("witness", o.witness());
        return node;
    }

    private static String name(Decision decision) {
        return decision.requirement() != null ? decision.requirement() : decision.id();
    }

    private static String values(Map<String, String> values) {
        return values.entrySet().stream().map(e -> e.getKey() + " = " + e.getValue()).collect(Collectors.joining(", "));
    }
}
