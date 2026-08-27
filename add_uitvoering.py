#!/usr/bin/env python3
"""
Voeg 'uitvoering' kolom toe aan automodellen_adas.csv.
Sleutel: (MERK, MODEL, bouwjaar_tot) → uitvoering-code/generatie.
Gebruik: python3 add_uitvoering.py automodellen_adas.csv > automodellen_uitvoering.csv
"""
import csv, sys

# (MERK_UPPER, MODEL_UPPER, bouwjaar_tot_str) → uitvoering
UITVOERING = {

    # ── BMW ──────────────────────────────────────────────────────────
    ('BMW', '1 SERIE', '2012'): 'E87',
    ('BMW', '1 SERIE', '2019'): 'F20',
    ('BMW', '1 SERIE', '2025'): 'F40',

    ('BMW', '2 SERIE', '2025'): 'G42',
    ('BMW', '2 SERIE ACTIVE TOURER', '2022'): 'F45',
    ('BMW', '2 SERIE ACTIVE TOURER', '2025'): 'U06',
    ('BMW', '2 SERIE GRAN TOURER', '2025'): 'F46',

    ('BMW', '3 SERIE', '1990'): 'E30',
    ('BMW', '3 SERIE', '1998'): 'E36',
    ('BMW', '3 SERIE', '2005'): 'E46',
    ('BMW', '3 SERIE', '2012'): 'E90',
    ('BMW', '3 SERIE', '2019'): 'F30',
    ('BMW', '3 SERIE', '2025'): 'G20',

    ('BMW', '3 SERIE CABRIO', '1992'): 'E30',
    ('BMW', '3 SERIE CABRIO', '1998'): 'E36',
    ('BMW', '3 SERIE CABRIO', '2005'): 'E46',
    ('BMW', '3 SERIE CABRIO', '2012'): 'E93',

    ('BMW', '3 SERIE COMPACT', '2000'): 'E36',
    ('BMW', '3 SERIE COMPACT', '2005'): 'E46',

    ('BMW', '3 SERIE COUPE', '1992'): 'E30',
    ('BMW', '3 SERIE COUPE', '1999'): 'E36',
    ('BMW', '3 SERIE COUPE', '2006'): 'E46',
    ('BMW', '3 SERIE COUPE', '2013'): 'E92',

    ('BMW', '4 SERIE CABRIO', '2025'): 'G23',
    ('BMW', '4 SERIE COUPE', '2025'): 'G22',

    ('BMW', '5 SERIE', '1987'): 'E28',
    ('BMW', '5 SERIE', '1995'): 'E34',
    ('BMW', '5 SERIE', '2003'): 'E39',
    ('BMW', '5 SERIE', '2010'): 'E60',
    ('BMW', '5 SERIE', '2017'): 'F10',
    ('BMW', '5 SERIE', '2021'): 'G30',
    ('BMW', '5 SERIE', '2025'): 'G60',

    ('BMW', '6 SERIE', '2011'): 'E63',
    ('BMW', '6 SERIE', '2025'): 'F13',

    ('BMW', '7 SERIE', '2001'): 'E38',
    ('BMW', '7 SERIE', '2008'): 'E65',
    ('BMW', '7 SERIE', '2015'): 'F01',
    ('BMW', '7 SERIE', '2022'): 'G11',
    ('BMW', '7 SERIE', '2025'): 'G70',

    ('BMW', 'X1', '2015'): 'E84',
    ('BMW', 'X1', '2022'): 'F48',
    ('BMW', 'X1', '2025'): 'U11',

    ('BMW', 'X2', '2025'): 'F39',

    ('BMW', 'X3', '2010'): 'E83',
    ('BMW', 'X3', '2017'): 'F25',
    ('BMW', 'X3', '2025'): 'G01',

    ('BMW', 'X4', '2018'): 'F26',
    ('BMW', 'X4', '2025'): 'G02',

    ('BMW', 'X5', '2006'): 'E53',
    ('BMW', 'X5', '2013'): 'E70',
    ('BMW', 'X5', '2018'): 'F15',
    ('BMW', 'X5', '2025'): 'G05',

    ('BMW', 'X6', '2014'): 'E71',
    ('BMW', 'X6', '2019'): 'F16',
    ('BMW', 'X6', '2025'): 'G06',

    ('BMW', 'Z3', '2003'): 'E36/7',
    ('BMW', 'Z4', '2009'): 'E85',

    ('BMW', 'M2', '2025'): 'G87',
    ('BMW', 'M3', '2025'): 'G80',
    ('BMW', 'M4', '2025'): 'G82',
    ('BMW', 'M5', '2025'): 'G90',

    # ── VW ───────────────────────────────────────────────────────────
    ('VW', 'GOLF', '1982'): 'Golf 1',
    ('VW', 'GOLF', '1991'): 'Golf 2',
    ('VW', 'GOLF', '1997'): 'Golf 3',
    ('VW', 'GOLF', '2003'): 'Golf 4',
    ('VW', 'GOLF', '2008'): 'Golf 5',
    ('VW', 'GOLF', '2012'): 'Golf 6',
    ('VW', 'GOLF', '2019'): 'Golf 7',
    ('VW', 'GOLF', '2025'): 'Golf 8',

    ('VW', 'GOLF CABRIO', '1993'): 'Golf 1',
    ('VW', 'GOLF CABRIO', '1995'): 'Golf 2',
    ('VW', 'GOLF CABRIO', '2000'): 'Golf 3',
    ('VW', 'GOLF CABRIO', '2016'): 'Golf 6',

    ('VW', 'GOLF VARIANT', '2011'): 'Golf 6',
    ('VW', 'GOLF VARIANT', '2025'): 'Golf 7/8',

    ('VW', 'POLO', '1995'): 'Polo 3 (6N)',
    ('VW', 'POLO', '1999'): 'Polo 3 (6N)',
    ('VW', 'POLO', '2001'): 'Polo 4 (9N)',
    ('VW', 'POLO', '2009'): 'Polo 4 (9N)',
    ('VW', 'POLO', '2017'): 'Polo 5 (6R)',
    ('VW', 'POLO', '2025'): 'Polo 6 (AW)',

    ('VW', 'PASSAT', '1996'): 'B4',
    ('VW', 'PASSAT', '2005'): 'B5',
    ('VW', 'PASSAT', '2014'): 'B6/B7',
    ('VW', 'PASSAT', '2024'): 'B8',
    ('VW', 'PASSAT', '2025'): 'B9',

    ('VW', 'TIGUAN', '2016'): '5N',
    ('VW', 'TIGUAN', '2025'): 'AD1',

    ('VW', 'TOUAREG', '2010'): '7L',
    ('VW', 'TOUAREG', '2018'): '7P',
    ('VW', 'TOUAREG', '2025'): 'CR7',

    ('VW', 'TOURAN', '2015'): '1T',
    ('VW', 'TOURAN', '2025'): '5T',

    ('VW', 'SHARAN', '2010'): 'Mk1',
    ('VW', 'SHARAN', '2025'): 'Mk2',

    ('VW', 'CADDY', '1995'): 'Mk1',
    ('VW', 'CADDY', '2004'): 'Mk2',
    ('VW', 'CADDY', '2025'): 'Mk3/Mk4',

    ('VW', 'TRANSPORTER', '1978'): 'T2',
    ('VW', 'TRANSPORTER', '1990'): 'T3',
    ('VW', 'TRANSPORTER', '2003'): 'T4',
    ('VW', 'TRANSPORTER', '2015'): 'T5',
    ('VW', 'TRANSPORTER', '2025'): 'T6',

    ('VW', 'CRAFTER', '2017'): 'Mk1',
    ('VW', 'CRAFTER', '2025'): 'Mk2',

    # ── MERCEDES ─────────────────────────────────────────────────────
    ('MERCEDES', 'A', '2004'): 'W168',
    ('MERCEDES', 'A', '2012'): 'W169',
    ('MERCEDES', 'A', '2018'): 'W176',
    ('MERCEDES', 'A', '2025'): 'W177',

    ('MERCEDES', 'B', '2011'): 'W245',
    ('MERCEDES', 'B', '2019'): 'W246',

    ('MERCEDES', 'C', '2007'): 'W203',
    ('MERCEDES', 'C', '2014'): 'W204',
    ('MERCEDES', 'C', '2021'): 'W205',
    ('MERCEDES', 'C', '2025'): 'W206',

    ('MERCEDES', 'E', '2002'): 'W210',
    ('MERCEDES', 'E', '2009'): 'W211',
    ('MERCEDES', 'E', '2016'): 'W212',
    ('MERCEDES', 'E', '2023'): 'W213',
    ('MERCEDES', 'E', '2025'): 'W214',

    ('MERCEDES', 'S', '1998'): 'W140',
    ('MERCEDES', 'S', '2005'): 'W220',
    ('MERCEDES', 'S', '2013'): 'W221',
    ('MERCEDES', 'S', '2020'): 'W222',
    ('MERCEDES', 'S', '2025'): 'W223',

    ('MERCEDES', 'CL', '2006'): 'C215',
    ('MERCEDES', 'CL', '2025'): 'C216',

    ('MERCEDES', 'CLA', '2019'): 'C117',
    ('MERCEDES', 'CLA', '2025'): 'C118',

    ('MERCEDES', 'CLK', '2002'): 'W208',
    ('MERCEDES', 'CLK', '2009'): 'W209',

    ('MERCEDES', 'CLS', '2011'): 'C219',
    ('MERCEDES', 'CLS', '2018'): 'C257',
    ('MERCEDES', 'CLS', '2025'): 'C257',

    ('MERCEDES', 'GLA', '2020'): 'X156',
    ('MERCEDES', 'GLA', '2025'): 'H247',

    ('MERCEDES', 'GLC', '2022'): 'X253',
    ('MERCEDES', 'GLC', '2025'): 'X254',

    ('MERCEDES', 'GLE', '2019'): 'W166',
    ('MERCEDES', 'GLE', '2025'): 'V167',

    ('MERCEDES', 'GLK', '2015'): 'X204',

    ('MERCEDES', 'GLS', '2019'): 'X166',
    ('MERCEDES', 'GLS', '2025'): 'X167',

    ('MERCEDES', 'M', '2005'): 'W163',
    ('MERCEDES', 'M', '2011'): 'W164',
    ('MERCEDES', 'M', '2015'): 'W166',

    ('MERCEDES', 'SL', '2001'): 'R129',
    ('MERCEDES', 'SL', '2012'): 'R230',
    ('MERCEDES', 'SLK', '2004'): 'R170',
    ('MERCEDES', 'SLK', '2011'): 'R171',
    ('MERCEDES', 'SLK', '2025'): 'R172',

    ('MERCEDES', 'SPRINTER', '2006'): 'W901',
    ('MERCEDES', 'SPRINTER', '2018'): 'W906',
    ('MERCEDES', 'SPRINTER', '2025'): 'W907',

    ('MERCEDES', 'VITO', '2003'): 'W638',
    ('MERCEDES', 'VITO', '2014'): 'W639',
    ('MERCEDES', 'VITO', '2025'): 'W447',

    ('MERCEDES', 'V', '2003'): 'W638',
    ('MERCEDES', 'V', '2025'): 'W447',

    # ── AUDI ─────────────────────────────────────────────────────────
    ('AUDI', 'A1', '2018'): '8X',
    ('AUDI', 'A1', '2025'): 'GB',

    ('AUDI', 'A3', '2003'): '8L',
    ('AUDI', 'A3', '2012'): '8P',
    ('AUDI', 'A3', '2020'): '8V',

    ('AUDI', 'A3 CABRIO', '2014'): '8P',
    ('AUDI', 'A3 CABRIO', '2025'): '8V',

    ('AUDI', 'A4', '2000'): 'B5',
    ('AUDI', 'A4', '2007'): 'B6/B7',
    ('AUDI', 'A4', '2015'): 'B8',
    ('AUDI', 'A4', '2025'): 'B9',

    ('AUDI', 'A4 CABRIO', '2009'): 'B6/B7',

    ('AUDI', 'A5', '2016'): '8T',
    ('AUDI', 'A5', '2025'): 'F5',

    ('AUDI', 'A5 CABRIO', '2017'): '8F',
    ('AUDI', 'A5 CABRIO', '2025'): 'F5',

    ('AUDI', 'A6', '1998'): 'C4',
    ('AUDI', 'A6', '2005'): 'C5',
    ('AUDI', 'A6', '2011'): 'C6',
    ('AUDI', 'A6', '2018'): 'C7',
    ('AUDI', 'A6', '2025'): 'C8',

    ('AUDI', 'A7', '2018'): '4G',
    ('AUDI', 'A7', '2025'): '4K',

    ('AUDI', 'A8', '2002'): 'D2',
    ('AUDI', 'A8', '2010'): 'D3',
    ('AUDI', 'A8', '2017'): 'D4',
    ('AUDI', 'A8', '2025'): 'D5',

    ('AUDI', 'Q3', '2018'): '8U',
    ('AUDI', 'Q3', '2025'): 'F3',

    ('AUDI', 'Q5', '2017'): '8R',
    ('AUDI', 'Q5', '2025'): 'FY',

    ('AUDI', 'Q7', '2015'): '4L',
    ('AUDI', 'Q7', '2025'): '4M',

    ('AUDI', 'TT', '2006'): '8N',
    ('AUDI', 'TT', '2014'): '8J',
    ('AUDI', 'TT', '2025'): '8S',

    ('AUDI', 'RS6', '2005'): 'C5',
    ('AUDI', 'RS6', '2011'): 'C6',
    ('AUDI', 'RS6', '2025'): 'C8',

    ('AUDI', 'S3', '2003'): '8L',
    ('AUDI', 'S3', '2012'): '8P',

    ('AUDI', 'S4', '2000'): 'B5',
    ('AUDI', 'S4', '2007'): 'B6/B7',

    ('AUDI', 'S5', '2016'): '8T',

    ('AUDI', 'S6', '1997'): 'C4',
    ('AUDI', 'S6', '2005'): 'C5',

    ('AUDI', 'SQ3', '2018'): '8U',
    ('AUDI', 'SQ3', '2025'): 'F3',

    ('AUDI', 'SQ5', '2017'): '8R',
    ('AUDI', 'SQ5', '2025'): 'FY',

    ('AUDI', 'SQ7', '2015'): '4L',
    ('AUDI', 'SQ7', '2025'): '4M',
}


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'automodellen_adas.csv'

    with open(csv_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    fieldnames = list(rows[0].keys()) + ['uitvoering']

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()

    gevonden = 0
    for r in rows:
        key = (r['merk'].upper().strip(), r['model'].upper().strip(), r['bouwjaar_tot'].strip())
        uitvoering = UITVOERING.get(key, '')
        if uitvoering:
            gevonden += 1
        r['uitvoering'] = uitvoering
        writer.writerow(r)

    print(f"# Uitvoering ingevuld: {gevonden} van {len(rows)} ({len(rows)-gevonden} leeg)", file=sys.stderr)


if __name__ == '__main__':
    main()
