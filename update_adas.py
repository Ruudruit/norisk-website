#!/usr/bin/env python3
"""
Voeg ADAS-data toe op basis van Hella Gutmann Coverage List V81 (Front Camera).
Verwijdert kalibratie_type kolom.
Gebruik: python3 update_adas.py automodellen_nieuw.csv > automodellen_adas.csv
"""
import csv, re, sys

def norm(text):
    """Lowercase + alleen alphanumeric + spaties."""
    t = text.lower().strip()
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# ── Hella Gutmann V81 – Vehicle Coverage Front Camera ──────────────────────
# Sleutel: (CSV_MERK_UPPER, set_van_genormaliseerde_model_keywords)
# Bij match op een keyword → adas = "ja"
ADAS = {
    'ALFA ROMEO': {'giulia', 'stelvio', 'tonale', 'junior'},
    'AUDI': {'a1', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
             'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8',
             'tt', 'e tron', 'etron', 'rs3', 'rs4', 'rs5', 'rs6', 'rs7',
             's3', 's4', 's5', 's6', 's7', 'sq3', 'sq5', 'sq7', 'sq8'},
    'BMW': {'1 serie', '2 serie', '3 serie', '4 serie', '5 serie',
            '6 serie', '7 serie', '8 serie',
            'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'xm',
            'z4', 'i3', 'i4', 'i5', 'i7', 'ix', 'm2', 'm3', 'm4', 'm5'},
    'CITROEN': {'berlingo', 'c3', 'c4', 'c5', 'jumper', 'jumpy',
                'spacetourer', 'e c3'},
    'CUPRA': {'born', 'formentor', 'tavascan', 'terramar', 'leon', 'ateca'},
    'DACIA': {'jogger', 'sandero', 'bigster'},
    'DS': {'ds 3', 'ds 4', 'ds 5', 'ds3', 'ds4', 'ds5'},
    'FIAT': {'500x', '500e', '600', 'ducato', 'panda', 'tipo', 'talento', 'scudo'},
    'FORD': {'fiesta', 'focus', 'galaxy', 'kuga', 'mondeo',
             'mustang', 'puma', 'ranger', 's max', 'transit',
             'explorer', 'capri'},
    'HONDA': {'accord', 'civic', 'cr v', 'hr v', 'jazz', 'zr v', 'insight'},
    'HYUNDAI': {'grand sante fe', 'grand santa fe', 'ioniq', 'kona',
                'santa fe', 'tucson', 'i20', 'i30', 'i40', 'nexo',
                'i10', 'inster'},
    'JAGUAR': {'e pace', 'f pace', 'xe', 'xf', 'i pace'},
    'JEEP': {'avenger', 'cherokee', 'compass', 'grand cherokee', 'renegade'},
    'KIA': {"cee d", 'ceed', 'niro', 'optima', 'proceed', 'xceed',
            'rio', 'sorento', 'soul', 'sportage', 'stinger', 'stonic',
            'ev6', 'ev9', 'ev5', 'ev3', 'ev4'},
    'LANDROVER': {'defender', 'discovery', 'evoque', 'range rover', 'velar', 'freelander'},
    'LEXUS': {'ct', 'es', 'gs', 'is', 'lx', 'nx', 'rc', 'rx', 'ux'},
    'LYNKCO': {'lynk co 01', 'lynk co 02'},
    'MAN': {'tge'},
    'MAZDA': {'2', '3', '6',
              'cx 3', 'cx 30', 'cx 5', 'cx 60', 'cx 80',
              'mx5', 'mx 5'},
    'MERCEDES': {'a', 'b', 'c', 'citan', 'cl', 'cla', 'cls', 'e',
                 'eqa', 'eqb', 'eqc', 'eqs', 'g', 'gl', 'gla', 'glb',
                 'glc', 'gle', 'glk', 'gls', 'm', 's', 'sl', 'slk',
                 'sprinter', 'v', 'vito', 'viano', 'x'},
    'MINI': {'mini', 'clubman', 'countryman', 'cabrio', 'coupe'},
    'MITSUBISHI': {'asx', 'eclipse cross', 'l200', 'outlander', 'triton'},
    'NISSAN': {'ariya', 'juke', 'leaf', 'micra', 'qashqai', 'x trail'},
    'OPEL': {'ampera', 'astra', 'combo', 'corsa', 'crossland',
             'grandland', 'insignia', 'karl', 'mokka', 'vivaro', 'zafira'},
    'PEUGEOT': {'108', '2008', '208', '3008', '308', '408', '5008', '508',
                'expert', 'partner', 'rifter', 'traveller'},
    'PORSCHE': {'911', 'boxster', 'cayenne', 'cayman', 'macan',
                'panamera', 'taycan'},
    'RENAULT': {'arkana', 'austral', 'captur', 'clio', 'espace',
                'kadjar', 'kangoo', 'kangooo', 'koleos', 'master',
                'megane', 'scenic', 'talisman', 'trafic', 'twingo', 'zoe',
                '4 e tech', '5 e tech'},
    'SEAT': {'alhambra', 'arona', 'ateca', 'ibiza', 'leon', 'mii', 'tarraco'},
    'SKODA': {'citigo', 'enyaq', 'fabia', 'kamiq', 'karoq',
              'kodiaq', 'octavia', 'superb', 'yeti'},
    'SMART': {'for four', 'forfour', 'for two', 'fortwo'},
    'SUBARU': {'forester', 'impreza', 'legacy', 'outback', 'solterra',
               'levorg', 'crosstrek'},
    'SUZUKI': {'across', 'ignis', 'jimny', 's cross', 'sx4', 'swace',
               'swift', 'vitara'},
    'TOYOTA': {'auris', 'avensis', 'aygo', 'bz4x', 'bx4x', 'c hr',
               'corolla', 'hilux', 'land cruiser', 'landcruiser', 'mirai',
               'prius', 'proace', 'rav', 'verso', 'yaris', 'fortuner',
               'highlander', 'tundra'},
    'VOLVO': {'s60', 's90', 'v40', 'v60', 'v90', 'xc40', 'xc60', 'xc90',
              'ex30', 'ex40', 's80'},
    'VW': {'amarok', 'arteon', 'caddy', 'crafter', 'golf',
           'id 3', 'id 4', 'id 5', 'id 7', 'id buzz',
           'id3', 'id4', 'id5', 'id7', 'idbuzz',
           'passat', 'polo', 'sharan', 't cross', 't roc',
           'tairon', 'tayron', 'tiguan', 'touareg', 'touran',
           'transporter', 'up'},
}

