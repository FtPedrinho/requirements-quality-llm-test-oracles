package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import java.util.List;
import org.junit.jupiter.api.Test;

class RequirementsFileTest {

    @Test
    void readsOneRequirementPerLineIgnoringCommentsAndBlankLines() {
        DecisionSet set = RequirementsFile.parse(List.of("# comentário", "", "REQ-1: A and B", "REQ-2: A or not B"), "teste");

        assertEquals(2, set.decisions().size());
        assertEquals("REQ-1", set.decisions().get(0).id());
        assertEquals("A or not B", set.decisions().get(1).text());
    }

    @Test
    void reportsTheRequirementWithASyntaxError() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> RequirementsFile.parse(List.of("REQ-1: A and"), "teste"));
        assertEquals("REQ-1: Expressão incompleta: esperava uma condição", e.getMessage());
    }

    @Test
    void rejectsLinesWithoutIdAndEmptyFiles() {
        assertThrows(IllegalArgumentException.class, () -> RequirementsFile.parse(List.of("A and B"), "teste"));
        assertThrows(IllegalArgumentException.class, () -> RequirementsFile.parse(List.of("# só comentário"), "teste"));
    }
}
