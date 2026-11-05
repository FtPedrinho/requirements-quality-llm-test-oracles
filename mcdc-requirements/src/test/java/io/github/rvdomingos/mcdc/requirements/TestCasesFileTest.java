package io.github.rvdomingos.mcdc.requirements;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class TestCasesFileTest {

    @Test
    void readsTestsGroupedByDecision() {
        TestCasesFile.Contents contents = TestCasesFile.parse(List.of(
                "decision,test,input,value,expected_outcome",
                "d1,T1,speed,101,T",
                "d1,T1,rain,false,T",
                "d2,T9,A,T,"), "teste");

        assertTrue(contents.hasDecisionColumn());
        TestCasesFile.RawTest t1 = contents.byDecision().get("d1").get("T1");
        assertEquals(Map.of("speed", "101", "rain", "false"), t1.values());
        assertEquals(true, t1.expected());
        assertEquals(null, contents.byDecision().get("d2").get("T9").expected());
    }

    @Test
    void acceptsTheCsvExportedByTheTool() {
        TestCasesFile.Contents contents = TestCasesFile.parse(List.of(
                "decision,requirement,test,input,value,expected_outcome,demonstrates,concrete_values",
                "REQ,,V2,A,T,T,A; B,",
                "REQ,,V2,\"x, y\",F,T,A; B,"), "teste");

        assertEquals(Map.of("A", "T", "x, y", "F"), contents.byDecision().get("REQ").get("V2").values());
    }

    @Test
    void worksWithoutTheDecisionColumn() {
        TestCasesFile.Contents contents = TestCasesFile.parse(List.of("test,input,value", "T1,A,T"), "teste");
        assertFalse(contents.hasDecisionColumn());
    }

    @Test
    void rejectsMissingColumns() {
        assertThrows(IllegalArgumentException.class, () -> TestCasesFile.parse(List.of("test,value", "T1,T"), "teste"));
        assertThrows(IllegalArgumentException.class, () -> TestCasesFile.parse(List.of("test,input,value"), "teste"));
    }
}
