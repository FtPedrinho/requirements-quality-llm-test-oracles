import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def get_decisions(experiment):
    exp = ROOT / "experimentacao" / experiment
    if experiment == "experimentacao-0":
        source = ROOT / "experimentacao" / experiment / "z3-analysis" / "results" / "formal-results.json"
        oracles = ROOT / "experimentacao" / experiment / "oracles" / "oracle-catalog.json"
        cases = None
    else:
        source = ROOT / "experimentacao" / experiment / "formalization" / "results" / "formal-results.json"
        oracles = ROOT / "experimentacao" / experiment / "oracles" / "oracle-catalog.json"
        cases = exp / "test-suites" / "generated-test-cases.csv"
    formal = json.loads(source.read_text(encoding="utf-8"))
    oracle_catalog = json.loads(oracles.read_text(encoding="utf-8"))
    oracle_by_decision = {
        item.get("Decision ID", item.get("Decision ID")): item
        for item in oracle_catalog
    }
    return exp, formal, oracle_by_decision, cases


def main():
    for exp_name, label in (
        ("experimentacao-0", "EXP0"),
        ("experimentacao-1", "EXP1"),
    ):
        exp, formal, oracle_by_decision, cases = get_decisions(exp_name)
        executable_dir = exp / "test-suites" / "executable-suite"
        executable_cases = {}
        executable_path = executable_dir / "executable-cases.csv"
        if executable_path.exists():
            with executable_path.open("r", newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    executable_cases[row["case_id"]] = row

        system_names = {
            "the_coffee_machine_system": "VM",
            "turn_indicator_system": "TIS",
            "safety_injection_system": "NPP",
            "generic": "GENERIC",
        }
        rows = []
        for record in formal:
            if record["system"] == "generic":
                continue
            decision_id = record["id"]
            oracle = oracle_by_decision.get(decision_id, {})
            oracle_id = oracle.get("Oracle ID", oracle.get("Oracle ID", ""))
            pass_id = f"E{0 if label == 'EXP0' else 1}-TC-{decision_id}-PASS"
            pass_status = executable_cases.get(pass_id, {}).get("evaluability", "NON-EVALUABLE")
            reserve = ""
            if label == "EXP1":
                reserve = oracle.get("Reserve", "")
            rows.append({
                "Experiment": label,
                "Test ID": pass_id,
                "System": system_names.get(record["system"], record["system"]),
                "Requirement ID": record["requirement"],
                "Decision ID": decision_id,
                "Oracle ID": oracle_id,
                "Kind": "PASS",
                "Concrete Status": pass_status,
                "MC/DC": "NO",
                "Reserve": reserve,
                "Source": record.get("source", "original Experiment 0/1 requirement"),
            })
            mcdc = record.get("mcdc_symbolic_pairs", [])
            for index, pair in enumerate(mcdc, 1):
                pair_id = f"E{0 if label == 'EXP0' else 1}-TC-{decision_id}-C{index}"
                pair_status = executable_cases.get(pair_id, {}).get("evaluability", "NON-EVALUABLE")
                rows.append({
                    "Experiment": label,
                    "Test ID": pair_id,
                    "System": system_names.get(record["system"], record["system"]),
                    "Requirement ID": record["requirement"],
                    "Decision ID": decision_id,
                    "Oracle ID": oracle_id,
                    "Kind": "MC/DC",
                    "Concrete Status": pair_status,
                    "MC/DC": "YES",
                    "Reserve": reserve,
                    "Source": record.get("source", "original Experiment 0/1 requirement"),
                })

        output = exp / "test-suites" / "suite-traceability.csv"
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=[
                "Experiment", "Test ID", "System", "Requirement ID", "Decision ID",
                "Oracle ID", "Kind", "Concrete Status", "MC/DC", "Reserve", "Source",
            ])
            writer.writeheader()
            writer.writerows(rows)
        print(json.dumps({"experiment": label, "trace_rows": len(rows), "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
