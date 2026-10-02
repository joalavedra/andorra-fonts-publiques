"""Command line interface for the cited assistant."""

from __future__ import annotations

import argparse
import json

from fonts_andorra.assistant.answer import ask


def main() -> None:
    parser = argparse.ArgumentParser(prog="fonts-andorra-ask")
    parser.add_argument("question")
    parser.add_argument("--lang", choices=["ca", "es", "fr", "en"])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = ask(args.question, args.lang)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return
    print(result["answer"])
    print("\nSources:")
    for item in result["sources"]:
        print(f"[{item['n']}] {item['title']} — {item['url']}")


if __name__ == "__main__":
    main()
