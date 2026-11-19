import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "experimentacao" / "experimentacao-1"
BASE = EXP / "mutation-testing"

CONFLICT_ORACLES = {"tis#2", "tis#3", "tis#4", "tis#6", "npp#5", "npp#8"}
NPP_OUTPUT_ORACLES = {"npp#9", "npp#10", "npp#11"}


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def metrics(items):
    equivalent = sum(item["classification"] == "EQUIVALENT" for item in items)
    unknown = sum(item["classification"] == "UNKNOWN" for item in items)
    killed = sum(item["killed"] == "YES" for item in items)
    survived = sum(item["survival"] == "SURVIVED" for item in items)
    tn = sum(item["classification"] == "EQUIVALENT" and item["killed"] == "NO" for item in items)
    fp = sum(item["classification"] == "EQUIVALENT" and item["killed"] == "YES" for item in items)
    recall = killed / (killed + survived) if (killed + survived) else None
    precision = killed / (killed + fp) if (killed + fp) else None
    f1 = (2 * precision * recall / (precision + recall)
          if precision is not None and recall is not None and (precision + recall)
          else None)
    ms_reported = 100 * killed / (len(items) - equivalent) if len(items) - equivalent else None
    ms_corrected = 100 * killed / (len(items) - equivalent - unknown) if len(items) - equivalent - unknown else None
    return {
        "total": len(items),
        "equivalent": equivalent,
        "unknown": unknown,
        "killed": killed,
        "survived": survived,
        "tp": killed,
        "tn": tn,
        "fp": fp,
        "fn": survived,
        "mutation_score_reported": ms_reported,
        "mutation_score_corrected": ms_corrected,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def main():
    audit_dir = BASE / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    mutants = json.loads((BASE / "mutants" / "mutants.json").read_text(encoding="utf-8"))
    original = read_csv(BASE / "execution" / "original-execution.csv")
    execution = read_csv(BASE / "execution" / "mutant-execution.csv")
    test_cases = read_csv(EXP / "test-suites" / "generated-test-cases.csv")

    unique_ids = len({item["mutant_id"] for item in mutants})
    unique_keys = len({(row["mutant_id"], row["case_id"]) for row in execution})
    killed_from_json = {item["mutant_id"] for item in mutants if item["killed"] == "YES"}
    killed_from_csv = {row["mutant_id"] for row in execution if row["mutant_status"] == "KILL"}

    aggregate = metrics(mutants)
    system_groups = defaultdict(list)
    for item in mutants:
        system = item["system"]
        system_groups[system].append(item)

    reserved = CONFLICT_ORACLES | NPP_OUTPUT_ORACLES
    sensitivity = metrics([item for item in mutants if item["oracle_id"] not in reserved])
    full_sensitive = metrics([item for item in mutants if item["oracle_id"] in reserved])

    reserved_cases = [case for case in test_cases if case["Reserve"] != "Nenhuma"]
    npp_output_cases = [case for case in test_cases if "NPP-SAFETY" in case["Reserve"]]
    conflict_cases = [case for case in test_cases if "CONFLITO-POTENCIAL" in case["Reserve"]]

    rows = []
    for experiment in ("EXP0", "EXP1"):
        if experiment == "EXP0":
            total, equivalent, killed, survived, unknown = 981, 21, 894, 42, 24
        else:
            total, equivalent, killed, survived, unknown = (
                aggregate["total"], aggregate["equivalent"], aggregate["killed"],
                aggregate["survived"], aggregate["unknown"],
            )
        rows.append({
            "experimento": experiment,
            "condicao": "C1" if experiment == "EXP1" else "original",
            "metrica": "mutants",
            "valor": total,
            "denominador": "unique mutant IDs",
            "unidade": "mutante",
            "observacoes": "linhas brutas únicas por mutante",
        })
        rows.append({
            "experimento": experiment,
            "condicao": "C1" if experiment == "EXP1" else "original",
            "metrica": "mutation_score_reported",
            "valor": 100 * killed / (total - equivalent),
            "denominador": total - equivalent,
            "unidade": "mutante não equivalente",
            "observacoes": "não exclui UNKNOWN",
        })
        rows.append({
            "experimento": experiment,
            "condicao": "C1" if experiment == "EXP1" else "original",
            "metrica": "mutation_score_corrected",
            "valor": 100 * killed / (total - equivalent - unknown),
            "denominador": total - equivalent - unknown,
            "unidade": "mutante não equivalente avaliável",
            "observacoes": "exclui equivalent e unknown",
        })

    results_csv = EXP / "results-summary.csv"
    with results_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "experimento", "condicao", "sistema", "metrica", "valor",
            "denominador", "unidade", "observacoes",
        ])
        writer.writeheader()
        for row in rows:
            row.setdefault("sistema", "GERAL")
            writer.writerow(row)
        for system, items in sorted(system_groups.items()):
            values = metrics(items)
            for metric in ("total", "equivalent", "unknown", "killed", "survived",
                           "mutation_score_reported", "mutation_score_corrected",
                           "precision", "recall", "f1"):
                writer.writerow({
                    "experimento": "EXP1",
                    "condicao": "C1",
                    "sistema": system,
                    "metrica": metric,
                    "valor": values[metric],
                    "denominador": values["total"] - values["equivalent"] - (values["unknown"] if "score" in metric else 0),
                    "unidade": "mutante",
                    "observacoes": "calculado independentemente por sistema",
                })

    with (audit_dir / "aggregate-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(aggregate.keys()))
        writer.writeheader()
        writer.writerow(aggregate)

    summary = f"""# Auditoria independente - Experimento 1

## Totais

- Mutantes únicos: {unique_ids}
- Pares únicos mutante/caso no CSV: {unique_keys}
- Equivalentes: {aggregate['equivalent']}
- Mortos: {aggregate['killed']}
- Sobreviventes: {aggregate['survived']}
- UNKNOWN: {aggregate['unknown']}
- Casos do modelo original: {len(original)}
- Casos originais passaram: {sum(row['passed'] == 'TRUE' for row in original)}
- Casos originais não avaliáveis: {sum(row['passed'] == 'NON-EVALUABLE' for row in original)}

## Reprodutibilidade

Os mortos no JSON e no CSV são conjuntos equivalentes:

- JSON: {len(killed_from_json)}
- CSV: {len(killed_from_csv)}
- Igualdade dos conjuntos: {killed_from_json == killed_from_csv}

## Métricas corrigidas

- Mutation Score reportado: {aggregate['mutation_score_reported']:.6f}%
- Mutation Score corrigido: {aggregate['mutation_score_corrected']:.6f}%
- Precision: {aggregate['precision']:.12f}
- Recall: {aggregate['recall']:.12f}
- F1: {aggregate['f1']:.12f}

## Unidade de análise

Positivo = mutante não equivalente morto. Negativo = mutante equivalente. FN = mutante não equivalente sobrevivente.

Os 24 UNKNOWN não foram TP, TN, FP ou FN.

## Ressalvas

- Oráculos em pares potencialmente conflitantes: {len(CONFLICT_ORACLES)}
- Oráculos relacionados a saída NPP não declarada: {len(NPP_OUTPUT_ORACLES)}
- Oráculos diretamente afetados pela união das ressalvas: {len(reserved)}
- Casos com reserva: {len(reserved_cases)}
- Casos com conflito potencial: {len(conflict_cases)}
- Casos com saída NPP não declarada: {len(npp_output_cases)}
- Mutantes diretamente associados às ressalvas: {sum(item['oracle_id'] in reserved for item in mutants)}

## Sensibilidade

Excluídos da sensibilidade:

- os 9 oráculos diretamente associados às ressalvas.

Resultado sem unidades reservadas:

- Total: {sensitivity['total']}
- Equivalentes: {sensitivity['equivalent']}
- UNKNOWN: {sensitivity['unknown']}
- Mortos: {sensitivity['killed']}
- Sobreviventes: {sensitivity['survived']}
- Mutation Score corrigido: {sensitivity['mutation_score_corrected']:.6f}%

Resultado somente das unidades reservadas:

- Total: {full_sensitive['total']}
- Equivalentes: {full_sensitive['equivalent']}
- UNKNOWN: {full_sensitive['unknown']}
- Mortos: {full_sensitive['killed']}
- Sobreviventes: {full_sensitive['survived']}
- Mutation Score corrigido: {full_sensitive['mutation_score_corrected']:.6f}%
"""
    (audit_dir / "audit-summary.md").write_text(summary, encoding="utf-8")

    print(json.dumps({
        **aggregate,
        "unique_mutant_ids": unique_ids,
        "unique_mutant_cases": unique_keys,
        "reserved_oracles": len(reserved),
        "reserved_cases": len(reserved_cases),
        "reserved_mutants": sum(item["oracle_id"] in reserved for item in mutants),
        "sensitivity": sensitivity,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
