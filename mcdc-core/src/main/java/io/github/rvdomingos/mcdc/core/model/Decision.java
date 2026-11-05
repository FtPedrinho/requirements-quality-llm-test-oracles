package io.github.rvdomingos.mcdc.core.model;

import java.util.List;

/**
 * Decisão de um requisito, pronta para análise.
 *
 * @param id          identificador da decisão, ex.: "REQ-001" ou "the_coffee_machine_system#1"
 * @param requirement requisito de origem, para rastreabilidade; null quando não informado
 * @param text        expressão como foi escrita, para os relatórios
 * @param expression  expressão já lida
 * @param actions     o que o sistema faz quando a decisão é verdadeira; vazio quando não informado
 */
public record Decision(String id, String requirement, String text, Expr expression, List<String> actions) {

    public Decision {
        actions = actions == null ? List.of() : List.copyOf(actions);
    }
}
