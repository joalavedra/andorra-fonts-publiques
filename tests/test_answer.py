from fonts_andorra.assistant import answer
from fonts_andorra.assistant.retrieve import Source


def test_ask_uses_question_language_by_default_and_preserves_explicit_lang(monkeypatch):
    monkeypatch.setattr(
        answer,
        "retrieve",
        lambda question: [Source(1, "Official source", "https://example.ad/source", "Facts.")],
    )
    prompts = []
    monkeypatch.setattr(
        answer.llm,
        "generate",
        lambda prompt, system_instruction=None: prompts.append(prompt) or "Answer [1].",
    )

    implicit = answer.ask("¿Dónde encuentro el trámite?")
    explicit = answer.ask("¿Dónde encuentro el trámite?", lang="fr")

    assert implicit["lang"] is None
    assert "Answer in the same language as the question." in prompts[0]
    assert explicit["lang"] == "fr"
    assert "language code 'fr'" in prompts[1]
