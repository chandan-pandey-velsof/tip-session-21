from django.http import HttpResponse


def index(request):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Law Firm Prosecution Analytics — TriangleIP</title>
    <link rel='stylesheet' href='/static/tip_design.css'>
    <style>
        .search-bar { display:flex; gap:0.75rem; align-items:center; flex-wrap:wrap; }
        .search-bar input { min-width:320px; }
        .suggestions-dropdown {
            position:absolute; top:100%; left:0; right:0; z-index:50;
            background:#fff; border:1px solid var(--tip-border, #e2e8f0);
            border-radius:8px; max-height:220px; overflow-y:auto;
            box-shadow:0 8px 24px rgba(0,0,0,.12); margin-top:4px;
        }
        .suggestions-dropdown .sug-item {
            padding:10px 14px; cursor:pointer; font-size:0.875rem;
            border-bottom:1px solid var(--tip-border, #e2e8f0);
        }
        .suggestions-dropdown .sug-item:last-child { border-bottom:none; }
        .suggestions-dropdown .sug-item:hover { background:var(--tip-primary-bg, #eff6ff); }
        .suggestions-dropdown .sug-item .sug-name { font-weight:600; color:var(--tip-text, #1a1a2e); }
        .suggestions-dropdown .sug-item .sug-sub { font-size:0.78rem; color:var(--tip-text-secondary, #6b7280); }
        .stats-row { display:grid; grid-template-columns:repeat(auto-fit, minmax(200px,1fr)); gap:1rem; margin-bottom:1.5rem; }
        .stat-card { text-align:center; }
        .stat-card .tip-card-value { font-size:2rem; }
        .stat-card .stat-label { font-size:0.8rem; color:var(--tip-text-secondary, #6b7280); margin-top:0.25rem; text-transform:uppercase; letter-spacing:0.5px; }
        .charts-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }
        @media(max-width:900px){ .charts-grid{grid-template-columns:1fr;} }
        .chart-card canvas { width:100%!important; height:280px!important; }
        .bar-chart-row { display:flex; align-items:flex-end; gap:6px; height:200px; padding-top:10px; }
        .bar-group { display:flex; flex-direction:column; align-items:center; flex:1; }
        .bar-pair { display:flex; gap:3px; align-items:flex-end; flex:1; width:100%; justify-content:center; }
        .bar { border-radius:4px 4px 0 0; min-width:18px; transition:height 0.4s ease; }
        .bar-allowed { background:var(--tip-primary, #4f8ef7); }
        .bar-rejected { background:#f97316; }
        .bar-label { font-size:0.7rem; color:var(--tip-text-secondary, #6b7280); margin-top:6px; text-align:center; word-break:break-word; line-height:1.2; max-width:70px; }
        .bar-value { font-size:0.65rem; font-weight:600; margin-bottom:2px; }
        .pie-legend { display:flex; flex-wrap:wrap; gap:0.75rem; margin-top:1rem; }
        .pie-legend-item { display:flex; align-items:center; gap:0.4rem; font-size:0.82rem; }
        .pie-legend-dot { width:12px; height:12px; border-radius:50%; flex-shrink:0; }
        .trend-row { display:flex; align-items:flex-end; gap:8px; height:200px; padding-top:10px; }
        .trend-group { display:flex; flex-direction:column; align-items:center; flex:1; }
        .trend-pair { display:flex; gap:3px; align-items:flex-end; flex:1; width:100%; justify-content:center; }
        .trend-bar { border-radius:4px 4px 0 0; min-width:14px; transition:height 0.4s ease; }
        .trend-granted { background:var(--tip-primary, #4f8ef7); }
        .trend-abandon { background:#ef4444; }
        .trend-label { font-size:0.7rem; color:var(--tip-text-secondary, #6b7280); margin-top:6px; }
        .timing-bars { display:flex; flex-direction:column; gap:1rem; }
        .timing-item { display:flex; align-items:center; gap:1rem; }
        .timing-label { width:80px; font-size:0.85rem; font-weight:600; color:var(--tip-text, #1a1a2e); flex-shrink:0; }
        .timing-bar-wrap { flex:1; display:flex; flex-direction:column; gap:2px; }
        .timing-bar-track { height:28px; background:#f1f5f9; border-radius:6px; overflow:hidden; display:flex; }
        .timing-bar-fill { height:100%; border-radius:6px; display:flex; align-items:center; padding-left:8px; font-size:0.75rem; font-weight:600; color:#fff; transition:width 0.5s ease; }
        .timing-bar-fill.resp { background:var(--tip-primary, #4f8ef7); }
        .timing-bar-fill.oa { background:#8b5cf6; }
        .timing-bar-legend { display:flex; gap:1rem; margin-top:0.5rem; }
        .timing-bar-legend span { font-size:0.75rem; display:flex; align-items:center; gap:4px; }
        .timing-bar-legend .dot { width:10px; height:10px; border-radius:50%; }
        .entity-row { display:flex; align-items:center; gap:0.75rem; padding:0.6rem 0; border-bottom:1px solid var(--tip-border, #e2e8f0); }
        .entity-row:last-child { border-bottom:none; }
        .entity-rank { width:28px; height:28px; border-radius:50%; background:var(--tip-primary-bg, #eff6ff); color:var(--tip-primary, #4f8ef7); display:flex; align-items:center; justify-content:center; font-size:0.78rem; font-weight:700; flex-shrink:0; }
        .entity-name { flex:1; font-size:0.88rem; font-weight:500; }
        .entity-count { font-size:0.82rem; color:var(--tip-text-secondary, #6b7280); min-width:50px; text-align:right; }
        .entity-rate { font-size:0.82rem; font-weight:600; min-width:60px; text-align:right; }
        .loading-spinner { display:inline-block; width:20px; height:20px; border:3px solid var(--tip-border, #e2e8f0); border-top-color:var(--tip-primary, #4f8ef7); border-radius:50%; animation:spin 0.8s linear infinite; }
        @keyframes spin { to { transform:rotate(360deg); } }
        .error-card { border-left:4px solid #ef4444; }
        .empty-state { text-align:center; padding:3rem 1rem; color:var(--tip-text-secondary, #6b7280); }
        .empty-state .empty-icon { font-size:3rem; margin-bottom:1rem; }
        .filter-section { display:flex; gap:0.75rem; flex-wrap:wrap; margin-top:1rem; }
        .filter-section select, .filter-section input { font-size:0.85rem; }
        .section-title { font-size:1.1rem; font-weight:700; margin-bottom:1rem; color:var(--tip-text, #1a1a2e); }
        .pie-chart-container { display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap; }
        .pie-chart-svg { flex-shrink:0; }
        .pie-info { flex:1; min-width:200px; }
    </style>
</head>
<body>
<div class='tip-page'>
    <nav class='tip-navbar'>
        <a class='tip-navbar-brand' href='/'>TriangleIP</a>
        <span style='color:var(--tip-text-secondary, #6b7280); font-size:0.85rem;'>Law Firm Prosecution Analytics</span>
    </nav>

    <h1 class='tip-page-title'>Law Firm Prosecution Analytics</h1>
    <p style='color:var(--tip-text-secondary, #6b7280); margin-bottom:1.5rem;'>
        Search for a law firm to view patent prosecution statistics, allowance rates, office action patterns, and more.
    </p>

    <!-- Search -->
    <div class='tip-card' style='margin-bottom:1.5rem;'>
        <div class='search-bar' style='position:relative;'>
            <input type='text' id='firmSearch' placeholder='Type a law firm name (e.g. "Mughal Gaudry")' autocomplete='off'
                   style='padding:0.6rem 1rem; border:1px solid var(--tip-border, #e2e8f0); border-radius:8px; font-size:0.95rem; outline:none;'
                   onfocus='this.style.borderColor="var(--tip-primary, #4f8ef7)"' onblur='setTimeout(()=>hideSuggestions(),200)' />
            <button class='tip-btn tip-btn-primary' id='searchBtn' onclick='doSearch()'>Search</button>
            <div id='suggestionsBox' class='suggestions-dropdown' style='display:none;'></div>
        </div>
        <div class='filter-section' id='filterSection' style='display:none;'>
            <select id='statusFilter' style='padding:0.5rem 0.75rem; border:1px solid var(--tip-border, #e2e8f0); border-radius:8px;'>
                <option value=''>All Statuses</option>
                <option value='pend'>Pending</option>
                <option value='iss'>Issued</option>
                <option value='abn'>Abandoned</option>
                <option value='exp'>Expired</option>
            </select>
            <input type='text' id='filingRange' placeholder='Filing range (MM/DD/YYYY - MM/DD/YYYY)'
                   style='padding:0.5rem 0.75rem; border:1px solid var(--tip-border, #e2e8f0); border-radius:8px; font-size:0.85rem; width:280px;' />
            <input type='text' id='gauFilter' placeholder='GAU codes (e.g. 1633, 1699)'
                   style='padding:0.5rem 0.75rem; border:1px solid var(--tip-border, #e2e8f0); border-radius:8px; font-size:0.85rem; width:200px;' />
            <button class='tip-btn tip-btn-outline' onclick='doSearch(true)' style='font-size:0.85rem;'>Apply Filters</button>
        </div>
    </div>

    <!-- Loading -->
    <div id='loadingState' style='display:none; text-align:center; padding:3rem;'>
        <div class='loading-spinner'></div>
        <p style='margin-top:1rem; color:var(--tip-text-secondary, #6b7280);'>Loading firm data&hellip;</p>
    </div>

    <!-- Error -->
    <div id='errorState' class='tip-card error-card' style='display:none; padding:1.5rem;'>
        <p id='errorMsg' style='color:#ef4444; font-weight:600;'></p>
    </div>

    <!-- Results -->
    <div id='resultsArea' style='display:none;'>
        <!-- Overview Stats -->
        <div class='tip-card' style='margin-bottom:1.5rem;'>
            <div class='section-title' id='firmNameTitle'>Firm Overview</div>
            <div class='stats-row' id='overviewStats'></div>
            <div id='overviewDetails' style='margin-top:1rem; display:grid; grid-template-columns:1fr 1fr; gap:1rem;'></div>
        </div>

        <!-- Charts Grid -->
        <div class='charts-grid'>
            <!-- Allowance Rate -->
            <div class='tip-card chart-card'>
                <div class='section-title'>Allowance Rate by Category</div>
                <div id='allowanceChart'></div>
                <div id='allowanceLegend' style='display:flex; gap:1rem; margin-top:0.75rem; font-size:0.8rem;">
                    <span><span style='display:inline-block;width:12px;height:12px;background:var(--tip-primary,#4f8ef7);border-radius:3px;margin-right:4px;vertical-align:middle;'></span>Allowed</span>
                    <span><span style='display:inline-block;width:12px;height:12px;background:#f97316;border-radius:3px;margin-right:4px;vertical-align:middle;'></span>Rejected</span>
                </div>
            </div>

            <!-- Office Actions -->
            <div class='tip-card chart-card'>
                <div class='section-title'>Office Action Distribution</div>
                <div id='oaChart' class='pie-chart-container'></div>
            </div>

            <!-- Allowance Trend -->
            <div class='tip-card chart-card'>
                <div class='section-title'>Historical Allowance Trend</div>
                <div id='trendChart'></div>
                <div id='trendLegend' style='display:flex; gap:1rem; margin-top:0.75rem; font-size:0.8rem;">
                    <span><span style='display:inline-block;width:12px;height:12px;background:var(--tip-primary,#4f8ef7);border-radius:3px;margin-right:4px;vertical-align:middle;'></span>Granted</span>
                    <span><span style='display:inline-block;width:12px;height:12px;background:#ef4444;border-radius:3px;margin-right:4px;vertical-align:middle;'></span>Abandoned</span>
                </div>
            </div>

            <!-- Response Timing -->
            <div class='tip-card chart-card'>
                <div class='section-title'>Response &amp; OA Timing</div>
                <div id='timingChart' class='timing-bars'></div>
                <div class='timing-bar-legend'>
                    <span><span class='dot' style='background:var(--tip-primary,#4f8ef7);'></span>Response Timing</span>
                    <span><span class='dot' style='background:#8b5cf6;'></span>OA Timing</span>
                </div>
            </div>
        </div>

        <!-- Top Entities -->
        <div class='tip-card' style='margin-top:1.5rem;'>
            <div class='section-title'>Top Applicants</div>
            <div id='topEntities'></div>
        </div>
    </div>

    <!-- Diagnostics -->
    <details class='tip-card' style='margin-top:2rem;'>
        <summary style='cursor:pointer; font-weight:600; color:var(--tip-text-secondary, #6b7280);'>Diagnostics</summary>
        <div style='margin-top:1rem;'>
            <div class='tip-table-wrap'>
                <table class='tip-table' id='diagTable'>
                    <thead><tr><th>Item</th><th>Details</th></tr></thead>
                    <tbody id='diagBody'>
                        <tr><td>Request</td><td id='diagRequest'></td></tr>
                        <tr><td>API Calls</td><td id='diagApiCalls'></td></tr>
                        <tr><td>Input Parameters</td><td id='diagInput'></td></tr>
                        <tr><td>Output Parameters</td><td id='diagOutput'></td></tr>
                        <tr><td>Field Mapping</td><td id='diagMapping'></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </details>
</div>

<script>
const USER_REQUEST = "Let me search a law firm and see their patent prosecution stats. Law-firm (prosecutor) page";

let currentFirm = '';
let diagCalls = [];
let diagInput = {};
let diagOutput = {};
let diagMapping = {};

// ── Suggest ──
const searchInput = document.getElementById('firmSearch');
let suggestTimer = null;
searchInput.addEventListener('input', function() {
    clearTimeout(suggestTimer);
    const q = this.value.trim();
    if (q.length < 2) { hideSuggestions(); return; }
    suggestTimer = setTimeout(() => fetchSuggestions(q), 300);
});
searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { e.preventDefault(); doSearch(); }
});

function fetchSuggestions(q) {
    fetch('/tip-api/v1/prosecutor/suggest?q=' + encodeURIComponent(q) + '&mode=lawfirm')
        .then(r => r.json())
        .then(json => {
            if (json.status && json.data && json.data.length) {
                renderSuggestions(json.data);
            } else {
                hideSuggestions();
            }
        })
        .catch(() => hideSuggestions());
}

function renderSuggestions(items) {
    const box = document.getElementById('suggestionsBox');
    box.innerHTML = items.map(i =>
        '<div class="sug-item" onmousedown="pickSuggestion(\\'' + i.id.replace(/'/g, "\\\\'") + '\\')">' +
        '<div class="sug-name">' + escHtml(i.text) + '</div></div>'
    ).join('');
    box.style.display = 'block';
}

function pickSuggestion(name) {
    searchInput.value = name;
    hideSuggestions();
    doSearch();
}

function hideSuggestions() {
    document.getElementById('suggestionsBox').style.display = 'none';
}

// ── Search ──
function doSearch(useFilters) {
    const firm = searchInput.value.trim();
    if (!firm) return;
    currentFirm = firm;
    diagCalls = [];
    diagInput = { search_data: firm, mode: 'lawfirm' };
    diagOutput = {};
    diagMapping = {};

    if (useFilters) {
        const sf = document.getElementById('statusFilter').value;
        const fr = document.getElementById('filingRange').value.trim();
        const gau = document.getElementById('gauFilter').value.trim();
        if (sf) diagInput.status_select = sf;
        if (fr) diagInput.filing_range = fr;
        if (gau) diagInput.refined_gaus = gau;
    }

    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('errorState').style.display = 'none';
    document.getElementById('resultsArea').style.display = 'none';
    document.getElementById('filterSection').style.display = 'flex';

    const body = Object.assign({}, diagInput);

    Promise.all([
        apiPost('/v1/prosecutor/overview', body, 'overview'),
        apiPost('/v1/prosecutor/allowance-rate', body, 'allowance-rate'),
        apiPost('/v1/prosecutor/office-actions', body, 'office-actions'),
        apiPost('/v1/prosecutor/allowance-trend', body, 'allowance-trend'),
        apiPost('/v1/prosecutor/response-timing', body, 'response-timing'),
        apiPost('/v1/prosecutor/top-entities', body, 'top-entities')
    ]).then(results => {
        document.getElementById('loadingState').style.display = 'none';
        const [overview, allowance, oa, trend, timing, entities] = results;
        if (!overview) {
            showError('No data returned for this law firm.');
            return;
        }
        renderAll(overview, allowance, oa, trend, timing, entities);
        updateDiagnostics();
    }).catch(err => {
        document.getElementById('loadingState').style.display = 'none';
        showError('Failed to load data: ' + err.message);
    });
}

function apiPost(path, body, label) {
    diagCalls.push('POST ' + path);
    return fetch('/tip-api' + path, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(r => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
    })
    .then(json => {
        if (!json.status) throw new Error(json.message || 'API error');
        diagOutput[label] = json.data;
        return json.data;
    })
    .catch(err => {
        diagOutput[label] = 'Error: ' + err.message;
        return null;
    });
}

function showError(msg) {
    document.getElementById('errorState').style.display = 'block';
    document.getElementById('errorMsg').textContent = msg;
}

// ── Render ──
function renderAll(overview, allowance, oa, trend, timing, entities) {
    document.getElementById('resultsArea').style.display = 'block';
    renderOverview(overview);
    renderAllowance(allowance);
    renderOA(oa);
    renderTrend(trend);
    renderTiming(timing);
    renderEntities(entities);
}

function renderOverview(d) {
    if (!d || !d.ex_rule) return;
    const p = d.ex_rule.profile || {};
    const oa = d.ex_rule.oa || {};
    const pend = d.ex_rule.pendency || {};

    document.getElementById('firmNameTitle').textContent = p.name || currentFirm;

    const statsHtml = [
        statCard(p.total, 'Total Applications'),
        statCard(p.granted, 'Granted'),
        statCard((p.grant_rate_text || '0') + '%', 'Grant Rate'),
        statCard(p.experience ? p.experience + ' yrs' : '—', 'Experience')
    ].join('');
    document.getElementById('overviewStats').innerHTML = statsHtml;

    diagMapping['data.ex_rule.profile.total'] = 'Total Applications';
    diagMapping['data.ex_rule.profile.granted'] = 'Granted';
    diagMapping['data.ex_rule.profile.grant_rate_text'] = 'Grant Rate %';
    diagMapping['data.ex_rule.profile.experience'] = 'Experience';

    const detailsHtml = `
        <div>
            <div style="font-size:0.82rem; color:var(--tip-text-secondary, #6b7280); margin-bottom:0.5rem;">Office Actions</div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.5rem;">
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.3rem;">${oa.least_oa != null ? oa.least_oa : '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Least OA</div>
                </div>
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.3rem;">${oa.average_oa != null ? oa.average_oa : '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Avg OA</div>
                </div>
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.3rem;">${oa.most_oa != null ? oa.most_oa : '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Most OA</div>
                </div>
            </div>
        </div>
        <div>
            <div style="font-size:0.82rem; color:var(--tip-text-secondary, #6b7280); margin-bottom:0.5rem;">Pendency</div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.5rem;">
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.1rem;">${pend.shortest || '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Shortest</div>
                </div>
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.1rem;">${pend.average || '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Average</div>
                </div>
                <div class="tip-card" style="padding:0.75rem; text-align:center;">
                    <div class="tip-card-value" style="font-size:1.1rem;">${pend.longest || '—'}</div>
                    <div style="font-size:0.75rem; color:var(--tip-text-secondary);">Longest</div>
                </div>
            </div>
        </div>
        <div style="grid-column:1/-1; margin-top:0.5rem;">
            <div style="font-size:0.82rem; color:var(--tip-text-secondary, #6b7280);">
                <strong>GAUs:</strong> ${escHtml(p.gau || '—')} &nbsp;&bull;&nbsp;
                <strong>App Range:</strong> ${escHtml(p.app_range || '—')}
            </div>
        </div>
    `;
    document.getElementById('overviewDetails').innerHTML = detailsHtml;

    diagMapping['data.ex_rule.oa.least_oa'] = 'Least OA';
    diagMapping['data.ex_rule.oa.average_oa'] = 'Avg OA';
    diagMapping['data.ex_rule.oa.most_oa'] = 'Most OA';
    diagMapping['data.ex_rule.pendency.shortest'] = 'Shortest Pendency';
    diagMapping['data.ex_rule.pendency.average'] = 'Average Pendency';
    diagMapping['data.ex_rule.pendency.longest'] = 'Longest Pendency';
}

function statCard(value, label) {
    return '<div class="stat-card"><div class="tip-card-value">' + escHtml(String(value || '—')) + '</div><div class="stat-label">' + escHtml(label) + '</div></div>';
}

function renderAllowance(d) {
    if (!d || !d.ex_rule || !d.ex_rule.allowance) {
        document.getElementById('allowanceChart').innerHTML = '<div class="empty-state"><p>No allowance data available</p></div>';
        return;
    }
    const a = d.ex_rule.allowance;
    const allowed = a.allowance || {};
    const rejected = a.allowance_rej || {};
    const cats = allowed.categories || [];
    const aSeries = allowed.series || [];
    const rSeries = rejected.series || [];
    const aPct = allowed.series_percentage || [];
    const rPct = rejected.series_percentage || [];

    const maxVal = Math.max(...aSeries.map(Number), ...rSeries.map(Number), 1);

    let html = '<div class="bar-chart-row">';
    cats.forEach((cat, i) => {
        const av = Number(aSeries[i]) || 0;
        const rv = Number(rSeries[i]) || 0;
        const ah = Math.max((av / maxVal) * 180, 2);
        const rh = Math.max((rv / maxVal) * 180, 2);
        html += '<div class="bar-group">' +
            '<div class="bar-pair">' +
                '<div class="bar bar-allowed" style="height:' + ah + 'px;" title="Allowed: ' + av + ' (' + (aPct[i]||0) + '%)"></div>' +
                '<div class="bar bar-rejected" style="height:' + rh + 'px;" title="Rejected: ' + rv + ' (' + (rPct[i]||0) + '%)"></div>' +
            '</div>' +
            '<div class="bar-label">' + escHtml(cat) + '</div>' +
        '</div>';
    });
    html += '</div>';
    html += '<div style="display:flex; justify-content:space-between; margin-top:0.75rem; font-size:0.82rem; color:var(--tip-text-secondary);">' +
        '<span>Total Allowed: <strong>' + (allowed.total || 0) + '</strong></span>' +
        '<span>Total Rejected: <strong>' + (rejected.total || 0) + '</strong></span>' +
    '</div>';
    document.getElementById('allowanceChart').innerHTML = html;

    diagMapping['data.ex_rule.allowance.allowance.series'] = 'Allowed bar heights';
    diagMapping['data.ex_rule.allowance.allowance_rej.series'] = 'Rejected bar heights';
    diagMapping['data.ex_rule.allowance.allowance.categories'] = 'Category labels';
}

function renderOA(d) {
    if (!d || !d.ex_rule) {
        document.getElementById('oaChart').innerHTML = '<div class="empty-state"><p>No office action data available</p></div>';
        return;
    }

    const drilldown = d.ex_rule.oa_drilldown || {};
    const pie = d.ex_rule.oa_actions_pie || {};
    const brands = drilldown.ex_brandsData || [];
    const pieData = pie.pie || [];

    let html = '';

    // Drilldown bars
    if (brands.length) {
        const maxV = Math.max(...brands.map(b => Number(b.y) || 0), 1);
        html += '<div style="flex:1; min-width:200px;">';
        html += '<div style="font-size:0.82rem; color:var(--tip-text-secondary); margin-bottom:0.5rem;">OA Type Distribution</div>';
        html += '<div style="display:flex; flex-direction:column; gap:0.5rem;">';
        brands.forEach(b => {
            const pct = Number(b.y) || 0;
            html += '<div>' +
                '<div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:2px;">' +
                    '<span>' + escHtml(b.name) + '</span><span style="font-weight:600;">' + pct + '%</span>' +
                '</div>' +
                '<div style="height:20px; background:#f1f5f9; border-radius:4px; overflow:hidden;">' +
                    '<div style="height:100%; width:' + pct + '%; background:var(--tip-primary, #4f8ef7); border-radius:4px; transition:width 0.5s;"></div>' +
                '</div></div>';
        });
        html += '</div></div>';
    }

    // Pie chart (simple SVG)
    if (pieData.length) {
        const total = pieData.reduce((s, p) => s + (Number(p[1]) || 0), 0);
        const colors = ['#4f8ef7', '#f97316', '#10b981', '#8b5cf6', '#ef4444', '#eab308'];
        let cumAngle = 0;
        const r = 60, cx = 70, cy = 70;
        let paths = '';
        let legendHtml = '<div class="pie-info"><div style="font-size:0.82rem; color:var(--tip-text-secondary); margin-bottom:0.5rem;">OA Count Distribution</div><div class="pie-legend">';
        pieData.forEach((p, i) => {
            const val = Number(p[1]) || 0;
            const pct = total > 0 ? (val / total) * 100 : 0;
            const angle = (pct / 100) * 360;
            const startRad = (cumAngle - 90) * Math.PI / 180;
            const endRad = (cumAngle + angle - 90) * Math.PI / 180;
            const x1 = cx + r * Math.cos(startRad);
            const y1 = cy + r * Math.sin(startRad);
            const x2 = cx + r * Math.cos(endRad);
            const y2 = cy + r * Math.sin(endRad);
            const large = angle > 180 ? 1 : 0;
            if (pieData.length === 1) {
                paths += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + colors[i % colors.length] + '"/>';
            } else {
                paths += '<path d="M' + cx + ',' + cy + ' L' + x1 + ',' + y1 + ' A' + r + ',' + r + ' 0 ' + large + ',1 ' + x2 + ',' + y2 + ' Z" fill="' + colors[i % colors.length] + '"/>';
            }
            legendHtml += '<div class="pie-legend-item"><span class="pie-legend-dot" style="background:' + colors[i % colors.length] + ';"></span>' + escHtml(String(p[0])) + ' (' + pct.toFixed(1) + '%)</div>';
            cumAngle += angle;
        });
        legendHtml += '</div></div>';
        html += '<div class="pie-chart-svg"><svg width="140" height="140" viewBox="0 0 140 140">' + paths + '</svg></div>' + legendHtml;
    }

    if (!html) html = '<div class="empty-state"><p>No office action data available</p></div>';
    document.getElementById('oaChart').innerHTML = html;

    diagMapping['data.ex_rule.oa_drilldown.ex_brandsData'] = 'OA Type bars';
    diagMapping['data.ex_rule.oa_actions_pie.pie'] = 'OA Count pie slices';
}

function renderTrend(d) {
    if (!d || !d.ex_rule) {
        document.getElementById('trendChart').innerHTML = '<div class="empty-state"><p>No trend data available</p></div>';
        return;
    }
    const ha = d.ex_rule.historical_allowance || {};
    const cats = ha.categories || [];
    const granted = ha.granted || [];
    const abandon = ha.abandon || [];

    if (!cats.length) {
        document.getElementById('trendChart').innerHTML = '<div class="empty-state"><p>No trend data available</p></div>';
        return;
    }

    const maxVal = Math.max(...granted.map(Number), ...abandon.map(Number), 1);

    let html = '<div class="trend-row">';
    cats.forEach((cat, i) => {
        const gv = Number(granted[i]) || 0;
        const av = Number(abandon[i]) || 0;
        const gh = Math.max((gv / maxVal) * 180, 2);
        const ah = Math.max((av / maxVal) * 180, 2);
        html += '<div class="trend-group">' +
            '<div class="trend-pair">' +
                '<div class="trend-bar trend-granted" style="height:' + gh + 'px;" title="Granted: ' + gv + '"></div>' +
                '<div class="trend-bar trend-abandon" style="height:' + ah + 'px;" title="Abandoned: ' + av + '"></div>' +
            '</div>' +
            '<div class="trend-label">' + escHtml(cat) + '</div>' +
        '</div>';
    });
    html += '</div>';
    document.getElementById('trendChart').innerHTML = html;

    diagMapping['data.ex_rule.historical_allowance.categories'] = 'Year labels';
    diagMapping['data.ex_rule.historical_allowance.granted'] = 'Granted bars';
    diagMapping['data.ex_rule.historical_allowance.abandon'] = 'Abandoned bars';
}

function renderTiming(d) {
    if (!d || !d.ex_rule || !d.ex_rule.av_nfr_fr || !d.ex_rule.av_nfr_fr.results) {
        document.getElementById('timingChart').innerHTML = '<div class="empty-state"><p>No timing data available</p></div>';
        return;
    }
    const results = d.ex_rule.av_nfr_fr.results || [];
    if (!results.length) {
        document.getElementById('timingChart').innerHTML = '<div class="empty-state"><p>No timing data available</p></div>';
        return;
    }

    const maxVal = Math.max(...results.flatMap(r => (r.data || []).map(Number)), 1);

    let html = '';
    results.forEach(r => {
        const name = r.name || '';
        const data = r.data || [];
        const respVal = Number(data[0]) || 0;
        const oaVal = Number(data[1]) || 0;
        const respW = Math.max((respVal / maxVal) * 100, 2);
        const oaW = Math.max((oaVal / maxVal) * 100, 2);
        html += '<div class="timing-item">' +
            '<div class="timing-label">' + escHtml(name) + '</div>' +
            '<div class="timing-bar-wrap">' +
                '<div class="timing-bar-track">' +
                    '<div class="timing-bar-fill resp" style="width:' + respW + '%;">' + respVal + 'd</div>' +
                    '<div class="timing-bar-fill oa" style="width:' + oaW + '%;">' + oaVal + 'd</div>' +
                '</div>' +
            '</div>' +
        '</div>';
    });
    document.getElementById('timingChart').innerHTML = html;

    diagMapping['data.ex_rule.av_nfr_fr.results'] = 'Timing bars (Response & OA days)';
}

function renderEntities(d) {
    if (!d || !d.ex_rule || !d.ex_rule.attornies) {
        document.getElementById('topEntities').innerHTML = '<div class="empty-state"><p>No entity data available</p></div>';
        return;
    }
    const att = d.ex_rule.attornies;
    const names = att.attornee_names || [];
    const counts = att.attornee_count || [];
    const rates = att.allowances || [];

    if (!names.length) {
        document.getElementById('topEntities').innerHTML = '<div class="empty-state"><p>No entity data available</p></div>';
        return;
    }

    let html = '';
    names.forEach((name, i) => {
        const count = counts[i] || 0;
        const rate = rates[i] || 0;
        const rateNum = Number(rate);
        const tagClass = rateNum >= 70 ? 'tip-tag tip-tag-success' : rateNum >= 40 ? 'tip-tag tip-tag-warning' : 'tip-tag tip-tag-error';
        html += '<div class="entity-row">' +
            '<div class="entity-rank">' + (i + 1) + '</div>' +
            '<div class="entity-name">' + escHtml(name) + '</div>' +
            '<div class="entity-count">' + count + ' apps</div>' +
            '<div class="entity-rate"><span class="' + tagClass + '">' + rateNum.toFixed(1) + '%</span></div>' +
        '</div>';
    });
    document.getElementById('topEntities').innerHTML = html;

    diagMapping['data.ex_rule.attornies.attornee_names'] = 'Applicant names';
    diagMapping['data.ex_rule.attornies.attornee_count'] = 'Application counts';
    diagMapping['data.ex_rule.attornies.allowances'] = 'Allowance rates';
}

// ── Diagnostics ──
function updateDiagnostics() {
    document.getElementById('diagRequest').textContent = USER_REQUEST;
    document.getElementById('diagApiCalls').innerHTML = diagCalls.map(c => '<code>' + escHtml(c) + '</code>').join('<br>');
    document.getElementById('diagInput').innerHTML = '<pre style="margin:0; font-size:0.82rem;">' + escHtml(JSON.stringify(diagInput, null, 2)) + '</pre>';

    let outHtml = '';
    for (const [k, v] of Object.entries(diagOutput)) {
        outHtml += '<strong>' + escHtml(k) + ':</strong> ';
        if (typeof v === 'string') {
            outHtml += escHtml(v);
        } else {
            outHtml += '<pre style="margin:0; font-size:0.78rem; max-height:150px; overflow:auto;">' + escHtml(JSON.stringify(v, null, 2)) + '</pre>';
        }
        outHtml += '<br>';
    }
    document.getElementById('diagOutput').innerHTML = outHtml;

    let mapHtml = '<table class="tip-table" style="font-size:0.82rem;"><thead><tr><th>Response Field</th><th>UI Element</th></tr></thead><tbody>';
    for (const [field, ui] of Object.entries(diagMapping)) {
        mapHtml += '<tr><td><code>' + escHtml(field) + '</code></td><td>' + escHtml(ui) + '</td></tr>';
    }
    mapHtml += '</tbody></table>';
    document.getElementById('diagMapping').innerHTML = mapHtml;
}

function escHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}
</script>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html")
