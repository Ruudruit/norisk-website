#!/usr/bin/env python3
"""Genereer /voorruit/{merk}/index.html voor elk merk."""

import csv, os, sys
from collections import defaultdict

# ── Merkkleuren (zelfde als in voorruit/index.html) ──────────────────────────
ACCENT = {
    'aiways':     '#1B539B', 'alfa-romeo': '#9B1016', 'audi':    '#BB0A0A',
    'bmw':        '#1C69D4', 'byd':        '#1B539B', 'chevrolet':'#D4A017',
    'chrysler':   '#2B2B2B', 'citroen':    '#E51C26', 'cupra':   '#BF9B47',
    'dacia':      '#003189', 'dodge':      '#CC0000', 'ds':      '#333333',
    'fiat':       '#8C1C20', 'fisker':     '#1B1B1B', 'ford':    '#003C92',
    'honda':      '#CC0000', 'hyundai':    '#002C5F', 'infinity':'#1A1A1A',
    'iveco':      '#003087', 'jaguar':     '#1A1A1A', 'jeep':    '#2B5134',
    'kia':        '#05141F', 'lancia':     '#003087', 'landrover':'#005A2B',
    'lexus':      '#1A1A1A', 'lynkco':     '#1B1B1B', 'man':     '#E2001A',
    'mazda':      '#820000', 'mercedes':   '#222222', 'mini':    '#1C1C1C',
    'mitsubishi': '#CC0000', 'nio':        '#1B539B', 'nissan':  '#C3002F',
    'opel':       '#FFCD00', 'peugeot':    '#0053A0', 'porsche': '#8B0000',
    'renault':    '#EFDF00', 'saab':       '#1A3A5C', 'seat':    '#1B1B1B',
    'skoda':      '#4BA82E', 'smart':      '#00ADEF', 'subaru':  '#003087',
    'suzuki':     '#003087', 'toyota':     '#EB0A1E', 'volvo':   '#003057',
    'vw':         '#001E50', 'xpeng':      '#1B539B', 'zeekr':   '#1B539B',
}

# Lichte merken waarbij tekst donker moet zijn
LIGHT_ACCENT = {'opel', 'renault'}

TELEFOON = '088-022 5800'

SEARCH_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'

PHONE_SVG = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:5px;flex-shrink:0"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.95 10.59 19.79 19.79 0 01.88 2 2 2 0 012.87 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L7.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>'


def fmt_prijs(p):
    try:
        return f"€ {int(float(p)):,}".replace(',', '.')
    except (ValueError, TypeError):
        return None


def model_card(r, depth='../../'):
    slug_mo = r['model_slug']
    bj_van  = r['bouwjaar_van']
    bj_tot  = r['bouwjaar_tot']
    model   = r['model']
    uitv    = r.get('uitvoering', '').strip()
    rep     = fmt_prijs(r.get('reparatie_prijs', ''))
    verv    = fmt_prijs(r.get('vervanging_prijs', ''))
    url     = f"{slug_mo}/{bj_van}-{bj_tot}/"

    uitv_html = f'<span class="mc-uitv">{uitv}</span>' if uitv else ''
    bj_html   = f'<span class="mc-bj">{bj_van} – {bj_tot}</span>'

    prijzen = []
    if rep:
        prijzen.append(f'<span class="mc-prijs-rep">Reparatie v.a. <strong>{rep}</strong></span>')
    if verv:
        prijzen.append(f'<span class="mc-prijs-verv">Vervanging v.a. <strong>{verv}</strong></span>')
    prijs_html = '<div class="mc-prijzen">' + ''.join(prijzen) + '</div>' if prijzen else ''

    return f'''<a href="{url}" class="model-card">
  <div class="mc-top">
    <span class="mc-naam">{model}</span>
    {uitv_html}
  </div>
  {bj_html}
  {prijs_html}
  <span class="mc-cta">Bekijk opties →</span>
</a>'''


