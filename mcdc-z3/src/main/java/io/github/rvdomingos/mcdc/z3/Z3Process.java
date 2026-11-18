package io.github.rvdomingos.mcdc.z3;

import java.io.IOException;
import java.io.OutputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/** Conversa com o executável do Z3 por SMT-LIB e lê as respostas. */
final class Z3Process {

    static final long TIMEOUT_SECONDS = 60;

    private Z3Process() {
    }

    /** Roda o script inteiro e devolve tudo o que o Z3 escreveu. */
    static String run(String command, String script) {
        return run(command, script, TIMEOUT_SECONDS);
    }

    /** A saída é lida em paralelo: assim o limite de tempo vale mesmo quando o Z3 trava sem fechar a saída. */
    static String run(String command, String script, long timeoutSeconds) {
        Process process;
        try {
            process = new ProcessBuilder(command, "-in", "-smt2").redirectErrorStream(true).start();
        } catch (IOException e) {
            throw new IllegalStateException("Z3 não encontrado (" + command + "). Instale com: brew install z3");
        }
        CompletableFuture<String> output = CompletableFuture.supplyAsync(() -> {
            try {
                return new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        });
        try {
            IOException writeError = null;
            try (OutputStream in = process.getOutputStream()) {
                in.write(script.getBytes(StandardCharsets.UTF_8));
            } catch (IOException e) {
                writeError = e;
            }
            if (!process.waitFor(timeoutSeconds, TimeUnit.SECONDS)) {
                process.destroyForcibly();
                throw new IllegalStateException("O Z3 não respondeu em " + timeoutSeconds + " segundos");
            }
            String text = output.get(timeoutSeconds, TimeUnit.SECONDS);
            if (writeError != null) {
                throw new IllegalStateException("Falha ao conversar com o Z3: " + writeError.getMessage() + " " + text.strip());
            }
            return text;
        } catch (InterruptedException e) {
            process.destroyForcibly();
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Interrompido esperando o Z3");
        } catch (ExecutionException | TimeoutException e) {
            throw new IllegalStateException("Falha ao conversar com o Z3: " + e.getCause());
        }
    }

    /** Respostas de check-sat; qualquer (error ...) vira exceção. */
    static List<String> atoms(String output) {
        List<String> atoms = new ArrayList<>();
        for (Object item : SExpr.parseAll(output)) {
            failOnError(item);
            if (item instanceof String atom) {
                atoms.add(atom);
            }
        }
        return atoms;
    }

    /** Listas de get-value, na ordem em que foram pedidas. */
    @SuppressWarnings("unchecked")
    static List<List<Object>> valueLists(String output) {
        List<List<Object>> lists = new ArrayList<>();
        for (Object item : SExpr.parseAll(output)) {
            failOnError(item);
            if (item instanceof List<?> list) {
                lists.add((List<Object>) list);
            }
        }
        return lists;
    }

    /** Átomos e listas, na ordem: "sat"/"unsat" seguidos dos get-value da mesma consulta. */
    static List<Object> all(String output) {
        List<Object> items = SExpr.parseAll(output);
        items.forEach(Z3Process::failOnError);
        return items;
    }

    private static void failOnError(Object item) {
        if (item instanceof List<?> list && !list.isEmpty() && "error".equals(list.get(0))) {
            throw new IllegalStateException("Erro do Z3: " + list.get(1));
        }
    }

    /** Se o executável responde; usado pelos testes para pular quando o Z3 não está instalado. */
    static boolean isAvailable(String command) {
        try {
            Process process = new ProcessBuilder(command, "--version").redirectErrorStream(true).start();
            process.getInputStream().readAllBytes();
            return process.waitFor(10, TimeUnit.SECONDS) && process.exitValue() == 0;
        } catch (IOException e) {
            return false;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
}
