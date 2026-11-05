package io.github.rvdomingos.mcdc.requirements;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.InputVariable;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Lê o JSON de decisões que o Extractor gera a partir do DFRS da NAT2TEST.
 * Formato descrito na seção 8 de docs/arquitetura-fase1.md; campos desconhecidos são ignorados.
 */
public final class Nat2TestJsonReader {

    private static final ObjectMapper MAPPER = new ObjectMapper()
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    record JsonFile(String system, List<JsonInput> inputs, List<JsonDecision> decisions) {
    }

    record JsonInput(String name, String type, List<String> values) {
    }

    record JsonDecision(String id, String requirement, String guard, String temporal, List<String> actions) {
    }

    private Nat2TestJsonReader() {
    }

    public static DecisionSet read(Path path) throws IOException {
        return read(Files.readString(path));
    }

    public static DecisionSet read(String json) {
        JsonFile file;
        try {
            file = MAPPER.readValue(json, JsonFile.class);
        } catch (JsonProcessingException e) {
            throw new IllegalArgumentException("JSON inválido: " + e.getOriginalMessage());
        }
        if (file.decisions() == null || file.decisions().isEmpty()) {
            throw new IllegalArgumentException("O JSON não tem decisões (campo \"decisions\")");
        }

        List<InputVariable> inputs = new ArrayList<>();
        if (file.inputs() != null) {
            for (JsonInput input : file.inputs()) {
                inputs.add(new InputVariable(input.name(), input.type(), input.values()));
            }
        }

        List<Decision> decisions = new ArrayList<>();
        Set<String> ids = new HashSet<>();
        for (int i = 0; i < file.decisions().size(); i++) {
            JsonDecision d = file.decisions().get(i);
            String id = isBlank(d.id()) ? "#" + (i + 1) : d.id();
            if (isBlank(d.guard())) {
                throw new IllegalArgumentException(id + ": decisão sem \"guard\"");
            }
            if (!ids.add(id)) {
                throw new IllegalArgumentException("Decisão repetida: " + id);
            }
            decisions.add(toDecision(id, d));
        }
        return new DecisionSet(file.system(), inputs, decisions);
    }

    /** A guarda temporal entra como mais uma condição ligada por "e" à guarda de dados. */
    private static Decision toDecision(String id, JsonDecision d) {
        try {
            Expr expression = ExpressionParser.parse(d.guard());
            String text = d.guard();
            if (!isBlank(d.temporal())) {
                expression = new And(expression, ExpressionParser.parse(d.temporal()));
                text = "(" + d.guard() + ") /\\ " + d.temporal();
            }
            return new Decision(id, d.requirement(), text, expression, d.actions());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException(id + ": " + e.getMessage());
        }
    }

    private static boolean isBlank(String text) {
        return text == null || text.isBlank();
    }
}