def generate_merk_page(merk_slug, rows, out_dir):
    merk_naam = rows[0]['merk']
    accent    = ACCENT.get(merk_slug, '#CC0000')
    dark_text = merk_slug in LIGHT_ACCENT
    txt_color = '#111' if dark_text else '#fff'
    depth     = '../../'

    # Logo: probeer svg, dan png, dan monogram
    logo_svg_path  = f'{depth}logos/{merk_slug}.svg'
    logo_png_path  = f'{depth}logos/{merk_slug}.png'
    monogram       = merk_naam[:3].upper()
    logo_html = f'''<div class="merk-logo-wrap">
      <img src="{logo_svg_path}" alt="{merk_naam} logo"
        onerror="this.src='{logo_png_path}';this.onerror=function(){{this.closest('.merk-logo-wrap').innerHTML='<div class=merk-monogram style=background:{accent};color:{txt_color}>{monogram}</div>'}}">
    </div>'''

    cards_html = '\n'.join(model_card(r, depth) for r in rows)

    n_modellen = len(rows)
    title = f"Voorruit {merk_naam} vervangen – Alle modellen | No-Risk Autoruitservice"
    desc  = (f"Bekijk alle {n_modellen} {merk_naam}-modellen waarvoor No-Risk Autoruitservice "
             f"een voorruit kan repareren of vervangen. Veelal €0,- eigen risico.")

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://no-risk.nl/voorruit/{merk_slug}/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --rood: #CC0000; --rood-hover: #aa0000; --wit: #fff;
      --accent: {accent};
      --radius: 8px; --transition: 0.2s ease;
    }}
    body {{ font-family: 'Inter', sans-serif; background: #f4f5f7; color: #222; }}

    /* ── NAV ── */
    nav {{
      position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
      background: rgba(17,17,17,0.97); backdrop-filter: blur(8px);
      padding: 0 2rem; height: 68px;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .nav-logo {{ display: flex; align-items: center; text-decoration: none; }}
    .nav-logo img {{ height: 34px; width: auto; }}
    .nav-links {{ display: flex; align-items: center; gap: 0.2rem; list-style: none; }}
    .nav-links a {{
      color: rgba(255,255,255,0.82); text-decoration: none;
      padding: 0.5rem 0.9rem; border-radius: var(--radius);
      font-size: 0.93rem; position: relative; transition: color var(--transition);
    }}
    .nav-links a::after {{
      content: ''; position: absolute; bottom: 4px; left: 0.9rem; right: 0.9rem;
      height: 2px; background: var(--rood);
      transform: scaleX(0); transform-origin: left; transition: transform var(--transition);
    }}
    .nav-links a:hover {{ color: #fff; }}
    .nav-links a:hover::after {{ transform: scaleX(1); }}
    .nav-cta {{ background: var(--rood); color: #fff !important;
      padding: 0.5rem 1.1rem !important; border-radius: var(--radius) !important;
      font-weight: 600; display: inline-flex; align-items: center; gap: 5px; }}
    .nav-cta:hover {{ background: var(--rood-hover) !important; }}
    .nav-cta::after {{ display: none !important; }}
    /* Zoekbalk */
    .nav-search {{ position: relative; display: flex; align-items: center; margin-left: 0.5rem; }}
    .search-toggle {{
      background: none; border: none; cursor: pointer; color: rgba(255,255,255,0.8);
      display: flex; align-items: center; justify-content: center;
      width: 38px; height: 38px; border-radius: 50%; transition: background 0.2s, color 0.2s;
    }}
    .search-toggle:hover, .search-toggle[aria-expanded="true"] {{ background: rgba(255,255,255,0.12); color: #fff; }}
    .search-toggle svg {{ width: 18px; height: 18px; }}
    .search-box {{
      display: none; position: absolute; right: 0; top: calc(100% + 10px);
      width: 360px; background: #fff; border-radius: 10px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.22); overflow: hidden; z-index: 2000;
    }}
    .search-box.open {{ display: block; }}
    .search-inner {{ display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-bottom: 1px solid #eee; }}
    .search-inner svg {{ width: 16px; height: 16px; color: #aaa; flex-shrink: 0; }}
    #search-input {{ flex: 1; border: none; outline: none; font-size: 0.97rem; color: #222; background: transparent; font-family: inherit; }}
    #search-input::placeholder {{ color: #bbb; }}
    #search-results {{ list-style: none; max-height: 320px; overflow-y: auto; padding: 4px 0; }}
    .sr-item {{ display: flex; align-items: center; justify-content: space-between; padding: 9px 14px; text-decoration: none; color: #222; transition: background 0.15s; }}
    .sr-item:hover, .sr-item:focus {{ background: #f5f5f5; outline: none; }}
    .sr-label {{ font-size: 0.9rem; font-weight: 500; }}
    .sr-label mark {{ background: none; color: var(--rood); font-weight: 700; }}
    .sr-bj {{ font-size: 0.78rem; color: #999; white-space: nowrap; margin-left: 8px; }}
    .sr-empty {{ padding: 12px 14px; color: #999; font-size: 0.88rem; }}
    /* Hamburger */
    .hamburger {{ display: none; flex-direction: column; gap: 5px; cursor: pointer;
      background: none; border: none; padding: 4px; }}
    .hamburger span {{ display: block; width: 24px; height: 2px; background: #fff; border-radius: 2px; }}

    /* ── HEADER ── */
    .page-header {{
      background: linear-gradient(135deg, #0f0f0f 50%, color-mix(in srgb, {accent} 30%, #0f0f0f) 100%);
      padding: 110px 2rem 56px; text-align: center;
    }}
    .breadcrumb {{
      font-size: 0.78rem; color: rgba(255,255,255,0.4);
      margin-bottom: 1.6rem; display: flex; justify-content: center; align-items: center; gap: 0.4rem;
    }}
    .breadcrumb a {{ color: rgba(255,255,255,0.4); text-decoration: none; }}
    .breadcrumb a:hover {{ color: #fff; }}
    .merk-logo-wrap {{
      width: 80px; height: 80px; background: rgba(255,255,255,0.08);
      border-radius: 50%; display: flex; align-items: center; justify-content: center;
      margin: 0 auto 1.2rem; overflow: hidden;
    }}
    .merk-logo-wrap img {{ width: 60px; height: 60px; object-fit: contain; }}
    .merk-monogram {{
      width: 80px; height: 80px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.3rem; font-weight: 800; letter-spacing: -0.5px;
      margin: 0 auto 1.2rem;
    }}
    .page-header h1 {{
      font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 800;
      color: #fff; line-height: 1.15; margin-bottom: 0.7rem;
    }}
    .page-header h1 em {{ color: var(--accent); font-style: normal; }}
    .page-header p {{ color: rgba(255,255,255,0.6); font-size: 1rem; max-width: 500px; margin: 0 auto; }}

    /* ── MODELLEN GRID ── */
    .modellen-wrap {{ max-width: 1100px; margin: 0 auto; padding: 2.5rem 1.5rem 4rem; }}
    .modellen-count {{ font-size: 0.85rem; color: #888; margin-bottom: 1.2rem; }}
    .modellen-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1rem;
    }}
    .model-card {{
      background: #fff; border: 1.5px solid #e8e8e8; border-radius: 10px;
      padding: 1.2rem 1.1rem 1rem;
      text-decoration: none; color: #222;
      display: flex; flex-direction: column; gap: 0.5rem;
      position: relative; overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .model-card::before {{
      content: ''; position: absolute; top: 0; left: 0; right: 0;
      height: 3px; background: var(--accent);
    }}
    .model-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.1); border-color: transparent; }}
    .mc-top {{ display: flex; flex-direction: column; gap: 2px; }}
    .mc-naam {{ font-weight: 700; font-size: 1rem; color: #111; }}
    .mc-uitv {{ font-size: 0.78rem; font-weight: 600; color: var(--accent); letter-spacing: 0.3px; }}
    .mc-bj {{ font-size: 0.8rem; color: #888; }}
    .mc-prijzen {{ display: flex; flex-direction: column; gap: 2px; margin-top: 2px; }}
    .mc-prijs-rep, .mc-prijs-verv {{ font-size: 0.76rem; color: #666; }}
    .mc-prijs-rep strong, .mc-prijs-verv strong {{ color: #222; font-weight: 700; }}
    .mc-cta {{
      margin-top: auto; padding-top: 0.6rem;
      font-size: 0.82rem; font-weight: 600; color: var(--accent);
    }}

    /* ── FOOTER ── */
    .footer-mini {{
      background: #111; color: rgba(255,255,255,0.4); text-align: center;
      padding: 1.5rem; font-size: 0.82rem;
    }}
    .footer-mini a {{ color: rgba(255,255,255,0.5); text-decoration: none; }}
    .footer-mini a:hover {{ color: #fff; }}

    @media (max-width: 768px) {{
      .hamburger {{ display: flex; }}
      .nav-links {{
        display: none; flex-direction: column; gap: 0;
        position: absolute; top: 68px; left: 0; right: 0;
        background: rgba(17,17,17,0.98); padding: 1rem 0;
      }}
      .nav-links.open {{ display: flex; }}
      .nav-links a {{ padding: 0.75rem 2rem; border-radius: 0; }}
      .nav-links a::after {{ display: none; }}
      .modellen-grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }}
    }}
  </style>
</head>
<body>

<nav>
  <a href="{depth}index.html" class="nav-logo" aria-label="No-Risk Autoruitservice - Home">
    <img src="{depth}logo.png" alt="No-Risk Autoruitservice">
  </a>
  <button class="hamburger" id="hamburger" aria-label="Menu openen">
    <span></span><span></span><span></span>
  </button>
  <ul class="nav-links" id="nav-links">
    <li><a href="{depth}index.html">Home</a></li>
    <li><a href="{depth}voorruit/">Voorruit per merk</a></li>
    <li><a href="{depth}diensten.html">Diensten</a></li>
    <li><a href="{depth}locaties.html">Locaties</a></li>
    <li><a href="{depth}contact.html">Contact</a></li>
    <li><a href="tel:{TELEFOON.replace('-','').replace(' ','')}" class="nav-cta">{PHONE_SVG}{TELEFOON}</a></li>
  </ul>
  <div class="nav-search">
    <button class="search-toggle" id="search-toggle" aria-label="Zoeken" aria-expanded="false">
      {SEARCH_SVG}
    </button>
    <div class="search-box" id="search-box" role="dialog" aria-label="Zoek een automodel">
      <div class="search-inner">
        {SEARCH_SVG}
        <input type="search" id="search-input" placeholder="Zoek merk of model…" autocomplete="off" spellcheck="false">
      </div>
      <ul id="search-results"></ul>
    </div>
  </div>
</nav>

<div class="page-header">
  <div class="breadcrumb">
    <a href="{depth}index.html">Home</a>
    <span>›</span>
    <a href="{depth}voorruit/">Voorruit per merk</a>
    <span>›</span>
    {merk_naam}
  </div>
  {logo_html}
  <h1>Voorruit <em>{merk_naam}</em><br>vervangen of repareren?</h1>
  <p>Kies uw model en ontdek de opties voor uw specifieke uitvoering.</p>
</div>

<div class="modellen-wrap">
  <p class="modellen-count">{n_modellen} model{'len' if n_modellen != 1 else ''} gevonden</p>
  <div class="modellen-grid">
    {cards_html}
  </div>
</div>

<footer class="footer-mini">
  © 2025 No-Risk Autoruitservice &nbsp;·&nbsp;
  <a href="{depth}index.html">Home</a> &nbsp;·&nbsp;
  <a href="{depth}locaties.html">Locaties</a> &nbsp;·&nbsp;
  <a href="{depth}contact.html">Contact</a>
</footer>

<script>
  const h = document.getElementById('hamburger');
  const n = document.getElementById('nav-links');
  h.addEventListener('click', () => n.classList.toggle('open'));
</script>
<script src="{depth}search.js"></script>
</body>
</html>"""

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def main(csv_path):
    # Groepeer rijen per merk
    merken = defaultdict(list)
    with open(csv_path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            merken[r['merk_slug']].append(r)

    base = os.path.join(os.path.dirname(csv_path), 'voorruit')
    count = 0
    for slug, rows in sorted(merken.items()):
        # Sorteer modellen alfabetisch, dan op bouwjaar
        rows_sorted = sorted(rows, key=lambda r: (r['model'], r['bouwjaar_van']))
        out_dir = os.path.join(base, slug)
        path = generate_merk_page(slug, rows_sorted, out_dir)
        print(f"  ✓ {path}")
        count += 1

    print(f"\n✅ {count} merkpagina's gegenereerd.")


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'automodellen_uitvoering.csv'
    main(csv_path)
