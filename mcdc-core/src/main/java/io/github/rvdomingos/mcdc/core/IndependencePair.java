package io.github.rvdomingos.mcdc.core;

/**
 * Dois vetores que mostram o efeito independente de uma condição.
 *
 * @param condition  condição analisada
 * @param whenTrue   vetor em que a condição é verdadeira
 * @param whenFalse  vetor em que a condição é falsa
 */
public record IndependencePair(String condition, TestVector whenTrue, TestVector whenFalse) {

    /** Os dois vetores diferem só na entrada da condição: o par também vale em causa única. */
    public boolean isUniqueCause() {
        return Integer.bitCount(whenTrue.index() ^ whenFalse.index()) == 1;
    }

    @Override
    public String toString() {
        return "(" + whenTrue.name() + ", " + whenFalse.name() + ")";
    }
}
