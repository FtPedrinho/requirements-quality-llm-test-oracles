package io.github.rvdomingos.mcdc.core;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Uma linha da tabela verdade. Os valores das entradas não são guardados: saem dos bits do índice
 * (bit 0 = verdadeira), e a lista de entradas é a mesma para todas as linhas. Assim 1 milhão de linhas
 * cabe em poucas dezenas de megabytes.
 *
 * @param index      posição na tabela, começando em 0
 * @param inputs     entradas da decisão, na ordem das colunas; compartilhada entre as linhas
 * @param outcome    resultado da decisão para esses valores
 * @param feasible   se a combinação é possível; linhas impossíveis não entram em pares
 * @param assignment valores concretos das variáveis que realizam a linha (ex.: speed = 101);
 *                   vazio quando não houve verificação de viabilidade
 */
public record TestVector(int index, List<String> inputs, boolean outcome, boolean feasible,
        Map<String, String> assignment) {

    public TestVector {
        assignment = assignment == null ? Map.of() : assignment;
    }

    /** Valor de uma entrada nesta linha. */
    public boolean value(String input) {
        int i = inputs.indexOf(input);
        if (i < 0) {
            throw new IllegalArgumentException("Entrada desconhecida: " + input);
        }
        return (index & (1 << (inputs.size() - 1 - i))) == 0;
    }

    /** Valor de cada entrada, na ordem das colunas. Montado a cada chamada; use {@link #value} em laços. */
    public Map<String, Boolean> values() {
        Map<String, Boolean> values = new LinkedHashMap<>();
        for (String input : inputs) {
            values.put(input, value(input));
        }
        return Collections.unmodifiableMap(values);
    }

    /** Nome usado nos relatórios: V1, V2, ... */
    public String name() {
        return "V" + (index + 1);
    }

    /** Valores das entradas como texto, ex.: "TTF". */
    public String bits() {
        return inputs.stream().map(input -> value(input) ? "T" : "F").collect(Collectors.joining());
    }
}
