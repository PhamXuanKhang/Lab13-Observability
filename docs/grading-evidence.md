# Evidence Collection Sheet

## Validation Scores
- **VALIDATE_LOGS_FINAL_SCORE**: 100 /100
- **TOTAL_TRACES_COUNT**: 61
- **PII_LEAKS_FOUND**: 0 (PII scrubbing is activated in logging_config.py)

---

## Required Screenshots

### 1. Langfuse trace list (>= 10 traces)
- **Path**: docs/screenshots/langfuse-trace-list.png
- **Instructions**: Open Langfuse dashboard > Traces, take screenshot showing 10+ traces

### 2. Full trace waterfall
- **Path**: docs/screenshots/trace-waterfall.png
- **Instructions**: Click on one trace, expand all spans, capture the full waterfall view

### 3. JSON logs with correlation_id
- **Path**: docs/screenshots/logs-correlation-id.png
- **Instructions**: Open `data/logs.jsonl`, find a line with `correlation_id` field, screenshot

### 4. Log line with PII redaction
- **Path**: docs/screenshots/pii-redaction.png
- **Instructions**: Find a log line showing `[REDACTED_EMAIL]` or similar patterns

### 5. Dashboard with 6 panels
- **Path**: docs/screenshots/dashboard-6-panels.png
- **Instructions**: Screenshot of your dashboard showing all 6 panels as per dashboard-spec.md

### 6. Alert rules with runbook link
- **Path**: docs/screenshots/alert-rules.png
- **Instructions**: Screenshot showing config/alert_rules.yaml or your alerting UI

---

## Optional Screenshots
- Incident before/after fix: docs/screenshots/incident-fix.png
- Cost comparison: docs/screenshots/cost-optimization.png
- Auto-instrumentation proof: docs/screenshots/auto-instrument.png
