import csv

import pytest

from src.pipeline import summarize
from pathlib import Path



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


def test_min_confidence_filter():
    result = summarize(
        Path("data/detections.csv"),
        min_confidence=0.5
    )

    assert result["total_detections"] == 3
    assert result["by_label"]["person"] == 2
    assert result["by_label"]["vehicle"] == 1

def test_invalid_min_confidence():
    with pytest.raises(ValueError, match="min_confidence"):
        summarize(
            Path("data/detections.csv"),
            min_confidence=1.5
        )