package io.github.rvdomingos.mcdc.core.model;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Optional;
import org.junit.jupiter.api.Test;

class ActionTest {

    @Test
    void readsAssignments() {
        assertEquals(Optional.of(new Action("the_system_mode", "choice")), Action.parse("the_system_mode := choice"));
        assertEquals(Optional.of(new Action("t", "0")), Action.parse("  t:=0 "));
        assertTrue(Action.parse("liga o alarme").isEmpty());
    }

    @Test
    void contradictsOnlyWithDifferentValuesOnTheSameVariable() {
        Action on = new Action("mode", "true");
        assertTrue(on.contradicts(new Action("mode", "false")));
        assertFalse(on.contradicts(new Action("mode", "TRUE")));
        assertFalse(on.contradicts(new Action("other", "false")));
        // números comparados como números
        assertFalse(new Action("timer", "0").contradicts(new Action("timer", "0.0")));
    }
}
