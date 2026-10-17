# Dějiny umění

**Web:** https://aurasscz.github.io/UKWEB/

Sbírka interaktivních výpisků a procvičovaček na Dějiny umění, kterou jsem si udělal jako
gymnazista. Každá lekce vznikla ze zápisků z hodin nebo z toho, co bylo na tabuli.
Nejde jen o přepsaný text: lekce mají režimy na zakrývání, kvízy a karty, které se
dají otáčet. Učivo se z nich tak dá opravdu procvičit, ne jen přečíst.

Hlavní stránka je zároveň archiv: nové lekce přibývají nahoru a ty starší zůstávají
dostupné, takže se k nim dá před písemkou nebo maturitou kdykoli vrátit.

## Co tu je

| Lekce | Obsah |
| --- | --- |
| **Svatí a atributy** | Apoštolové a světoví svatí s obrázky. Poznávání podle atributů, režim zkoušení se zamícháním karet. |
| **Náboženství z tabule** | Egypt (Atonův kult), judaismus, křesťanství a islám: bůh, postava, místa, symbol, posvátný text. Přehled, zakrývání a kvíz. |

Další lekce budou průběžně přibývat.

## Jak to funguje

Web je čistě statický a běží na GitHub Pages, bez frameworku a bez build kroku na straně
prohlížeče.

- Každá lekce je samostatná HTML stránka ve složce [`lekce/`](lekce). Buď jeden soubor,
  nebo složka s `index.html` a obrázky.
- Po každém nahrání spustí GitHub Action [`Seznam lekcí`](.github/workflows/seznam-lekci.yml)
  skript [`build_manifest.py`](scripts/build_manifest.py). Ten projde lekce, vytáhne z nich
  název, popis a datum a zapíše je do `lekce.json`.
- [`index.html`](index.html) z `lekce.json` vykreslí přehled s vyhledáváním a s lekcemi
  seskupenými po měsících.
- [`lekce.html`](lekce.html) otevře vybranou lekci s lištou pro návrat na přehled.

Díky tomu se nová lekce přidává jen nahráním souboru. Na hlavní stránce není potřeba nic
ručně upravovat.

## Jak to vzniklo

Lekce i celý web vytvořil **Claude Opus 5.5** (Anthropic) s nastavením úsilí **High**,
v aplikaci Claude Code. Podklady dodávám já: fotky zápisků, tabule a obrázků z hodin. Claude
je převádí na interaktivní stránky a stará se o web a jeho nasazení.

## Licence

Kód webu je pod licencí [Apache 2.0](LICENSE). Obrázky uměleckých děl v lekcích pocházejí
ze školních podkladů a slouží jen ke studiu. Na ně se licence repozitáře nevztahuje, viz
[NOTICE](NOTICE).
