package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.List;
import org.junit.jupiter.api.Test;

class Nat2TestJsonReaderTest {

    private static final String JSON = """
            {
              "system": "the_coffee_machine_system",
              "inputs": [
                { "name": "A", "type": "enum", "values": ["x", "z"] },
                { "name": "C", "type": "bool" }
              ],
              "decisions": [
                {
                  "id": "the_coffee_machine_system#1",
                  "requirement": "REQ-001",
                  "guard": "(A = x /\\\\ B = y) \\\\/ C",
                  "temporal": "timer <= 30",
                  "actions": ["atr1", "atr2"],
                  "campoQueNaoConhecemos": 42
                }
              ]
            }
            """;

    @Test
    void readsSystemInputsAndDecisions() {
        DecisionSet set = Nat2TestJsonReader.read(JSON);

        assertEquals("the_coffee_machine_system", set.system());
        assertEquals(2, set.inputs().size());
        assertEquals(List.of("x", "z"), set.inputs().get(0).values());

        Decision decision = set.decisions().get(0);
        assertEquals("the_coffee_machine_system#1", decision.id());
        assertEquals("REQ-001", decision.requirement());
        assertEquals(List.of("atr1", "atr2"), decision.actions());
    }

    @Test
    void temporalGuardIsJoinedWithAnd() {
        Decision decision = Nat2TestJsonReader.read(JSON).decisions().get(0);

        Cond ax = new Cond(new Predicate("A", "=", "x"));
        Cond by = new Cond(new Predicate("B", "=", "y"));
        Cond timer = new Cond(new Predicate("timer", "<=", "30"));
        assertEquals(new And(new Or(new And(ax, by), new Cond("C")), timer), decision.expression());
        assertTrue(decision.text().endsWith("/\\ timer <= 30"));
    }

    @Test
    void rejectsInvalidFiles() {
        assertThrows(IllegalArgumentException.class, () -> Nat2TestJsonReader.read("{ nao é json"));
        assertThrows(IllegalArgumentException.class, () -> Nat2TestJsonReader.read("{ \"decisions\": [] }"));
        assertThrows(IllegalArgumentException.class,
                () -> Nat2TestJsonReader.read("{ \"decisions\": [ { \"id\": \"d1\" } ] }"));
        assertThrows(IllegalArgumentException.class,
                () -> Nat2TestJsonReader.read("{ \"decisions\": [ { \"id\": \"d1\", \"guard\": \"A and\" } ] }"));
    }

    @Test
    void rejectsRepeatedIds() {
        String json = """
                { "decisions": [ { "id": "d1", "guard": "A" }, { "id": "d1", "guard": "B" } ] }
                """;
        assertThrows(IllegalArgumentException.class, () -> Nat2TestJsonReader.read(json));
    }
}
