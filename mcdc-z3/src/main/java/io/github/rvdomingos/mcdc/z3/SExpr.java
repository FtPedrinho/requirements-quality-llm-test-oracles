package io.github.rvdomingos.mcdc.z3;

import java.util.ArrayList;
import java.util.List;

/** Leitor mínimo das respostas do Z3: átomos viram String, listas viram List. */
final class SExpr {

    private final String text;
    private int pos;

    private SExpr(String text) {
        this.text = text;
    }

    /** Todas as expressões da saída, na ordem: "sat", "unsat", listas de get-value, erros. */
    static List<Object> parseAll(String text) {
        SExpr parser = new SExpr(text);
        List<Object> result = new ArrayList<>();
        parser.skipSpaces();
        while (parser.pos < text.length()) {
            result.add(parser.next());
            parser.skipSpaces();
        }
        return result;
    }

    private Object next() {
        char c = text.charAt(pos);
        if (c == '(') {
            pos++;
            List<Object> list = new ArrayList<>();
            skipSpaces();
            while (pos < text.length() && text.charAt(pos) != ')') {
                list.add(next());
                skipSpaces();
            }
            pos++; // ')'
            return list;
        }
        int start = pos;
        if (c == '|' || c == '"') {
            int end = text.indexOf(c, pos + 1);
            pos = end < 0 ? text.length() : end + 1;
            return text.substring(start, pos);
        }
        while (pos < text.length() && !Character.isWhitespace(text.charAt(pos))
                && text.charAt(pos) != '(' && text.charAt(pos) != ')') {
            pos++;
        }
        return text.substring(start, pos);
    }

    private void skipSpaces() {
        while (pos < text.length() && Character.isWhitespace(text.charAt(pos))) {
            pos++;
        }
    }
}
