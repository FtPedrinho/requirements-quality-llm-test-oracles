# -*- coding: utf-8 -*-
"""Gerador das consultas SMT-LIB do experimento C4 e executor do Z3 independente.

Escreve experimento/z3/*.smt2, roda o Z3 (independente do mcdc-z3) e grava os
arquivos .out e resumo-z3.csv. Respostas diferentes do esperado, unknown ou
timeout sao erro tecnico (exit code != 0).
"""
import csv
import subprocess
import sys
from pathlib import Path

Z3 = r"C:\Users\User\AppData\Roaming\Python\bin\z3.exe"
BASE = Path(__file__).resolve().parent / "z3"
BASE.mkdir(exist_ok=True)

ARQUIVOS = {}   # nome -> (conteudo, esperado[list[(rotulo, resposta)]])


def conflito(nome, descricao, decls, fundo, stmts, checks):
    """stmts: {rotulo: (citacao, formula)}; checks: [(rotulo, [stmts], esperado)]."""
    linhas = [f"; {descricao}", "(set-logic ALL)", ""]
    linhas += decls
    for r, (cit, f) in stmts.items():
        linhas.append(f"; {r}: {cit}")
    linhas.append("")
    for f in fundo:
        linhas.append(f"(assert {f})")
    esperado = []
    for rotulo, ids, esp in checks:
        linhas.append("")
        linhas.append(f'(echo "{rotulo}")')
        linhas.append("(push)")
        for i in ids:
            linhas.append(f"(assert {stmts[i][1]}) ; {i}")
        linhas.append("(check-sat)")
        linhas.append("(pop)")
        esperado.append((rotulo, esp))
    ARQUIVOS[nome] = ("\n".join(linhas) + "\n", esperado)


