from __future__ import annotations

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observability Dashboard · Day 13</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, 'Segoe UI', sans-serif; font-size: 14px; }

    /* ---- Header ---- */
    header {
      background: #161b22; border-bottom: 1px solid #30363d;
      padding: 14px 24px; display: flex; align-items: center; justify-content: space-between;
    }
    header h1 { font-size: 16px; font-weight: 700; color: #e6edf3; }
    header .subtitle { font-size: 11px; color: #8b949e; margin-top: 2px; }
    #last-update { font-size: 11px; color: #8b949e; }
    #countdown { font-size: 11px; color: #58a6ff; margin-top: 2px; }

    /* ---- Status bar ---- */
    .status-bar {
      display: flex; flex-wrap: wrap; gap: 8px;
      padding: 10px 24px; background: #0d1117; border-bottom: 1px solid #21262d;
    }
    .badge {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;
    }
    .badge.green  { background: #1a4731; color: #56d364; }
    .badge.red    { background: #4c1d1d; color: #f85149; }
    .badge.blue   { background: #1c2f4d; color: #58a6ff; }
    .badge.yellow { background: #3d2f00; color: #e3b341; }
    .badge.purple { background: #2d1f4e; color: #a371f7; }

    /* ---- Panel grid ---- */
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px; padding: 16px 24px;
    }
    @media (max-width: 900px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }

    .panel {
      background: #161b22; border: 1px solid #30363d; border-radius: 8px;
      padding: 14px; display: flex; flex-direction: column; gap: 6px;
    }
    .panel h3 {
      font-size: 10px; font-weight: 700; color: #8b949e;
      text-transform: uppercase; letter-spacing: 0.8px;
    }
    .slo-label { font-size: 11px; }
    .slo-label.pass   { color: #56d364; }
    .slo-label.warn   { color: #e3b341; }
    .slo-label.fail   { color: #f85149; }
    .slo-label.neutral{ color: #8b949e; }
    .big-num { font-size: 32px; font-weight: 700; line-height: 1.1; }
    .big-num.pass   { color: #56d364; }
    .big-num.warn   { color: #e3b341; }
    .big-num.fail   { color: #f85149; }
    .big-num.blue   { color: #58a6ff; }
    .big-num.purple { color: #a371f7; }
    .sub-num { font-size: 11px; color: #8b949e; margin-top: -4px; }
    canvas { max-height: 140px; margin-top: 4px; }

    /* ---- Tables ---- */
    .section { margin: 0 24px 16px; }
    .section h2 { font-size: 12px; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; }
    thead th { background: #21262d; padding: 8px 14px; text-align: left; color: #8b949e; font-weight: 600; }
    tbody td { padding: 8px 14px; border-top: 1px solid #21262d; }
    .pass-cell  { color: #56d364; font-weight: 600; }
    .warn-cell  { color: #e3b341; font-weight: 600; }
    .fail-cell  { color: #f85149; font-weight: 600; }

    /* ---- Incidents ---- */
    .incident-row { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-top: 1px solid #21262d; }
    .incident-row:first-child { border-top: none; }
    .incident-name { width: 120px; font-size: 13px; font-weight: 600; }
    .toggle-btn {
      padding: 4px 14px; border-radius: 4px; border: none; cursor: pointer;
      font-size: 11px; font-weight: 700; transition: opacity .15s;
    }
    .toggle-btn:hover { opacity: 0.8; }
    .toggle-btn.enable-btn  { background: #1a4731; color: #56d364; }
    .toggle-btn.disable-btn { background: #4c1d1d; color: #f85149; }

    footer { text-align: center; padding: 14px; color: #484f58; font-size: 11px; margin-top: 8px; }
    footer a { color: #58a6ff; text-decoration: none; }
  </style>
</head>
<body>

<!-- ====== HEADER ====== -->
<header>
  <div>
    <h1>⚡ Day 13 Observability Dashboard</h1>
    <div class="subtitle">Real-time metrics &nbsp;·&nbsp; SLO compliance &nbsp;·&nbsp; Incident controls</div>
  </div>
  <div style="text-align:right">
    <div id="last-update">Loading…</div>
    <div id="countdown">Refreshing in 15s</div>
  </div>
</header>

<!-- ====== STATUS BAR ====== -->
<div class="status-bar">
  <span id="badge-health"   class="badge">● Health</span>
  <span id="badge-tracing"  class="badge">● Tracing</span>
  <span id="badge-traffic"  class="badge blue">0 requests</span>
  <span id="badge-inflight" class="badge blue">0 in-flight</span>
  <span id="badge-errors"   class="badge green">0 errors</span>
  <span id="badge-incidents"class="badge green">No incidents</span>
</div>

<!-- ====== 6 PANELS ====== -->
<div class="grid">

  <!-- Panel 1: Latency P95 -->
  <div class="panel">
    <h3>Panel 1 · Request Latency P95</h3>
    <div id="slo-latency" class="slo-label neutral">SLO: &lt;2000 ms</div>
    <div id="num-p95" class="big-num blue">— ms</div>
    <div id="sub-latency" class="sub-num">P50: — &nbsp;|&nbsp; P99: —</div>
    <canvas id="chart-latency"></canvas>
  </div>

  <!-- Panel 2: Error Rate -->
  <div class="panel">
    <h3>Panel 2 · Error Rate</h3>
    <div id="slo-error" class="slo-label neutral">SLO: &lt;5%</div>
    <div id="num-error" class="big-num blue">0.00 %</div>
    <div id="sub-error" class="sub-num">Total errors: 0</div>
    <canvas id="chart-error"></canvas>
  </div>

  <!-- Panel 3: Token Usage / Cost -->
  <div class="panel">
    <h3>Panel 3 · Token Usage / Cost</h3>
    <div id="slo-cost" class="slo-label neutral">SLO: &lt;$0.50 / 1k req</div>
    <div id="num-cost" class="big-num blue">$0.0000</div>
    <div id="sub-tokens" class="sub-num">In: 0 &nbsp;|&nbsp; Out: 0 tokens</div>
    <canvas id="chart-tokens"></canvas>
  </div>

  <!-- Panel 4: Active Requests / Traffic -->
  <div class="panel">
    <h3>Panel 4 · Traffic / Active Requests</h3>
    <div class="slo-label neutral">Live in-flight + total throughput</div>
    <div id="num-traffic" class="big-num blue">0 req</div>
    <div id="sub-inflight" class="sub-num">In-flight: 0</div>
    <canvas id="chart-traffic"></canvas>
  </div>

  <!-- Panel 5: Trace Count (approx) -->
  <div class="panel">
    <h3>Panel 5 · Trace Count</h3>
    <div class="slo-label neutral">Approx. via traffic &nbsp;·&nbsp; Verify on Langfuse</div>
    <div id="num-traces" class="big-num purple">0</div>
    <div id="sub-traces" class="sub-num">traces (≈ total requests)</div>
    <canvas id="chart-traces"></canvas>
  </div>

  <!-- Panel 6: Quality Score -->
  <div class="panel">
    <h3>Panel 6 · Quality Score (avg)</h3>
    <div id="slo-quality" class="slo-label neutral">SLO: &ge;0.75</div>
    <div id="num-quality" class="big-num blue">0.000</div>
    <div id="sub-quality" class="sub-num">Heuristic quality avg over all requests</div>
    <canvas id="chart-quality"></canvas>
  </div>

</div>

<!-- ====== SLO TABLE ====== -->
<div class="section">
  <h2>SLO Compliance</h2>
  <div class="card">
    <table>
      <thead>
        <tr>
          <th>SLI</th>
          <th>Objective</th>
          <th>SLO Target</th>
          <th>Window</th>
          <th>Current Value</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody id="slo-tbody">
        <tr><td colspan="6" style="color:#8b949e; text-align:center; padding:16px;">Loading…</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ====== INCIDENT CONTROLS ====== -->
<div class="section">
  <h2>Incident Injection Controls</h2>
  <div class="card" id="incidents-card">
    <div style="padding:12px; color:#8b949e;">Loading…</div>
  </div>
</div>

<!-- ====== LATENCY DISTRIBUTION ====== -->
<div class="section">
  <h2>Latency Distribution (P50 / P95 / P99)</h2>
  <div class="card" style="padding:14px;">
    <canvas id="chart-latency-dist" style="max-height:120px;"></canvas>
  </div>
</div>

<footer>
  Day 13 Observability Lab &nbsp;·&nbsp;
  <a href="/docs">API Docs</a> &nbsp;·&nbsp;
  <a href="/metrics">/metrics JSON</a> &nbsp;·&nbsp;
  <a href="/health">/health JSON</a>
</footer>

<!-- ====== JAVASCRIPT ====== -->
<script>
  // ── Constants ──────────────────────────────────────────────────────────────
  const MAX_H = 20;          // history points
  const POLL_MS = 15000;     // 15 s

  // ── History buffers ────────────────────────────────────────────────────────
  const H = {
    labels:      [],
    p95:         [],
    p50:         [],
    p99:         [],
    errorRate:   [],
    traffic:     [],   // delta per interval
    inFlight:    [],
    tokensIn:    [],
    tokensOut:   [],
    cost:        [],
    quality:     [],
  };
  let prevTraffic = 0;
  let countdown = POLL_MS / 1000;

  // ── Chart.js defaults ──────────────────────────────────────────────────────
  Chart.defaults.color = '#8b949e';
  Chart.defaults.borderColor = '#21262d';

  function lineChart(id, label, color, sloVal, sloColor) {
    const ctx = document.getElementById(id).getContext('2d');
    const datasets = [{
      label, data: [],
      borderColor: color, backgroundColor: color + '22',
      fill: true, tension: 0.35, pointRadius: 2, borderWidth: 1.5,
    }];
    if (sloVal !== null) {
      datasets.push({
        label: 'SLO', data: [],
        borderColor: sloColor, borderDash: [5, 3],
        borderWidth: 1.5, pointRadius: 0, fill: false,
      });
    }
    return new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets },
      options: {
        animation: false, responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { beginAtZero: true, grid: { color: '#21262d' } },
        },
      },
    });
  }

  function barChart(id) {
    const ctx = document.getElementById(id).getContext('2d');
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          { label: 'Tokens In',  data: [], backgroundColor: '#388bfd66', borderColor: '#388bfd', borderWidth: 1 },
          { label: 'Tokens Out', data: [], backgroundColor: '#a371f766', borderColor: '#a371f7', borderWidth: 1 },
        ],
      },
      options: {
        animation: false, responsive: true,
        plugins: { legend: { display: true, labels: { boxWidth: 8, font: { size: 10 } } } },
        scales: {
          x: { display: false, stacked: true },
          y: { stacked: true, beginAtZero: true, grid: { color: '#21262d' } },
        },
      },
    });
  }

  function latencyDistChart(id) {
    const ctx = document.getElementById(id).getContext('2d');
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['P50', 'P95', 'P99'],
        datasets: [{ data: [0, 0, 0], backgroundColor: ['#388bfd', '#f0883e', '#f85149'] }],
      },
      options: {
        animation: false, responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: '#21262d' } },
          y: { beginAtZero: true, grid: { color: '#21262d' }, title: { display: true, text: 'ms', color: '#8b949e' } },
        },
      },
    });
  }

  // ── Init charts ────────────────────────────────────────────────────────────
  const charts = {
    latency:  lineChart('chart-latency',  'P95 ms',    '#f0883e', 2000, '#f85149'),
    error:    lineChart('chart-error',    'Error %',   '#f85149', 5,    '#f85149'),
    tokens:   barChart('chart-tokens'),
    traffic:  lineChart('chart-traffic',  'Req/poll',  '#58a6ff', null, null),
    traces:   lineChart('chart-traces',   'Traces',    '#a371f7', null, null),
    quality:  lineChart('chart-quality',  'Quality',   '#56d364', 0.75, '#3fb950'),
    latDist:  latencyDistChart('chart-latency-dist'),
  };

  // ── Helpers ────────────────────────────────────────────────────────────────
  function push(arr, val) { arr.push(val); if (arr.length > MAX_H) arr.shift(); }

  function updateLine(chart, labels, mainData, sloVal) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = mainData;
    if (chart.data.datasets[1] && sloVal !== null)
      chart.data.datasets[1].data = labels.map(() => sloVal);
    chart.update('none');
  }

  function updateBar(chart, labels, d1, d2) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = d1;
    chart.data.datasets[1].data = d2;
    chart.update('none');
  }

  function sloClass(val, threshold, mode) {
    const pass = mode === 'lt' ? val <= threshold : val >= threshold;
    if (pass) return 'pass';
    const borderline = mode === 'lt' ? val <= threshold * 1.25 : val >= threshold * 0.85;
    return borderline ? 'warn' : 'fail';
  }

  function sloText(cls, pass_label, fail_label) {
    if (cls === 'pass') return '✓ ' + pass_label;
    if (cls === 'warn') return '⚠ ' + fail_label;
    return '✗ ' + fail_label;
  }

  // ── Main refresh ───────────────────────────────────────────────────────────
  async function refresh() {
    try {
      const [m, h] = await Promise.all([
        fetch('/metrics').then(r => r.json()),
        fetch('/health').then(r => r.json()),
      ]);

      const now = new Date().toLocaleTimeString();
      document.getElementById('last-update').textContent = 'Updated: ' + now;

      // Derived values
      const p95       = m.latency_p95     || 0;
      const p50       = m.latency_p50     || 0;
      const p99       = m.latency_p99     || 0;
      const errRate   = m.error_rate_pct  || 0;
      const errTotal  = m.error_total     || 0;
      const traffic   = m.traffic         || 0;
      const inFlight  = m.in_flight       || 0;
      const tokIn     = m.tokens_in_total || 0;
      const tokOut    = m.tokens_out_total|| 0;
      const cost      = m.total_cost_usd  || 0;
      const quality   = m.quality_avg     || 0;
      const deltaReq  = Math.max(0, traffic - prevTraffic);
      prevTraffic     = traffic;
      const costPer1k = traffic > 0 ? (cost / traffic * 1000) : 0;

      // Push history
      push(H.labels,    now);
      push(H.p95,       p95);
      push(H.p50,       p50);
      push(H.p99,       p99);
      push(H.errorRate, errRate);
      push(H.traffic,   deltaReq);
      push(H.inFlight,  inFlight);
      push(H.tokensIn,  tokIn);
      push(H.tokensOut, tokOut);
      push(H.cost,      cost);
      push(H.quality,   quality);

      // ── Status badges ──
      const hB = document.getElementById('badge-health');
      hB.textContent = h.ok ? '● Health: OK' : '● Health: ERROR';
      hB.className = 'badge ' + (h.ok ? 'green' : 'red');

      const tB = document.getElementById('badge-tracing');
      tB.textContent = '◉ Tracing: ' + (h.tracing_enabled ? 'ON (Langfuse)' : 'OFF');
      tB.className = 'badge ' + (h.tracing_enabled ? 'green' : 'yellow');

      document.getElementById('badge-traffic').textContent  = traffic + ' total req';
      document.getElementById('badge-inflight').textContent = inFlight + ' in-flight';

      const eB = document.getElementById('badge-errors');
      eB.textContent = errTotal + (errTotal === 1 ? ' error' : ' errors');
      eB.className = 'badge ' + (errTotal === 0 ? 'green' : 'red');

      const incidents  = h.incidents || {};
      const activeInc  = Object.values(incidents).filter(Boolean).length;
      const iB = document.getElementById('badge-incidents');
      iB.textContent = activeInc > 0 ? '⚠ ' + activeInc + ' incident(s) active' : '● No incidents';
      iB.className = 'badge ' + (activeInc > 0 ? 'red' : 'green');

      // ── Panel 1: Latency P95 ──
      const lCls = sloClass(p95, 2000, 'lt');
      document.getElementById('num-p95').textContent = p95.toFixed(0) + ' ms';
      document.getElementById('num-p95').className = 'big-num ' + lCls;
      document.getElementById('slo-latency').textContent = 'SLO <2000ms · ' + sloText(lCls, 'PASS', 'BREACH');
      document.getElementById('slo-latency').className = 'slo-label ' + lCls;
      document.getElementById('sub-latency').textContent = 'P50: ' + p50.toFixed(0) + 'ms  |  P99: ' + p99.toFixed(0) + 'ms';
      updateLine(charts.latency, H.labels, H.p95, 2000);

      // ── Panel 2: Error Rate ──
      const eCls = sloClass(errRate, 5, 'lt');
      document.getElementById('num-error').textContent = errRate.toFixed(2) + ' %';
      document.getElementById('num-error').className = 'big-num ' + eCls;
      document.getElementById('slo-error').textContent = 'SLO <5% · ' + sloText(eCls, 'PASS', 'BREACH');
      document.getElementById('slo-error').className = 'slo-label ' + eCls;
      document.getElementById('sub-error').textContent = 'Total errors: ' + errTotal + ' (' + (m.error_breakdown ? JSON.stringify(m.error_breakdown) : '{}') + ')';
      updateLine(charts.error, H.labels, H.errorRate, 5);

      // ── Panel 3: Token / Cost ──
      const cCls = sloClass(costPer1k, 0.5, 'lt');
      document.getElementById('num-cost').textContent = '$' + cost.toFixed(4) + ' total';
      document.getElementById('num-cost').className = 'big-num ' + cCls;
      document.getElementById('slo-cost').textContent = 'SLO <$0.50/1k · $' + costPer1k.toFixed(4) + '/1k · ' + sloText(cCls, 'PASS', 'BREACH');
      document.getElementById('slo-cost').className = 'slo-label ' + cCls;
      document.getElementById('sub-tokens').textContent = 'In: ' + tokIn + '  |  Out: ' + tokOut + ' tokens';
      updateBar(charts.tokens, H.labels, H.tokensIn, H.tokensOut);

      // ── Panel 4: Traffic ──
      document.getElementById('num-traffic').textContent = traffic + ' req';
      document.getElementById('sub-inflight').textContent = 'In-flight: ' + inFlight + '  |  +' + deltaReq + ' this interval';
      updateLine(charts.traffic, H.labels, H.traffic, null);

      // ── Panel 5: Trace Count ──
      document.getElementById('num-traces').textContent = traffic;
      document.getElementById('sub-traces').textContent = 'traces ≈ total requests · verify on Langfuse';
      updateLine(charts.traces, H.labels, H.traffic, null);

      // ── Panel 6: Quality ──
      const qCls = sloClass(quality, 0.75, 'gt');
      document.getElementById('num-quality').textContent = quality.toFixed(3);
      document.getElementById('num-quality').className = 'big-num ' + qCls;
      document.getElementById('slo-quality').textContent = 'SLO ≥0.75 · ' + sloText(qCls, 'PASS', 'BREACH');
      document.getElementById('slo-quality').className = 'slo-label ' + qCls;
      updateLine(charts.quality, H.labels, H.quality, 0.75);

      // ── Latency Distribution chart ──
      charts.latDist.data.datasets[0].data = [p50, p95, p99];
      charts.latDist.update('none');

      // ── SLO Table ──
      const rows = [
        { sli: 'Latency P95', obj: '&lt;2000 ms', target: '99.5%', window: '28d', val: p95.toFixed(0)+' ms',        cls: lCls },
        { sli: 'Error Rate',  obj: '&lt;5%',      target: '99%',   window: '28d', val: errRate.toFixed(2)+'%',       cls: eCls },
        { sli: 'Cost / 1k',  obj: '&lt;$0.50',   target: '99%',   window: '28d', val: '$'+costPer1k.toFixed(4),     cls: cCls },
        { sli: 'Quality Avg', obj: '&ge;0.75',    target: '95%',   window: '28d', val: quality.toFixed(3),           cls: qCls },
      ];
      document.getElementById('slo-tbody').innerHTML = rows.map(r => `
        <tr>
          <td>${r.sli}</td>
          <td>${r.obj}</td>
          <td>${r.target}</td>
          <td>${r.window}</td>
          <td><strong>${r.val}</strong></td>
          <td class="${r.cls}-cell">${r.cls === 'pass' ? '✓ PASS' : r.cls === 'warn' ? '⚠ WARN' : '✗ BREACH'}</td>
        </tr>
      `).join('');

      // ── Incidents ──
      const DESCS = {
        rag_slow:   'Simulates slow RAG retrieval (+2.5 s)',
        tool_fail:  'Simulates vector store timeout error',
        cost_spike: 'Simulates 4× token output (cost spike)',
      };
      document.getElementById('incidents-card').innerHTML = Object.entries(incidents).map(([name, active]) => `
        <div class="incident-row">
          <span class="incident-name">${name}</span>
          <span class="badge ${active ? 'red' : 'green'}">${active ? '⚠ ACTIVE' : '● OFF'}</span>
          <span style="flex:1; font-size:11px; color:#8b949e;">${DESCS[name] || ''}</span>
          <button class="toggle-btn ${active ? 'disable-btn' : 'enable-btn'}"
                  onclick="toggleIncident('${name}', ${!active})">
            ${active ? 'Disable' : 'Enable'}
          </button>
        </div>
      `).join('');

    } catch (err) {
      document.getElementById('last-update').textContent = 'Error: ' + err.message;
    }
  }

  // ── Incident toggle ────────────────────────────────────────────────────────
  async function toggleIncident(name, enable) {
    await fetch('/incidents/' + name + '/' + (enable ? 'enable' : 'disable'), { method: 'POST' });
    await refresh();
  }

  // ── Countdown ticker ──────────────────────────────────────────────────────
  setInterval(() => {
    countdown -= 1;
    if (countdown < 0) countdown = POLL_MS / 1000;
    document.getElementById('countdown').textContent = 'Refreshing in ' + countdown + 's';
  }, 1000);

  // ── Boot ──────────────────────────────────────────────────────────────────
  refresh();
  setInterval(() => { countdown = POLL_MS / 1000; refresh(); }, POLL_MS);
</script>
</body>
</html>"""
