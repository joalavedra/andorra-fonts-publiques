from pathlib import Path

import pytest

from fonts_andorra.assistant import retrieve

FIXTURES = Path(__file__).parent / "fixtures"


def test_local_procedure_index_ranks_title_and_slug_overlap(monkeypatch):
    procedures = [
        {"id": "GV000866", "title": "Autorització de taxi", "url": "https://example.ad/taxi"},
        {"id": "GV000484", "title": "Residència i treball: autorització inicial",
         "url": "https://example.ad/residencia-treball"},
    ]
    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["autorització inicial"])
    monkeypatch.setattr(
        retrieve.index,
        "search",
        lambda query, limit, source: procedures if source == "e-tramits" else [],
    )
    monkeypatch.setattr(retrieve.tramits, "search", lambda keyword: pytest.fail("unexpected live search"))
    monkeypatch.setattr(retrieve.tramits, "list_all", lambda: pytest.fail("unexpected full listing"))
    detail = {
        "title": procedures[1]["title"],
        "url": procedures[1]["url"],
        "sections": {},
        "price": None,
        "max_resolution": None,
    }
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: detail)

    result = retrieve.retrieve("Initial residence and work permit")

    assert result[0].url == "https://example.ad/residencia-treball"


RANKING_PROCEDURES = [
    {"code": "GV000039", "title": "Renovació de targeta blava", "url": "https://example.ad/targeta-blava"},
    {"code": "GV000037", "title": "Duplicat de targeta blava", "url": "https://example.ad/targeta-blava"},
    {"code": "GV000038", "title": "Targeta blava: primer sol·licitud", "url": "https://example.ad/targeta-blava"},
    {"code": "GV000036", "title": "Modificació de targeta blava", "url": "https://example.ad/targeta-blava"},
    {"code": "GV000278", "title": "Ampliació d'horari comercial", "url": "https://example.ad/horaris"},
]


def test_keyword_ranking_finds_blue_card_initial_request_and_shop_hours():
    ranked = retrieve._rank_candidates(RANKING_PROCEDURES, ["targeta blava", "primera demanda"])
    assert ranked[0]["code"] == "GV000038"

    ranked = retrieve._rank_candidates(RANKING_PROCEDURES, ["horaris comercials"])
    assert ranked[0]["code"] == "GV000278"


def test_keyword_ranking_preserves_index_order_before_unranked_candidates():
    items = [RANKING_PROCEDURES[1], RANKING_PROCEDURES[0]]
    ranked = retrieve._rank_candidates(
        items,
        ["targeta blava"],
        index_ranks={"GV000037": (0, 0), "GV000039": (1, 1)},
    )
    assert [item["code"] for item in ranked] == ["GV000037", "GV000039"]

    ranked = retrieve._rank_candidates(
        [RANKING_PROCEDURES[0], RANKING_PROCEDURES[1]],
        ["targeta blava"],
        index_ranks={"GV000037": (5, 0)},
    )
    assert [item["code"] for item in ranked] == ["GV000037", "GV000039"]


def test_keyword_generation_filters_stopwords_and_uses_procedure_title_prompt(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        retrieve.llm,
        "generate",
        lambda prompt, system_instruction=None: (
            captured.update(prompt=prompt, system_instruction=system_instruction)
            or '["Preu cost quant temps targeta blava", '
            '"Tràmit procediment sol·licitud horaris comercials", '
            '"Termini deadline ampliació horaris", "Procediment matrícula", "Targeta blava"]'
        ),
    )

    keywords = retrieve.llm.keywords("How much does a shop charge?")

    assert keywords == ["targeta blava", "horaris comercials", "ampliació horaris", "matrícula"]
    assert "sol·licitud" in captured["prompt"]
    assert "fishing licence" in captured["prompt"]
    assert "do not invent another topic" in captured["prompt"]


def test_retrieve_places_key_facts_first(monkeypatch):
    item = {
        "code": "GV000484",
        "title": "Residència i treball: autorització inicial",
        "url": "https://www.e-tramits.ad/tramits/example/p/GV000484",
    }
    detail = {
        "code": "GV000484",
        "title": item["title"],
        "url": item["url"],
        "sections": {"Detall": "Long procedure text."},
        "price": "190,96 €",
        "max_resolution": "60 dia/dies hàbil(s)",
        "application_period": "Tot l’any.",
        "online_available": False,
        "appointment_required": True,
    }
    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["residència inicial"])
    monkeypatch.setattr(
        retrieve.index,
        "search",
        lambda query, limit, source: [item] if source == "e-tramits" else [],
    )
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: detail)

    sources = retrieve.retrieve("Quant triga l'autorització inicial?")

    assert sources[0].text.startswith(
        "Title: Residència i treball: autorització inicial\n"
        "Price: 190,96 €\n"
        "Maximum resolution time: 60 dia/dies hàbil(s)\n"
        "Application period: Tot l’any.\n"
        "Online available: False\n"
        "Appointment required: True"
    )


