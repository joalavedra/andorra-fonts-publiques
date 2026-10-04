![CI](https://github.com/joalavedra/andorra-fonts-publiques/actions/workflows/ci.yml/badge.svg)

# Andorra public sources

An educational catalog and small Python clients for finding and querying public sources in Andorra. It documents the endpoint shapes, reuse terms, verified behavior and practical traps, then exposes selected live data through Python, an MCP server and a cited assistant.

Aquest projecte educatiu reuneix fonts públiques d'Andorra, amb exemples i clients per consultar-les. És independent i no està afiliat al Govern d'Andorra.

This project adapts ideas and code from [BquantFinance/Administracion-fuentes-publicas](https://github.com/BquantFinance/Administracion-fuentes-publicas), an upstream project released under CC0-1.0.

**Independent educational project. Not affiliated with the Govern d'Andorra or any listed institution.**

## Sources

<!-- AUTO:SOURCES -->
| ID | Source | Sector | Access | Licence |
|---|---|---|---|---|
| `afa-feeds` | [Andorran Financial Authority feeds](https://www.afa.ad) | finance | feed | Feed redistribution terms were not checked; use for live retrieval and link to the original item. |
| `bopa` | [Butlletí Oficial del Principat d'Andorra](https://www.bopa.ad/) | legislation | api, downloads | Reuse including copying, adaptation, extraction, redistribution and public communication is allowed subject to preserving metadata and update dates, not distorting meaning, and not implying BOPA endorsement. |
| `carburants` | [Fuel stations and reference prices](https://sig.govern.ad/server/rest/services/CARBURANTS/CARBURANTS/FeatureServer) | energy | arcgis-rest | All rights reserved under Govern d'Andorra terms; this project fetches the layers live and cites links without redistributing their content. |
| `cass-estadistiques` | [CASS statistics downloads](https://www.cass.ad/estadistiques) | social-security | downloads | Reuse terms were not checked; consult the publisher before redistributing files. |
| `consell-general-feeds` | [Consell General news feeds](https://www.consellgeneral.ad) | parliament | feed | Feed redistribution terms were not checked; use for live retrieval and link to the original item. |
| `e-tramits` | [e-tramits procedures](https://www.e-tramits.ad/tramits) | public-services | html | All rights reserved under Govern d'Andorra terms; this project fetches pages live and cites them, and does not redistribute their content. |
| `estadistica-api` | [Andorra Department of Statistics API](https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api) | statistics | api | Creative Commons Attribution 4.0 International for statistics owned by the Department; third-party data may have other terms. |
| `govern-ad` | [Govern d'Andorra information pages](https://www.govern.ad/) | public-services | html | All rights reserved under Govern d'Andorra terms; this project fetches pages live and cites them, and does not redistribute page content. Its local index stores titles, URLs and section headings only. |
| `meteo-ad` | [meteo.ad station charts](https://www.meteo.ad) | meteorology | html | No usable legal notice was found; legal page was empty, so reuse terms are unknown. |
| `sig-arcgis` | [Govern d'Andorra ArcGIS Enterprise](https://sig.govern.ad/server/rest/services) | geography | arcgis-rest | All rights reserved under Govern d'Andorra terms; layer licenses were not stated, so this project fetches live and cites links without redistributing layer content. |
| `transparencia` | [Transparency portal](https://www.transparencia.ad/) | transparency | html, downloads | All rights reserved under Govern d'Andorra terms; this project fetches pages live and cites them, and does not redistribute their content. |
<!-- /AUTO:SOURCES -->

## Quickstart

Python 3.10 or newer:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/fonts-andorra-mcp
```

The MCP server communicates over stdio. Configure Claude Desktop, Claude Code or Cursor with the installed command:

```json
{
  "mcpServers": {
    "andorra-fonts-publiques": {
      "command": "/absolute/path/to/andorra-fonts-publiques/.venv/bin/fonts-andorra-mcp"
    }
  }
}
```

## Install the MCP server

Run the published server with `uvx`:

```bash
uvx fonts-andorra
```

Claude Desktop configuration:

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

Ask a cited question using Gemini REST. Set `GEMINI_API_KEY` in the environment; it is never stored in this repository:

```bash
GEMINI_API_KEY=... .venv/bin/fonts-andorra-ask "Quant triga l'autorització inicial de residència i treball?"
.venv/bin/fonts-andorra-ask "Where can I find official unemployment statistics?" --lang en --json
```

The clients can also be imported directly:

```python
from fonts_andorra.clients.estadistica import data, search

tables = search("atur")
rows = data(1070)  # Defaults to startDate=1900 and endDate=2100.
```

## Source data terms

This repository's own code and catalog are dedicated to the public domain under CC0-1.0. That does not relicense the source material:

- **BOPA** permits copying, adaptation, extraction and redistribution subject to its conditions: preserve source and update metadata, do not distort meaning, and do not imply endorsement.
- **Statistics** data owned by the Department of Statistics is CC BY 4.0; third-party data may have separate terms.
- **govern.ad, e-tramits and Transparency** are all-rights-reserved Government content. The project fetches page bodies live, cites and links them, and does not redistribute their content. Written consent is required for republication. The Govern local index contains only titles, URLs and section headings.
- **ArcGIS and fuel layers** are treated as all-rights-reserved Govern content because item-level licenses were not stated; this project fetches them live, cites links and does not redistribute their content.
- **Feeds, meteo.ad and CASS**: item-specific terms are absent or were not checked; review the publisher's terms before redistributing data.

The catalog marks sources and terms individually. Verify the terms that apply to each item before using it commercially or republishing it.

## Catalog files

- `sources/<id>.yaml` contains the source fiches.
- `schema/source.schema.json` and `schema/vocab.yaml` define the fiche contract and closed vocabularies.
- `indices/dead-routes.yaml` lists unresolved domains checked on 2026-10-02.
- `catalog.json`, `llms.txt` and `llms-full.txt` are generated by `python scripts/build.py`.
- `python scripts/validate.py` checks source schema, vocabularies and related source IDs.

## Local search index

`fonts_andorra/data/index.json` contains e-tramits titles and URLs, plus Govern page titles, URLs and section headings only; all page bodies are fetched live and cited because the source content is all rights reserved. Assistant procedure and Govern retrieval use local BM25 search and fetch matching pages live; Govern's disallowed site search is not used.
Rebuild it from live e-tramits and the Catalan Govern sitemap with `.venv/bin/python scripts/build_index.py`; this networked builder is intentionally not part of CI.

## Tests

The test suite is offline and uses saved public response fixtures:

```bash
.venv/bin/ruff check .
.venv/bin/pytest -q
python scripts/validate.py
python scripts/build.py
```

## CI

`ci.yml` runs lint, offline tests, validation and generated-file checks on pushes and pull requests; `live.yml` runs weekly live checks and uploads a report.
The assistant check in `live.yml` requires a repository `GEMINI_API_KEY` secret.

## Assistant evaluation

`evals/procedures.yaml` has 10 real procedures with ground truth (price, maximum resolution time, application period, in-person requirement) taken from the live e-tramits pages on 2026-10-02. Run it with:

```bash
GEMINI_API_KEY=... .venv/bin/python evals/run.py --baseline
```

Latest result (`evals/results-2026-10-03.md`, `gemini-2.5-flash`): 10/10 cases pass with the right procedure cited and 18/18 facts correct. The same model answering closed-book got 3/18 facts. These 10 cases were also used while tuning retrieval, so treat this as a regression set rather than a held-out benchmark.

### Held-out set

`evals/heldout.yaml` has 20 more cases written after tuning ended: 15 procedures not used for tuning (ca/es/fr/en) and 5 questions no source here can answer (weather, ski pass prices, border queues, a minister's personal phone, the user's own vacation days), which must be declined without stating any amount.

```bash
GEMINI_API_KEY=... .venv/bin/python evals/run.py --cases evals/heldout.yaml --baseline
```

- First run (`evals/results-heldout-2026-10-03-first-run.md`): 15/20 as scored. Three failures were scorer bugs (citations written as `[1, 2]` were not parsed, and "no se encontró" was not recognised as declining). Rescoring the same answers gives 18/20. The two real failures:
  - The redactor masked dates such as `23-09-2026` as phone numbers, so the assistant could not state an application period. Now fixed.
  - For "I'm selling my flat and need the habitability certificate", it answered from the *cèdula d'habitabilitat* (2 months) instead of the *certificat d'habitabilitat* (72 hours). The question is arguably ambiguous, since a sale needs the cèdula.
- After the fixes (`evals/results-heldout-2026-10-03.md`): 20/20, 23/23 facts, 5/5 unanswerable questions declined, 0 bad citations. The same model closed-book got 6/23 facts. The habitability case passed because retrieval returned a different set of procedures, not because of a fix. Keyword generation is not fully deterministic, so expect that case to flip.

From here this set is no longer strictly held out: one bug fix was found with it. New failures should be fixed against new cases.

The one-page proposal for the Govern is in `docs/pitch.md`.
