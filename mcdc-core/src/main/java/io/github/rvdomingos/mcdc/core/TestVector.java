package io.github.rvdomingos.mcdc.core;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Uma linha da tabela verdade. Os valores das entradas saem dos bits do índice (bit 0 = verdadeira),
 * o que deixa 1 milhão de linhas em poucas dezenas de megabytes.
 *
 * @param inputs     entradas da decisão, compartilhadas entre as linhas
 * @param feasible   se a combinação é possível; linhas impossíveis não entram em pares
 * @param assignment valores concretos que realizam a linha; vazio sem verificação de viabilidade
 */
public record TestVector(int index, List<String> inputs, boolean outcome, boolean feasible,
        Map<String, String> assignment) {

    public TestVector {
        assignment = assignment == null ? Map.of() : assignment;
    }

    public boolean value(String input) {
        int i = inputs.indexOf(input);
        if (i < 0) {
            throw new IllegalArgumentException("Entrada desconhecida: " + input);
        }
        return (index & (1 << (inputs.size() - 1 - i))) == 0;
    }

    /** Valor de cada entrada, montado a cada chamada; em laços, use {@link #value}. */
    public Map<String, Boolean> values() {
        Map<String, Boolean> values = new LinkedHashMap<>();
        for (String input : inputs) {
            values.put(input, value(input));
        }
        return Collections.unmodifiableMap(values);
    }

    /** Nome nos relatórios: V1, V2, ... */
    public String name() {
        return "V" + (index + 1);
    }

    /** Valores das entradas como texto, ex.: "TTF". */
    public String bits() {
        return inputs.stream().map(input -> value(input) ? "T" : "F").collect(Collectors.joining());
    }
}
