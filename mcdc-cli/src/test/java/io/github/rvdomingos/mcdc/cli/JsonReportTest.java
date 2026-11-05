package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import java.util.List;
import org.junit.jupiter.api.Test;

class JsonReportTest {

    private static DecisionAnalysis analyze(String id, String requirement, String text) {
        Decision decision = new Decision(id, requirement, text, ExpressionParser.parse(text), List.of("atr1"));
        return Mcdc.analyze(decision, McdcOptions.defaults());
    }

    @Test
    void carriesTraceabilityAndResultsOfEachDecision() throws Exception {
        String json = JsonReport.format("sistema", McdcOptions.defaults(), null,
                List.of(analyze("d1", "REQ-001", "(A = x /\\ B = y) \\/ C")));
        JsonNode root = new ObjectMapper().readTree(json);

        assertEquals("sistema", root.get("system").asText());
        assertEquals("MASKING", root.get("variant").asText());
        assertTrue(root.get("complete").asBoolean());

        JsonNode decision = root.get("decisions").get(0);
        assertEquals("d1", decision.get("id").asText());
        assertEquals("REQ-001", decision.get("requirement").asText());
        assertEquals(8, decision.get("truthTable").size());
        assertEquals(4, decision.get("minimalSuite").size());
        assertEquals("[\"V2\",\"V6\"]", decision.get("independencePairs").get("A = x").get(0).toString());
    }

    @Test
    void describesPredicatesOfEachInput() throws Exception {
        String json = JsonReport.format(null, McdcOptions.defaults(), null,
                List.of(analyze("d1", null, "speed > 100 and door")));
        JsonNode inputs = new ObjectMapper().readTree(json).get("decisions").get(0).get("inputs");

        assertEquals("speed > 100", inputs.get(0).get("name").asText());
        assertEquals("speed", inputs.get(0).get("variable").asText());
        assertEquals(">", inputs.get(0).get("operator").asText());
        assertEquals("100", inputs.get(0).get("value").asText());
        assertFalse(inputs.get(1).has("variable"));
    }

    @Test
    void reportsUncoveredConditions() throws Exception {
        String json = JsonReport.format(null, McdcOptions.defaults(), null,
                List.of(analyze("d1", null, "A or (A and B)")));
        JsonNode root = new ObjectMapper().readTree(json);

        assertFalse(root.get("complete").asBoolean());
        assertTrue(root.get("decisions").get(0).get("uncoveredConditions").toString().contains("B"));
    }
}