# ---------------------------------------------------------------- z01
def z01():
    L = ["; Consistencia aritmetica dos numeros declarados no texto C4 (nao prova fidelidade).",
         "(set-logic ALL)"]
    sistemas = {
        "vm": dict(req=5, comp=5, cond=21, comb=152, imp=4, tst=26, mut=152, eq=0, peg=152, conf=0),
        "tis": dict(req=17, comp=14, cond=69, comb=268, imp=4, tst=80, mut=450, eq=21, peg=428, conf=3),
        "npp": dict(req=11, comp=11, cond=29, comb=76, imp=1, tst=40, mut=146, eq=0, peg=146, conf=1),
        "tot": dict(req=33, comp=30, cond=119, comb=496, imp=9, tst=146, mut=748, eq=21, peg=726, conf=4),
    }
    for s, d in sistemas.items():
        for k in d:
            L.append(f"(declare-const {s}_{k} Int)")
    L.append("(declare-const escapou Int)")
    L.append("")
    for s, d in sistemas.items():
        for k, v in d.items():
            L.append(f"(assert (= {s}_{k} {v})) ; linha {s}, coluna {k}")
    esperado = []

    def check(rot, extra, esp="sat"):
        L.append("")
        L.append(f'(echo "{rot}")')
        L.append("(push)")
        for e in extra:
            L.append(f"(assert {e})")
        L.append("(check-sat)")
        L.append("(pop)")
        esperado.append((rot, esp))

    check("A01 linha Total = soma das tres linhas (todas as colunas)", [
        "(= tot_req (+ vm_req tis_req npp_req))", "(= tot_comp (+ vm_comp tis_comp npp_comp))",
        "(= tot_cond (+ vm_cond tis_cond npp_cond))", "(= tot_comb (+ vm_comb tis_comb npp_comb))",
        "(= tot_imp (+ vm_imp tis_imp npp_imp))", "(= tot_tst (+ vm_tst tis_tst npp_tst))",
        "(= tot_mut (+ vm_mut tis_mut npp_mut))", "(= tot_eq (+ vm_eq tis_eq npp_eq))",
        "(= tot_peg (+ vm_peg tis_peg npp_peg))", "(= tot_conf (+ vm_conf tis_conf npp_conf))"])
    check("A02 requisito completo: testes = condicoes + 1 (VM e NPP, todos os requisitos completos)", [
        "(= vm_comp vm_req)", "(= vm_tst (+ vm_cond vm_comp))", "(= npp_comp npp_req)",
        "(= npp_tst (+ npp_cond npp_comp))"])
    check("A03 TIS: detectados + equivalentes + escapou = total de mutantes, escapou = 1 (linha 407)", [
        "(= escapou 1)", "(= tis_mut (+ tis_peg tis_eq escapou))", "(= (- tot_mut tot_eq) 727)",
        "(= (- tot_mut tot_eq tot_peg) escapou)"])
    check("A04 TIS: com escapou = 0 (linha 409) a soma nao fecha (unsat esperado)", [
        "(= escapou 0)", "(= tis_mut (+ tis_peg tis_eq escapou))"], "unsat")
    check("A05 soma dos testes por classe listados = 171 e 34 arquivos", [
        "(= (+ 4 1 2  4 4  3 6  8 2 4 8 4 5 6 6 14 2 5 6  9 3 4 4 4  12 2 5 4 4 4  14 3 2 3) 171)"])
    check("A06 testes por modulo 78+24+34+35 = 171", ["(= (+ 78 24 34 35) 171)"])
    check("A07 arquivos de teste: 12 core + 7 transversais + 5 requisitos + 6 z3 + 4 cli = 34", [
        "(= (+ 12 7 5 6 4) 34)"])
    check("A08 mutacao por modulo: numeradores 319+140+269+196 = 924 e denominadores 333+145+295+256 = 1029", [
        "(= (+ 319 140 269 196) 924)", "(= (+ 333 145 295 256) 1029)"])
    check("A09 percentuais 95,5% (1911/2001), 90,3% (1170/1296), 89,8% (924/1029), 92,7% (924/997)", [
        "(> (/ 1911.0 2001.0) 0.9545)", "(< (/ 1911.0 2001.0) 0.9555)",
        "(> (/ 1170.0 1296.0) 0.9025)", "(< (/ 1170.0 1296.0) 0.9035)",
        "(> (/ 924.0 1029.0) 0.8975)", "(< (/ 924.0 1029.0) 0.8985)",
        "(> (/ 924.0 997.0) 0.9265)", "(< (/ 924.0 997.0) 0.9275)"])
    check("A10 limites: 2^20 = 1048576 ~ 1 milhao; 12 (Z3 linha a linha) < 20 (tabela) < 30 (direto)", [
        "(= (* 1024 1024) 1048576)", "(< 12 20)", "(< 20 30)"])
    ARQUIVOS["z01-aritmetica-documental"] = ("\n".join(L) + "\n", esperado)


z01()

# ---------------------------------------------------------------- conflitos
conflito("z02-conflito-truth-csv",
         "Conflito textual: conteudo do formato truth-csv (linhas 5 e 7 da fonte C4).",
         ["(declare-const truthcsv_tem_tabela_completa Bool)"], [],
         {"S1": ("linha 5: `truth-csv` | tabela-verdade inteira, combinacoes impossiveis marcadas",
                 "truthcsv_tem_tabela_completa"),
          "S2": ("linha 7: Regra de saida: truth-csv contem somente [...] independencia, nunca tabela-verdade",
                 "(not truthcsv_tem_tabela_completa)")},
         [("S1 isolada", ["S1"], "sat"), ("S2 isolada", ["S2"], "sat"), ("S1 e S2", ["S1", "S2"], "unsat")])

