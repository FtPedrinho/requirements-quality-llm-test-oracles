package io.github.rvdomingos.mcdc.z3;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.PosixFilePermissions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledOnOs;
import org.junit.jupiter.api.condition.OS;
import org.junit.jupiter.api.io.TempDir;

/** Robustez da conversa com o Z3, com executáveis falsos no lugar dele. */
@DisabledOnOs(OS.WINDOWS)
class Z3ProcessTest {

    private static String fake(Path dir, String body) throws IOException {
        Path script = dir.resolve("z3-falso");
        Files.writeString(script, "#!/bin/sh\n" + body + "\n");
        Files.setPosixFilePermissions(script, PosixFilePermissions.fromString("rwxr-xr-x"));
        return script.toString();
    }

    @Test
    void stopsWhenZ3HangsWithoutClosingItsOutput(@TempDir Path dir) throws IOException {
        String hanging = fake(dir, "exec sleep 30");
        long start = System.nanoTime();
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> Z3Process.run(hanging, "(check-sat)\n", 1));
        long seconds = (System.nanoTime() - start) / 1_000_000_000L;
        assertTrue(e.getMessage().contains("não respondeu"), e.getMessage());
        assertTrue(seconds < 10, "esperou " + seconds + " s");
    }

    @Test
    void readsLargeOutputsWithoutBlocking(@TempDir Path dir) throws IOException {
        // mais saída do que cabe no buffer do pipe: só funciona se a leitura correr em paralelo
        String chatty = fake(dir, "cat > /dev/null; i=0; while [ $i -lt 20000 ]; do echo sat; i=$((i+1)); done");
        String output = Z3Process.run(chatty, "(check-sat)\n".repeat(1000), 20);
        assertEquals(20000, Z3Process.atoms(output).size());
    }

    @Test
    void missingExecutableHasAClearMessage() {
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> Z3Process.run("/caminho/que/nao/existe/z3", "(check-sat)\n"));
        assertTrue(e.getMessage().contains("Z3 não encontrado"), e.getMessage());
    }

    @Test
    void errorAnswersBecomeExceptions(@TempDir Path dir) throws IOException {
        String failing = fake(dir, "cat > /dev/null; echo '(error \"line 1: unknown constant x\")'");
        String output = Z3Process.run(failing, "(assert x)\n", 20);
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> Z3Process.atoms(output));
        assertTrue(e.getMessage().contains("unknown constant"), e.getMessage());
    }
}