# Exclusief: deze modellen NIET als ADAS markeren ook al matcht een keyword
# (bijv. BMW Z3 staat niet in Hella lijst)
EXCLUDE = {
    'BMW': {'z3'},
    'MERCEDES': {'actros', 'antos', 'atego', 'vario'},
    'OPEL': {'adam', 'agila', 'antara', 'frontera', 'meriva', 'movano',
             'sintra', 'tigra', 'vectra'},
    'HONDA': {'cr z', 'crz', 'fr v', 'frv', 'prelude'},
    'FORD': {'b max', 'c max', 'ka', 'fusion'},
    'TOYOTA': {'celica', 'gt86', 'iq', 'mr2', 'paseo', 'picnic',
               'previa', 'celica'},
    'MAZDA': {'5', 'mx3', 'mx6', 'premacy'},
    'PEUGEOT': {'106', '107', '206', '207', '307', '406', '407',
                '4008', 'boxer', 'bipper', 'rcz'},
    'RENAULT': {'laguna', 'modus', 'twizzy', 'twingo electric'},
    'VW': {'bora', 'eos', 'fox', 'jetta', 'lt', 'lupo',
           'new beetle', 'scirocco'},
    'SUBARU': {'trezia'},
    'SUZUKI': {'alto', 'baleno', 'celerio', 'kizashi', 'liana',
               'splash', 'wagon r'},
    'NISSAN': {'almera tino', 'cabstar', 'cube', 'interstar',
               'kubistar', 'note', 'nv200', 'nv250', 'nv300',
               'nv400', 'pathfinder', 'pixo', 'primastar'},
    'FIAT': {'500', '500 cabrio', '500l', 'croma', 'doblo',
             'fiorino', 'grande punto', 'idea', 'punto'},
    'HYUNDAI': {'getz', 'h100', 'h200', 'matrix', 'sonata',
                'trajet', 'ix20', 'ix35', 'ix55'},
    'KIA': {'carens', 'carnival', 'opirus', 'picanto', 'venga'},
    'MITSUBISHI': {'canter', 'carisma', 'colt', 'lancer',
                   'pajero', 'spacestar', 'spacewagon'},
    'SEAT': {'altea', 'arosa', 'inca', 'toledo'},
    'SKODA': {'rapid', 'roomster'},
    'VOLVO': {'c30', 's40', 's70', 'v50', 'v70', 'xc70',
              '740', '760', '850', '940', '960'},
    'CITROEN': {'c crosser', 'c zero', 'c1', 'c15', 'c2',
                'c3 picasso', 'c4 aircross', 'c6', 'nemo', 'saxo'},
    'LANDROVER': {},
    'LEXUS': {},
    'DACIA': {'dokker', 'duster', 'lodgy', 'logan'},
    'DS': {},
}


