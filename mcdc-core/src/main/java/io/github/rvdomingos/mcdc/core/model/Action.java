package io.github.rvdomingos.mcdc.core.model;

import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Uma ação de requisito na forma de atribuição, ex.: {@code the_system_mode := choice}. */
public record Action(String variable, String value) {

    private static final Pattern ASSIGNMENT = Pattern.compile("^\\s*([^\\s:=]+)\\s*:=\\s*(.+?)\\s*$");

    /** Lê "x := v"; vazio quando o texto não é uma atribuição. */
    public static Optional<Action> parse(String text) {
        Matcher m = ASSIGNMENT.matcher(text);
        return m.matches() ? Optional.of(new Action(m.group(1), m.group(2))) : Optional.empty();
    }

    /** Se as duas ações escrevem valores diferentes na mesma variável. */
    public boolean contradicts(Action other) {
        return variable.equals(other.variable) && !sameValue(value, other.value);
    }

    /** Números comparados como números (0 e 0.0 são iguais); o resto, como texto. */
    private static boolean sameValue(String a, String b) {
        try {
            return new java.math.BigDecimal(a).compareTo(new java.math.BigDecimal(b)) == 0;
        } catch (NumberFormatException e) {
            return a.equalsIgnoreCase(b);
        }
    }

    @Override
    public String toString() {
        return variable + " := " + value;
    }
}
