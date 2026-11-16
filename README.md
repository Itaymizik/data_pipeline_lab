# Data Pipeline Lab

A small practice project for Git, GitHub Actions CI, Docker, logging, and long-running jobs.

## Input
`data/detections.csv`: frame_id, label, confidence.

## Run
```bash
python -m src.pipeline --input data/detections.csv --output output/summary.json
python -m pytest -q
```

Expected baseline summary: 5 detections (person 2, vehicle 2, animal 1).

## Exercise
Add optional `--min-confidence` (default 0.0). When provided, skip rows with confidence less than the threshold. Validate the threshold in [0,1], add unit tests, and open a PR. With threshold 0.5, expected output: 3 detections (person 2, vehicle 1).

## Docker
```bash
docker build -t data-pipeline-lab .
docker run --rm -v "$(pwd)/data:/app/data:ro" -v "$(pwd)/output:/app/output" data-pipeline-lab --input data/detections.csv --output output/summary.json
```

Note: Docker volume syntax shown is for bash (Linux/macOS/Git Bash); on Windows PowerShell use ${PWD} for current folder.
