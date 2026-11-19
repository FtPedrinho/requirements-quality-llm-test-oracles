package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import static org.junit.jupiter.api.Assertions.fail;

import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class C2ComplementarySuiteTest {

    @Test
    void validCsvCheckUsesObservedInputFormat(@TempDir Path dir) throws Exception {
        Path csv = dir.resolve("tests.csv");
        Path report = dir.resolve("check.txt");
        Files.writeString(csv, """
                test,input,value,expected_outcome
                T1,A,true,true
                T1,B,true,true
                T2,A,false,false
                T2,B,true,false
                T3,A,true,false
                T3,B,false,false
                """);

        assertEquals(Main.OK, Main.run(new String[] {
                "check", "A and B", "--tests", csv.toString(), "-o", report.toString()
        }));
        assertTrue(Files.readString(report).contains("Cobertura MC/DC"));
    }

    @Test
    void repeatedInputOccurrencesAreDistinguishedInJson(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("repeated.json");
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", "(A and B) or (not A and C)", "--unique-cause",
                "--format", "json", "-o", report.toString()
        }));
        String json = Files.readString(report);
        assertTrue(json.contains("A#1"));
        assertTrue(json.contains("A#2"));
    }

    @Test
    void infeasibleConstraintIsReportedAsUncovered(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("infeasible.json");
        assertEquals(Main.UNCOVERED, Main.run(new String[] {
                "analyze", "A", "--constraint", "not A", "--format", "json", "-o", report.toString()
        }));
        assertTrue(Files.readString(report).contains("INFEASIBLE"));
    }

    @Test
    void defaultSuiteIsReportedAsGreedy(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("greedy.json");
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", "((E or D) and (not A or D)) or B",
                "--format", "json", "-o", report.toString()
        }));
        assertTrue(Files.readString(report).contains("\"suiteMethod\" : \"GREEDY\""));
    }

    @Test
    void exactSuiteIsNoLargerThanGreedy(@TempDir Path dir) throws Exception {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        Path greedy = dir.resolve("greedy.json");
        Path exact = dir.resolve("exact.json");
        String expression = "((E or D) and (not A or D)) or B";
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", expression, "--format", "json", "-o", greedy.toString()
        }));
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", expression, "--exact", "--format", "json", "-o", exact.toString()
        }));
        assertTrue(testCount(exact) <= testCount(greedy));
        assertTrue(Files.readString(exact).contains("\"suiteMethod\" : \"EXACT\""));
    }

    @Test
    void mutationOptionReportsObservedScore(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("mutation.json");
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", "A and (B or C)", "--mutation", "--format", "json", "-o", report.toString()
        }));
        String json = Files.readString(report);
        assertTrue(json.contains("\"mutation\""));
        assertTrue(json.contains("\"score\""));
        assertTrue(json.contains("\"survivors\""));
    }

    @Test
    void compatibleOverlapDoesNotReturnConflict(@TempDir Path dir) throws Exception {
        Path source = dir.resolve("compatible.json");
        Path report = dir.resolve("verify.json");
        Files.writeString(source, """
                {"system":"s","decisions":[
                  {"id":"s#1","requirement":"REQ1","guard":"A","actions":["mode := weak"]},
                  {"id":"s#2","requirement":"REQ2","guard":"A or B","actions":["mode := weak"]}
                ]}
                """);
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "Z3 not installed");
        assertEquals(Main.OK, Main.run(new String[] {
                "verify", "--json", source.toString(), "--format", "json", "-o", report.toString()
        }));
        assertTrue(Files.readString(report).contains("\"compatibleOverlaps\""));
    }

    @Disabled("C2 não define nem oferece meio determinístico de provocar Z3 UNKNOWN")
    @Test
    void z3UnknownResultCannotBeSpecifiedFromC2() {
        fail("Não existe oráculo C2 defensável para o resultado UNKNOWN.");
    }

    @Test
    void truthCsvContainsOneRecordPerBooleanCombination(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("truth.csv");
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", "A and B", "--format", "truth-csv", "-o", report.toString()
        }));
        String csv = Files.readString(report);
        assertTrue(csv.startsWith("decision,requirement,row,A,B,outcome,feasible,in_suite,demonstrates,concrete_values"));
        assertEquals(5, csv.lines().count());
    }

    @Test
    void textReportTruncatesLongPairLists(@TempDir Path dir) throws Exception {
        Path report = dir.resolve("pairs.txt");
        assertEquals(Main.OK, Main.run(new String[] {
                "analyze", "A and (B or C or D or E or F)", "-o", report.toString()
        }));
        assertTrue(Files.readString(report).contains("... ("));
    }

    private static long testCount(Path report) throws Exception {
        String json = Files.readString(report);
        int start = json.indexOf("\"minimalSuite\"");
        int open = json.indexOf('[', start);
        int close = json.indexOf(']', open);
        if (start < 0 || open < 0 || close < 0) {
            throw new IllegalStateException("minimalSuite ausente no relatório JSON");
        }
        String contents = json.substring(open + 1, close).trim();
        return contents.isEmpty() ? 0 : contents.split("\\},\\s*\\{").length;
    }
}
