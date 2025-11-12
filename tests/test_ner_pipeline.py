from src.app.services.ner_pipeline import ner_pipeline


def test_regex_entities_capture_materials() -> None:
    text = "Fabric uses 100% recycled polyester with knitting process and zipper closures."
    entities = ner_pipeline.extract_entities(text)
    labels = {entity["label"] for entity in entities}
    assert "MATERIAL" in labels
    assert "PROCESS" in labels
