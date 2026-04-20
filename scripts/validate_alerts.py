import yaml
import pandas as pd
import json
from pathlib import Path

ALERT_RULES_PATH = "config/alert_rules.yaml"
LOGS_PATH = "data/logs.jsonl"

def load_alert_rules(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_logs(path):
    records = []
    if Path(path).exists():
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return pd.DataFrame(records)

def check_alerts(rules, df):
    print("=== ALERT VALIDATION ===")
    for rule in rules.get("alerts", []):
        name = rule.get("name", "Unnamed Alert")
        expr = rule.get("expr", "")
        runbook = rule.get("runbook", "")
        try:
            # Đánh giá biểu thức trên DataFrame df
            triggered = df.query(expr)
            if not triggered.empty:
                print(f"[ALERT TRIGGERED] {name}")
                print(f"  Rule: {expr}")
                print(f"  Runbook: {runbook}")
                print(f"  Triggered rows: {len(triggered)}")
            else:
                print(f"[OK] {name}")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

def main():
    rules = load_alert_rules(ALERT_RULES_PATH)
    df = load_logs(LOGS_PATH)
    if df.empty:
        print("No logs found. Please generate data/logs.jsonl first.")
        return
    check_alerts(rules, df)

if __name__ == "__main__":
    main()
