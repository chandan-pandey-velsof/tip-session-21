from django.http import HttpResponse


def index(request):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dashboard</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         "Helvetica Neue", Arial, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            color: #1a1a2e;
        }

        /* ── Top nav ── */
        header {
            background: #1a1a2e;
            padding: 0 2rem;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0,0,0,.35);
        }
        header .brand {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: .5px;
        }
        header .brand span { color: #4f8ef7; }
        header .nav-right {
            font-size: .85rem;
            color: #a0a8bf;
        }

        /* ── Page wrapper ── */
        main {
            max-width: 1100px;
            margin: 2.5rem auto;
            padding: 0 1.5rem;
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: .4rem;
            color: #1a1a2e;
        }
        .subtitle {
            font-size: .95rem;
            color: #6b7280;
            margin-bottom: 2.2rem;
        }

        /* ── Stats grid ── */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.8rem 2rem;
            display: flex;
            align-items: center;
            gap: 1.4rem;
            box-shadow: 0 4px 18px rgba(0,0,0,.07);
            transition: transform .2s ease, box-shadow .2s ease;
            position: relative;
            overflow: hidden;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 28px rgba(0,0,0,.12);
        }
        /* Decorative accent strip */
        .card::before {
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 5px; height: 100%;
            border-radius: 16px 0 0 16px;
        }
        .card-users::before  { background: linear-gradient(180deg, #4f8ef7, #6a5af9); }
        .card-revenue::before { background: linear-gradient(180deg, #34d399, #059669); }
        .card-orders::before  { background: linear-gradient(180deg, #f97316, #ef4444); }

        /* Icon bubble */
        .icon-bubble {
            width: 58px; height: 58px;
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.6rem;
            flex-shrink: 0;
        }
        .card-users   .icon-bubble { background: #eff4ff; }
        .card-revenue .icon-bubble { background: #ecfdf5; }
        .card-orders  .icon-bubble { background: #fff7ed; }

        .card-body { flex: 1; }
        .card-label {
            font-size: .8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #9ca3af;
            margin-bottom: .35rem;
        }
        .card-value {
            font-size: 2.1rem;
            font-weight: 800;
            line-height: 1;
            color: #1a1a2e;
        }
        .card-users   .card-value { color: #4f8ef7; }
        .card-revenue .card-value { color: #059669; }
        .card-orders  .card-value { color: #f97316; }

        .card-trend {
            margin-top: .55rem;
            font-size: .82rem;
            color: #6b7280;
        }
        .card-trend .badge {
            display: inline-block;
            padding: .15rem .5rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: .75rem;
            margin-right: .35rem;
        }
        .badge-up   { background: #dcfce7; color: #16a34a; }
        .badge-down { background: #fee2e2; color: #dc2626; }

        /* ── Footer note ── */
        .footer-note {
            text-align: center;
            margin-top: 3rem;
            font-size: .8rem;
            color: #9ca3af;
        }
    </style>
</head>
<body>

<header>
    <div class="brand">Admin<span>Panel</span></div>
    <div class="nav-right">Welcome back, Admin &nbsp;👋</div>
</header>

<main>
    <h1>Dashboard Overview</h1>
    <p class="subtitle">Here&rsquo;s a summary of your key metrics at a glance.</p>

    <div class="stats-grid">

        <!-- Total Users -->
        <div class="card card-users">
            <div class="icon-bubble">👥</div>
            <div class="card-body">
                <div class="card-label">Total Users</div>
                <div class="card-value">1,234</div>
                <div class="card-trend">
                    <span class="badge badge-up">▲ 12%</span> vs last month
                </div>
            </div>
        </div>

        <!-- Revenue -->
        <div class="card card-revenue">
            <div class="icon-bubble">💰</div>
            <div class="card-body">
                <div class="card-label">Revenue</div>
                <div class="card-value">$56,789</div>
                <div class="card-trend">
                    <span class="badge badge-up">▲ 8%</span> vs last month
                </div>
            </div>
        </div>

        <!-- Orders -->
        <div class="card card-orders">
            <div class="icon-bubble">📦</div>
            <div class="card-body">
                <div class="card-label">Orders</div>
                <div class="card-value">890</div>
                <div class="card-trend">
                    <span class="badge badge-down">▼ 3%</span> vs last month
                </div>
            </div>
        </div>

    </div>

    <p class="footer-note">Data refreshed daily &bull; Last updated: today</p>
</main>

</body>
</html>
"""
    return HttpResponse(html, content_type="text/html")