conflito("z03-conflito-sat-unsat",
         "Conflito textual: significado de unsat/sat para combinacoes impossiveis (linhas 81 e 83).",
         ["(declare-const q_unsat Bool)", "(declare-const impossivel Bool)"], ["q_unsat"],
         {"S1": ("linha 81: as que retornam `unsat` sao consideradas impossiveis e nao participam da analise",
                 "(= impossivel q_unsat)"),
          "S2": ("linha 83: resultados `unsat` representam combinacoes possiveis [...] `sat` impossiveis",
                 "(= impossivel (not q_unsat))")},
         [("S1 isolada (consulta com resposta unsat)", ["S1"], "sat"),
          ("S2 isolada (consulta com resposta unsat)", ["S2"], "sat"),
          ("S1 e S2", ["S1", "S2"], "unsat")])

conflito("z04-conflito-criterio-pares",
         "Conflito textual: criterio do par de independencia (linhas 85 e 87).",
         ["(declare-const decisao_precisa_mudar Bool)"], [],
         {"S1": ("linha 85: a condicao muda, o resultado da decisao tambem muda",
                 "decisao_precisa_mudar"),
          "S2": ("linha 87: o resultado da decisao pode permanecer igual [...] mudanca isolada e suficiente",
                 "(not decisao_precisa_mudar)")},
         [("S1 isolada", ["S1"], "sat"), ("S2 isolada", ["S2"], "sat"), ("S1 e S2", ["S1", "S2"], "unsat")])

conflito("z05-conflito-minimalidade",
         "Conflito textual: guloso x exato (linhas 53, 89 e 91; Z3RandomizedTest).",
         ["(declare-const minimo Int)", "(declare-const exato Int)", "(declare-const guloso Int)"],
         ["(<= minimo exato)", "(<= exato guloso)"],
         {"G": ("linha 91: a estrategia gulosa sempre encontra a suite globalmente minima", "(= guloso minimo)"),
          "X": ("linha 53: (aqui, 5 testes em vez de 6 da escolha gulosa)", "(and (= exato 5) (= guloso 6))"),
          "E": ("linha 89: com `--exact`, o Z3 procura suite de tamanho minimo", "(= exato minimo)"),
          "M": ("linha 91: --exact [...] pode retornar uma suite maior", "(> exato minimo)")},
         [("G isolada", ["G"], "sat"), ("X isolada", ["X"], "sat"), ("E isolada", ["E"], "sat"),
          ("M isolada", ["M"], "sat"), ("G e X", ["G", "X"], "unsat"), ("E e M", ["E", "M"], "unsat"),
          ("G, X, E e M", ["G", "X", "E", "M"], "unsat")])

conflito("z06-conflito-classificacao",
         "Conflito textual: redundante x bloqueada (linhas 93 e 95).",
         ["(declare-datatypes ((Rot 0)) (((redundante) (bloqueada))))",
          "(declare-const rot_sem_par_em_todas Rot)", "(declare-const rot_perde_par_por_impossiveis Rot)"], [],
         {"R1": ("linha 93: sem par mesmo considerando todas as combinacoes -> redundante; perde par por impossiveis -> bloqueada",
                 "(and (= rot_sem_par_em_todas redundante) (= rot_perde_par_por_impossiveis bloqueada))"),
          "R2": ("linha 95: sem par em qualquer cenario -> bloqueada; perde par so por impossiveis -> redundante",
                 "(and (= rot_sem_par_em_todas bloqueada) (= rot_perde_par_por_impossiveis redundante))"),
          "R3": ("linha 95: as duas classificacoes sao intercambiaveis e nao dependem do caso de ausencia de par",
                 "(= rot_sem_par_em_todas rot_perde_par_por_impossiveis)")},
         [("R1 isolada", ["R1"], "sat"), ("R2 isolada", ["R2"], "sat"), ("R3 isolada", ["R3"], "sat"),
          ("R1 e R2", ["R1", "R2"], "unsat"), ("R1 e R3", ["R1", "R3"], "unsat"),
          ("R1, R2 e R3", ["R1", "R2", "R3"], "unsat")])

