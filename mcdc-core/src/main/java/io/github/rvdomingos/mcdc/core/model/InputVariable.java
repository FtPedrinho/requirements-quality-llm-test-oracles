package io.github.rvdomingos.mcdc.core.model;

import java.util.List;

/**
 * Variável de entrada do sistema, como declarada no DFRS.
 *
 * @param name   nome da variável
 * @param type   tipo: bool, int, real ou enum
 * @param values valores possíveis, para enumerações; vazio nos outros tipos
 */
public record InputVariable(String name, String type, List<String> values) {

    public InputVariable {
        values = values == null ? List.of() : List.copyOf(values);
    }
}
