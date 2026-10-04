![Fonts públiques d'Andorra](https://raw.githubusercontent.com/joalavedra/andorra-fonts-publiques/main/docs/banner.svg)

![CI](https://github.com/joalavedra/andorra-fonts-publiques/actions/workflows/ci.yml/badge.svg)

# Fonts públiques d'Andorra

Catàleg educatiu i petits clients Python per trobar i consultar les fonts públiques d'Andorra. Documenta com són els endpoints, les condicions de reutilització, el comportament verificat i els paranys pràctics, i exposa una selecció de dades en directe a través de Python, un servidor MCP i un assistent que cita les fonts.

**Projecte educatiu independent. No està afiliat al Govern d'Andorra ni a cap de les institucions esmentades.**

## Fonts

<!-- AUTO:SOURCES -->
| ID | Font | Sector | Accés |
|---|---|---|---|
| `afa-feeds` | [Andorran Financial Authority feeds](https://www.afa.ad) | Finances i regulació | feed |
| `bopa` | [Butlletí Oficial del Principat d'Andorra](https://www.bopa.ad/) | Legislació i butlletins oficials | api, downloads |
| `carburants` | [Fuel stations and reference prices](https://sig.govern.ad/server/rest/services/CARBURANTS/CARBURANTS/FeatureServer) | Energia i carburants | arcgis-rest |
| `cass-estadistiques` | [CASS statistics downloads](https://www.cass.ad/estadistiques) | Seguretat social | downloads |
| `consell-general-feeds` | [Consell General news feeds](https://www.consellgeneral.ad) | Parlament i informació cívica | feed |
| `e-tramits` | [e-tramits procedures](https://www.e-tramits.ad/tramits) | Serveis públics i tràmits | html |
| `estadistica-api` | [Andorra Department of Statistics API](https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api) | Estadística oficial | api |
| `govern-ad` | [Govern d'Andorra information pages](https://www.govern.ad/) | Serveis públics i tràmits | html |
| `meteo-ad` | [meteo.ad station charts](https://www.meteo.ad) | Meteorologia i clima | html |
| `sig-arcgis` | [Govern d'Andorra ArcGIS Enterprise](https://sig.govern.ad/server/rest/services) | Geografia i cartografia | arcgis-rest |
| `transparencia` | [Transparency portal](https://www.transparencia.ad/) | Transparència i administració pública | html, downloads |
<!-- /AUTO:SOURCES -->

Les condicions de reutilització de cada font es detallen a [Condicions de les dades d'origen](#condicions-de-les-dades-dorigen) i a cada fitxa de `sources/`.

## Inici ràpid

Cal Python 3.10 o posterior:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/fonts-andorra-mcp
```

El servidor MCP es comunica per stdio. Configura Claude Desktop, Claude Code o Cursor amb l'ordre instal·lada:

```json
{
  "mcpServers": {
    "andorra-fonts-publiques": {
      "command": "/absolute/path/to/andorra-fonts-publiques/.venv/bin/fonts-andorra-mcp"
    }
  }
}
```

## Instal·lar el servidor MCP

Executa el servidor publicat amb `uvx`:

```bash
uvx fonts-andorra
```

Configuració de Claude Desktop:

```json
{
  "mcpServers": {
    "andorra": {
      "command": "uvx",
      "args": ["fonts-andorra"]
    }
  }
}
```

<!-- mcp-name: io.github.joalavedra/andorra-fonts-publiques -->

## Assistent amb cites

Fes una pregunta amb cites fent servir l'API REST de Gemini. Defineix `GEMINI_API_KEY` a l'entorn; mai no es desa en aquest repositori:

```bash
GEMINI_API_KEY=... .venv/bin/fonts-andorra-ask "Quant triga l'autorització inicial de residència i treball?"
.venv/bin/fonts-andorra-ask "Where can I find official unemployment statistics?" --lang en --json
```

Els clients també es poden importar directament:

```python
from fonts_andorra.clients.estadistica import data, search

tables = search("atur")
rows = data(1070)  # Per defecte, startDate=1900 i endDate=2100.
```

## Condicions de les dades d'origen

El codi i el catàleg d'aquest repositori es dediquen al domini públic sota CC0-1.0. Això no canvia la llicència del material d'origen:

- **BOPA** permet copiar, adaptar, extreure i redistribuir el contingut amb condicions: cal conservar la font i les metadades d'actualització, no desvirtuar-ne el sentit i no donar a entendre cap aval.
- Les dades d'**Estadística** propietat del Departament d'Estadística són CC BY 4.0; les dades de tercers poden tenir condicions pròpies.
- **govern.ad, e-tràmits i Transparència** són continguts del Govern amb tots els drets reservats. El projecte en descarrega el cos de les pàgines en directe, les cita i hi enllaça, però no en redistribueix el contingut. Per republicar-lo cal un consentiment per escrit. L'índex local del Govern només conté títols, URL i encapçalaments de secció.
- **Les capes ArcGIS i de carburants** es tracten com a contingut del Govern amb tots els drets reservats perquè no s'indica cap llicència per element; el projecte les consulta en directe, n'enllaça la font i no en redistribueix el contingut.
- **Feeds, meteo.ad i CASS**: les condicions per element no existeixen o no s'han revisat; consulta les condicions de l'editor abans de redistribuir-ne les dades.

El catàleg indica les fonts i les condicions una per una. Verifica les condicions de cada element abans de fer-ne un ús comercial o de republicar-lo.

## Fitxers del catàleg

- `sources/<id>.yaml` conté les fitxes de les fonts.
- `schema/source.schema.json` i `schema/vocab.yaml` defineixen el contracte de les fitxes i els vocabularis tancats.
- `indices/dead-routes.yaml` recull els dominis que no responen, comprovats el 2026-10-02.
- `catalog.json`, `llms.txt` i `llms-full.txt` es generen amb `python scripts/build.py`.
- `python scripts/validate.py` comprova l'esquema de les fonts, els vocabularis i els identificadors de fonts relacionades.

## Índex de cerca local

`fonts_andorra/data/index.json` conté els títols i URL d'e-tràmits i, del Govern, només títols, URL i encapçalaments de secció; el cos de totes les pàgines es descarrega en directe i es cita, perquè el contingut d'origen té tots els drets reservats. L'assistent cerca tràmits i pàgines del Govern amb BM25 en local i descarrega en directe les pàgines trobades; no fa servir el cercador del web del Govern, que està prohibit.
Per reconstruir-lo a partir d'e-tràmits i del sitemap en català del Govern, executa `.venv/bin/python scripts/build_index.py`; aquest generador necessita xarxa i, per això, no forma part de la CI.

## Proves

Les proves funcionen sense connexió i fan servir respostes públiques desades:

```bash
.venv/bin/ruff check .
.venv/bin/pytest -q
python scripts/validate.py
python scripts/build.py
```

## CI

`ci.yml` executa el lint, les proves sense connexió, la validació i la comprovació dels fitxers generats a cada push i pull request; `live.yml` fa comprovacions setmanals en directe i en penja un informe.
La comprovació de l'assistent de `live.yml` necessita el secret `GEMINI_API_KEY` al repositori.

## Avaluació de l'assistent

`evals/procedures.yaml` conté 10 tràmits reals amb la resposta de referència (preu, termini màxim de resolució, període de sol·licitud i si cal anar-hi presencialment), presa de les pàgines d'e-tràmits el 2026-10-02. S'executa amb:

```bash
GEMINI_API_KEY=... .venv/bin/python evals/run.py --baseline
```

Últim resultat (`evals/results-2026-10-03.md`, `gemini-2.5-flash`): 10/10 casos superats amb el tràmit correcte citat i 18/18 dades correctes. El mateix model sense fonts n'encerta 3/18. Aquests 10 casos també es van fer servir per ajustar la cerca, així que s'han de considerar un joc de regressió i no pas una avaluació independent.

### Joc reservat

`evals/heldout.yaml` conté 20 casos més, escrits un cop acabat l'ajust: 15 tràmits que no s'havien fet servir per ajustar (ca/es/fr/en) i 5 preguntes que cap font d'aquí no pot respondre (el temps, preus de forfets d'esquí, cues a la frontera, el telèfon personal d'un ministre i els dies de vacances de l'usuari), que l'assistent ha de declinar sense donar cap xifra.

```bash
GEMINI_API_KEY=... .venv/bin/python evals/run.py --cases evals/heldout.yaml --baseline
```

- Primera execució (`evals/results-heldout-2026-10-03-first-run.md`): 15/20 segons el puntuador. Tres errors eren del puntuador (no llegia cites escrites com `[1, 2]` i no reconeixia "no se encontró" com a resposta declinada). Tornant a puntuar les mateixes respostes surt 18/20. Els dos errors reals:
  - El filtre de dades personals emmascarava dates com `23-09-2026` com si fossin telèfons, i l'assistent no podia donar el període de sol·licitud. Ja està corregit.
  - Per a "I'm selling my flat and need the habitability certificate", va respondre a partir de la *cèdula d'habitabilitat* (2 mesos) en lloc del *certificat d'habitabilitat* (72 hores). La pregunta és ambigua, perquè una venda necessita la cèdula.
- Després de les correccions (`evals/results-heldout-2026-10-03.md`): 20/20, 23/23 dades, 5/5 preguntes sense resposta declinades i 0 cites incorrectes. El mateix model sense fonts n'encerta 6/23. El cas de l'habitabilitat va passar perquè la cerca va retornar uns altres tràmits, no gràcies a cap correcció. La generació de paraules clau no és del tot determinista, així que aquest cas pot canviar.

A partir d'aquí aquest joc ja no és estrictament reservat: s'hi va trobar una correcció. Les noves fallades s'han de corregir amb casos nous.

La proposta d'una pàgina per al Govern és a `docs/pitch.md`.