conflito("z07-conflito-parenteses",
         "Conflito textual: defeitos de parenteses (linhas 407 e 409) e coluna Pegos da tabela (linha 291).",
         ["(declare-const escapam_agrupamento Int)", "(declare-const tis_nao_equivalentes Int)",
          "(declare-const tis_pegos Int)"], ["(= tis_nao_equivalentes 429)", "(= tis_pegos 428)",
                                            "(= escapam_agrupamento (- tis_nao_equivalentes tis_pegos))"],
         {"P1": ("linha 407: unico tipo de defeito sem garantia MC/DC; nos exemplos, 1 de 727 detectaveis escapou, desse tipo",
                 "(= escapam_agrupamento 1)"),
          "P2": ("linha 409: nenhum defeito de agrupamento pode escapar da suite", "(= escapam_agrupamento 0)")},
         [("P1 isolada (coerente com a tabela: 428 de 429)", ["P1"], "sat"),
          ("P2 isolada", ["P2"], "unsat"), ("P1 e P2", ["P1", "P2"], "unsat")])

conflito("z08-conflito-z3-arquitetura",
         "Conflito textual: Z3 como processo externo x biblioteca na JVM; timeout (linhas 119, 121, 123).",
         ["(declare-const z3_processo_externo Bool)", "(declare-const timeout_encerra_execucao Bool)"], [],
         {"A1": ("linha 119: O Z3 e executado como processo externo [...] limite de 60 segundos", "z3_processo_externo"),
          "A2": ("linha 123: Z3 e carregado como biblioteca dentro da JVM e nao e iniciado processo externo",
                 "(not z3_processo_externo)"),
          "T1": ("linha 119 e Z3ProcessTest: Z3 travado no limite de tempo encerra o processo", "timeout_encerra_execucao"),
          "T2": ("linha 123: o valor de 60 segundos [...] nunca encerra a execucao", "(not timeout_encerra_execucao)")},
         [("A1 isolada", ["A1"], "sat"), ("A2 isolada", ["A2"], "sat"), ("A1 e A2", ["A1", "A2"], "unsat"),
          ("T1 isolada", ["T1"], "sat"), ("T2 isolada", ["T2"], "sat"), ("T1 e T2", ["T1", "T2"], "unsat")])

conflito("z09-conflito-cobertura",
         "Conflito textual: cobertura de linhas x desvios sao a mesma metrica (linha 147) x tabela (linha 143).",
         ["(declare-const linhas Real)", "(declare-const desvios Real)"], [],
         {"C1": ("linha 143: linhas 95,5% (1911 de 2001); desvios 90,3% (1170 de 1296)",
                 "(and (= linhas (/ 1911.0 2001.0)) (= desvios (/ 1170.0 1296.0)))"),
          "C2": ("linha 147: cobertura de linhas e de desvios sao a mesma metrica [...] sempre o mesmo percentual",
                 "(= linhas desvios)")},
         [("C1 isolada", ["C1"], "sat"), ("C2 isolada", ["C2"], "sat"), ("C1 e C2", ["C1", "C2"], "unsat")])

conflito("z10-conflito-mutacao-pit",
         "Conflito textual: o que a nota de mutacao mede (linhas 149 e 151).",
         ["(declare-const mede_deteccao_de_defeitos Bool)"], [],
         {"M1": ("linha 149: mede se os testes revelam determinados defeitos, alem de medir se o codigo foi executado",
                 "mede_deteccao_de_defeitos"),
          "M2": ("linha 151: a nota de mutacao mede exclusivamente cobertura de linhas e nao tem relacao com deteccao de defeitos",
                 "(not mede_deteccao_de_defeitos)")},
         [("M1 isolada", ["M1"], "sat"), ("M2 isolada", ["M2"], "sat"), ("M1 e M2", ["M1", "M2"], "unsat")])

