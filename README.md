# UKWEB – Dějiny umění

Rozcestník na výpisky a procvičovačky. Běží na GitHub Pages:
**https://aurasscz.github.io/UKWEB/**

## Přidání nové lekce

1. Otevři složku [`lekce`](lekce) → **Add file** → **Upload files**.
2. Přetáhni tam stažený artefakt:
   - jeden soubor, např. `gotika.html`, **nebo**
   - celou složku, pokud má lekce obrázky (např. `gotika/index.html` + `gotika/img/…`).
3. **Commit changes**. Za 1–2 minuty je lekce na hlavní stránce.

Nic dalšího se upravovat nemusí. Akce [`Seznam lekcí`](.github/workflows/seznam-lekci.yml)
po každém nahrání přepočítá `lekce.json` a hlavní stránka z něj čte.

- **Název** lekce = `<title>` v HTML souboru.
- **Popis** = `<meta name="description">`, jinak první odstavec stránky.
- **Datum** = kdy byl soubor nahrán. Dá se přepsat:
  `<meta name="ukweb-datum" content="2026-10-06">`.
- Soubor nebo složka začínající `_` se na hlavní stránce nezobrazí (např. rozpracovaná lekce).

Smazání nebo přejmenování lekce funguje stejně – po commitu se seznam sám aktualizuje.

## Struktura

```
index.html                 hlavní stránka (seznam lekcí)
lekce.html                 otevře lekci s lištou „← Dějiny umění“
lekce.json                 seznam lekcí – generuje se automaticky, ručně neupravovat
lekce/                     sem se nahrávají lekce
scripts/build_manifest.py  skript, který sestaví lekce.json
```

Lokálně: `python scripts/build_manifest.py` a pak `python -m http.server`.
