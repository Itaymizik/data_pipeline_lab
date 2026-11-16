"""Simple data-curation pipeline for detection records."""

import argparse
import csv
import json
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def summarize(input_path: Path, delay: float = 0.0, min_confidence: float = 0.0) -> dict:
    """Count detections and categories from a CSV file."""
    if not 0.0 <= min_confidence <= 1.0:
        raise ValueError("min_confidence must be between 0 and 1")

    count = 0
    by_label = {}
    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        expected = {"frame_id", "label", "confidence"}
        if not expected.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must contain columns: {sorted(expected)}")
        for row in reader:
            confidence = float(row["confidence"])

            if not 0.0 <= confidence <= 1.0:
                raise ValueError(f"Invalid confidence: {confidence}")
            label = row["label"].strip()
            if not label:
                raise ValueError("Label must not be empty")
            if confidence < min_confidence:
                continue
            count += 1
            by_label[label] = by_label.get(label, 0) + 1
            if delay:
                time.sleep(delay)
    return {"total_detections": count, "by_label": by_label}


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize detection data")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds per record (demo only)")
    parser.add_argument("--min-confidence", type=float, default=0.0)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger.info("Starting input=%s", args.input)
    try:
        result = summarize(args.input, delay=args.delay, min_confidence=args.min_confidence)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as output:
            output.write(json.dumps(result, indent=2) + "\n")
    except (OSError, ValueError) as exc:
        logger.exception("Pipeline failed: %s", exc)
        raise SystemExit(1) from exc
    logger.info("Completed detections=%d output=%s", result["total_detections"], args.output)


if __name__ == "__main__":
    main()
