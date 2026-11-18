package io.github.rvdomingos.mcdc.cli;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * Desempenho com o Z3 (RNF09), pelo mesmo caminho da linha de comando, sem contar a partida do Java. Os limites
 * têm folga de cerca de 10 vezes sobre o tempo medido; o tempo de cada caso aparece na saída do teste.
 */
class SystemsPerformanceTest {

    /** Análise completa de um sistema de exemplo: Z3, mutação e relatório. */
    private static final double MAX_SECONDS_SYSTEM = 3.0;
    /** Verificação entre os requisitos de um sistema. */
    private static final double MAX_SECONDS_VERIFY = 3.0;
    /** Modo direto acima do limite da tabela. */
    private static final double MAX_SECONDS_DIRECT = 10.0;

    private static final Path EXAMPLES = Path.of("..", "exemplos");

    @BeforeAll
    static void requiresZ3() {
        assumeTrue(Z3FeasibilityChecker.isAvailable("z3"), "z3 não instalado; testes pulados");
    }

    private static void timed(String label, double maxSeconds, String... args) {
        long start = System.nanoTime();
        int code = Main.run(args);
        double seconds = (System.nanoTime() - start) / 1e9;
        System.out.printf("desempenho: %s em %.2f s (limite %.1f s)%n", label, seconds, maxSeconds);
        assertTrue(code == Main.OK || code == Main.UNCOVERED, label + ": código de saída " + code);
        assertTrue(seconds < maxSeconds, label + " levou " + seconds + " s");
    }

    @ParameterizedTest(name = "{0}")
    @ValueSource(strings = {"vm", "tis", "npp"})
    void eachExampleSystem(String system, @TempDir Path dir) {
        Path source = EXAMPLES.resolve(system + "-decisoes.json");
        assumeTrue(Files.exists(source), "sistema de exemplo não encontrado");
        timed(system + ": análise com Z3, fronteiras e mutação", MAX_SECONDS_SYSTEM, "analyze", "--json", source.toString(),
                "--z3", "--boundary", "--mutation", "--format", "json", "-o", dir.resolve("r.json").toString());
        timed(system + ": busca exata", MAX_SECONDS_SYSTEM, "analyze", "--json", source.toString(),
                "--z3", "--exact", "--format", "json", "-o", dir.resolve("e.json").toString());
        timed(system + ": verificação entre requisitos", MAX_SECONDS_VERIFY, "verify", "--json", source.toString(),
                "--format", "json", "-o", dir.resolve("v.json").toString());
    }

    @Test
    void directModeBeyondTheTable(@TempDir Path dir) {
        // 26 comparações sobre variáveis diferentes: acima das 20 entradas da tabela inteira
        List<String> parts = new ArrayList<>();
        for (int i = 0; i < 26; i++) {
            parts.add("x" + i + " > " + i);
        }
        timed("modo direto, 26 entradas", MAX_SECONDS_DIRECT, "analyze", String.join(" and ", parts), "--z3",
                "--format", "json", "-o", dir.resolve("d.json").toString());
    }
}
