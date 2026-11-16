import csv

import pytest

from src.pipeline import summarize


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["frame_id", "label", "confidence"])
        writer.writeheader()
        writer.writerows(rows)


def test_summarize(tmp_path):
    source = tmp_path / "records.csv"
    write_csv(source, [
        {"frame_id": "1", "label": "person", "confidence": "0.95"},
        {"frame_id": "2", "label": "vehicle", "confidence": "0.31"},
        {"frame_id": "3", "label": "person", "confidence": "0.70"},
    ])
    assert summarize(source) == {"total_detections": 3, "by_label": {"person": 2, "vehicle": 1}}


def test_reject_invalid_confidence(tmp_path):
    source = tmp_path / "bad.csv"
    write_csv(source, [{"frame_id": "1", "label": "person", "confidence": "1.5"}])
    with pytest.raises(ValueError, match="Invalid confidence"):
        summarize(source)
