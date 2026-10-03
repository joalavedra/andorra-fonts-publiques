# Andorra Fonts Públiques: public data and procedures that AI agents can use

*A one-page proposal for the Govern d'Andorra. An independent, educational, open-source (CC0) project.*

## The problem

Andorra publishes a lot. The official bulletin has 230,000 documents since 1989, the statistics department has 2,709 tables, there are about 200 GIS services, and 645 procedures. But it all sits in four separate backends with no shared catalogue and no documented APIs. A developer, a researcher or an AI assistant has to reverse-engineer each one. So ChatGPT-style tools answer questions about Andorra from memory, and they get prices, deadlines and requirements wrong.

## What the project delivers (working today)

1. **A catalogue of 10 official sources.** Each one is a YAML file covering endpoint, format, licence, freshness and the traps found with real calls (for example, the statistics CSV uses a decimal comma, and the e-tramits search silently ignores the text you give it in one URL form).
2. **Python clients and an MCP server.** MCP is the open standard Claude, ChatGPT, Cursor and others use to plug in tools, so any AI assistant can search BOPA, pull statistics tables, read a procedure's price and deadline, or query fuel prices and traffic counts. Every answer is live from the official source.
3. **A cited procedures assistant** in Catalan, Spanish, French and English.
   - It answers only from official pages.
   - Every sentence links to its source.
   - Personal data (emails, phone numbers, IBANs, NRT tax ids, passport numbers) is masked before anything leaves the user's machine.
   - Results on 10 real procedures: **10/10** answered correctly with citations, getting 18 of 18 prices, deadlines and application periods right. The same model answering from memory got 3 of 18 (`evals/results-2026-10-03.md`).

## Why it matters for the Govern

- **Citizens and residents** get correct answers in their language, with a link to the official page, at no cost.
- **The Govern** gets an independent, reproducible map of its own data surface, with every endpoint and its traps documented and re-testable.
- **Andorra's AI strategy** gains a clean Catalan legal and administrative corpus (BOPA, which its licence already allows to be reused) and an agent-ready interface. Few countries of its size have one.
- **Zero procurement:** the work is CC0 and can be adopted, forked or ignored, and it runs on a laptop.

## What we ask (all optional, no budget)

1. **Confirmation that BOPA's API may be used** at polite request rates, and a technical contact. Today it depends on keys embedded in the website's code.
2. **A licence statement for e-tramits and the ArcGIS layers.** Statistics is already CC BY 4.0 and BOPA allows reuse. e-tramits currently falls under govern.ad's all-rights-reserved notice, so the project only links to it and quotes it.
3. **A one-line mention in a future open-data plan:** a national catalogue (e.g. `dades.govern.ad`) could start from this one.

## Ground rules the project follows

- It is independent and not endorsed by the Govern. It uses no logos or official branding.
- It only reads public data. No logins, no form submission, no CAPTCHAs.
- It is live-first: procedures and government pages are fetched and cited, never republished.
- BOPA keeps its metadata and its terms of use, as its legal notice requires.

**Repository:** github.com/joalavedra/andorra-fonts-publiques · **Contact:** Joan Alavedra, joan@openfort.xyz
