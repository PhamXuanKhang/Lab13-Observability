# Dashboard Spec

## Required Layer-2 Panels (6 panels)

### Panel 1: Request Latency P95
- **Metric source**: metrics.py snapshot → latency_p95_ms
- **Unit**: milliseconds (ms)
- **SLO threshold line**: 2000ms (red dashed line)
- **Visualization**: Time series line chart
- **Refresh**: 15 seconds

### Panel 2: Error Rate
- **Metric source**: metrics.py snapshot → error_count / total_count * 100
- **Unit**: percentage (%)
- **SLO threshold line**: 5% (red dashed line)
- **Visualization**: Time series with breakdown by error_type
- **Refresh**: 15 seconds

### Panel 3: Token Usage / Cost
- **Metric source**: Langfuse usage_details + metrics.py → tokens_in, tokens_out, cost_usd
- **Unit**: tokens (left axis), USD (right axis)
- **SLO threshold line**: $0.50 per 1k requests
- **Visualization**: Stacked bar for tokens, line overlay for cost
- **Refresh**: 30 seconds

### Panel 4: Active Requests (Traffic)
- **Metric source**: metrics.py → in_flight_requests counter
- **Unit**: count
- **Visualization**: Gauge or time series
- **Refresh**: 15 seconds

### Panel 5: Trace Count
- **Metric source**: Langfuse API → trace count per time bucket
- **Unit**: count per minute
- **Visualization**: Bar chart grouped by feature tag
- **Refresh**: 30 seconds

### Panel 6: Quality Score
- **Metric source**: metrics.py → quality_score_avg
- **Unit**: score (0.0 - 1.0)
- **SLO threshold line**: 0.75 (green line)
- **Visualization**: Time series with rolling average
- **Refresh**: 30 seconds

---

## Quality Bar Requirements
- Default time range: 1 hour
- Auto refresh: 15-30 seconds per panel
- Visible SLO threshold lines on relevant panels
- Units clearly labeled on all axes
- Maximum 6-8 panels on main layer (we have 6)
- Color coding: green = healthy, yellow = warning, red = critical
