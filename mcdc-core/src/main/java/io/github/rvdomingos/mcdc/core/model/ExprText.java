package io.github.rvdomingos.mcdc.core.model;

/** Escreve uma expressão como texto, com parênteses só onde a precedência exige (not > and > or). */
public final class ExprText {

    private ExprText() {
    }

    public static String format(Expr expr) {
        return switch (expr) {
            case Cond c -> c.id();
            case Not(var operand) -> "not " + (operand instanceof Cond ? format(operand) : "(" + format(operand) + ")");
            case And(var left, var right) -> inAnd(left) + " and " + inAnd(right);
            case Or(var left, var right) -> format(left) + " or " + format(right);
        };
    }

    private static String inAnd(Expr expr) {
        return expr instanceof Or ? "(" + format(expr) + ")" : format(expr);
    }
}
