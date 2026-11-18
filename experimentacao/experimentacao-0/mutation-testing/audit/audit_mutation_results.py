import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "experimentacao" / "experimentacao-0" / "mutation-testing"
OUT = BASE / "audit"


def read_csv(name):
    with (BASE / name).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def percent(numerator, denominator):
    return None if denominator == 0 else 100 * numerator / denominator


def ratio(numerator, denominator):
    return None if denominator == 0 else numerator / denominator


def main():
    mutants = json.loads((BASE / "mutants" / "mutants.json").read_text(encoding="utf-8"))
    original = read_csv("execution/original-execution.csv")
    execution = read_csv("execution/mutant-execution.csv")

    classification = Counter(mutant["classification"] for mutant in mutants)
    survival = Counter(mutant["survival"] for mutant in mutants)
    killed = Counter(mutant["killed"] for mutant in mutants)

    unique_mutant_ids = len({mutant["mutant_id"] for mutant in mutants})
    unique_execution_keys = len({
        (row["mutant_id"], row["case_id"]) for row in execution
    })
    execution_status = Counter(row["mutant_status"] for row in execution)

    equivalent = classification["EQUIVALENT"]
    unknown = classification["UNKNOWN"]
    not_equivalent = classification["NON-EQUIVALENT"]
    killed_total = sum(mutant["killed"] == "YES" for mutant in mutants)
    survived_total = sum(mutant["survival"] == "SURVIVED" for mutant in mutants)

    original_passed = sum(row["passed"] == "TRUE" for row in original)
    original_not_evaluable = sum(row["passed"] == "NON-EVALUABLE" for row in original)

    reported_score = percent(killed_total, len(mutants) - equivalent)
    evaluable_score = percent(killed_total, len(mutants) - equivalent - unknown)
    precision = ratio(killed_total, killed_total)
    recall = ratio(killed_total, killed_total + survived_total)
    f1 = None if recall is None or precision is None or (precision + recall == 0) else (
        2 * precision * recall / (precision + recall)
    )

    execution_kill_mutants = {
        row["mutant_id"] for row in execution if row["mutant_status"] == "KILL"
    }
    json_kill_mutants = {
        mutant["mutant_id"] for mutant in mutants if mutant["killed"] == "YES"
    }

    (OUT / "audit-summary.md").write_text(
        rf"""# Auditoria independente dos cálculos

## Totais verificados

| Item | Quantidade |
|---|---:|
| Mutantes no JSON | {len(mutants)} |
| IDs únicos | {unique_mutant_ids} |
| Equivalentes | {equivalent} |
| Não equivalentes | {not_equivalent} |
| UNKNOWN | {unknown} |
| Mortos | {killed_total} |
| Sobreviventes | {survived_total} |
| Casos do modelo original | {len(original)} |
| Casos que passaram | {original_passed} |
| Casos não avaliáveis | {original_not_evaluable} |
| Linhas de execução de mutantes | {len(execution)} |
| Pares únicos mutante/caso | {unique_execution_keys} |

## Partição dos mutantes

\[
981 = 894 + 42 + 21 + 24
\]

As 981 entradas são únicas por `mutant_id`.

- Mortos: 894.
- Sobreviventes: 42.
- Equivalentes: 21.
- UNKNOWN ou não avaliáveis por erro de formalização: 24.

Não existe nenhuma categoria adicional.

## Mutation Score

Número reportado:

\[
MS = \frac{{894}}{{981-21}} = {reported_score:.6f}\%
\]

Partição metodologicamente corrigida, excluindo os 24 não avaliáveis:

\[
MS = \frac{{894}}{{981-21-24}} = \frac{{894}}{{936}} = {evaluable_score:.6f}\%
\]

Portanto, a fórmula reportada é aritmética para `{len(mutants) - equivalent}` denominador, mas não exclui os 24 mutantes não avaliáveis. O valor mais defensável nesta auditoria é **{evaluable_score:.6f}%**.

## Recall

Com mutante agregado:

- TP = 894;
- FN = 42;
- Positivos avaliáveis = 936.

\[
Recall = \frac{{894}}{{894+42}} = {recall:.12f}
\]

O Recall usa uma população coerente de mutantes não equivalentes avaliados. Os 24 UNKNOWN não são incluídos como falsos negativos.

## Precision

- FP = 0;
- TN = 21 equivalentes não mortos.

\[
Precision = \frac{{894}}{{894+0}} = {precision:.12f}
\]

## F1

\[
F1 = 2\times\frac{{1.000\times {recall:.12f}}}{{1.000+{recall:.12f}}} = {f1:.12f}
\]

O cálculo é reproduzível e matematicamente coerente, observando que TN não entra no F1 e UNKNOWN foi excluído.

## Casos não concretizados

O arquivo `execution/original-execution.csv` contém 152 linhas:

- 140 passaram;
- 12 ficaram com `passed=NON-EVALUABLE`.

Esses 12 pares não foram usados como TP, FP, TN ou FN. Não há evidência de que tenham sido reutilizados como mortes de mutantes.

Os 24 mutantes `NOT-EVALUABLE` são uma categoria separada. Não são os mesmos registros dos 12 pares não concretizados.

## Dupla contagem

- IDs de mutante únicos: {unique_mutant_ids}.
- Linhas mutante/caso únicas: {unique_execution_keys}.
- Linhas total de execução: {len(execution)}.
- Mutantes mortos pela coluna JSON: {len(json_kill_mutants)}.
- Mutantes mortos pelo CSV: {len(execution_kill_mutants)}.
- Conjunto morto JSON == conjunto morto CSV: {json_kill_mutants == execution_kill_mutants}.

Não foi encontrada dupla contagem dentro da agregação por mutante: mortes são calculadas por existência de pelo menos um caso `KILL`, não pela quantidade de linhas `KILL`.

## Reprodutibilidade

Os totais podem ser recomputados a partir de:

- `mutants/mutants.json`;
- `execution/original-execution.csv`;
- `execution/mutant-execution.csv`;
- `mutants/mutation-summary.csv`.

O registro JSON contém classificação, morte e sobrevivência por mutante. O CSV contém a evidência por execução.

## Conclusão

Os indicadores **matemáticos agregados podem ser considerados consistentes dentro da convenção reportada**. Porém, o relatório original não exclui os 24 mutantes UNKNOWN do denominador da Mutation Score, então o **93,125% reportado não é o Mutation Score mais metodologicamente defensável**.

A precisão de 1,000 é reproduzível, mas representa apenas ausência de falsos positivos identificados no conjunto; não prova correção semântica.

Classificação recomendada deste cálculo: **matematicamente consistente nas métricas TP/FP/TN/FN, mas com ressalva metodológica no denominador da Mutation Score e na separação explícita dos não avaliáveis**.
""",
        encoding="utf-8",
    )

    audit_csv = [
        {
            "metric": "total_mutants",
            "value": len(mutants),
            "definition": "IDs únicos no mutants.json",
        },
        {
            "metric": "equivalent",
            "value": equivalent,
            "definition": "classification == EQUIVALENT",
        },
        {
            "metric": "killed",
            "value": killed_total,
            "definition": "killed == YES",
        },
        {
            "metric": "survived",
            "value": survived_total,
            "definition": "survival == SURVIVED",
        },
        {
            "metric": "unknown",
            "value": unknown,
            "definition": "classification == UNKNOWN",
        },
        {
            "metric": "reported_mutation_score",
            "value": reported_score,
            "definition": "894 / (981 - 21)",
        },
        {
            "metric": "evaluated_mutation_score",
            "value": evaluable_score,
            "definition": "894 / (981 - 21 - 24)",
        },
        {
            "metric": "precision",
            "value": precision,
            "definition": "894 / (894 + 0)",
        },
        {
            "metric": "recall",
            "value": recall,
            "definition": "894 / (894 + 42)",
        },
        {
            "metric": "f1",
            "value": f1,
            "definition": "2 * precision * recall / (precision + recall)",
        },
        {
            "metric": "original_cases",
            "value": len(original),
            "definition": "linhas do original-execution.csv",
        },
        {
            "metric": "original_cases_passed",
            "value": original_passed,
            "definition": "passed == TRUE",
        },
        {
            "metric": "original_cases_not_evaluable",
            "value": original_not_evaluable,
            "definition": "passed == NON-EVALUABLE",
        },
    ]

    with (OUT / "reproduced-metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "definition"])
        writer.writeheader()
        writer.writerows(audit_csv)

    print(json.dumps({
        "mutants": len(mutants),
        "equivalent": equivalent,
        "unknown": unknown,
        "killed": killed_total,
        "survived": survived_total,
        "reported_mutation_score": reported_score,
        "evaluated_mutation_score": evaluable_score,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "json_kill_equals_csv_kill": json_kill_mutants == execution_kill_mutants,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
