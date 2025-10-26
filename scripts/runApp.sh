#!/bin/bash

set -e

cd "$(dirname "$(dirname "$0")")"

if [ -d ".venv" ]; then
  source .venv/bin/activate
  echo "Virtual environment activated"
else
  echo "⚠No virtual environment found. Run 'python3 -m venv .venv' first."
fi

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt --quiet
  echo "📦 Dependencies installed"
fi

mkdir -p logs

export PYTHONPATH=$(pwd)

echo "Starting the Bitcoin tracker app..."
python3 src/main.py
