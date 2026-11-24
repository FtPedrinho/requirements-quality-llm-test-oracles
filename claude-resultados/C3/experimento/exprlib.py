"""Avaliador independente de expressões lógicas usado pelo oráculo C3.

Escrito a partir do texto da fonte C3 (operadores, precedência "e antes de ou"),
sem consultar o SUT. Átomos são variáveis booleanas ou comparações
`nome op valor`. A tabela-verdade é montada sobre as entradas distintas, que
aqui são os átomos distintos (ver análise, seção 3, decisão A1).
"""
import re

OPS_AND = {"and", "&&", "/\\"}
OPS_OR = {"or", "||", "\\/"}
OPS_NOT = {"not", "!"}
CMP = ["==", "!=", "<=", ">=", "=", "<", ">"]

TOKEN = re.compile(r"\s*(\(|\)|&&|\|\||/\\|\\/|==|!=|<=|>=|=|<|>|!|-?[A-Za-z0-9_.#]+)")


def tokenize(s):
    pos, out = 0, []
    s = s.strip()
    while pos < len(s):
        m = TOKEN.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError(f"token inválido em {s[pos:]!r}")
        out.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    return out


class Parser:
    def __init__(self, s):
        self.t = tokenize(s)
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self, x=None):
        tok = self.peek()
        if tok is None or (x is not None and tok != x):
            raise ValueError(f"esperado {x!r}, obtido {tok!r}")
        self.i += 1
        return tok

    def parse(self):
        e = self.orx()
        if self.peek() is not None:
            raise ValueError(f"sobra {self.t[self.i:]}")
        return e

    def orx(self):
        e = self.andx()
        while self.peek() in OPS_OR:
            self.eat()
            e = ("or", e, self.andx())
        return e

    def andx(self):
        e = self.notx()
        while self.peek() in OPS_AND:
            self.eat()
            e = ("and", e, self.notx())
        return e

    def notx(self):
        if self.peek() in OPS_NOT:
            self.eat()
            return ("not", self.notx())
        if self.peek() == "(":
            self.eat("(")
            e = self.orx()
            self.eat(")")
            return e
        name = self.eat()
        if name in OPS_AND | OPS_OR | {")"}:
            raise ValueError("operando ausente")
        if self.peek() in CMP:
            op = self.eat()
            val = self.eat()
            return ("atom", f"{name} {op} {val}")
        return ("atom", name)


def parse(s):
    return Parser(s).parse()


def atoms_occ(e, acc=None):
    acc = [] if acc is None else acc
    if e[0] == "atom":
        acc.append(e[1])
    else:
        for x in e[1:]:
            atoms_occ(x, acc)
    return acc


def atoms(e):
    seen = []
    for a in atoms_occ(e):
        if a not in seen:
            seen.append(a)
    return seen


def ev(e, val):
    k = e[0]
    if k == "atom":
        return val[e[1]]
    if k == "not":
        return not ev(e[1], val)
    if k == "and":
        return ev(e[1], val) and ev(e[2], val)
    return ev(e[1], val) or ev(e[2], val)


def smt(e, names):
    k = e[0]
    if k == "atom":
        return names[e[1]]
    if k == "not":
        return f"(not {smt(e[1], names)})"
    return f"({k} {smt(e[1], names)} {smt(e[2], names)})"


def eval_atom_concrete(atom, values, types=None):
    """Avalia um átomo com valores concretos (bool, número ou enum)."""
    parts = atom.split()
    if len(parts) == 1:
        v = values[parts[0]]
        return _as_bool(v)
    name, op, lit = parts
    v = values[name]
    t = (types or {}).get(name)
    if t in ("int", "real") or _isnum(v) and _isnum(lit):
        a, b = float(v), float(lit)
    elif lit in ("true", "false") or t == "bool":
        a, b = _as_bool(v), _as_bool(lit)
    else:
        a, b = str(v), str(lit)
    return {"=": a == b, "==": a == b, "!=": a != b, "<": a < b, "<=": a <= b,
            ">": a > b, ">=": a >= b}[op]


def _isnum(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


def _as_bool(v):
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in ("t", "true", "1", "verdadeiro", "v"):
        return True
    if s in ("f", "false", "0", "falso"):
        return False
    raise ValueError(f"valor lógico inválido {v!r}")
