from fonts_andorra.assistant import retrieve


def test_local_procedure_fallback_ranks_title_and_slug_overlap(monkeypatch):
    procedures = [
        {"code": "GV000866", "title": "Autorització de taxi", "url": "https://example.ad/taxi"},
        {"code": "GV000484", "title": "Residència i treball: autorització inicial",
         "url": "https://example.ad/residencia-treball"},
    ]
    monkeypatch.setattr(retrieve.tramits, "list_all", lambda: procedures)
    result = retrieve._fallback(["autorització inicial"])
    assert result[0]["code"] == "GV000484"


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


def test_keyword_ranking_preserves_site_order_before_fallback():
    items = [RANKING_PROCEDURES[1], RANKING_PROCEDURES[0]]
    ranked = retrieve._rank_candidates(
        items,
        ["targeta blava"],
        site_ranks={"GV000037": (0, 0), "GV000039": (1, 1)},
        fallback_ranks={"GV000039": 0},
    )
    assert [item["code"] for item in ranked] == ["GV000037", "GV000039"]

    ranked = retrieve._rank_candidates(
        [RANKING_PROCEDURES[0], RANKING_PROCEDURES[1]],
        ["targeta blava"],
        site_ranks={"GV000037": (5, 0)},
        fallback_ranks={"GV000039": 0},
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
    monkeypatch.setattr(retrieve.tramits, "search", lambda keyword: [item])
    monkeypatch.setattr(retrieve, "_fallback", lambda keywords: [])
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


def test_retrieve_fetches_five_procedures_and_caps_passages(monkeypatch):
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
    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["targeta blava"])
    monkeypatch.setattr(retrieve.tramits, "search", lambda keyword: items)
    monkeypatch.setattr(retrieve, "_fallback", lambda keywords: [])
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: fetched.append(url) or detail)

    sources = retrieve.retrieve("Quin tràmit necessito?")

    assert len(sources) == 5
    assert len(fetched) == 5
    assert all(len(source.text) <= 2500 for source in sources)