ADAS_MIN_JAAR = 2010  # ADAS front camera bestaat niet in auto's ouder dan dit

def has_adas(merk, model, bouwjaar_tot=None):
    # Te oude auto's nooit ADAS
    try:
        if bouwjaar_tot and int(bouwjaar_tot) < ADAS_MIN_JAAR:
            return False
    except ValueError:
        pass
    merk_up = merk.upper().strip()
    keywords = ADAS.get(merk_up, set())
    excludes = EXCLUDE.get(merk_up, set())
    model_n  = norm(model)

    model_words = set(model_n.split())

    # Check exclusions first
    for ex in excludes:
        ex_n = norm(ex)
        if not ex_n:
            continue
        if model_n == ex_n:
            return False
        # Startswith alleen voor meerdere woorden (voorkomt "5" → "cx 5")
        ex_words = set(ex_n.split())
        if len(ex_words) >= 2:
            if model_n.startswith(ex_n + ' ') or model_n.startswith(ex_n):
                return False
            if ex_words.issubset(model_words):
                return False

    # Check ADAS keywords
    for kw in keywords:
        kw_n = norm(kw)
        if not kw_n:
            continue
        kw_words = set(kw_n.split())
        # Exact match (werkt voor '2', '3', '6', 'cx 5', etc.)
        if model_n == kw_n:
            return True
        # Multi-word keyword: startswith of subset check
        if len(kw_words) >= 2:
            if model_n.startswith(kw_n + ' ') or model_n.startswith(kw_n):
                return True
            if kw_words.issubset(model_words):
                return True
        # Single-word keyword min 2 tekens: model begint ermee
        elif len(kw_n) >= 2:
            if model_n.startswith(kw_n + ' ') or model_n.startswith(kw_n + '-'):
                return True

    return False


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'automodellen_nieuw.csv'
    output_cols = ['merk', 'model', 'merk_slug', 'model_slug', 'adas',
                   'bouwjaar_van', 'bouwjaar_tot', 'reparatie_prijs', 'vervanging_prijs']

    with open(csv_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    writer = csv.DictWriter(sys.stdout, fieldnames=output_cols, lineterminator='\n')
    writer.writeheader()

    adas_ja = 0
    for r in rows:
        adas_val = 'ja' if has_adas(r['merk'], r['model'], r.get('bouwjaar_tot')) else 'nee'
        if adas_val == 'ja':
            adas_ja += 1
        out = {c: r.get(c, '') for c in output_cols}
        out['adas'] = adas_val
        writer.writerow(out)

    print(f"# ADAS ja: {adas_ja} van {len(rows)}", file=sys.stderr)


if __name__ == '__main__':
    main()
