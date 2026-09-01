#!/usr/bin/env python3
"""
Genereer search-data.json — combineert automodellen + merkpagina's + locaties + diensten + overige pagina's.
Gebruik: python3 generate_search.py [automodellen_uitvoering.csv]
"""
import csv, json, os, sys

def main(csv_path='automodellen_uitvoering.csv'):
    entries = []

    # ── 1. Vaste pagina's (locaties, diensten, overige) ─────────────────────
    VASTE = [
        # Locaties
        {"l": "Amsterdam",              "s": "/amsterdam.html",      "b": "Locatie", "t": "locatie"},
        {"l": "Rotterdam",              "s": "/rotterdam.html",      "b": "Locatie", "t": "locatie"},
        {"l": "Den Haag",               "s": "/denhaag.html",        "b": "Locatie", "t": "locatie"},
        {"l": "Barendrecht",            "s": "/barendrecht.html",    "b": "Locatie", "t": "locatie"},
        {"l": "Spijkenisse",            "s": "/spijkenisse.html",    "b": "Locatie", "t": "locatie"},

        # Diensten / services
        {"l": "Schade melden",          "s": "/contact.html",        "b": "Dienst",  "t": "dienst"},
        {"l": "Voorruit reparatie",     "s": "/diensten.html",       "b": "Dienst",  "t": "dienst"},
        {"l": "Voorruit vervangen",     "s": "/diensten.html",       "b": "Dienst",  "t": "dienst"},
        {"l": "Achterruit vervangen",   "s": "/diensten.html",       "b": "Dienst",  "t": "dienst"},
        {"l": "ADAS kalibratie",        "s": "/diensten.html",       "b": "Dienst",  "t": "dienst"},
        {"l": "Mobiele ruitservice",    "s": "/diensten.html",       "b": "Dienst",  "t": "dienst"},

        # Verzekering / eigen risico
        {"l": "Verzekering eigen risico", "s": "/contact.html",      "b": "Info",    "t": "info"},
        {"l": "WA+ ruitschade",         "s": "/contact.html",        "b": "Info",    "t": "info"},
        {"l": "Allrisk ruitschade",     "s": "/contact.html",        "b": "Info",    "t": "info"},
        {"l": "Sterreparatie €0 eigen risico", "s": "/diensten.html","b": "Info",    "t": "info"},

        # Overig
        {"l": "Contact",               "s": "/contact.html",         "b": "Pagina",  "t": "pagina"},
        {"l": "Locaties overzicht",    "s": "/locaties.html",        "b": "Pagina",  "t": "pagina"},
        {"l": "Alle merken",           "s": "/voorruit/",            "b": "Overzicht","t": "pagina"},
        {"l": "Over ons",              "s": "/over-ons.html",        "b": "Pagina",  "t": "pagina"},
        {"l": "BOVAG garantie",        "s": "/diensten.html",        "b": "Info",    "t": "info"},
    ]
    entries.extend(VASTE)

    # ── 2. Merkpagina's ──────────────────────────────────────────────────────
    merken_gezien = set()
    if os.path.exists(csv_path):
        with open(csv_path, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                slug = r['merk_slug']
                naam = r['merk']
                if slug not in merken_gezien:
                    merken_gezien.add(slug)
                    entries.append({
                        "l": naam,
                        "s": f"/voorruit/{slug}/",
                        "b": "Merk",
                        "t": "merk"
                    })

    # ── 3. Automodellen ──────────────────────────────────────────────────────
    if os.path.exists(csv_path):
        with open(csv_path, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                merk      = r['merk']
                model     = r['model']
                bj_van    = r['bouwjaar_van']
                bj_tot    = r['bouwjaar_tot']
                merk_slug = r['merk_slug']
                model_slug= r['model_slug']
                uitv      = r.get('uitvoering', '').strip()

                label = f"{merk} {model}"
                if uitv:
                    label += f" {uitv}"

                entries.append({
                    "l": label,
                    "s": f"/voorruit/{merk_slug}/{model_slug}/{bj_van}-{bj_tot}/",
                    "b": f"{bj_van}–{bj_tot}",
                    "t": "model"
                })

    out = json.dumps(entries, ensure_ascii=False, separators=(',', ':'))
    out_path = os.path.join(os.path.dirname(csv_path) or '.', 'search-data.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"✅ {len(entries)} items → {out_path}")
    return out_path


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'automodellen_uitvoering.csv'
    main(csv_path)
