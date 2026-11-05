package io.github.rvdomingos.mcdc.requirements;

import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Arquivo .mcdc: um requisito por linha, "ID: expressão". Linhas vazias e começando com # são ignoradas. */
public final class RequirementsFile {

    private RequirementsFile() {
    }

    public static DecisionSet read(Path path) throws IOException {
        return parse(Files.readAllLines(path), path.toString());
    }

    static DecisionSet parse(List<String> lines, String source) {
        List<Decision> decisions = new ArrayList<>();
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i).strip();
            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }
            int colon = line.indexOf(':');
            if (colon <= 0) {
                throw new IllegalArgumentException(
                        "Linha " + (i + 1) + " sem identificador. Formato: REQ-001: expressão");
            }
            String id = line.substring(0, colon).strip();
            String text = line.substring(colon + 1).strip();
            decisions.add(expression(id, id, text));
        }
        if (decisions.isEmpty()) {
            throw new IllegalArgumentException("Nenhum requisito em " + source);
        }
        return new DecisionSet(null, List.of(), decisions);
    }

    /** Uma decisão a partir de uma expressão avulsa; erros de sintaxe saem com o id na frente. */
    public static Decision expression(String id, String requirement, String text) {
        try {
            return new Decision(id, requirement, text, ExpressionParser.parse(text), List.of());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException(id + ": " + e.getMessage());
        }
    }
}
