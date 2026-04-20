# Mock Debug Q&A (Day 13 Observability)

This sheet is for oral and written practice before the live demo.

## Part A. Oral Questions

1. Why do we need correlation IDs in an observability stack?
- Expected points: Link one request across logs, traces, and downstream calls; speed up incident triage.

2. What does our middleware add to each request/response?
- Expected points: Read or generate x-request-id, bind correlation_id into structlog context, return x-request-id and x-response-time-ms headers.

3. How is PII protected in logs?
- Expected points: scrub_event processor sanitizes payload and event text; pii patterns redact email, phone, CCCD, credit card, passport, and VN address.

4. Where is request context enrichment done?
- Expected points: /chat handler binds user_id_hash, session_id, feature, model, and env before logging.

5. What is the flow to debug high latency?
- Expected points: Check metrics (P95 breach), open slow traces to identify bottleneck span, confirm with correlated logs by correlation_id.

6. How is trace metadata attached?
- Expected points: @observe decorator on agent/LLM path and langfuse_context updates for trace tags and observation usage details.

7. Which incident toggles are supported?
- Expected points: rag_slow, tool_fail, cost_spike via incident endpoints or inject_incident.py.

8. How is error rate calculated in current metrics?
- Expected points: error_rate_pct = error_total / traffic * 100, where traffic is successful requests recorded in metrics.

9. What does the dashboard panel "Trace Count" represent?
- Expected points: Traffic-based proxy in this lab dashboard; official trace verification is done in Langfuse UI.

10. What triggers the rag_slow alert and where is the runbook?
- Expected points: rag_retrieval_latency_ms > 2000 for 5m; runbook is docs/alerts.md section 4.

## Part B. Written Debug Prompts

### Prompt 1: Latency spike
Given: P95 goes from ~170ms to >2500ms after incident injection.
- Explain which metric first signals the issue.
- Name the trace span that proves root cause.
- Show the log fields you would filter by.

Expected structure:
- Signal: latency_p95 breach in dashboard/metrics.
- Root cause: retrieval span in trace (rag_slow sleep path).
- Log filters: event, error_type, correlation_id, feature, session_id.

### Prompt 2: Error burst
Given: error_rate_pct exceeds 5% for 5 minutes.
- List 3 likely causes in this lab.
- Describe one mitigation per cause.

Expected causes:
- tool_fail incident (vector store timeout).
- tracing integration issue from dependency/API mismatch.
- schema/tooling change causing runtime exception.

Expected mitigations:
- disable incident toggle.
- patch/rollback tracing wrapper.
- rollback recent deployment and verify with smoke requests.

### Prompt 3: Cost anomaly
Given: cost per 1k requests breaches target.
- Explain what values to inspect first.
- Propose 2 optimization actions.

Expected checks:
- tokens_in_total, tokens_out_total, total_cost_usd, feature/model breakdown in Langfuse.

Expected actions:
- shorten prompts and trim context.
- route low-complexity traffic to cheaper model.

## Part C. Grader Follow-up Checklist

1. Student can explain one incident end-to-end using Metrics -> Traces -> Logs.
2. Student can point to exact files for middleware, logging, tracing, metrics, alerts.
3. Student can justify SLO thresholds and current values shown in docs.
4. Student can show commit evidence for assigned role.
