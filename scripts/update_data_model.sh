#!/bin/bash
# Update data model documentation in multiple formats

cd "$(dirname "$0")/.."

echo "Generating data model documentation..."
python scripts/generate_data_model_docs.py "$@"

echo "Data model documentation updated successfully!"
