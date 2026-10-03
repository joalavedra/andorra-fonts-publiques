"""Score the cited assistant on evals/procedures.yaml.

Per case:
- retrieved: some returned source URL contains the expected procedure code
- cited: the answer cites [n] for a source whose URL contains the code
- facts: every fact matches at least one of its alternative regexes
- bad_citations: [n] markers with no matching source (must be 0)
A case passes when retrieved, cited, all facts and no bad citations.

Usage: python evals/run.py [--baseline] [--only ID] [--out evals/results-YYYY-MM-DD.md]
--baseline also asks the same model closed-book (no sources) and scores facts only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fonts_andorra.assistant.answer import ask

GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def fact_hits(answer: str, facts: dict) -> dict:
    a = norm(answer)
    return {k: any(re.search(rx, a, re.IGNORECASE) for rx in alts) for k, alts in facts.items()}


def closed_book(question: str) -> str:
    model = os.environ.get("FONTS_ANDORRA_MODEL", "gemini-2.5-flash")
    body = {"contents": [{"role": "user", "parts": [{"text": question}]}],
            "generationConfig": {"temperature": 0}}
    r = requests.post(GEMINI.format(model=model), params={"key": os.environ["GEMINI_API_KEY"]},
                      json=body, timeout=120)
    r.raise_for_status()
    parts = r.json()["candidates"][0]["content"].get("parts", [])
    return "".join(p.get("text", "") for p in parts)


def score_case(case: dict) -> dict:
    t0 = time.time()
    res = ask(case["question"], lang=case.get("lang"))
    secs = round(time.time() - t0, 1)
    answer, sources = res["answer"], res["sources"]
    by_n = {int(s["n"]): s for s in sources}
    cited_ns = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    code = case["code"]
    retrieved = any(code in s["url"] for s in sources)
    cited = any(n in by_n and code in by_n[n]["url"] for n in cited_ns)
    bad = sorted(n for n in cited_ns if n not in by_n)
    facts = fact_hits(answer, case["facts"])
    ok = retrieved and cited and all(facts.values()) and not bad
    return {"id": case["id"], "lang": case["lang"], "code": code, "pass": ok, "retrieved": retrieved,
            "cited": cited, "facts": facts, "bad_citations": bad, "secs": secs, "answer": answer,
            "sources": [{"n": s["n"], "url": s["url"]} for s in sources]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--out", default=str(ROOT / "evals" / f"results-{datetime.now(tz=timezone.utc).date()}.md"))
    args = ap.parse_args()
    cases = yaml.safe_load((ROOT / "evals" / "procedures.yaml").read_text())["cases"]
    if args.only:
        cases = [c for c in cases if c["id"] == args.only]
    rows = []
    for c in cases:
        r = score_case(c)
        if args.baseline:
            r["baseline_facts"] = fact_hits(closed_book(c["question"]), c["facts"])
        rows.append(r)
        print(json.dumps({k: r[k] for k in ("id", "pass", "retrieved", "cited", "facts", "bad_citations", "secs")},
                         ensure_ascii=False), flush=True)
    model = os.environ.get("FONTS_ANDORRA_MODEL", "gemini-2.5-flash")
    n = len(rows)
    lines = [f"# Assistant eval, {datetime.now(tz=timezone.utc).date()}", "",
             f"Model `{model}`, temperature 0, {n} cases from `evals/procedures.yaml`.", "",
             f"- Pass: **{sum(r['pass'] for r in rows)}/{n}**",
             f"- Right procedure retrieved: {sum(r['retrieved'] for r in rows)}/{n}",
             f"- Right procedure cited: {sum(r['cited'] for r in rows)}/{n}",
             f"- Facts correct: {sum(sum(r['facts'].values()) for r in rows)}/{sum(len(r['facts']) for r in rows)}",
             f"- Citations to non-existent sources: {sum(len(r['bad_citations']) for r in rows)}"]
    if args.baseline:
        lines.append(f"- Closed-book baseline (same model, no sources), facts correct: "
                     f"{sum(sum(r['baseline_facts'].values()) for r in rows)}/{sum(len(r['facts']) for r in rows)}")
    lines += ["", "| case | lang | pass | retrieved | cited | facts | secs |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        f = " ".join(f"{k}:{'ok' if v else 'MISS'}" for k, v in r["facts"].items())
        lines.append(f"| {r['id']} | {r['lang']} | {'PASS' if r['pass'] else 'FAIL'} | {r['retrieved']} | "
                     f"{r['cited']} | {f} | {r['secs']} |")
    lines += ["", "## Answers", ""]
    for r in rows:
        lines += [f"### {r['id']} ({r['code']})", "", r["answer"].strip(), "",
                  "Sources: " + ", ".join(f"[{s['n']}] {s['url']}" for s in r["sources"]), ""]
    Path(args.out).write_text("\n".join(lines))
    print("wrote", args.out)
    return 0 if all(r["pass"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
