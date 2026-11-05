package io.github.rvdomingos.mcdc.core.model;

import java.math.BigDecimal;
import java.util.Map;

/**
 * O que uma condição afirma sobre uma variável, ex.: {@code speed > 100}.
 *
 * @param variable variável comparada
 * @param operator um de =, !=, <, <=, >, >=
 * @param value    valor comparado, como texto: número, true/false ou nome de um valor de enumeração
 */
public record Predicate(String variable, String operator, String value) {

    /**
     * Se o predicado vale para valores concretos, ex.: speed = 101. O valor comparado pode ser outra
     * variável do mapa. Números são comparados como números; o resto, como texto (true/false sem
     * diferenciar maiúsculas).
     */
    public boolean holds(Map<String, String> values) {
        String actual = values.get(variable);
        if (actual == null) {
            throw new IllegalArgumentException("Sem valor para a variável " + variable);
        }
        String expected = values.getOrDefault(value, value);
        BigDecimal a = number(actual);
        BigDecimal b = number(expected);
        if (a != null && b != null) {
            int c = a.compareTo(b);
            return switch (operator) {
                case "=" -> c == 0;
                case "!=" -> c != 0;
                case "<" -> c < 0;
                case "<=" -> c <= 0;
                case ">" -> c > 0;
                case ">=" -> c >= 0;
                default -> throw new IllegalArgumentException("Operador desconhecido: " + operator);
            };
        }
        boolean equal = actual.equalsIgnoreCase(expected);
        return switch (operator) {
            case "=" -> equal;
            case "!=" -> !equal;
            default -> throw new IllegalArgumentException(
                    "Comparação " + operator + " precisa de números: " + variable + " = " + actual);
        };
    }

    private static BigDecimal number(String text) {
        try {
            return new BigDecimal(text);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    @Override
    public String toString() {
        return variable + " " + operator + " " + value;
    }
}