conflito("z11-conflito-regra-global",
         "Conflito textual: verificacao por modulo x agregada (linhas 165, 169 e 171).",
         ["(declare-const verificacao_por_modulo Bool)", "(declare-const modulo_abaixo_interrompe_build Bool)"],
         ["(= modulo_abaixo_interrompe_build verificacao_por_modulo)"],
         {"V1": ("linha 169: a cobertura e conferida pelo JaCoCo separadamente em cada modulo; abaixo da nota minima o build e interrompido",
                 "modulo_abaixo_interrompe_build"),
          "V2": ("linha 171: um modulo abaixo da nota minima nunca interrompe o build se a media geral for suficiente",
                 "(not modulo_abaixo_interrompe_build)")},
         [("V1 isolada", ["V1"], "sat"), ("V2 isolada", ["V2"], "sat"), ("V1 e V2", ["V1", "V2"], "unsat")])

# ---------------------------------------------------------------- z12 combinacoes dos casos DETERMINADOS
def z12():
    L = ["; Contagens combinatorias usadas nos casos DETERMINADOS (2^n sobre entradas distintas; linha 79).",
         "(set-logic ALL)"]
    esperado = []
    casos = [("D22 speed>100 /\\ mode=idle: 2 entradas -> 4", 2, 4), ("D23 B or (C and D): 3 entradas -> 8", 3, 8),
             ("D24 B or (not B and C): 2 entradas distintas -> 4", 2, 4),
             ("D26 20 entradas -> 1048576", 20, 1048576), ("D29 paridade de 3 entradas -> 8 combinacoes (= 8 testes)", 3, 8)]
    for rot, n, c in casos:
        L.append("")
        L.append(f'(echo "{rot}")')
        L.append("(push)")
        L.append(f"(declare-const n Int)(declare-const c Int)(assert (= n {n}))")
        L.append("(assert (= c " + ("(* " + " ".join(["2"] * n) + ")" if n > 1 else "2") + "))")
        L.append(f"(assert (= c {c}))")
        L.append("(check-sat)")
        L.append("(pop)")
        esperado.append((rot, "sat"))
    L.append("")
    L.append('(echo "D26 contra-prova: 2^20 diferente de 1000000 exato, mas na faixa de cerca de 1 milhao (1e6 a 1,1e6)")')
    L.append("(push)(declare-const c Int)(assert (= c 1048576))(assert (>= c 1000000))(assert (<= c 1100000))(check-sat)(pop)")
    esperado.append(("D26 contra-prova", "sat"))
    ARQUIVOS["z12-combinacoes-casos-determinados"] = ("\n".join(L) + "\n", esperado)


z12()


def main():
    resumo = []
    erro = False
    for nome, (conteudo, esperado) in ARQUIVOS.items():
        p = BASE / f"{nome}.smt2"
        p.write_text(conteudo, encoding="utf-8", newline="\n")
        r = subprocess.run([Z3, "-T:60", str(p)], capture_output=True, text=True, encoding="utf-8")
        out = r.stdout + r.stderr
        (BASE / f"{nome}.out").write_text(out, encoding="utf-8", newline="\n")
        respostas = [l.strip() for l in r.stdout.splitlines() if l.strip() in ("sat", "unsat", "unknown", "timeout")]
        ok = len(respostas) == len(esperado) and all(a == e[1] for a, e in zip(respostas, esperado)) and r.returncode == 0
        if not ok:
            erro = True
        for (rot, esp), obs in zip(esperado, respostas + [""] * len(esperado)):
            resumo.append([nome, rot, esp, obs, "OK" if obs == esp else "DIVERGENTE"])
    with open(BASE / "resumo-z3.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["arquivo", "verificacao", "esperado_pelo_autor", "resposta_z3", "estado"])
        w.writerows(resumo)
    print("arquivos:", len(ARQUIVOS), "verificacoes:", len(resumo), "erro:", erro)
    return 1 if erro else 0


if __name__ == "__main__":
    sys.exit(main())
