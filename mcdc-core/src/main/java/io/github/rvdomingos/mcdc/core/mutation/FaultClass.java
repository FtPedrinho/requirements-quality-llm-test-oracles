package io.github.rvdomingos.mcdc.core.mutation;

/** Tipos de falha em expressões booleanas estudados por Kapoor e Bowen e por Hayhurst e Veerhusen. */
public enum FaultClass {
    ORF("troca de operador"),
    ENF("negação de subexpressão"),
    VNF("negação de variável"),
    ASF("parênteses deslocados"),
    MVF("variável ausente"),
    VRF("troca de variável");

    private final String description;

    FaultClass(String description) {
        this.description = description;
    }

    public String description() {
        return description;
    }
}
