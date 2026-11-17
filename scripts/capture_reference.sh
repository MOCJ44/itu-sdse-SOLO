#!/usr/bin/env bash
# Runs the untouched notebooks and saves their JSON results as reference results.
# Usage, from anywhere: bash scripts/capture_reference.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# Start clean, so the run cannot reuse an earlier model or MLflow run
rm -rf artifacts mlflow-state models/model

# Run both notebooks. The executed copies go to /tmp, so the notebooks in Git stay untouched
for notebook in notebooks/01_training.ipynb notebooks/02_deployment.ipynb; do
    uv run --with nbconvert jupyter nbconvert --execute --to notebook \
        --output-dir /tmp/reference-run "$notebook"
done

# Keep only the JSON results (never model weights), in a folder named after the commit
target="tests/fixtures/$(git rev-parse HEAD)/artifacts"
mkdir -p "$target"
cp artifacts/*.json "$target/"
echo "Saved reference results in $target"
