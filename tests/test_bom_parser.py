from pathlib import Path

from src.app.services import bom_parser


def test_parse_csv_bom(tmp_path: Path) -> None:
    csv_content = "material,composition,gsm,process,unit_cost,moq,lead_time\nCotton,100% cotton,150,Weaving,2.5,1000,20"
    file_path = tmp_path / "sample.csv"
    file_path.write_text(csv_content, encoding="utf-8")
    response = bom_parser.parse_bom(file_path.read_bytes(), file_path.name)
    assert len(response.items) == 1
    item = response.items[0]
    assert item.material == "Cotton"
    assert item.unit_cost == 2.5