def test_procedure_passage_preserves_key_facts_before_long_sections():
    detail = {
        "title": "PLA ENGEGA",
        "price": "0,00 €",
        "max_resolution": "2 mesos",
        "application_period": "Del 19/03/2026 al 15/11/2026.",
        "online_available": True,
        "appointment_required": False,
        "sections": {
            "Representant": "r" * 3000,
            "Descripció": "Official description.",
            "Normativa": "n" * 3000,
        },
    }

    passage = retrieve._procedure_passage(detail)

    expected_header = (
        "Title: PLA ENGEGA\n"
        "Price: 0,00 €\n"
        "Maximum resolution time: 2 mesos\n"
        "Application period: Del 19/03/2026 al 15/11/2026.\n"
        "Online available: True\n"
        "Appointment required: False"
    )
    assert passage.startswith(expected_header)
    assert expected_header in passage
    assert passage.index("Descripció: Official description.") < passage.index("Representant:")
    assert len(passage) <= 2500


def test_retrieve_fetches_five_procedures_from_the_index(monkeypatch):
    items = [
        {"code": f"GV00000{index}", "title": "Targeta blava", "url": f"https://example.ad/p/GV00000{index}"}
        for index in range(1, 7)
    ]
    detail = {
        "title": "Targeta blava",
        "url": items[0]["url"],
        "sections": {"Detall": "x" * 3000},
        "price": None,
        "max_resolution": None,
        "online_available": None,
        "appointment_required": None,
    }
    fetched = []
    index_searches = []

    def search(query, limit, source):
        index_searches.append((query, limit, source))
        return items if source == "e-tramits" else []

    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["targeta blava"])
    monkeypatch.setattr(retrieve.index, "search", search)
    monkeypatch.setattr(retrieve.tramits, "search", lambda keyword: pytest.fail("unexpected live search"))
    monkeypatch.setattr(retrieve.tramits, "list_all", lambda: pytest.fail("unexpected full listing"))
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: fetched.append(url) or detail)

    sources = retrieve.retrieve("Quin tràmit necessito?")

    assert len(sources) == 5
    assert len(fetched) == 5
    assert index_searches == [
        ("targeta blava", 8, "e-tramits"),
        ("targeta blava", 3, "govern.ad"),
    ]
    assert all(len(source.text) <= 2500 for source in sources)


def test_retrieve_adds_govern_passage_using_keywords_only(monkeypatch):
    procedure = {
        "id": "GV000001",
        "title": "Passport application",
        "url": "https://www.e-tramits.ad/tramits/passport/p/GV000001",
    }
    page_item = {
        "id": "/ca/tematiques/passaport",
        "title": "Passaports",
        "url": "https://www.govern.ad/ca/tematiques/passaport",
    }
    detail = {
        "title": "Passport application",
        "url": procedure["url"],
        "sections": {},
        "price": None,
        "max_resolution": None,
    }
    page = {
        "title": "Passaports",
        "description": "Passport information from Govern d'Andorra.",
        "url": page_item["url"],
        "sections": {
            "General information": "General administrative information. " * 100,
            "Import": "Passaport: 49,31 euros for the ten-year passport.",
        },
    }
    searches = []

    def search(query, limit, source):
        searches.append((query, limit, source))
        return [procedure] if source == "e-tramits" else [page_item]

    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["passaport"])
    monkeypatch.setattr(retrieve.index, "search", search)
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: detail)
    monkeypatch.setattr(retrieve.govern, "page", lambda url: page)

    sources = retrieve.retrieve("Quin és l'import del passaport?")

    assert [source.n for source in sources] == [1, 2]
    assert sources[1].title == "Passaports"
    assert sources[1].text.index("General information:") < sources[1].text.index("Import:")
    assert "49,31 euros" in sources[1].text
    assert "Description: Passport information" in sources[1].text
    assert len(sources[1].text) <= 4000
    assert searches == [
        ("passaport", 8, "e-tramits"),
        ("passaport", 3, "govern.ad"),
    ]


def test_govern_passage_keeps_a_late_amount_sentence_and_is_deterministic():
    detail = {
        "title": "Residència sense treball",
        "description": "Economic means for applicants.",
        "sections": {
            "Mitjans econòmics": (
                "General information about the administrative process. " * 60
                + "Applicants must document annual income equal to 300% of the minimum wage."
            ),
        },
    }

    first = retrieve._govern_passage(detail, "income")
    second = retrieve._govern_passage(detail, "income")

    assert "300% of the minimum wage" in first
    assert len(first) <= 4000
    assert first == second


def test_govern_passage_includes_lost_passport_section_for_lost_passport_question():
    html = (FIXTURES / "govern_passaports.html").read_text(encoding="utf-8")
    parser = retrieve.govern._Page()
    parser.feed(html)
    detail = {
        "title": parser.title,
        "description": parser.description,
        "sections": parser.sections,
    }

    passage = retrieve._govern_passage(
        detail,
        "passaport",
        "I lost my passport abroad, who do I contact? he perdut el passaport a l'estranger",
    )

    assert "Pèrdua o robatori:" in passage
    assert "Ambaixada d'Andorra" in passage


def test_govern_search_uses_safe_question_when_keywords_are_empty(monkeypatch):
    searches = []
    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: [])
    monkeypatch.setattr(
        retrieve.index,
        "search",
        lambda query, limit, source: searches.append((query, limit, source)) or [],
    )

    retrieve.retrieve("Informació general sobre una pàgina")

    assert searches == [("Informació general sobre una pàgina", 3, "govern.ad")]
