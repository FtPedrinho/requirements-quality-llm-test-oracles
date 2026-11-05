package io.github.rvdomingos.mcdc.requirements;

import io.github.rvdomingos.mcdc.core.model.And;
import io.github.rvdomingos.mcdc.core.model.Cond;
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.core.model.Not;
import io.github.rvdomingos.mcdc.core.model.Or;
import io.github.rvdomingos.mcdc.core.model.Predicate;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/**
 * Lê expressões como "(A and B) or not C" e "speed > 100 /\ mode = idle".
 * Aceita and, &amp;&amp; ou {@code /\}; or, || ou {@code \/}; not ou !.
 *
 * <pre>
 * expr       := termo ( "or" termo )*
 * termo      := fator ( "and" fator )*
 * fator      := "not" fator | "(" expr ")" | comparacao | IDENT
 * comparacao := IDENT OP VALOR        OP: = == != &lt; &lt;= &gt; &gt;=
 * </pre>
 */
public final class ExpressionParser {

    private static final Set<String> KEYWORDS = Set.of("and", "or", "not");
    private static final Set<String> OPERATORS = Set.of("=", "!=", "<", "<=", ">", ">=");

    private final List<String> tokens;
    private int pos;

    private ExpressionParser(String text) {
        this.tokens = tokenize(text);
    }

    public static Expr parse(String text) {
        var parser = new ExpressionParser(text);
        Expr expr = parser.expr();
        if (parser.pos < parser.tokens.size()) {
            throw new IllegalArgumentException("Sobrou texto na expressão: " + parser.tokens.get(parser.pos));
        }
        return expr;
    }

    private Expr expr() {
        Expr left = term();
        while (accept("or")) {
            left = new Or(left, term());
        }
        return left;
    }

    private Expr term() {
        Expr left = factor();
        while (accept("and")) {
            left = new And(left, factor());
        }
        return left;
    }

    private Expr factor() {
        if (accept("not")) {
            return new Not(factor());
        }
        if (accept("(")) {
            Expr inner = expr();
            if (!accept(")")) {
                throw new IllegalArgumentException("Faltou fechar parêntese");
            }
            return inner;
        }
        String name = word("uma condição");
        if (pos < tokens.size() && OPERATORS.contains(tokens.get(pos))) {
            String operator = tokens.get(pos++);
            String value = word("um valor depois de " + operator);
            return new Cond(new Predicate(name, operator, value));
        }
        return new Cond(name);
    }

    /** Consome um nome ou valor; parênteses, operadores e palavras-chave não servem. */
    private String word(String expected) {
        if (pos >= tokens.size()) {
            throw new IllegalArgumentException("Expressão incompleta: esperava " + expected);
        }
        String token = tokens.get(pos);
        if (KEYWORDS.contains(token) || OPERATORS.contains(token) || token.equals("(") || token.equals(")")) {
            throw new IllegalArgumentException("Esperava " + expected + ", encontrei: " + token);
        }
        pos++;
        return token;
    }

    private boolean accept(String token) {
        if (pos < tokens.size() && tokens.get(pos).equals(token)) {
            pos++;
            return true;
        }
        return false;
    }

    private static List<String> tokenize(String text) {
        List<String> tokens = new ArrayList<>();
        int i = 0;
        while (i < text.length()) {
            char c = text.charAt(i);
            if (Character.isWhitespace(c)) {
                i++;
            } else if (c == '(' || c == ')') {
                tokens.add(String.valueOf(c));
                i++;
            } else if (text.startsWith("&&", i) || text.startsWith("/\\", i)) {
                tokens.add("and");
                i += 2;
            } else if (text.startsWith("||", i) || text.startsWith("\\/", i)) {
                tokens.add("or");
                i += 2;
            } else if (text.startsWith("!=", i) || text.startsWith("<=", i) || text.startsWith(">=", i)) {
                tokens.add(text.substring(i, i + 2));
                i += 2;
            } else if (text.startsWith("==", i)) {
                tokens.add("=");
                i += 2;
            } else if (c == '=' || c == '<' || c == '>') {
                tokens.add(String.valueOf(c));
                i++;
            } else if (c == '!') {
                tokens.add("not");
                i++;
            } else if (isWordChar(c) || (c == '-' && i + 1 < text.length() && Character.isDigit(text.charAt(i + 1)))) {
                // nomes e valores; o '-' só entra no começo de um número negativo
                int start = i;
                i++;
                while (i < text.length() && isWordChar(text.charAt(i))) {
                    i++;
                }
                String word = text.substring(start, i);
                String lower = word.toLowerCase(Locale.ROOT);
                tokens.add(KEYWORDS.contains(lower) ? lower : word);
            } else {
                throw new IllegalArgumentException("Caractere inválido '" + c + "' na posição " + i);
            }
        }
        return tokens;
    }

    private static boolean isWordChar(char c) {
        return Character.isLetterOrDigit(c) || c == '_' || c == '.';
    }
}
