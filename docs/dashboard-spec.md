# Dashboard Spec

## Required Layer-2 Panels (6 panels)

### Panel 1: Request Latency P95
- **Metric source**: metrics.py snapshot -> latency_p95
- **Unit**: milliseconds (ms)
- **SLO threshold line**: 2000ms (red dashed line)
- **Visualization**: Time series line chart
- **Refresh**: 15 seconds

### Panel 2: Error Rate
- **Metric source**: metrics.py snapshot -> error_rate_pct (derived as error_total / traffic * 100)
- **Unit**: percentage (%)
- **SLO threshold line**: 5% (red dashed line)
- **Visualization**: Time series with breakdown by error_type
- **Refresh**: 15 seconds

### Panel 3: Token Usage / Cost
- **Metric source**: metrics.py snapshot -> tokens_in_total, tokens_out_total, total_cost_usd
- **Unit**: tokens (left axis), USD (right axis)
- **SLO threshold line**: $0.50 per 1k requests (derived as total_cost_usd / traffic * 1000)
- **Visualization**: Stacked bar for tokens, line overlay for cost
- **Refresh**: 15 seconds

### Panel 4: Active Requests (Traffic)
- **Metric source**: metrics.py -> in_flight and traffic
- **Unit**: count
- **Visualization**: Time series for request delta per refresh and current in-flight text
- **Refresh**: 15 seconds

### Panel 5: Trace Count
- **Metric source**: traffic-based proxy from metrics.py (trace ~= total requests), with manual verification in Langfuse
- **Unit**: count
- **Visualization**: Time series line chart
- **Refresh**: 15 seconds

### Panel 6: Quality Score
- **Metric source**: metrics.py -> quality_avg
- **Unit**: score (0.0 - 1.0)
- **SLO threshold line**: 0.75 (green line)
- **Visualization**: Time series with rolling average
- **Refresh**: 15 seconds

---

## Quality Bar Requirements
- Default time range: 1 hour
- Auto refresh: 15 seconds per panel
- Visible SLO threshold lines on relevant panels
- Units clearly labeled on all axes
- Maximum 6-8 panels on main layer (we have 6)
- Color coding: green = healthy, yellow = warning, red = critical
