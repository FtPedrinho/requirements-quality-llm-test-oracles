package io.github.rvdomingos.mcdc.core.model;

import java.util.List;

/**
 * Decisão de um requisito, pronta para análise.
 *
 * @param requirement requisito de origem; null quando não informado
 * @param text        expressão como foi escrita, para os relatórios
 * @param actions     o que o sistema faz quando a decisão é verdadeira
 */
public record Decision(String id, String requirement, String text, Expr expression, List<String> actions) {

    public Decision {
        actions = actions == null ? List.of() : List.copyOf(actions);
    }
}
