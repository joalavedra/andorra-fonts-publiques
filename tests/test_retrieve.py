from fonts_andorra.assistant import retrieve


def test_local_procedure_fallback_ranks_title_and_slug_overlap(monkeypatch):
    procedures = [
        {"code": "GV000866", "title": "Autorització de taxi", "url": "https://example.ad/taxi"},
        {"code": "GV000484", "title": "Residència i treball: autorització inicial",
         "url": "https://example.ad/residencia-treball"},
    ]
    monkeypatch.setattr(retrieve.tramits, "list_all", lambda: procedures)
    result = retrieve._fallback("residencia initial treball", ["autorització inicial"])
    assert result[0]["code"] == "GV000484"


def test_retrieve_places_maximum_resolution_time_first(monkeypatch):
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
        "online_available": False,
        "appointment_required": True,
    }
    monkeypatch.setattr(retrieve.llm, "keywords", lambda question: ["residència inicial"])
    monkeypatch.setattr(retrieve.tramits, "search", lambda keyword: [item])
    monkeypatch.setattr(retrieve, "_fallback", lambda question, keywords: [])
    monkeypatch.setattr(retrieve.tramits, "procedure", lambda url: detail)

    sources = retrieve.retrieve("Quant triga l'autorització inicial?")

    assert sources[0].text.startswith("Maximum resolution time: 60 dia/dies hàbil(s)")
